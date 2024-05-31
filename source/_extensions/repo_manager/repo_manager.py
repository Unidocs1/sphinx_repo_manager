"""
Xsolla Sphinx Extension: repo_manager
------------------------------------

Description:
This Sphinx extension is designed to automate the management of multiple documentation repositories as part
of building a larger, unified doc system. It facilitates the cloning and updating of external repositories
specified in a YAML manifest file, ensuring that each repository is checked out to the specified
tag before Sphinx documentation generation proceeds.

How it Works:
1. The extension reads a manifest file (`repo_manifest.yml`) that lists repositories with their respective
clone URLs and tags.
2. It checks if each repository is already cloned at the specified location.
3. If a repository is not found, it clones the repository from the provided URL to an initial clone path.
4. Git checkouts use sparse cloning in combination with git exclusions to only keep [ .git, docs ] dirs.
5. Symlinks are created from the clone path to the base symlink path specified in the YAML.

Usage:
1. Edit the `repo_manifest.yml` at your repo project root.
2. Ensure each repository listed in the manifest includes at least a `url` and a `tag`.
3. Optionally, specify `init_clone_path` and `base_symlink_path` in the manifest to manage where repositories
are cloned and how they are accessed.
4. Include this extension in your Sphinx `conf.py` file by adding the extension's path to `sys.path`
(source/_extensions/repo_manager) and including in the `extensions` list.

Requirements: See project root `requirements.txt` -> Install easily via project `root tools/requirements-install.ps1`

Entry point: setup(app) | This script is executed during the 'builder-inited' event of Sphinx,
which is triggered after Sphinx inits but before the build process begins.

# Tested in:
- Windows 11 via PowerShell7
"""
import os  # file path ops
import re  # regex ops
import subprocess
import sys  # Just for sys.exit, if !repositories

import yaml  # YAML file parsing
from log_styles import *  # Custom logging styles
from git_helper import GitHelper  # Helper functions for git operations
from sphinx.util import logging  # Sphinx logging utility

# Define base path and manifest path
ABS_BASE_PATH = os.path.abspath(os.path.dirname(__file__))
MANIFEST_NAME = 'repo_manifest.yml'
ABS_MANIFEST_PATH = os.path.normpath(os.path.join(
    ABS_BASE_PATH, '..', '..', '..', MANIFEST_NAME))

STOP_BUILD_ON_ERROR = True  # Whether to stop build on error
logger = logging.getLogger(__name__)  # Get logger instance


# Custom exception class for repository management errors
class RepositoryManagementError(Exception):
    pass


