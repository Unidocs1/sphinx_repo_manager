"""
Xsolla Sphinx Extension: sphinx_repo_manager
- See README for more info
- If you edit this, be sure to re-run `pip -r requirements.txt` from proj root since it's an embedded pkg
"""

# Core, pathing, ops >>
import os  # file path ops
from pathlib import Path  # Path ops
import re  # regex ops
import sys  # Just for sys.exit, if !repositories
import time  # How long did it take to build?
import traceback  # Allow for stacktracing

# Async >>
import concurrent.futures  # Async multitasking
import threading  # Async multitasking
import queue  # For managing log entries
import signal  # For CTRL+C detection

# Yaml and logging >>
import yaml  # YAML file parsing
from dotenv import load_dotenv

from .log_styles import *  # Custom logging styles
from .git_helper import GitHelper  # Helper functions for git operations
from sphinx.util import logging  # Sphinx logging utility

# Constants for default settings
DEFAULT_STAGE = "dev_stage"  # 'dev_stage' or 'production_stage'
DEFAULT_MAX_WORKERS_LOCAL = 5
DEFAULT_MAX_WORKERS_RTD = 1  # Max 1 for free tiers; 2 for premium
DEFAULT_DEBUG_MODE = False
DEFAULT_STASH_AND_CONTINUE_IF_WIP = True
DEFAULT_INIT_CLONE_PATH = "_repos-available"
DEFAULT_BASE_SYMLINK_PATH = "content"
DEFAULT_REPO_SPARSE_PATH = "docs"
DEFAULT_DEFAULT_BRANCH = "dev"  # Since we'll be working with tags, 'master' wouldn't make sense as a fallback
DEFAULT_PRESERVE_GITLAB_GROUP = True
DEFAULT_GITLAB_GROUP_TO_LOWERCASE = True
DEFAULT_DOTENV_REPO_AUTH_USER = 'oauth2'  # Default user when using an access token / 2FA
DEFAULT_DOTENV_REPO_AUTH_TOKEN = ''
DEFAULT_REPOSITORIES = {}
DEFAULT_SKIP_REPO_UPDATES = False

# Options
THROW_ON_REPO_ERROR = False  # Recommended True

logger = logging.getLogger(__name__)  # Get logger instance

# Global flag to signal threads to shutdown
shutdown_flag = False


# Custom exception class for repository management errors
class RepositoryManagementError(Exception):
    if THROW_ON_REPO_ERROR:
        shutdown_flag = True
    pass


