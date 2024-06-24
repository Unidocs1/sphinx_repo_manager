"""
Xsolla Sphinx Extension: sphinx_repo_manager
--------------------------------------------

Description:
Automates management of multiple documentation repositories by cloning and updating
external repos specified in a YAML manifest file, ensuring each repo is checked out
to the specified tag before Sphinx doc-gen (`make html`).

Quickstart:
1. Edit `repo_manifest.yml` in the project root.
2. Ensure each repo in the manifest includes at least a `url`.
4. Include this extension in `conf.py` by adding the extension's path to `sys.path`
   and adding it to the `extensions` list:
   ```
   sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_repo_manager')))
   extensions = [sphinx_repo_manager]
   ```

Entry Point:
- setup(app): Executes during Sphinx 'builder-inited' event.

Default Dir Tree:
Inspired by nginx, repos are cloned to `_repos_available` -> then symlinked to `content/`:
- docs/
  - source/
    - _extensions/
    - _repos_available/
      - (eg) account_services-v2.1.0/
    - content/
      - (eg) account_services/
    - conf.py
    - index.rst

Tested in:
- Windows 11 via PowerShell7
- Ubuntu 24.04 LTS via ReadTheDocs (RTD) deployment
"""
# Core, pathing, ops >>
import os  # file path ops
from pathlib import Path  # Path ops
import re  # regex ops
import subprocess
import sys  # Just for sys.exit, if !repositories

# Async >>
import concurrent.futures  # Async multitasking
import threading  # Async multitasking
import queue  # For managing log entries
import signal  # For CTRL+C detection

# Yaml and logging >>
import yaml  # YAML file parsing
from log_styles import *  # Custom logging styles
from git_helper import GitHelper  # Helper functions for git operations
from sphinx.util import logging  # Sphinx logging utility

# Define base path and manifest path
ABS_BASE_PATH = os.path.abspath(os.path.dirname(__file__))
MANIFEST_NAME = 'repo_manifest.yml'
ABS_MANIFEST_PATH = os.path.normpath(os.path.join(
    ABS_BASE_PATH, '..', '..', '..', MANIFEST_NAME))
ABS_MANIFEST_PATH_DIR = os.path.dirname(ABS_MANIFEST_PATH)

# Constants for default settings
DEFAULT_MAX_WORKERS_LOCAL = 5
DEFAULT_DEBUG_MODE = False
DEFAULT_STASH_AND_CONTINUE_IF_WIP = True
DEFAULT_INIT_CLONE_PATH = 'repos'
DEFAULT_DEFAULT_BRANCH = 'master'
DEFAULT_PRESERVE_GITLAB_GROUP = True
DEFAULT_GITLAB_GROUP_TO_LOWERCASE = True
DEFAULT_REPOSITORIES = {}

logger = logging.getLogger(__name__)  # Get logger instance

# Global flag to signal threads to shutdown
shutdown_flag = False


# Custom exception class for repository management errors
class RepositoryManagementError(Exception):
    pass