# RepoManager class to handle repository operations
class RepoManager:
    def __init__(self, abs_manifest_path):
        self.manifest_path = abs_manifest_path
        self.manifest = None

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
        logger.info(colorize_path(f"   - Base Path: '{brighten(ABS_BASE_PATH)}'"))
        logger.info(colorize_path(f"   - Manifest Src: '{brighten(MANIFEST_NAME)}'"))

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
        repo_sparse_path = manifest['repo_sparse_path']
        logger.info(colorize_path(f"   - repo_sparse_path: '{brighten(repo_sparse_path)}'"))

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
        manifest.setdefault('debug_mode', False)
        manifest.setdefault('stash_and_continue_if_wip', True)
        manifest.setdefault('default_branch', 'master')
        manifest.setdefault('init_clone_path', os.path.normpath('source/_repos-available'))
        manifest.setdefault('base_symlink_path', os.path.normpath('source/content'))
        manifest.setdefault('repo_sparse_path', 'docs')
        manifest.setdefault('repositories', {})

        # Validate repositories
        if not manifest['repositories']:
            logger.warning("[repo_manager] No repositories found in manifest - skipping extension!")
            sys.exit(0)

        repo_sparse_path = manifest['repo_sparse_path']
        manifest['repo_sparse_path'] = repo_sparse_path.replace('\\', '/')  # Normalize to forward/slashes
        init_clone_path = manifest['init_clone_path']
        base_symlink_path = manifest['base_symlink_path']
        repo_i = 0

        # Handle repositories dictionary
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
                'url_dotgit': '',                         # eg: "https://gitlab.acceleratxr.com/core/account_services.git"
                'repo_name': '',                          # eg: "account_services"
                'has_tag': False,                         # True if tag exists
                'rel_symlinked_repo_path': '',     # "{base_symlink_path}{symlink_path}-{tag_or_branch}"; eg: "source/content/account_services" (no tag)
                'tag_versioned_clone_src_repo_name': '',  # "repo-{repo_tag}"; eg: "account-services-v2.1.0"
                'tag_versioned_clone_src_path': '',       # "{init_clone_path}/{tag_versioned_clone_src_repo_name}";
                                                          # - eg: "source/_repos-available/account_services-v2.1.0"
                                                          # - eg: "source/_repos-available/account_services--master"
            }

        # url: Req'd - Strip ".git" from suffix, if any (including SSH urls; we'll add it back via url_dotgit)
        url = repo_info.get('url', None)
        if not url:
            logger.error(f"Missing 'url' for repo '{repo_name}'")
            raise RepositoryManagementError(f"Missing 'url' for repo '{repo_name}'")

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
            _meta['tag_versioned_clone_src_repo_name'] = f"{repo_name}-{tag}"  # "repo-{tag}"; eg: "account-services-v2.1.0"
        else:
            # "repo-{"cleaned_branch"}"; eg: "account-services--master" or "account-services--some_nested_branch"
            # ^ Notice the "--" double slash separator. Only accept alphanumeric chars; replace all others with "_"
            pattern = r'\W+'
            normalized_repo_name_for_dir = branch.replace("/", "--")
            normalized_repo_name_for_dir = re.sub(pattern, '_', normalized_repo_name_for_dir)
            _meta['tag_versioned_clone_src_repo_name'] = f"{repo_name}--{normalized_repo_name_for_dir}"

        # "{init_clone_path}/{tag_versioned_clone_src_repo_name}"
        tag_versioned_clone_src_repo_name = _meta['tag_versioned_clone_src_repo_name']
        _meta['tag_versioned_clone_src_path'] = os.path.normpath(os.path.join(
            init_clone_path, tag_versioned_clone_src_repo_name))

        _meta['rel_symlinked_repo_path'] = os.path.normpath(os.path.join(
            base_symlink_path, repo_name))

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

        logger.info(colorize_path(f"   - init_clone_path: '{brighten(rel_init_clone_path)}'"))
        logger.info(colorize_path(f"   - base_symlink_path: '{brighten(abs_base_symlink_path)}'"))

        self.setup_directory_skeleton(abs_init_clone_path)  # eg: source/_repos-available
        self.setup_directory_skeleton(abs_base_symlink_path)  # eg: source/content

    def read_manifest_manage_repos(self, app):
        """
        Handle the repository cloning and updating process when Sphinx initializes.
        - Read/noramlize/validate the manifest
        - Initialize the directory tree skeleton
        - Manage the repositories (cloning, updating, and symlinking)
        """
        logger.info(colorize_success(f"\n══{brighten('BEGIN REPO_MANAGER')}══\n"))
        try:
            manifest = self.read_normalize_manifest()

            # Is this extension enabled (default true)?
            enable_repo_manager = manifest.get('enable_repo_manager', True)
            if not enable_repo_manager:
                logger.warning("[repo_manager] Disabled in manifest (enable_repo_manager) - skipping extension!")
                return

            self.init_dir_tree(manifest)
            self.manage_repositories(manifest)
        except Exception as e:
            logger.error(f"Failed to manage_repositories {brighten('*See `Extension error` below*')}")
            if STOP_BUILD_ON_ERROR:
                raise RepositoryManagementError(f"clone_update_repos failure:\n- {e}")
        finally:
            logger.info(colorize_success(f"\n══{brighten('END REPO_MANAGER')}══\n"))

    @staticmethod
    def setup_directory_skeleton(create_path_to):
        """
        Ensure directory exists and optionally clear its contents.
        (!) Deleting or overriding may require ADMIN
        """
        try:
            os.makedirs(create_path_to, exist_ok=True)
        except OSError as e:
            raise RepositoryManagementError(f"Failed to create directory '{create_path_to}': {str(e)}")

    @staticmethod
    def create_symlink(rel_symlinked_repo_path, tag_versioned_clone_src_path):
        """
        Create or update a symlink using relative paths.
        (!) overwrite only works if running in ADMIN
        (!) In Windows, symlinking is the *opposite* src and destination of Unix
        - tag_versioned_clone_src_path   # eg: "source/_repos-available/account_services-v2.1.0"
        - rel_symlinked_repo_path # eg: "source/content/account_services"
        - ^ We need a lingering /slash on the end
        """
        # Is it already symlinked?
        if os.path.islink(rel_symlinked_repo_path):
            logger.info(colorize_success(f"  - Already linked."))
            return

        # Get the directory of the symlink path
        symlink_dir_name = os.path.dirname(rel_symlinked_repo_path)

        # Get the relative path from the symlink directory to the clone source path
        rel_tag_versioned_clone_src_path = os.path.relpath(tag_versioned_clone_src_path, symlink_dir_name)

        # Path is clean: Symlink now, after we ensure a "/" on the end
        os.symlink(rel_tag_versioned_clone_src_path, rel_symlinked_repo_path)

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

    def process_repo(self, repo_info, stash_and_continue_if_wip):
        """ Process a single repository from the manifest. """
        # Get paths from _meta
        _meta = repo_info['_meta']
        tag_versioned_clone_src_repo_name = _meta['tag_versioned_clone_src_repo_name']  # eg: "account_services-v2.1.0"
        rel_symlinked_repo_path = _meta['rel_symlinked_repo_path']  # eg: "source/content/account_services"

        # Ensure repo is active
        active = repo_info['active']
        if not active:
            logger.info(colorize_action(f"[{rel_symlinked_repo_path}] Repository !active; skipping..."))
            return

        # eg: "source/_repos-available/account_services-v2.1.0"
        tag_versioned_clone_src_path = _meta['tag_versioned_clone_src_path']
        debug_mode = self.manifest['debug_mode']
        repo_sparse_path = self.manifest['repo_sparse_path']

        self.log_repo_paths(
            debug_mode,
            tag_versioned_clone_src_repo_name,
            tag_versioned_clone_src_path,
            rel_symlinked_repo_path)

        self.clone_and_symlink(
            repo_info,
            tag_versioned_clone_src_repo_name,
            tag_versioned_clone_src_path,
            rel_symlinked_repo_path,
            stash_and_continue_if_wip,
            repo_sparse_path)

    def manage_repositories(self, manifest):
        """ Manage the cloning and checking out of repositories as defined in the manifest. """
        stash_and_continue_if_wip = manifest['stash_and_continue_if_wip']
        repositories = manifest['repositories'].items()

        # Track current/max repositories
        total_repos_num = len(repositories)
        current_repo_num = 1

        # for each repo:
        #     Prep paths, clone/fetch, checkout tagged version
        for repo_name, repo_info in repositories:
            logger.info(colorize_action(
                "\n-----------------------\n"
                f"[Repo {current_repo_num}/{total_repos_num}]"))

            self.process_repo(repo_info, stash_and_continue_if_wip)
            current_repo_num += 1

    def clone_and_symlink(
            self,
            repo_info,
            tag_versioned_clone_src_repo_name,
            tag_versioned_clone_src_path,
            rel_symlinked_repo_path,
            stash_and_continue_if_wip,
            repo_sparse_path,
    ):
        """
        Clone the repository if it does not exist and create a symlink in the base symlink path.
        - repo_name                       # eg: "account_services"
        - tag_versioned_clone_src_repo_name         # eg: "account_services-v2.1.0"
        - rel_init_clone_path             # eg: "source/_repos-available"
        - tag_versioned_clone_src_path    # eg: "source/_repos-available/account_services-v2.1.0"
        - rel_symlinked_repo_path  # eg: "source/content/account_services"
        """
        _meta = repo_info['_meta']
        repo_url_dotgit = _meta['url_dotgit']
        has_tag = _meta['has_tag']

        tag = repo_info['tag'] if has_tag else None
        branch = repo_info['branch']

        try:
            # Clone the repo, if we haven't done so already
            cloned = False
            if not os.path.exists(tag_versioned_clone_src_path):
                action_str = colorize_action(f"📦 | Sparse-cloning repo...")
                logger.info(f"[{tag_versioned_clone_src_repo_name}] {action_str}")
                logger.info(colorize_path(f"  - Src Repo URL: '{brighten(tag_versioned_clone_src_path)}'"))

                git_helper = GitHelper()  # TODO: Place this instance @ top?
                git_helper.git_sparse_clone(
                    tag_versioned_clone_src_path,
                    repo_url_dotgit,
                    branch,
                    repo_sparse_path,
                    stash_and_continue_if_wip)

                # Clean the repo to only use the specified sparse paths
                action_str = colorize_action(f"🧹 | Cleaning up what sparse-cloning missed...")
                logger.info(f"[{tag_versioned_clone_src_repo_name}] {action_str}")
                GitHelper.git_clean_sparse_docs_clone(tag_versioned_clone_src_path, repo_sparse_path)

                cloned = True
            else:
                action_str = colorize_action(f"🔃 | Fetching updates...")
                logger.info(f"[{tag_versioned_clone_src_repo_name}] {action_str}")

                GitHelper.git_fetch(tag_versioned_clone_src_path)

            # Checkout to the specific branch or tag
            has_branch = 'branch' in repo_info
            if not cloned and has_branch:
                action_str = colorize_action(f"🔄 | Checking out branch '{brighten(branch)}'...")
                logger.info(f"[{tag_versioned_clone_src_repo_name}] {action_str}")
                GitHelper.git_checkout(tag_versioned_clone_src_path, branch, stash_and_continue_if_wip)

            # If we don't have a tag, just checking out the branch is enough (we'll grab the latest commit)
            if has_tag:
                action_str = colorize_action(f"🔄 | Checking out tag '{brighten(tag)}'...")
                logger.info(f"[{tag_versioned_clone_src_repo_name}] {action_str}")
                GitHelper.git_checkout(tag_versioned_clone_src_path, tag, stash_and_continue_if_wip)

            # Manage symlinks
            action_str = colorize_action(f"🔗 | Symlinking...")
            logger.info(f"[{tag_versioned_clone_src_repo_name}] {action_str}")
            logger.info(colorize_path(f"  - From clone src path: '{brighten(tag_versioned_clone_src_path)}'"))
            logger.info(colorize_path(f"  - To symlink path: '{brighten(rel_symlinked_repo_path)}'"))
            self.create_symlink(rel_symlinked_repo_path, tag_versioned_clone_src_path)

            # Done with this repo
            success_str = colorize_success("✅ | Done.")
            logger.info(f"[{tag_versioned_clone_src_repo_name}] {success_str}")

        except subprocess.CalledProcessError as e:
            error_url = f"{repo_url_dotgit}/tree/{tag}"
            tags_url = f"{repo_url_dotgit}/-/tags"

            error_message = (f"\n\n{Fore.RED}[repo_manager] "
                             f"Failed to checkout branch/tag '{rel_symlinked_repo_path}'\n"
                             f"- Does the '{tag}' tag exist? {error_url}\n"
                             f"- Check available tags: {tags_url}{Fore.RESET}\n\n")
            raise RepositoryManagementError(error_message)
        except Exception as e:
            error_message = (f"\n\n{Fore.RED}[repo_manager] "
                             f"Error during clone and checkout process for '{rel_symlinked_repo_path}'\n"
                             f"- Error: {str(e)}\n\n")
            raise RepositoryManagementError(error_message)


# [ENTRY POINT] Set up the Sphinx extension
def setup(app):
    repo_manager = RepoManager(ABS_MANIFEST_PATH)
    app.connect('builder-inited', repo_manager.read_manifest_manage_repos)
    # app.connect('source-read', replace_paths)  # (!) WIP