# RepoManager class to handle repository operations
class SphinxRepoManager:
    def __init__(self):
        load_dotenv()
        self.default_repo_auth_user = None
        self.default_repo_auth_token = None
        self.has_default_repo_auth_token = False
        
        self.start_time = time.time()  # Track how long it takes to build all repos
        self.end_time = None

        self.read_the_docs_build = os.environ.get("READTHEDOCS", None) == "True"
        self.manifest_path = ""
        self.manifest_base_path = ""
        self.manifest = {}
        self.debug_mode = False  # If True: +logs; stops build after ext is done

        # Multi-threading >>
        self.lock = threading.Lock()  # Lock for thread-safe logging
        self.shutdown_flag = False  # Flag to handle graceful shutdown
        self.errored_repo_name = None
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        if not self.shutdown_flag:
            print("⛔ Signal received (CTRL+C), initiating graceful shutdown...")
        self.shutdown_flag = True

    @staticmethod
    def _print_realtime_log(msg):
        """When multi-threading via a Future, print realtime logs here for the main thread."""
        print(msg)
        sys.stdout.flush()

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
        logger.info(colorize_action(f"📜 | [sphinx_repo_manager] Reading manifest..."))
        logger.info(
            colorize_path(f"   - Extension Src: '{brighten(self.manifest_base_path)}'")
        )
        logger.info(
            colorize_path(f"   - Manifest Src: '{brighten(self.manifest_path)}'")
        )

        # Read manifest file
        if not os.path.exists(self.manifest_path):
            logger.warning(
                f"repo_manifest.yml !found @ '{brighten(self.manifest_path)}' - skipping extension!"
            )
            sys.exit(0)

        with open(self.manifest_path, "r") as file:
            manifest = yaml.safe_load(file)

        # Remove .git from urls; inject hidden _meta prop per repo, etc
        # (!) Exits if repositories are empty
        manifest = self.validate_normalize_manifest_set_meta(manifest)
        self.manifest = manifest

        # Logs
        rel_repo_sparse_path = manifest["repo_sparse_path"]
        logger.info(
            colorize_path(f"   - repo_sparse_path: '{brighten(rel_repo_sparse_path)}'")
        )

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

        # Set constant root defaults
        manifest.setdefault('stage', DEFAULT_STAGE)
        manifest.setdefault('max_workers_local', DEFAULT_MAX_WORKERS_LOCAL)
        manifest.setdefault('max_workers_rtd', DEFAULT_MAX_WORKERS_RTD)
        manifest.setdefault('debug_mode', DEFAULT_DEBUG_MODE)
        manifest.setdefault('stash_and_continue_if_wip', DEFAULT_STASH_AND_CONTINUE_IF_WIP)
        manifest.setdefault('default_branch', DEFAULT_DEFAULT_BRANCH)
        manifest.setdefault('init_clone_path', DEFAULT_INIT_CLONE_PATH)
        manifest.setdefault('base_symlink_path', DEFAULT_BASE_SYMLINK_PATH)
        manifest.setdefault('repo_sparse_path', DEFAULT_REPO_SPARSE_PATH)
        manifest.setdefault('repositories', DEFAULT_REPOSITORIES)
        manifest.setdefault('dotenv_repo_auth_user', DEFAULT_DOTENV_REPO_AUTH_USER)
        manifest.setdefault('dotenv_repo_auth_token', DEFAULT_DOTENV_REPO_AUTH_TOKEN)

        # Set dynamic root defaults
        repo_sparse_path = manifest["repo_sparse_path"]
        manifest.setdefault(
            "init_clone_path_root_symlink_src", f"{repo_sparse_path}/source"
        )

        # Normalize path/to/slashes
        manifest["init_clone_path"] = os.path.normpath(manifest["init_clone_path"])
        manifest["init_clone_path_root_symlink_src"] = os.path.normpath(
            manifest["init_clone_path_root_symlink_src"]
        )
        manifest["base_symlink_path"] = os.path.normpath(manifest["base_symlink_path"])

        # Validate repositories
        if not manifest["repositories"]:
            logger.warning(
                "[sphinx_repo_manager] No repositories found in manifest - skipping extension!"
            )
            sys.exit(0)

        # Get the repo .env auth key *names* (not the key val) from the manifest
        dotenv_repo_auth_user_key_name = manifest['dotenv_repo_auth_user_key_name']
        dotenv_repo_auth_token_key_name = manifest['dotenv_repo_auth_token_key_name']

        # Get the .env key *values* from the .env using the key name from the manifest
        # (This allows for potentially multiple, overridable auth credentials)
        if dotenv_repo_auth_user_key_name:
            self.default_repo_auth_user = os.getenv(dotenv_repo_auth_user_key_name)
        if dotenv_repo_auth_token_key_name:
            self.default_repo_auth_token = os.getenv(dotenv_repo_auth_token_key_name)
            self.has_default_repo_auth_token = True
            
        if not self.default_repo_auth_token:
            logger.warning(f"WARNING: Missing or empty '{dotenv_repo_auth_token_key_name}' key in .env file")

        manifest['repo_sparse_path'] = repo_sparse_path.replace('\\', '/')  # Normalize to forward/slashes
        init_clone_path = os.path.normpath(manifest['init_clone_path'])
        base_symlink_path = os.path.normpath(manifest['base_symlink_path'])

        # Handle repositories dictionary
        repo_i = 0
        for repo_name, repo_info in manifest["repositories"].items():
            self.set_repo_meta(
                repo_info, repo_name, init_clone_path, base_symlink_path, manifest
            )

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
        """(!) Global manifest changes should be +1 up; not here (where it's an individual repo)."""
        if "_meta" not in repo_info:
            repo_info["_meta"] = {
                "url_dotgit": "",  # eg: "https://source.goxbe.io/core/account_services.git"
                "repo_name": "",  # eg: "account_services"
                "has_tag": False,
                "selected_repo_stage_info": {},  # { checkout, checkout_type }
                "rel_selected_repo_sparse_path": "",
                # "account-services-v2.1.0"
                # "repo-{repo_tag}"
                # - eg: "account-services-v2.1.0"
                "tag_versioned_clone_src_repo_name": "",
                # "{base_symlink_path}{symlink_path}-{tag_or_branch}"
                # - eg: "source/content/account_services" (no tag)
                "rel_symlinked_repo_path": "",
                # "{init_clone_path}/{tag_versioned_clone_src_repo_name}";
                # - eg: "source/_repos-available/account_services-v2.1.0"
                # - eg: "source/_repos-available/account_services--master"
                "tag_versioned_clone_src_path": "",
                # "{tag_versioned_clone_src_path}/docs/source/_static/{repo_name}"
                # eg: "source/_repos-available/account_services--master/docs/source/_static/{repo_name}"
                "tag_versioned_clone_path_to_inner_static": "",
            }

        # Dev or Production stage? Set fallbacks toe ach
        default_branch = manifest["default_branch"]
        fallback_stage_info = {
            "checkout": default_branch,
            "checkout_type": "branch",
        }
        repo_info.setdefault("dev_stage", fallback_stage_info)
        repo_info.setdefault("production_stage", fallback_stage_info)

        stage = manifest["stage"]  # 'dev_stage' or 'production_stage'
        selected_repo_stage_info = repo_info[stage]
        selected_repo_stage_info.setdefault("checkout", fallback_stage_info["checkout"])
        selected_repo_stage_info.setdefault(
            "checkout_type", fallback_stage_info["checkout_type"]
        )

        # Explicitly normalize checkout slashes/to/forward (if branch)
        selected_repo_stage_info["checkout"] = selected_repo_stage_info[
            "checkout"
        ].replace("\\", "/")
        selected_stage_checkout_branch_or_tag_name = selected_repo_stage_info[
            "checkout"
        ]  # Defaults to 'master'
        selected_stage_checkout_type = selected_repo_stage_info[
            "checkout_type"
        ]  # 'branch' or 'tag'
        has_tag = selected_stage_checkout_type == "tag"

        # Sanity check tag -- in XBE, we prefix with `v`
        if has_tag and not selected_stage_checkout_branch_or_tag_name.startswith("v"):
            print(
                f'{colorize_error(brighten("*[REALTIME]"))} tag \'{selected_stage_checkout_branch_or_tag_name}\' '
                f'does NOT prefix with a "v"'
            )

        # url: Req'd - Strip ".git" from suffix, if any (including SSH urls; we'll add it back via url_dotgit)
        url = repo_info.get("url", None)
        if not url:
            logger.error(f"Missing 'url' for repo '{repo_name}'")
            raise RepositoryManagementError(f"\nMissing 'url' for repo '{repo_name}'")

        if url.endswith(".git"):
            url = url[:-4]

        repo_info["url"] = url

        # Useful if we want to build with WIP changes (without stashing or committing)
        repo_info.setdefault("skip_repo_updates", DEFAULT_SKIP_REPO_UPDATES)

        # It's ok if !tag (we'll just checkout the branch); great for debugging
        # (!) However, this will affect our naming convention, normally "{repo}-{tag_or_branch}"
        tag = selected_stage_checkout_branch_or_tag_name if has_tag else None

        # Default symlink_path == repo name (the end of url after the last slash/)
        repo_name = url.split("/")[-1]
        repo_info.setdefault("symlink_path", repo_name)

        # Set other defaults
        repo_info.setdefault("active", True)
        repo_info.setdefault("repo_sparse_path_override", None)

        init_clone_path_root_symlink_src = manifest["init_clone_path_root_symlink_src"]
        repo_info.setdefault(
            "init_clone_path_root_symlink_src_override",
            init_clone_path_root_symlink_src,
        )

        # Set dynamic meta
        _meta = repo_info["_meta"]
        _meta["has_tag"] = has_tag
        _meta["url_dotgit"] = f"{url}.git"
        _meta["repo_name"] = repo_name

        # Repo auth
        dotenv_repo_auth_user = repo_info.get('dotenv_repo_auth_user', None)
        dotenv_repo_auth_token = repo_info.get('dotenv_repo_auth_token', None)
        _meta['dotenv_repo_auth_user'] = dotenv_repo_auth_user
        _meta['dotenv_repo_auth_token'] = dotenv_repo_auth_token

        # If tag, append "-{tag} to clone src repo name
        # If !tag, append "--{branch} to clone src repo name
        # This helps us easily identify the clone src without even entering the dir
        # (!) All repos must have unique names for this to auto-symlink without repo names or tags
        if has_tag:
            # "repo-{tag}"; eg: "account-services-v2.1.0"
            _meta["tag_versioned_clone_src_repo_name"] = f"{repo_name}-{tag}"
        else:
            # "repo-{"cleaned_branch"}"; eg: "account-services--master" or "account-services--some_nested_branch"
            # ^ Notice the "--" double slash separator. Only accept alphanumeric chars; replace all others with "_"
            pattern = r"\W+"
            normalized_repo_name_for_dir = (
                selected_stage_checkout_branch_or_tag_name.replace("/", "--")
            )
            normalized_repo_name_for_dir = re.sub(
                pattern, "_", normalized_repo_name_for_dir
            )
            _meta["tag_versioned_clone_src_repo_name"] = (
                f"{repo_name}--{normalized_repo_name_for_dir}"
            )

        # {base_symlink_path}{symlink_path}-{tag_or_branch}
        # eg: "source/content/account_services" (no tag)
        symlink_path = repo_info[
            "symlink_path"
        ]  # eg: "account_services" (or "-" for xbe_static_docs)
        _meta["rel_symlinked_repo_path"] = os.path.normpath(
            os.path.join(base_symlink_path, symlink_path)
        )

        # "{init_clone_path}/{tag_versioned_clone_src_repo_name}"
        tag_versioned_clone_src_repo_name = _meta["tag_versioned_clone_src_repo_name"]
        _meta["tag_versioned_clone_src_path"] = os.path.normpath(
            os.path.join(init_clone_path, tag_versioned_clone_src_repo_name)
        )

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
        rel_init_clone_path = manifest["init_clone_path"]
        rel_base_symlink_path = manifest["base_symlink_path"]

        # Normalize paths -> log -> create dir skeleton
        abs_init_clone_path = os.path.abspath(rel_init_clone_path)
        abs_base_symlink_path = os.path.abspath(rel_base_symlink_path)

        logger.info(
            colorize_path(f"   - init_clone_path: '{brighten(abs_init_clone_path)}'")
        )
        logger.info(
            colorize_path(
                f"   - base_symlink_path: '{brighten(abs_base_symlink_path)}'"
            )
        )
        logger.info(
            colorize_path(
                f"   - source_static_path: '{brighten(self.source_static_path)}'"
            )
        )
        logger.info(
            colorize_path(
                f"   - source_doxygen_path: '{brighten(self.source_doxygen_path)}'"
            )
        )

        self.setup_directory_skeleton(
            abs_init_clone_path
        )  # eg: source/_repos-available
        self.setup_directory_skeleton(abs_base_symlink_path)  # eg: source/content

    def get_normalized_manifest(self, path: str | Path):
        """
        Handle the repository cloning and updating process when Sphinx initializes.
        - Read/normalize/validate the manifest
        - Initialize the directory tree skeleton
        - Manage the repositories (cloning, updating, and symlinking)
        - returns: manifest
        """
        logger.info(
            colorize_success(f"\n══{brighten('BEGIN SPHINX_REPO_MANAGER')}══\n")
        )
        self.manifest_path = Path(path).absolute()
        self.manifest_base_path = self.manifest_path.parent
        self.source_static_path = Path(self.manifest_base_path, "source", "_static")
        self.source_doxygen_path = Path(self.manifest_base_path, "source", "_doxygen")

        # Ensure working dir is always from manifest working dir for consistency
        manifest = self.read_normalize_manifest()
        self.debug_mode = manifest["debug_mode"]
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
            raise RepositoryManagementError(
                f"\nFailed to create directory '{create_path_to}': {str(e)}"
            )

    @staticmethod
    def create_symlink(
        symlink_src_existing_real_path, symlink_target_new_sym_path, log_entries
    ):
        """
        Create or update a symlink using relative paths.
        (!) overwrite only works if running in ADMIN
        (!) In Windows, symlinking is the *opposite* src and destination of Unix
        - symlink_src_path       # eg: "source/_repos-available/account_services-v2.1.0/docs/source"
        - symlink_target_path    # eg: "source/content/account_services"
                                 # eg: "source/content/account_services/RELEASE_NOTES.rst"
        """
        # Check if the symlink already exists
        if os.path.islink(symlink_target_new_sym_path):
            # Check if the existing symlink points to the correct source path
            if os.readlink(symlink_target_new_sym_path) == str(
                symlink_src_existing_real_path
            ):
                log_entries.append(
                    colorize_success(f"  - Symlink already exists and is correct.")
                )
                return
            else:
                log_entries.append(
                    colorize_action(
                        f"  - Removing old symlink: '{brighten(symlink_target_new_sym_path)}'..."
                    )
                )
                os.unlink(symlink_target_new_sym_path)
        elif os.path.exists(symlink_target_new_sym_path):
            log_entries.append(
                colorize_error(
                    f"Error: Target path exists and is not a symlink: {symlink_target_new_sym_path}"
                )
            )
            raise RepositoryManagementError(
                f"\nCannot create symlink, target path exists and is not a symlink: {symlink_target_new_sym_path}"
            )

        # Create the symlink
        os.symlink(symlink_src_existing_real_path, symlink_target_new_sym_path)
        logger.info(
            colorize_success(
                f"  - New symlink created: "
                f"'{brighten(symlink_target_new_sym_path)}' -> "
                f"'{brighten(symlink_src_existing_real_path)}'"
            )
        )

    @staticmethod
    def log_repo_paths(
        debug_mode,
        tag_versioned_clone_src_repo_name,
        rel_tag_versioned_clone_src_path,
        rel_symlinked_repo_path,
        log_entries,
    ):
        """Log paths for production [and optionally debugging, if debug_mode]."""

        action_str = colorize_action("Working Dirs:")
        log_entries.append(f"📁 [{tag_versioned_clone_src_repo_name}] {action_str}")

        abs_tag_versioned_clone_src_path = Path(
            rel_tag_versioned_clone_src_path
        ).resolve()
        
        abs_symlinked_repo_path = Path(rel_symlinked_repo_path).resolve()
        log_entries.append(
            colorize_path(
                f"  - Repo clone src path: '{brighten(abs_tag_versioned_clone_src_path.resolve())}'"
            )
        )
        log_entries.append(
            colorize_path(
                f"  - Repo symlink target path: '{brighten(abs_symlinked_repo_path.resolve())}'"
            )
        )

    def process_repo(
        self,
        stage,
        repo_info,
        stash_and_continue_if_wip,
        log_queue,
        current_repo_num,
        total_repos_num,
    ):
        """Process a single repository and queue logs."""
        log_entries = []
        _meta = repo_info["_meta"]
        repo_name = _meta["repo_name"]
        tag_versioned_clone_src_repo_name = _meta[
            "tag_versioned_clone_src_repo_name"
        ]  # eg: "account_services-v2.1.0"
        
        rel_symlinked_repo_path = _meta[
            "rel_symlinked_repo_path"
        ]  # eg: "source/content/account_services"
        
        log_entries.append(
            colorize_action(
                "\n-----------------------\n"
                f"[{repo_name}] [Repo {current_repo_num}/{total_repos_num}]"
            )
        )

        # Ensure repo is active
        active = repo_info["active"]
        if not active:
            log_entries.append(
                colorize_action(
                    f"{rel_symlinked_repo_path} Repository "
                    f"'{brighten(repo_name)}' !active; skipping..."
                )
            )
            for entry in log_entries:
                log_queue.put(entry)
            return

        # eg: "source/_repos-available/account_services-v2.1.0"
        tag_versioned_clone_src_path = _meta["tag_versioned_clone_src_path"]
        debug_mode = self.manifest["debug_mode"]
        repo_sparse_path = self.manifest["repo_sparse_path"]

        # eg: "{repo_sparse_path}/source/content"
        repo_sparse_path_override = repo_info["repo_sparse_path_override"]
        has_repo_sparse_path_override = bool(repo_sparse_path_override)
        rel_selected_repo_sparse_path = (
            repo_sparse_path_override
            if has_repo_sparse_path_override
            else repo_sparse_path
        )
        _meta["rel_selected_repo_sparse_path"] = rel_selected_repo_sparse_path

        # Get rel_selected_clone_path_root_symlink_src
        # eg: 'docs' - overridable with optional {repo_sparse_path} replacements
        init_clone_path_root_symlink_src_override = repo_info[
            "init_clone_path_root_symlink_src_override"
        ]
        has_init_clone_path_root_symlink_src_override = bool(
            init_clone_path_root_symlink_src_override
        )
        if has_init_clone_path_root_symlink_src_override:
            # Supports {repo_sparse_path} template to replace -- use the selected path (already considered overrides)
            repo_info["init_clone_path_root_symlink_src_override"] = repo_info[
                "init_clone_path_root_symlink_src_override"
            ].replace("{repo_sparse_path}", rel_selected_repo_sparse_path)
            
            # Update the local var
            init_clone_path_root_symlink_src_override = repo_info[
                "init_clone_path_root_symlink_src_override"
            ]
            
            has_init_clone_path_root_symlink_src_override = True
        rel_selected_clone_path_root_symlink_src = (
            init_clone_path_root_symlink_src_override
            if has_init_clone_path_root_symlink_src_override
            else repo_sparse_path
        )

        # Misc
        repo_name = _meta["repo_name"]

        # Logs + Override checks
        self.log_repo_paths(
            debug_mode,
            tag_versioned_clone_src_repo_name,
            tag_versioned_clone_src_path,
            rel_symlinked_repo_path,
            log_entries,
        )

        if has_repo_sparse_path_override:
            log_entries.append(
                colorize_path(
                    f"  - (!) Overriding repo_sparse_path: '{brighten(repo_sparse_path_override)}'"
                )
            )

        if has_init_clone_path_root_symlink_src_override:
            log_entries.append(
                colorize_path(
                    f"  - (!) Overriding init_clone_path_root_symlink_src: '{brighten(init_clone_path_root_symlink_src_override)}'"
                )
            )

        # Pass the info (mostly paths) to an individual repo handler
        try:
            self.clone_and_symlink(
                stage,
                repo_info,
                repo_name,
                tag_versioned_clone_src_repo_name,
                tag_versioned_clone_src_path,
                rel_symlinked_repo_path,
                stash_and_continue_if_wip,
                rel_selected_repo_sparse_path,
                rel_selected_clone_path_root_symlink_src,
                log_entries,
            )
        except Exception as e:
            info1 = (
                f"- HINT: For continued issues, try deleting your source/ "
                f"`_repos-available/` and/or `content/` dirs to regenerate."
            )
            info2 = f"- HINT: You may see more logs below due to already-queued async-threaded logs"
            bright_info = colorize_error(brighten(f"{info1}\n{info2}\n"))
            stacktrace = traceback.format_exc()
            error_message = f"\n{Fore.RED}Failed to clone_and_symlink: {str(e)}.\n{stacktrace}\n{bright_info}"

            self.errored_repo_name = repo_name
            raise RepositoryManagementError(f"\n{error_message}")
        finally:
            # Log the queued entries at once
            for entry in log_entries:
                logger.info(entry)

    def manage_repositories(self, manifest):
        if not manifest:
            raise RepositoryManagementError(
                "No manifest found (or failed when normalizing)"
            )

        self.init_dir_tree(manifest)

        stash_and_continue_if_wip = manifest["stash_and_continue_if_wip"]
        debug_mode = manifest["debug_mode"]
        stage = manifest["stage"]
        repositories = list(manifest["repositories"].items())
        log_queue = queue.Queue()  # Queue for handling log entries

        # Decide number of workers to use, depending if local or RTD host
        max_num_workers = (
            manifest["max_workers_local"]
            if not self.read_the_docs_build
            else manifest["max_workers_rtd"]
        )
        logger.info(
            colorize_action(
                f"🤖 | Using {max_num_workers} worker(s) for multi-threading\n"
            )
        )

        total_repos_num = len(repositories)
        current_repo_num = 1
        num_done = 0

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=max_num_workers
        ) as executor:
            futures = []
            for repo_name, repo_info in repositories:
                # Attempt to cancel all futures if a shutdown (CTRL+C) is detected
                if self.shutdown_flag:
                    raise SystemExit

                if debug_mode:
                    logger.info(
                        f'{colorize_action(brighten("*[REALTIME]"))} Starting {repo_name} mgmt...'
                    )

                future = executor.submit(
                    self.process_repo,
                    stage,
                    repo_info,
                    stash_and_continue_if_wip,
                    log_queue,
                    current_repo_num,
                    total_repos_num,
                )

                futures.append(future)
                current_repo_num += 1

            # Handle the completion of tasks, ensuring we process results or catch exceptions
            for future_inner in concurrent.futures.as_completed(futures):
                try:
                    future_inner.result()

                    # Process all remaining logs
                    while not log_queue.empty():
                        log_entry = log_queue.get()
                        logger.info(log_entry)

                    num_done += 1
                    completed_msg = (
                        f"{colorize_action(brighten('*[REALTIME]'))} ✅ | Completed "
                        f"{brighten(f'{num_done}/{total_repos_num}')} repositories."
                    )
                    logger.info(colorize_success(completed_msg))
                except Exception as e:
                    with self.lock:
                        logger.error(f"Failed to manage repository: {str(e)}")
                    if THROW_ON_REPO_ERROR:
                        for inner_future in futures:
                            inner_future.cancel()
                        raise SystemExit

        all_completed_msg = f"✅ | Job's done ({brighten(total_repos_num)} repos)."
        logger.info(f"\n{colorize_success(all_completed_msg)}")

    def clone_and_symlink(
        self,
        stage,  # 'dev_stage' or 'production_stage'
        repo_info,
        repo_name,
        tag_versioned_clone_src_repo_name,
        rel_tag_versioned_clone_src_path,
        rel_symlinked_repo_path,
        stash_and_continue_if_wip,
        rel_selected_repo_sparse_path,
        rel_selected_clone_path_root_symlink_src,
        log_entries,
    ):
        """
        1. Clone the repository if it does not exist
        2. Create a filtered repo symlink
        3. Create a RELEASE_NOTES symlink
        4. Create a _static/{repo_name} symlink
        ----------------------------------------------
        - stage                                      # eg: "dev_stage" or "production_stage"
        - repo_name                                  # eg: "account_services"
        - rel_tag_versioned_clone_src_repo_name      # eg: "account_services-v2.1.0"
        - rel_init_clone_path                        # eg: "source/_repos-available"
        - rel_tag_versioned_clone_src_path           # eg: "source/_repos-available/account_services-v2.1.0"
        - rel_symlinked_repo_path                    # eg: "source/content/account_services/docs/source"
        - rel_selected_repo_sparse_path              # eg: "docs"
        - rel_selected_clone_path_root_symlink_src   # eg: "docs/source"
        - abs_static_dir_path                        # eg: main repo "docs/source/_static"
        - log_entries will be appended with the results of the operation, logging in chunks
          - This is to handle async logs so it's still chronological
        """

        _meta = repo_info["_meta"]
        repo_url_dotgit = _meta["url_dotgit"]
        skip_repo_updates = repo_info["skip_repo_updates"]

        repo_stage_info = repo_info[stage]  # { checkout, checkout_type }
        checkout_branch_or_tag_name = repo_stage_info["checkout"]
        has_tag = _meta["has_tag"]

        # Clone the repo, if we haven't done so already
        cloned = False
        already_stashed = False  # To prevent some redundancy

        if self.shutdown_flag:  # Multi-threaded CTRL+C check
            raise SystemExit

        clone_repo = not os.path.exists(rel_tag_versioned_clone_src_path)
        if clone_repo:
            action_str = colorize_action(f"📦 [{repo_name}] Cloning repo...")
            print(f'{colorize_action(brighten("*[REALTIME]"))} {action_str}')
            log_entries.append(action_str)
            log_entries.append(
                colorize_path(
                    f"  - Src Repo URL: '{brighten(rel_tag_versioned_clone_src_path)}'"
                )
            )

            git_helper = GitHelper()  # TODO: Place this instance @ top?

            if self.has_default_repo_auth_token:
                formatted_repo_url = repo_url_dotgit.replace(
                    "://", 
                    f"://{self.default_repo_auth_user}:{self.default_repo_auth_token}@")
            else:
                formatted_repo_url = repo_url_dotgit

            try:
                git_helper.git_sparse_clone(
                    rel_tag_versioned_clone_src_path,
                    formatted_repo_url,
                    checkout_branch_or_tag_name,
                    has_tag,
                    rel_selected_repo_sparse_path,
                    stash_and_continue_if_wip,
                    log_entries=log_entries,
                )
            except Exception as e:
                inner_additional_info = (
                    f"Error sparse-cloning repo '{brighten(repo_name)}':\n- {str(e)}"
                )
                raise Exception(f"{inner_additional_info}") from e

            if self.shutdown_flag:  # Multi-threaded CTRL+C check
                raise SystemExit

            # Clean the repo to only use the specified sparse paths
            action_str = colorize_action("Cleaning up what sparse-cloning missed...")
            log_entries.append(f"🧹 [{tag_versioned_clone_src_repo_name}] {action_str}")

            try:
                GitHelper.git_clean_sparse_docs_clone(
                    rel_tag_versioned_clone_src_path,
                    rel_selected_repo_sparse_path,
                    log_entries=log_entries,
                )
            except Exception as e:
                additional_info = f"Error cleaning up sparse clone '{brighten(repo_name)}':\n- {str(e)}"
                raise Exception(f"{additional_info}") from e

            cloned = True
            print(
                f'{colorize_action(brighten("*[REALTIME]"))} ✅ [{repo_name}] Successfully cloned'
            )
            if stash_and_continue_if_wip:
                already_stashed = True
        else:
            # No need to clone: Let's still fetch (no pull) - including tags
            if skip_repo_updates:
                action_str = colorize_action(
                    f"Skipping pulled updates ({brighten('skip_repo_updates')}),"
                    f"but we'll still fetch..."
                )
                log_entries.append(
                    f"🔃 [{tag_versioned_clone_src_repo_name}] {action_str}"
                )
            elif has_tag:
                action_str = colorize_action(
                    f"Skipping pulled updates ({brighten('has_tag')}),"
                    f"but we'll still fetch..."
                )
                log_entries.append(
                    f"🔃 [{tag_versioned_clone_src_repo_name}] {action_str}"
                )
            else:
                action_str = colorize_action(f"Fetching updates...")
            log_entries.append(f"🔃 [{tag_versioned_clone_src_repo_name}] {action_str}")

            # Fetch (only), including new tags
            try:
                GitHelper.git_fetch(
                    rel_tag_versioned_clone_src_path, log_entries=log_entries
                )
            except Exception as e:
                additional_info = (
                    f"Error fetching updates for '{brighten(repo_name)}':\n- {str(e)}"
                )
                raise Exception(f"{additional_info}") from e

        if self.shutdown_flag:  # Multi-threaded CTRL+C check
            raise SystemExit

        # Checkout to the specific branch or tag (!) Requires a git fetch if checking out new tags)
        has_branch = "branch" in repo_info
        should_skip_branch_checkout = not cloned and has_branch and skip_repo_updates
        should_check_out_branch = not cloned and not has_tag and has_branch

        if should_skip_branch_checkout:
            action_str = colorize_action(
                f"Skipping branch checkout ({brighten('skip_repo_updates')})..."
            )
            log_entries.append(f"🔃 [{tag_versioned_clone_src_repo_name}] {action_str}")
        elif should_check_out_branch:
            action_str = colorize_action(
                f"Checking out branch '{brighten(checkout_branch_or_tag_name)}'..."
            )
            log_entries.append(f"🔄 [{tag_versioned_clone_src_repo_name}] {action_str}")

            should_stash = stash_and_continue_if_wip and not already_stashed

            try:
                GitHelper.git_checkout(
                    rel_tag_versioned_clone_src_path,
                    checkout_branch_or_tag_name,
                    should_stash,
                    log_entries=log_entries,
                )
            except Exception as e:
                additional_info = f"Error checking out branch '{brighten(checkout_branch_or_tag_name)}' for '{brighten(repo_name)}':\n- {str(e)}"
                raise Exception(f"{additional_info}") from e

            if stash_and_continue_if_wip:
                already_stashed = True

        # If we don't have a tag, just checking out the branch is enough (we'll grab the latest commit)
        if has_tag and skip_repo_updates:
            action_str = colorize_action(
                f"Skipping tag checkout ({brighten('skip_repo_updates')})..."
            )
            log_entries.append(f"🔃 [{tag_versioned_clone_src_repo_name}] {action_str}")
        if has_tag:
            action_str = colorize_action(
                f"Checking out tag '{brighten(checkout_branch_or_tag_name)}'..."
            )
            log_entries.append(f"🔄 [{tag_versioned_clone_src_repo_name}] {action_str}")

            should_stash = stash_and_continue_if_wip and not already_stashed

            try:
                GitHelper.git_checkout(
                    rel_tag_versioned_clone_src_path,
                    checkout_branch_or_tag_name,
                    should_stash,
                    log_entries=log_entries,
                )
            except Exception as e:
                additional_info = (
                    f"Error checking out tag '{brighten(checkout_branch_or_tag_name)}'"
                    f"for'{brighten(repo_name)}':\n- {str(e)}"
                )
                raise Exception(f"{additional_info}") from e

            if stash_and_continue_if_wip:
                already_stashed = True

        if self.shutdown_flag:  # Multi-threaded CTRL+C check
            raise SystemExit

        skip_git_pull = (not cloned and skip_repo_updates) or has_tag
        if skip_git_pull:
            skip_reason = "has_tag" if has_tag else "skip_repo_updates"
            action_str = colorize_action(
                f"Skipping git pull ({brighten(skip_reason)})..."
            )
            log_entries.append(f"🔃 [{tag_versioned_clone_src_repo_name}] {action_str}")
        elif not cloned:
            should_stash = stash_and_continue_if_wip and not already_stashed

            try:
                GitHelper.git_pull(
                    rel_tag_versioned_clone_src_path,
                    should_stash,
                    log_entries=log_entries,
                )
            except Exception as e:
                additional_info = (
                    f"Error pulling updates for '{brighten(repo_name)}':\n- {str(e)}"
                )
                raise Exception(f"{additional_info}") from e

            if stash_and_continue_if_wip:
                already_stashed = True

        if self.shutdown_flag:  # Multi-threaded CTRL+C check
            raise SystemExit

        self.repo_add_symlinks(
            repo_name,
            tag_versioned_clone_src_repo_name,
            rel_tag_versioned_clone_src_path,
            rel_symlinked_repo_path,
            rel_selected_clone_path_root_symlink_src,
            rel_selected_repo_sparse_path,
            log_entries,
        )

    def check_is_enabled_ext(self, manifest):
        """
        Reads against manifest `enable_repo_manager` `enable_repo_manager_local`:
        If !enabled, logs intention to skip the extension.
        - Returns: enabled (bool)
        """
        enable_repo_manager = manifest.get("enable_repo_manager", True)
        if not enable_repo_manager:
            logger.warning(
                f"\nDisabled in manifest ({brighten('enable_repo_manager')}) - skipping extension!"
            )
            return False  # not enabled

        enable_repo_manager_local = manifest.get("enable_repo_manager_local", True)
        if not self.read_the_docs_build and not enable_repo_manager_local:
            logger.warning(
                f"\nDisabled in manifest ({brighten('enable_repo_manager_local')}) - skipping extension!"
            )
            return False  # not enabled

        return True  # enabled

    def log_end_build_time(self):
        """Call when done building to set end_time and log calc from start_time."""
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        minutes, seconds = divmod(elapsed_time, 60)
        time_str = f"{int(minutes)}m{int(seconds)}s"
        logger.info(colorize_success(f"Build time: {brighten(time_str)}"))

    def main(self, app):
        """
        Handle the repository cloning and updating process when Sphinx initializes.
        - Read/normalize/validate the manifest
        - Initialize the directory tree skeleton
        - Manage the repositories (cloning, updating, and symlinking)
        """
        try:
            manifest = self.get_normalized_manifest(app.config.repo_manager_manifest)
            enabled = self.check_is_enabled_ext(manifest)
            if not enabled:
                return  # Skip this extension

            self.manage_repositories(manifest)
            self.log_end_build_time()

            if self.debug_mode and not self.read_the_docs_build:
                raise RepositoryManagementError(
                    "\nManifest 'debug_mode' flag enabled: Stopping build for log review."
                )
        except Exception as e:
            self.shutdown_flag = True  # Signal shutdown to other threads
            raise RepositoryManagementError(f"\nsphinx_repo_manager failure: {e}")
        finally:
            if self.shutdown_flag:
                repo_name_hint = (
                    f" Find '{brighten(self.errored_repo_name)}' error logs above ^"
                    if self.errored_repo_name
                    else ""
                )
                logger.error(
                    f"ERROR: Ended early (likely CTRL+C || error){repo_name_hint}"
                )

            logger.info(
                colorize_success(f"\n══{brighten('END SPHINX_REPO_MANAGER')}══\n")
            )

    def repo_add_symlink1_content_dir(
        self,
        tag_versioned_clone_src_repo_name,
        abs_clone_src_nested_path,
        rel_selected_clone_path_root_symlink_src,
        rel_symlinked_repo_path,
        log_entries,
    ):
        # (1) Symlink content -> to nested repo
        action_str = colorize_action("Symlinking repo nested sparse content...")
        log_entries.append(f"🔗 [{tag_versioned_clone_src_repo_name}] {action_str}")

        # Log + Validate clone src path
        log_entries.append(
            colorize_path(
                f"  - (1) From clone src path: '{brighten(abs_clone_src_nested_path)}'"
            )
        )
        if not abs_clone_src_nested_path.exists():
            raise Exception(
                f"Error creating symlink (1):\n- {abs_clone_src_nested_path}\n- Src path !exists"
            )

        log_entries.append(
            colorize_path(
                f"  - To symlink path: '{brighten(rel_selected_clone_path_root_symlink_src)}'"
            )
        )

        try:
            self.create_symlink(
                abs_clone_src_nested_path,
                rel_symlinked_repo_path,
                log_entries,
            )

            if not Path(rel_symlinked_repo_path).is_symlink():
                log_entries.append(
                    colorize_error(
                        f"Error creating symlink (1): '{rel_symlinked_repo_path}'"
                    )
                )

        except Exception as e:
            logger.error(f"Error creating symlink (1):\n- {str(e)}")

        if self.shutdown_flag:  # Multi-threaded CTRL+C check
            raise SystemExit

    def repo_add_symlink2_release_notes(
        self,
        tag_versioned_clone_src_repo_name,
        rel_symlinked_repo_path,
        init_symlink_src_path,
        log_entries,
    ):
        # (2) Symlink content/RELEASE_NOTES.rst -> to nested repo/RELEASE_NOTES.rst (if src file exists)
        # Existing real file path; eg: 'source/_repos-available/account_services-v2.1.0/RELEASE_NOTES.rst'
        abs_existing_real_release_notes_path = (
            Path(init_symlink_src_path).joinpath("RELEASE_NOTES.rst").resolve()
        )

        # Check if the source existing "real" file exists before attempting to create a symlink
        if abs_existing_real_release_notes_path.exists():
            try:
                # New symlink path; eg: 'source/content/account_services/RELEASE_NOTES.rst'
                abs_path_to_manifest = Path(self.manifest_base_path).resolve()
                abs_symlinked_repo_path = abs_path_to_manifest.joinpath(
                    rel_symlinked_repo_path
                )
                abs_new_symlink_release_notes_path = abs_symlinked_repo_path.joinpath(
                    "RELEASE_NOTES.rst"
                )

                action_str = colorize_action(
                    f"Symlinking '{brighten('RELEASE_NOTES.rst')}' content (from clone src root)..."
                )
                log_entries.append(
                    f"🔗 [{tag_versioned_clone_src_repo_name}] {action_str}"
                )
                log_entries.append(
                    colorize_path(
                        f"  - (2) From clone src path: '{brighten(abs_existing_real_release_notes_path)}'"
                    )
                )
                log_entries.append(
                    colorize_path(
                        f"  - To symlink path: '{brighten(abs_new_symlink_release_notes_path)}'"
                    )
                )

                self.create_symlink(
                    abs_existing_real_release_notes_path,
                    abs_new_symlink_release_notes_path,
                    log_entries,
                )

                # Sanity check for successful link
                if not Path(rel_symlinked_repo_path).is_symlink():
                    raise Exception("File is not detected as a symlink")
            except Exception as inner_e:
                normalized_e = str(inner_e).replace("\\\\", "/")
                log_entries.append(
                    colorize_error(f"Error creating symlink (2): {normalized_e}")
                )
        else:
            log_entries.append(
                colorize_warning(f"  - (2) No RELEASE_NOTES.rst found in source repo.")
            )

    def repo_add_symlink3_static_images_dir(
        self,
        tag_versioned_clone_src_repo_name,
        abs_clone_src_nested_path,
        rel_symlinked_repo_path,
        repo_name,
        rel_tag_versioned_clone_src_path,
        rel_selected_repo_sparse_path,
        log_entries,
    ):
        # (3) Symlink _static/images/{repo_name} -> to main doc
        action_str = colorize_action(f"Symlinking '_static/images/{repo_name}'...")
        log_entries.append(f"🔗 [{tag_versioned_clone_src_repo_name}] {action_str}")

        # Log + Validate clone src path to _static/{repo_name}
        abs_repo_static_dir_path = Path(
            rel_tag_versioned_clone_src_path,
            rel_selected_repo_sparse_path,
            "source",
            "_static",
            "images",
            repo_name,
        ).resolve()

        log_entries.append(
            colorize_path(
                f"  - (3) From from {repo_name} src path: "
                f"'{brighten(abs_repo_static_dir_path)}'"
            )
        )

        if not abs_repo_static_dir_path.exists():
            err_msg = f"Error creating symlink (3):\n- {abs_clone_src_nested_path}\n- abs_clone_src_nested_path !found"
            if THROW_ON_REPO_ERROR:
                raise Exception(
                    err_msg
                )  # TODO: Use this instead, once the architecture is setup
            else:
                log_entries.append(colorize_warning(err_msg))

        # source/_static/{repo_name}; eg: "source/_static/images/account_services"
        target_symlinked_static_dir_path = self.source_static_path.joinpath(
            "images", repo_name
        )
        log_entries.append(
            colorize_path(
                f"  - To symlink path: "
                f"'{brighten(target_symlinked_static_dir_path)}'"
            )
        )

        try:
            self.create_symlink(
                abs_repo_static_dir_path,
                target_symlinked_static_dir_path,
                log_entries,
            )

            if not Path(rel_symlinked_repo_path).is_symlink():
                raise Exception("File is not detected as a symlink")
        except Exception as e:
            logger.error(f"Error creating symlink (3):\n- {str(e)}")

    def repo_add_symlink4_static_blobs_dir(
        self,
        tag_versioned_clone_src_repo_name,
        abs_clone_src_nested_path,
        rel_symlinked_repo_path,
        repo_name,
        rel_tag_versioned_clone_src_path,
        rel_selected_repo_sparse_path,
        log_entries,
    ):
        """Src dir may not exist (unlike images/ that will 100% exist)"""
        abs_repo_static_dir_path = Path(
            rel_tag_versioned_clone_src_path,
            rel_selected_repo_sparse_path,
            "source",
            "_static",
            "blobs",
            repo_name,
        ).resolve()

        # If dir !exists, return
        if not abs_repo_static_dir_path.exists():
            # log_entries.append(colorize_warning(f"  - (4) No blobs found in source repo."))
            return

        # (4) Symlink _static/blobs/{repo_name} -> to main doc
        action_str = colorize_action(f"Symlinking '_static/blobs/{repo_name}'...")
        log_entries.append(f"🔗 [{tag_versioned_clone_src_repo_name}] {action_str}")

        # Log + Validate clone src path to _static/{repo_name}
        log_entries.append(
            colorize_path(
                f"  - (4) From from {repo_name} src path: "
                f"'{brighten(abs_repo_static_dir_path)}'"
            )
        )

        if not abs_repo_static_dir_path.exists():
            err_msg = f"Error creating symlink (3):\n- {abs_clone_src_nested_path}\n- abs_clone_src_nested_path !found"
            if THROW_ON_REPO_ERROR:
                raise Exception(
                    err_msg
                )  # TODO: Use this instead, once the architecture is setup
            else:
                log_entries.append(colorize_warning(err_msg))

        # source/_static/{repo_name}; eg: "source/_static/blobs/account_services"
        target_symlinked_static_dir_path = self.source_static_path.joinpath(
            "blobs", repo_name
        )
        log_entries.append(
            colorize_path(
                f"  - To symlink path: "
                f"'{brighten(target_symlinked_static_dir_path)}'"
            )
        )

        try:
            self.create_symlink(
                abs_repo_static_dir_path,
                target_symlinked_static_dir_path,
                log_entries,
            )

            if not Path(rel_symlinked_repo_path).is_symlink():
                raise Exception("File is not detected as a symlink")
        except Exception as e:
            logger.error(f"Error creating symlink (3):\n- {str(e)}")

    def repo_add_symlink5_doxygen_dir(
        self,
        tag_versioned_clone_src_repo_name,
        abs_clone_src_nested_path,
        rel_symlinked_repo_path,
        repo_name,
        rel_tag_versioned_clone_src_path,
        rel_selected_repo_sparse_path,
        log_entries,
    ):
        """Src dir may not exist"""
        abs_repo_doxygen_dir_path = Path(
            rel_tag_versioned_clone_src_path,
            rel_selected_repo_sparse_path,
            "source",
            "_doxygen",
            repo_name,
        ).resolve()

        # If dir !exists, return
        if not abs_repo_doxygen_dir_path.exists():
            # log_entries.append(colorize_warning(f"  - (4) No blobs found in source repo."))
            return

        # (5) Symlink _doxygen/{repo_name} -> to main doc
        action_str = colorize_action(f"Symlinking '_doxygen/{repo_name}'...")
        log_entries.append(f"🔗 [{tag_versioned_clone_src_repo_name}] {action_str}")

        # Log + Validate clone src path to _static/{repo_name}
        log_entries.append(
            colorize_path(
                f"  - (5) From from {repo_name} src path: "
                f"'{brighten(abs_repo_doxygen_dir_path)}'"
            )
        )

        if not abs_repo_doxygen_dir_path.exists():
            err_msg = f"Error creating symlink (3):\n- {abs_clone_src_nested_path}\n- abs_clone_src_nested_path !found"
            if THROW_ON_REPO_ERROR:
                raise Exception(
                    err_msg
                )  # TODO: Use this instead, once the architecture is setup
            else:
                log_entries.append(colorize_warning(err_msg))

        # source/_static/{repo_name}; eg: "source/_static/blobs/account_services"
        target_symlinked_doxygen_dir_path = self.source_doxygen_path.joinpath(repo_name)
        log_entries.append(
            colorize_path(
                f"  - To symlink path: "
                f"'{brighten(target_symlinked_doxygen_dir_path)}'"
            )
        )

        try:
            self.create_symlink(
                abs_repo_doxygen_dir_path,
                target_symlinked_doxygen_dir_path,
                log_entries,
            )

            if not Path(rel_symlinked_repo_path).is_symlink():
                raise Exception("File is not detected as a symlink")
        except Exception as e:
            logger.error(f"Error creating symlink:\n- {str(e)}")

    def repo_add_symlinks(
        self,
        repo_name,
        tag_versioned_clone_src_repo_name,
        rel_tag_versioned_clone_src_path,
        rel_symlinked_repo_path,
        rel_selected_clone_path_root_symlink_src,
        rel_selected_repo_sparse_path,
        log_entries,
    ):
        # Manage symlinks -- we want src to be the nested: <repo>/docs/source/
        # (!) `docs` may have an override (repo_sparse_path_override)
        # (Optionally overridden via manifest `init_clone_path_root_symlink_src_override`)
        #
        # Convert string paths to Path objects and use the dynamic path
        init_symlink_src_path = Path(rel_tag_versioned_clone_src_path)
        abs_clone_src_nested_path = init_symlink_src_path.joinpath(
            rel_selected_clone_path_root_symlink_src
        ).resolve()

        self.repo_add_symlink1_content_dir(
            tag_versioned_clone_src_repo_name,
            abs_clone_src_nested_path,
            rel_selected_clone_path_root_symlink_src,
            rel_symlinked_repo_path,
            log_entries,
        )

        self.repo_add_symlink2_release_notes(
            tag_versioned_clone_src_repo_name,
            rel_symlinked_repo_path,
            init_symlink_src_path,
            log_entries,
        )

        self.repo_add_symlink3_static_images_dir(
            tag_versioned_clone_src_repo_name,
            abs_clone_src_nested_path,
            rel_symlinked_repo_path,
            repo_name,
            rel_tag_versioned_clone_src_path,
            rel_selected_repo_sparse_path,
            log_entries,
        )

        self.repo_add_symlink4_static_blobs_dir(
            tag_versioned_clone_src_repo_name,
            abs_clone_src_nested_path,
            rel_symlinked_repo_path,
            repo_name,
            rel_tag_versioned_clone_src_path,
            rel_selected_repo_sparse_path,
            log_entries,
        )

        self.repo_add_symlink5_doxygen_dir(
            tag_versioned_clone_src_repo_name,
            abs_clone_src_nested_path,
            rel_symlinked_repo_path,
            repo_name,
            rel_tag_versioned_clone_src_path,
            rel_selected_repo_sparse_path,
            log_entries,
        )

        # -------------------
        # Done with this repo
        log_entries.append(
            f"✅️[{tag_versioned_clone_src_repo_name}] {colorize_success('Done.')}"
        )

        if self.shutdown_flag:  # Multi-threaded CTRL+C check
            raise SystemExit