# RepoManager class to handle repository operations
class SphinxRepoManager:
    def __init__(self, abs_manifest_path):
        self.read_the_docs_build = os.environ.get("READTHEDOCS", None) == 'True'
        self.manifest_path = abs_manifest_path
        self.manifest = None
        self.debug_mode = False  # If True: +logs; stops build after ext is done

        # Multi-threading >>
        self.lock = threading.Lock()  # Lock for thread-safe logging
        self.shutdown_flag = False  # Flag to handle graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)

    @staticmethod
    def _log_err_if_invalid_symlink(rel_symlinked_repo_path):
        if not Path(rel_symlinked_repo_path).is_symlink():
            logger.error(f"Failed to create symlink: '{rel_symlinked_repo_path}'")

    def _signal_handler(self, signum, frame):
        if not self.shutdown_flag:
            print("Signal received (CTRL+C), initiating graceful shutdown...")
        self.shutdown_flag = True

    def read_normalize_manifest(self):
        """
        Read and return the repository manifest from YAML file.
        - validate_normalize_manifest_set_meta():
            - Normalizes data, such as removing .git from git urls
            - Injects _meta prop objs per repo
            - Sets defaults, if any
            - Validates required fields
        """
        # Logs
        logger.info(colorize_action(f'📜 | [repo_manager] Reading manifest...'))
        logger.info(colorize_path(f"   - Extension Src: '{brighten(ABS_BASE_PATH)}'"))
        logger.info(colorize_path(f"   - Manifest Src: '{brighten(ABS_MANIFEST_PATH)}'"))

        # Read manifest file
        if not os.path.exists(self.manifest_path):
            logger.warning(f"repo_manifest.yml !found @ '{brighten(self.manifest_path)}' - skipping extension!")
            sys.exit(0)

        with open(self.manifest_path, 'r') as file:
            manifest = yaml.safe_load(file)

        # Remove .git from urls; inject hidden _meta prop per repo, etc
        # (!) Exits if repositories are empty
        manifest = self.validate_normalize_manifest_set_meta(manifest)
        self.manifest = manifest

        # Logs
        rel_repo_sparse_path = manifest['repo_sparse_path']
        logger.info(colorize_path(f"   - repo_sparse_path: '{brighten(rel_repo_sparse_path)}'"))

        return manifest

    def validate_normalize_manifest_set_meta(self, manifest):
        """
        Validates + normalizes YAML v1.2 manifest vals, such as removing .git from URLs,
        +injects hidden '_meta' prop, etc.
        - (!) Exits if !repositories
        - Sets default fallbacks, if any
        - Adds to repositories.x: {
            - url_dotgit
            - repo_name
            - rel_symlinked_repo_path
            - tag_versioned_clone_src_repo_name
            - tag_versioned_clone_src_path
        }
        """
        logger.info(colorize_action("🧹 | Validating & normalizing manifest..."))

        # Set root defaults
        manifest.setdefault('max_workers_local', DEFAULT_MAX_WORKERS_LOCAL)
        manifest.setdefault('debug_mode', DEFAULT_DEBUG_MODE)
        manifest.setdefault('stash_and_continue_if_wip', DEFAULT_STASH_AND_CONTINUE_IF_WIP)
        manifest.setdefault('default_branch', DEFAULT_DEFAULT_BRANCH)
        manifest.setdefault('init_clone_path', DEFAULT_INIT_CLONE_PATH)
        manifest.setdefault('init_clone_path_root_symlink_src', DEFAULT_INIT_CLONE_PATH)
        manifest.setdefault('base_symlink_path', DEFAULT_INIT_CLONE_PATH)
        manifest.setdefault('repo_sparse_path', DEFAULT_INIT_CLONE_PATH)
        manifest.setdefault('repositories', DEFAULT_REPOSITORIES)

        # Normalize path/to/slashes
        manifest['init_clone_path'] = os.path.normpath(manifest['init_clone_path'])
        manifest['init_clone_path_root_symlink_src'] = os.path.normpath(manifest['init_clone_path_root_symlink_src'])
        manifest['base_symlink_path'] = os.path.normpath(manifest['base_symlink_path'])

        # Validate repositories
        if not manifest['repositories']:
            logger.warning("[repo_manager] No repositories found in manifest - skipping extension!")
            sys.exit(0)

        repo_sparse_path = manifest['repo_sparse_path']
        manifest['repo_sparse_path'] = repo_sparse_path.replace('\\', '/')  # Normalize to forward/slashes
        init_clone_path = os.path.normpath(manifest['init_clone_path'])
        base_symlink_path = os.path.normpath(manifest['base_symlink_path'])

        # Handle repositories dictionary
        repo_i = 0
        for repo_name, repo_info in manifest['repositories'].items():
            self.set_repo_meta(
                repo_info,
                repo_name,
                init_clone_path,
                base_symlink_path,
                manifest)

            repo_i += 1

        return manifest

    @staticmethod
    def set_repo_meta(
            repo_info,
            repo_name,
            init_clone_path,
            base_symlink_path,
            manifest,
    ):
        if '_meta' not in repo_info:
            repo_info['_meta'] = {
                'url_dotgit': '',  # eg: "https://gitlab.acceleratxr.com/core/account_services.git"
                'repo_name': '',  # eg: "account_services"
                'has_tag': False,  # True if tag exists
                'rel_symlinked_repo_path': '',
                # "{base_symlink_path}{symlink_path}-{tag_or_branch}"; eg: "source/content/account_services" (no tag)
                'tag_versioned_clone_src_repo_name': '',  # "repo-{repo_tag}"; eg: "account-services-v2.1.0"
                'tag_versioned_clone_src_path': '',  # "{init_clone_path}/{tag_versioned_clone_src_repo_name}";
                # - eg: "source/_repos-available/account_services-v2.1.0"
                # - eg: "source/_repos-available/account_services--master"
            }

        # Workers for multi-threading
        manifest.setdefault('max_workers_local', 1)
        manifest.setdefault('max_workers_rtd', 2)

        # url: Req'd - Strip ".git" from suffix, if any (including SSH urls; we'll add it back via url_dotgit)
        url = repo_info.get('url', None)
        if not url:
            logger.error(f"Missing 'url' for repo '{repo_name}'")
            raise RepositoryManagementError(f"\nMissing 'url' for repo '{repo_name}'")

        if url.endswith('.git'):
            url = url[:-4]
        repo_info['url'] = url

        # Default branch == parent {default_branch}
        if 'default_branch' not in repo_info:
            repo_info.setdefault('branch', manifest['default_branch'])

        # Explicitly normalize branch slashes/to/forward
        branch = repo_info['branch']
        repo_info['branch'] = branch.replace('\\', '/')

        # Default symlink_path == repo name (the end of url after the last slash/)
        repo_name = url.split('/')[-1]
        repo_info.setdefault('symlink_path', repo_name)

        # It's ok if !tag (we'll just checkout the branch); great for debugging
        # (!) However, this will affect our naming convention, normally "{repo}-{tag_or_branch}"
        tag = repo_info.get('tag', None)
        has_tag = bool(tag)

        # Set other defaults
        repo_info.setdefault('active', True)

        init_clone_path_root_symlink_src = manifest['init_clone_path_root_symlink_src']
        repo_info.setdefault('init_clone_path_root_symlink_src_override', init_clone_path_root_symlink_src)

        # Set dynamic meta
        _meta = repo_info['_meta']
        _meta['has_tag'] = has_tag
        _meta['url_dotgit'] = f"{url}.git"
        _meta['repo_name'] = repo_name

        # If tag, append "-{tag} to clone src repo name
        # If !tag, append "--{branch} to clone src repo name
        # This helps us easily identify the clone src without even entering the dir
        # (!) All repos must have unique names for this to auto-symlink without repo names or tags
        if has_tag:
            # "repo-{tag}"; eg: "account-services-v2.1.0"
            _meta['tag_versioned_clone_src_repo_name'] = f"{repo_name}-{tag}"
        else:
            # "repo-{"cleaned_branch"}"; eg: "account-services--master" or "account-services--some_nested_branch"
            # ^ Notice the "--" double slash separator. Only accept alphanumeric chars; replace all others with "_"
            pattern = r'\W+'
            normalized_repo_name_for_dir = branch.replace("/", "--")
            normalized_repo_name_for_dir = re.sub(pattern, '_', normalized_repo_name_for_dir)
            _meta['tag_versioned_clone_src_repo_name'] = f"{repo_name}--{normalized_repo_name_for_dir}"

        # {base_symlink_path}{symlink_path}-{tag_or_branch}
        # eg: "source/content/account_services" (no tag)
        symlink_path = repo_info['symlink_path']  # eg: "account_services" (or "-" for xbe_static_docs)
        _meta['rel_symlinked_repo_path'] = os.path.normpath(os.path.join(
            base_symlink_path, symlink_path))

        # "{init_clone_path}/{tag_versioned_clone_src_repo_name}"
        tag_versioned_clone_src_repo_name = _meta['tag_versioned_clone_src_repo_name']
        _meta['tag_versioned_clone_src_path'] = os.path.normpath(os.path.join(
            init_clone_path, tag_versioned_clone_src_repo_name))

    def init_dir_tree(self, manifest):
        """
        Initialize or clear paths based on manifest configuration. Default tree:
        ########################################################################
        - source
          - _repos-available
            - content
        ########################################################################
        """
        logger.info(colorize_action("⚙️ | Crafting dir skeleton from manifest..."))

        # Setup target symlink path skeleton tree from manifest vals
        rel_init_clone_path = manifest['init_clone_path']
        rel_base_symlink_path = manifest['base_symlink_path']

        # Normalize paths -> log -> create dir skeleton
        abs_init_clone_path = os.path.abspath(rel_init_clone_path)
        abs_base_symlink_path = os.path.abspath(rel_base_symlink_path)

        logger.info(colorize_path(f"   - init_clone_path: '{brighten(abs_init_clone_path)}'"))
        logger.info(colorize_path(f"   - base_symlink_path: '{brighten(abs_base_symlink_path)}'"))

        self.setup_directory_skeleton(abs_init_clone_path)  # eg: source/_repos-available
        self.setup_directory_skeleton(abs_base_symlink_path)  # eg: source/content

    def get_normalized_manifest(self):
        """
        Handle the repository cloning and updating process when Sphinx initializes.
        - Read/normalize/validate the manifest
        - Initialize the directory tree skeleton
        - Manage the repositories (cloning, updating, and symlinking)
        - returns: manifest
        """
        logger.info(colorize_success(f"\n══{brighten('BEGIN REPO_MANAGER')}══\n"))

        # Ensure working dir is always from manifest working dir for consistency
        # (!) This particularly fixes a RTD bug that adds an extra source/ dir, breaking paths
        os.chdir(ABS_MANIFEST_PATH_DIR)
        logger.info(colorize_path(f"- working_dir (ABS_MANIFEST_PATH_DIR): '{brighten(os.getcwd())}'"))

        manifest = self.read_normalize_manifest()

        # Is this extension enabled (default true)?
        enable_repo_manager = manifest.get('enable_repo_manager', True)
        if not enable_repo_manager:
            logger.warning("[repo_manager] Disabled in manifest (enable_repo_manager) - skipping extension!")
            return manifest

        self.debug_mode = manifest['debug_mode']

        enable_repo_manager_local = manifest.get('enable_repo_manager_local', True)
        if not self.read_the_docs_build and not enable_repo_manager_local:
            logger.warning("[repo_manager] Disabled in manifest (enable_repo_manager_local) - skipping extension"
                           f" (but only skipping {brighten('locally')}; will resume in RTD deployments)!")
            return manifest

        self.init_dir_tree(manifest)
        return manifest

    @staticmethod
    def setup_directory_skeleton(create_path_to):
        """
        Ensure directory exists and optionally clear its contents.
        (!) Deleting or overriding may require ADMIN
        """
        try:
            os.makedirs(create_path_to, exist_ok=True)
        except OSError as e:
            raise RepositoryManagementError(f"\nFailed to create directory '{create_path_to}': {str(e)}")

    @staticmethod
    def create_symlink(symlink_src_path, symlink_target_path):
        """
        Create or update a symlink using relative paths.
        (!) overwrite only works if running in ADMIN
        (!) In Windows, symlinking is the *opposite* src and destination of Unix
        - symlink_src_path       # eg: "source/_repos-available/account_services-v2.1.0/docs/source"
        - symlink_target_path    # eg: "source/content/account_services"
                                 # eg: "source/content/account_services/RELEASE_NOTES.rst"
        """
        # Check if the symlink already exists
        if os.path.islink(symlink_target_path):
            # Check if the existing symlink points to the correct source path
            if os.readlink(symlink_target_path) == str(symlink_src_path):
                logger.info(colorize_success(f"  - Symlink already exists and is correct."))
                return
            else:
                logger.info(colorize_action(f"  - Removing old symlink: '{brighten(symlink_target_path)}'"))
                os.unlink(symlink_target_path)
        elif os.path.exists(symlink_target_path):
            logger.error(f"  - Error: Target path exists and is not a symlink: {symlink_target_path}")
            raise RepositoryManagementError(
                f"\nCannot create symlink, target path exists and is not a symlink: {symlink_target_path}")

        # Create the symlink
        os.symlink(symlink_src_path, symlink_target_path)
        logger.info(colorize_success(f"  - New symlink created: "
                                     f"'{brighten(symlink_target_path)}' -> "
                                     f"'{brighten(symlink_src_path)}'"))

    @staticmethod
    def log_repo_paths(
            debug_mode,
            tag_versioned_clone_src_repo_name,
            tag_versioned_clone_src_path,
            rel_symlinked_repo_path,
    ):
        """ Log paths for production [and optionally debugging, if debug_mode]. """

        action_str = colorize_action(f"📁 | Working Dirs:")
        logger.info(f"[{tag_versioned_clone_src_repo_name}] {action_str}")
        logger.info(colorize_path(f"  - Repo clone src path: '{brighten(tag_versioned_clone_src_path)}'"))
        logger.info(colorize_path(f"  - Repo symlink target path: '{brighten(rel_symlinked_repo_path)}'"))

    def process_repo(
            self,
            repo_info,
            stash_and_continue_if_wip,
            log_queue,
            current_repo_num,
            total_repos_num,
    ):
        """ Process a single repository and queue logs. """
        log_entries = []
        _meta = repo_info['_meta']
        tag_versioned_clone_src_repo_name = _meta['tag_versioned_clone_src_repo_name']  # eg: "account_services-v2.1.0"
        rel_symlinked_repo_path = _meta['rel_symlinked_repo_path']  # eg: "source/content/account_services"

        log_entries.append(colorize_action("\n-----------------------\n"
                                           f"[Repo {current_repo_num}/{total_repos_num}]"))

        # Ensure repo is active
        active = repo_info['active']
        if not active:
            log_entries.append(colorize_action(f"[{rel_symlinked_repo_path}] Repository !active; skipping..."))
            for entry in log_entries:
                log_queue.put(entry)
            return

        # eg: "source/_repos-available/account_services-v2.1.0"
        tag_versioned_clone_src_path = _meta['tag_versioned_clone_src_path']
        debug_mode = self.manifest['debug_mode']
        repo_sparse_path = self.manifest['repo_sparse_path']
        rel_init_clone_path_root_symlink_src = repo_info['init_clone_path_root_symlink_src_override']

        log_entries.append(colorize_action(f"📁 | Working Dirs:"))
        log_entries.append(colorize_path(f"  - Repo clone src path: '{brighten(tag_versioned_clone_src_path)}'"))
        log_entries.append(colorize_path(f"  - Repo symlink target path: '{brighten(rel_symlinked_repo_path)}'"))

        self.clone_and_symlink(
            repo_info,
            tag_versioned_clone_src_repo_name,
            tag_versioned_clone_src_path,
            rel_symlinked_repo_path,
            stash_and_continue_if_wip,
            repo_sparse_path,
            rel_init_clone_path_root_symlink_src,
            log_entries,
        )

        # Queue log entries
        for entry in log_entries:
            log_queue.put(entry)

    def manage_repositories(self, manifest):
        if not manifest:
            raise RepositoryManagementError('No manifest found (or failed when normalizing)')

        stash_and_continue_if_wip = manifest['stash_and_continue_if_wip']
        repositories = list(manifest['repositories'].items())
        log_queue = queue.Queue()  # Queue for handling log entries

        # Decide number of workers to use, depending if local or RTD host
        max_num_workers = manifest['max_workers_local'] if not self.read_the_docs_build \
            else manifest['max_workers_rtd']
        logger.info(colorize_action(f"🤖 | Using {max_num_workers} worker(s) for multi-threading"))

        total_repos_num = len(repositories)
        current_repo_num = 1
        num_done = 0

        with concurrent.futures.ThreadPoolExecutor(max_num_workers) as executor:
            futures = []
            for repo_name, repo_info in repositories:
                # Attempt to cancel all futures if a shutdown (CTRL+C) is detected
                if self.shutdown_flag:
                    raise SystemExit

                future = executor.submit(
                    self.process_repo,
                    repo_info,
                    stash_and_continue_if_wip,
                    log_queue,
                    current_repo_num,
                    total_repos_num)

                futures.append(future)
                current_repo_num += 1

            # Handle the completion of tasks, ensuring we process results or catch exceptions
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()

                    num_done += 1
                    completed_msg = f"✅ | Completed {brighten(f'{num_done}/{total_repos_num}')} repositories."
                    logger.info(colorize_success(completed_msg))
                except Exception as e:
                    with self.lock:
                        logger.error(f"Failed to manage repository: {e}")
                    for future in futures:
                        future.cancel()
                    raise SystemExit

        # Process all remaining logs
        while not log_queue.empty():
            log_entry = log_queue.get()
            logger.info(log_entry)

        completed_msg = f"✅ | Job's done ({brighten(total_repos_num)} repos)."
        logger.info(f'\n{colorize_success(completed_msg)}')

    def clone_and_symlink(
            self,
            repo_info,
            tag_versioned_clone_src_repo_name,
            rel_tag_versioned_clone_src_path,
            rel_symlinked_repo_path,
            stash_and_continue_if_wip,
            repo_sparse_path,
            rel_init_clone_path_root_symlink_src,
            log_entries,
    ):
        """
        Clone the repository if it does not exist and create a symlink in the base symlink path.
        - repo_name                              # eg: "account_services"
        - rel_tag_versioned_clone_src_repo_name  # eg: "account_services-v2.1.0"
        - rel_init_clone_path                    # eg: "source/_repos-available"
        - rel_tag_versioned_clone_src_path       # eg: "source/_repos-available/account_services-v2.1.0"
        - rel_symlinked_repo_path                # eg: "source/content/account_services/docs/source"
        - log_entries will be appended with the results of the operation, logging in chunks
          - This is to handle async logs so it's still chronological
        """
        _meta = repo_info['_meta']
        repo_url_dotgit = _meta['url_dotgit']
        has_tag = _meta['has_tag']

        tag = repo_info['tag'] if has_tag else None
        branch = repo_info['branch']

        try:
            # Clone the repo, if we haven't done so already
            cloned = False
            already_stashed = False  # To prevent some redundancy

            if self.shutdown_flag:  # Multi-threaded CTRL+C check
                raise SystemExit

            if not os.path.exists(rel_tag_versioned_clone_src_path):
                action_str = colorize_action(f"📦 | Sparse-cloning repo...")
                log_entries.append(f"[{tag_versioned_clone_src_repo_name}] {action_str}")
                log_entries.append(colorize_path(f"  - Src Repo URL: '{brighten(rel_tag_versioned_clone_src_path)}'"))

                git_helper = GitHelper()  # TODO: Place this instance @ top?
                git_helper.git_sparse_clone(
                    rel_tag_versioned_clone_src_path,
                    repo_url_dotgit,
                    branch,
                    repo_sparse_path,
                    stash_and_continue_if_wip,
                    log_entries=log_entries
                )

                if self.shutdown_flag:  # Multi-threaded CTRL+C check
                    raise SystemExit

                # Clean the repo to only use the specified sparse paths
                action_str = colorize_action(f"🧹 | Cleaning up what sparse-cloning missed...")
                log_entries.append(f"[{tag_versioned_clone_src_repo_name}] {action_str}")
                GitHelper.git_clean_sparse_docs_clone(
                    rel_tag_versioned_clone_src_path,
                    repo_sparse_path,
                    log_entries=log_entries
                )

                cloned = True
                if stash_and_continue_if_wip:
                    already_stashed = True
            else:
                action_str = colorize_action(f"🔃 | Fetching updates...")
                log_entries.append(f"[{tag_versioned_clone_src_repo_name}] {action_str}")

                GitHelper.git_fetch(
                    rel_tag_versioned_clone_src_path,
                    log_entries=log_entries
                )

            if self.shutdown_flag:  # Multi-threaded CTRL+C check
                raise SystemExit

            # Checkout to the specific branch or tag
            has_branch = 'branch' in repo_info
            if not cloned and has_branch:
                action_str = colorize_action(f"🔄 | Checking out branch '{brighten(branch)}'...")
                log_entries.append(f"[{tag_versioned_clone_src_repo_name}] {action_str}")

                should_stash = stash_and_continue_if_wip and not already_stashed
                GitHelper.git_checkout(
                    rel_tag_versioned_clone_src_path,
                    branch,
                    should_stash,
                    log_entries=log_entries
                )

                if stash_and_continue_if_wip:
                    already_stashed = True

            # If we don't have a tag, just checking out the branch is enough (we'll grab the latest commit)
            if has_tag:
                action_str = colorize_action(f"🔄 | Checking out tag '{brighten(tag)}'...")
                log_entries.append(f"[{tag_versioned_clone_src_repo_name}] {action_str}")

                should_stash = stash_and_continue_if_wip and not already_stashed
                GitHelper.git_checkout(
                    rel_tag_versioned_clone_src_path,
                    tag,
                    should_stash,
                    log_entries=log_entries
                )

                if stash_and_continue_if_wip:
                    already_stashed = True

            if self.shutdown_flag:  # Multi-threaded CTRL+C check
                raise SystemExit

            if not cloned:
                should_stash = stash_and_continue_if_wip and not already_stashed
                GitHelper.git_pull(
                    rel_tag_versioned_clone_src_path,
                    should_stash,
                    log_entries=log_entries
                )

                if stash_and_continue_if_wip:
                    already_stashed = True

            if self.shutdown_flag:  # Multi-threaded CTRL+C check
                raise SystemExit

            # Manage symlinks -- we want src to be the nested <repo>/docs/source/
            # (Optionally overridden via manifest `init_clone_path_root_symlink_src_override`)
            #
            # Convert string paths to Path objects and use the dynamic path
            init_symlink_src_path = Path(rel_tag_versioned_clone_src_path)
            abs_symlink_src_nested_path = init_symlink_src_path.joinpath(rel_init_clone_path_root_symlink_src).resolve()

            action_str = colorize_action("🔗 | Symlinking...")
            log_entries.append(f"[{tag_versioned_clone_src_repo_name}] {action_str}")

            # (1) Symlink content -> to nested repo
            log_entries.append(colorize_path(f"  - From clone src path: '{brighten(abs_symlink_src_nested_path)}'"))
            log_entries.append(
                colorize_path(f"  - To symlink path: '{brighten(rel_init_clone_path_root_symlink_src)}'"))

            try:
                self.create_symlink(
                    abs_symlink_src_nested_path,
                    rel_symlinked_repo_path
                )

                self._log_err_if_invalid_symlink(rel_symlinked_repo_path)  # Sanity check for successful link
            except Exception as e:
                logger.error(f"Error creating symlink: {str(e)}")

            if self.shutdown_flag:  # Multi-threaded CTRL+C check
                raise SystemExit

            # (2) Symlink content/RELEASE_NOTES.rst -> to nested repo/RELEASE_NOTES.rst (if src file exists)
            abs_release_notes_symlink_src_repo_path = Path(os.path.normpath(
                str(init_symlink_src_path.joinpath('docs/source/RELEASE_NOTES.rst')))).resolve()

            # Target path
            release_notes_symlink_target_repo_path = Path(os.path.normpath(
                str(Path(ABS_MANIFEST_PATH_DIR) / Path(rel_symlinked_repo_path) / 'RELEASE_NOTES.rst'))).resolve()

            if self.debug_mode:
                print(
                    f"*[debug_mode] Resolved source path for RELEASE_NOTES.rst: {abs_release_notes_symlink_src_repo_path}")
                print(
                    f"*[debug_mode] Resolved target path for RELEASE_NOTES.rst: {release_notes_symlink_target_repo_path}")

            if not abs_release_notes_symlink_src_repo_path.exists():
                logger.warning(f"No RELEASE_NOTES.rst found in '{abs_release_notes_symlink_src_repo_path}'")
            else:
                try:
                    self.create_symlink(
                        abs_release_notes_symlink_src_repo_path,
                        release_notes_symlink_target_repo_path)

                    # Sanity check for successful link
                    self._log_err_if_invalid_symlink(release_notes_symlink_target_repo_path)
                except Exception as e:
                    normalized_e = str(e).replace('\\\\', '/')
                    logger.error(f"Error creating symlink: {normalized_e}")

            # -------------------
            # Done with this repo
            success_str = colorize_success("✔️| Done.")
            log_entries.append(f"[{tag_versioned_clone_src_repo_name}] {success_str}")

        except subprocess.CalledProcessError as e:
            self.shutdown_flag = True  # Signal shutdown to other threads
            error_url = f"{repo_url_dotgit}/tree/{tag}"
            tags_url = f"{repo_url_dotgit}/-/tags"

            error_message = (f"\n\n{Fore.RED}[repo_manager] "
                             f"Failed to checkout branch/tag '{rel_symlinked_repo_path}'\n"
                             f"- Does the '{tag}' tag exist? {error_url}\n"
                             f"- Check available tags: {tags_url}{Fore.RESET}\n\n")
            log_entries.append(error_message)
            raise RepositoryManagementError(f'\n{error_message}')
        except Exception as e:
            self.shutdown_flag = True  # Signal shutdown to other threads
            error_message = (f"\n\n{Fore.RED}[repo_manager] "
                             f"Error during clone and checkout process for '{rel_symlinked_repo_path}'\n"
                             f"- Error: {str(e)}\n\n")
            log_entries.append(error_message)
            raise RepositoryManagementError(f'\n{error_message}')
        finally:
            # Log the queued entries at once
            for entry in log_entries:
                logger.info(entry)

    def main(self, app):
        """
        Handle the repository cloning and updating process when Sphinx initializes.
        - Read/normalize/validate the manifest
        - Initialize the directory tree skeleton
        - Manage the repositories (cloning, updating, and symlinking)
        """
        try:
            manifest = self.get_normalized_manifest()
            self.manage_repositories(manifest)
        except Exception as e:
            self.shutdown_flag = True  # Signal shutdown to other threads
            raise RepositoryManagementError(f"\nrepo_manager failure: {e}")
        finally:
            logger.info(colorize_success(f"\n══{brighten('END REPO_MANAGER')}══\n"))
            if self.debug_mode and not self.read_the_docs_build:
                raise RepositoryManagementError("\nManifest 'debug_mode' flag enabled: Stopping build for log review.")


# [ENTRY POINT] Set up the Sphinx extension
def setup(app):
    repo_manager = SphinxRepoManager(ABS_MANIFEST_PATH)
    app.connect('builder-inited', repo_manager.main)
