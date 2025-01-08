"""
Xsolla Sphinx Extension: sphinx_repo_manager
- See README for more info
"""
from sphinx.application import Sphinx
import os
from pathlib import Path
import re
import sys
import time
import traceback
import copy
import concurrent.futures
import threading
import queue
import signal
import yaml
from dotenv import load_dotenv
from .log_styles import *
from .git_helper import GitHelper
from sphinx.util import logging

# Progress bars, spinners >>
from rich.live import Live
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)

# Constants for default settings
CANDIDATE_RELEASE_NOTE_FILE_NAMES = ["RELEASE_NOTES.md", "RELEASE_NOTES.rst"]
STATIC_DOCS_DIR_NAME = "_static-docs"  # Static .rst content goes here, to be symlinked to DEFAULT_BASE_SYMLINK_PATH
DEFAULT_STAGE = "dev_stage"  # 'dev_stage' or 'production_stage'
DEFAULT_MAX_WORKERS_LOCAL = 5
DEFAULT_MAX_WORKERS_RTD = 1  # Max 1 for free tiers; 2 for premium
DEFAULT_DEBUG_MODE = False
DEFAULT_STASH_AND_CONTINUE_IF_WIP = True
DEFAULT_BASE_CLONE_PATH = "_repos-available"
DEFAULT_BASE_SYMLINK_PATH = "content"
DEFAULT_REPO_SPARSE_PATH = "docs"
DEFAULT_DEFAULT_BRANCH = ""  # Could be None; "" will prevent errs on normalization logic
DEFAULT_PRESERVE_GITLAB_GROUP = True
DEFAULT_GITLAB_GROUP_TO_LOWERCASE = True
DEFAULT_DOTENV_REPO_AUTH_USER_KEY_NAME = 'REPO_AUTH_USER'
DEFAULT_DOTENV_REPO_AUTH_USER_NAME = 'oauth2'  # Default user when using an access token / 2FA
DEFAULT_DOTENV_REPO_AUTH_TOKEN_KEY_NAME = 'REPO_AUTH_TOKEN'
DEFAULT_DOTENV_THROW_ON_MISSING_AUTH_TOKEN = True
DEFAULT_REPOSITORIES = {}
DEFAULT_SKIP_REPO_UPDATES = False
DEFAULT_STATIC_DOCS_SYMLINKED_CONTENT_DIR_NAME = '-'
DEFAULT_REPO_STAGE_CHECKOUT_TYPE = "branch"

# Options
THROW_ON_REPO_ERROR = True  # Recommended True

logger = logging.getLogger(__name__)  # Get logger instance
shutdown_flag = False


class RepositoryManagementError(Exception):
    """ Custom exception class for repository management errors. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if THROW_ON_REPO_ERROR:
            global shutdown_flag  # Ensure we modify the global variable
            shutdown_flag = True


class GitCloneError(RepositoryManagementError):
    """Raised when Git cloning fails."""
    pass


class SymlinkError(RepositoryManagementError):
    """Raised when symlink creation fails."""
    pass


class RepoTask:
    def __init__(self,
                 stage,
                 repo_info,
                 repo_name,
                 tag_versioned_clone_src_repo_name,
                 abs_tag_versioned_clone_src_path,
                 abs_symlinked_repo_path,
                 stash_and_continue_if_wip,
                 rel_selected_repo_sparse_path,
                 rel_selected_clone_path_root_symlink_src,
                 log_entries,
                 worker_task_id,
                 ):
        """ Object passed between repo operations to prevent arg spam. """
        self.stage = stage
        self.repo_info = repo_info
        self.repo_name = repo_name
        self.tag_versioned_clone_src_repo_name = tag_versioned_clone_src_repo_name
        self.abs_tag_versioned_clone_src_path = abs_tag_versioned_clone_src_path
        self.abs_symlinked_repo_path = abs_symlinked_repo_path
        self.stash_and_continue_if_wip = stash_and_continue_if_wip
        self.rel_selected_repo_sparse_path = rel_selected_repo_sparse_path
        self.rel_selected_clone_path_root_symlink_src = rel_selected_clone_path_root_symlink_src
        self.log_entries = log_entries
        self.worker_task_id = worker_task_id

        # Additional extracted data
        self.meta = repo_info["_meta"]  # Extract commonly accessed info
        self.skip_repo_updates = repo_info["skip_repo_updates"]
        self.has_branch = "branch" in repo_info
        self.has_tag = self.meta["has_tag"]
        self.repo_url_dotgit = self.meta["url_dotgit"]
        self.repo_url_dotgit_is_local_file = self.meta["repo_url_dotgit_is_local_file"]
        self.tag_versioned_clone_src_repo_name = self.meta["tag_versioned_clone_src_repo_name"]
        self.should_clone_repo = not os.path.exists(self.abs_tag_versioned_clone_src_path)
        self.checkout_branch_or_tag_name = self.get_selected_checkout_branch_or_tag_name()
        self.total_num_git_stages = self.calc_total_num_git_stages()
        self.progress_total = self.total_num_git_stages + 1
        self.should_stash = stash_and_continue_if_wip  # Later updated to False, if already stashed

        # Set later
        self.cloned = False
        self.already_stashed = False
        self.current_git_stage_num = 0
        self.is_done = False

    def get_selected_checkout_branch_or_tag_name(self):
        repo_stage_info = self.repo_info[self.stage]
        return repo_stage_info["checkout"]

    def calc_total_num_git_stages(self):
        if self.should_clone_repo:
            return 4  # 3 for clone stages: Receiving, Compressing, Resolving; then 1 for git switch

        if self.skip_repo_updates:
            return 0

        # git fetch (tag) || pull (!tag)
        total_stages = 1

        if self.has_tag:
            total_stages += 1  # git checkout the latest tag

        return total_stages


class SphinxRepoManager:
    """ See README for more info. """

    def __init__(self, app: Sphinx):
        self.app = app
        self.abs_confdir = app.confdir

        # Set @ conf.py
        self.repo_manager_manifest_path = app.config.repo_manager_manifest_path

        self._load_env()

        self.source_static_path = None
        self.source_doxygen_path = None
        self.base_symlink_path = DEFAULT_BASE_SYMLINK_PATH  # Eg: "content"

        self.env_repo_auth_user = None
        self.env_repo_auth_token = None
        self.has_env_repo_auth_token = False

        self.progress = Progress(
            SpinnerColumn(),
            "[white]{task.description}",
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            TextColumn("[{task.completed}/{task.total}]"),
            TimeElapsedColumn(),
        )
        self.live = Live(self.progress, refresh_per_second=10)

        self.start_time = time.time()  # Track how long it takes to build all repos
        self.end_time = None

        self.raw_manifest = {}
        self.manifest = {}
        self.debug_mode = False  # If True: +logs and stops build after ext is done (via arbitrary error)
        self.debug_stop_build_on_extension_done = False  # Allows for speedier iterations when debugging this extension

        # Multi-threading >>
        self.lock = threading.Lock()  # Allows thread-safe logging
        self.shutdown_flag = False
        self.errored_repo_name = None
        signal.signal(signal.SIGINT, self._signal_handler)

        # Initialize the main process
        self._init_main()

    def _load_env(self):
        """ Check for .env in several possible locations; ignore if RTD. """
        self.read_the_docs_build = os.getenv("READTHEDOCS", None) == "True"
        if self.read_the_docs_build:
            return

        # 1. Try default (working dir)
        dotenv_path = Path(os.getcwd(), ".env")
        success = load_dotenv(dotenv_path)
        if success:
            self.dotenv_path = dotenv_path
            return

        # 2. Try confdir-1 (from docs/source to /docs/
        dotenv_path = Path(self.abs_confdir, "../.env")
        success = load_dotenv(dotenv_path)
        if success:
            self.dotenv_path = dotenv_path
            return

        # 3. Try confdir-2 (from docs/source to /)
        dotenv_path = Path(self.abs_confdir, "../../.env")
        success = load_dotenv(dotenv_path)
        if success:
            self.dotenv_path = dotenv_path
            return

        # 4. Try default (working dir)-1
        dotenv_path = Path("../.env")
        success = load_dotenv(dotenv_path)
        if success:
            self.dotenv_path = dotenv_path
            return

        # Warning: No .env file found
        self.dotenv_path = dotenv_path

    def _signal_handler(self, signum, frame):
        if not self.shutdown_flag:
            print("⛔ Signal received (CTRL+C), initiating graceful shutdown ...")
        self.shutdown_flag = True

    def read_normalize_manifest(self, manifest_path):
        """
        Read and return the repository manifest from YAML file.
        - validate_normalize_manifest_set_meta():
            - Normalizes data, such as removing .git from git urls
            - Injects _meta prop objs per repo
            - Sets defaults, if any
            - Validates required fields
        """
        logger.info(colorize_action(f"📜 | Reading repo_manifest.yml ..."))
        logger.info(colorize_path(f"   - Manifest Src: '{brighten(manifest_path)}'"))

        # Read manifest file
        if not os.path.exists(manifest_path):
            logger.warning(f"repo_manifest.yml !found @ '{brighten(manifest_path)}' - skipping extension!")
            sys.exit(0)

        with open(manifest_path, "r") as file:
            self.raw_manifest = yaml.safe_load(file)  # Don't touch the raw ver

        # Remove .git from urls; inject hidden _meta prop per repo, etc
        self.manifest = copy.deepcopy(self.raw_manifest)
        self.manifest = self.validate_normalize_manifest_set_meta(self.manifest)
        self.debug_mode = self.manifest["debug_mode"]

        if self.debug_mode:
            print(f"   - 💡 | [debug_mode] .env REPO_AUTH_USER={os.getenv('REPO_AUTH_USER')}")

        rel_repo_sparse_path = self.manifest["repo_sparse_path"]
        logger.info(colorize_path(f"   - repo_sparse_path: '{brighten(rel_repo_sparse_path)}'"))

        return self.manifest

    def validate_normalize_manifest_set_meta(self, manifest):
        """
        Validates + normalizes YAML v1.2 manifest vals, such as removing .git from URLs,
        +injects hidden '_meta' prop, etc, sets default fallbacks, injects vals to to repositories{}
        """
        logger.info(colorize_action("🧹 | Validating & normalizing manifest ..."))

        # Set constant root defaults
        manifest.setdefault('stage', DEFAULT_STAGE)
        manifest.setdefault('max_workers_local', DEFAULT_MAX_WORKERS_LOCAL)
        manifest.setdefault('max_workers_rtd', DEFAULT_MAX_WORKERS_RTD)
        manifest.setdefault('debug_mode', DEFAULT_DEBUG_MODE)
        manifest.setdefault('stash_and_continue_if_wip', DEFAULT_STASH_AND_CONTINUE_IF_WIP)
        manifest.setdefault('default_branch', DEFAULT_DEFAULT_BRANCH)
        manifest.setdefault('base_clone_path', DEFAULT_BASE_CLONE_PATH)
        manifest.setdefault('base_symlink_path', DEFAULT_BASE_SYMLINK_PATH)
        manifest.setdefault('repo_sparse_path', DEFAULT_REPO_SPARSE_PATH)
        manifest.setdefault('repositories', DEFAULT_REPOSITORIES)
        manifest.setdefault('dotenv_repo_auth_user_key_name', DEFAULT_DOTENV_REPO_AUTH_USER_KEY_NAME)
        manifest.setdefault('dotenv_repo_auth_token_key_name', DEFAULT_DOTENV_REPO_AUTH_TOKEN_KEY_NAME)
        manifest.setdefault('throw_on_missing_auth_tokens', DEFAULT_DOTENV_THROW_ON_MISSING_AUTH_TOKEN)

        # Sanity check to ensure defaults for important vals (eg: If set explicitly as None by mistake)
        if not manifest['dotenv_repo_auth_user_key_name']:
            manifest['dotenv_repo_auth_user_key_name'] = DEFAULT_DOTENV_REPO_AUTH_USER_KEY_NAME
        if not manifest['dotenv_repo_auth_token_key_name']:
            manifest['dotenv_repo_auth_token_key_name'] = DEFAULT_DOTENV_REPO_AUTH_TOKEN_KEY_NAME

        # Dynamic defaults based on others
        repo_sparse_path = manifest['repo_sparse_path']
        default_base_clone_path_root_symlink_src = f"{repo_sparse_path}/source/content"
        manifest.setdefault('base_clone_path_root_symlink_src', default_base_clone_path_root_symlink_src)

        repo_sparse_path = manifest.get("repo_sparse_path", DEFAULT_REPO_SPARSE_PATH)

        # Normalize paths using Path and self.confdir
        manifest["base_clone_path"] = Path(self.abs_confdir) / manifest["base_clone_path"]
        manifest["base_symlink_path"] = Path(self.abs_confdir) / manifest["base_symlink_path"]
        manifest["base_clone_path_root_symlink_src"] = Path(manifest["base_clone_path_root_symlink_src"])

        # Convert to absolute paths
        manifest["base_clone_path"] = manifest["base_clone_path"].resolve()
        manifest["base_symlink_path"] = manifest["base_symlink_path"].resolve()

        # Validate repositories
        if not manifest["repositories"]:
            logger.warning("[sphinx_repo_manager] No repositories found in manifest - skipping extension!")
            sys.exit(0)

        # Get the repo env auth key *names* (not the key val) from the manifest
        # (!) This will be None if RTD, but will fallback to DEFAULT_DOTENV_REPO_AUTH_TOKEN_KEY_NAME, etc
        dotenv_repo_auth_user_key_name = manifest['dotenv_repo_auth_user_key_name']  # Default: 'REPO_AUTH_USER'
        dotenv_repo_auth_token_key_name = manifest['dotenv_repo_auth_token_key_name']  # Default: 'REPO_AUTH_TOKEN'

        # Get env by key name -- the user will *only* be injected into the url if the token is also present
        self.env_repo_auth_user = os.getenv(dotenv_repo_auth_user_key_name, DEFAULT_DOTENV_REPO_AUTH_USER_NAME)
        self.env_repo_auth_token = os.getenv(dotenv_repo_auth_token_key_name)

        # Sanity check - does the env have the commonly-required auth token val?
        self.has_env_repo_auth_token = bool(self.env_repo_auth_token)
        if not self.has_env_repo_auth_token:
            throw_on_missing_auth_token = self.manifest["throw_on_missing_auth_token"]
            logger.warning(f"   - ⚠️ WARNING: Missing '{dotenv_repo_auth_token_key_name}' env key "
                           f"(throw_on_missing_auth_token={throw_on_missing_auth_token})")
            if throw_on_missing_auth_token:
                raise RepositoryManagementError(f"\nMissing required env key '{dotenv_repo_auth_token_key_name}'")
        else:
            masked_token = '*' * len(self.env_repo_auth_token) if self.has_env_repo_auth_token else "None"
            print(f"   - 💡 | [debug_mode] .env {dotenv_repo_auth_token_key_name}={masked_token}")

        manifest['repo_sparse_path'] = Path(repo_sparse_path)

        # Convert to absolute paths based on self.confdir
        abs_base_clone_path = Path(self.abs_confdir) / manifest['base_clone_path']
        abs_base_symlink_path = Path(self.abs_confdir) / manifest['base_symlink_path']

        # Add to self
        self.base_symlink_path = self.manifest["base_symlink_path"]

        repo_i = 0
        for repo_name, repo_info in manifest["repositories"].items():
            self.set_repo_meta(
                repo_info,
                repo_name,
                abs_base_clone_path,
                abs_base_symlink_path,
                manifest,
            )

            repo_i += 1

        return manifest

    @staticmethod
    def set_repo_meta(
            repo_info,
            repo_name,
            base_clone_path,
            abs_base_symlink_path,
            manifest,
    ):
        if "_meta" not in repo_info:
            repo_info["_meta"] = {
                "url_dotgit": "",
                "repo_url_dotgit_is_local_file": False,
                "repo_url_dotgit_local_file_abs_path": "",
                "repo_name": "",
                "has_tag": False,
                "selected_repo_stage_info": {},
                "rel_selected_repo_sparse_path": "",
                "tag_versioned_clone_src_repo_name": "",
                "abs_symlinked_repo_path": "",
                "tag_versioned_clone_src_path": "",
                "tag_versioned_clone_path_to_inner_static": "",
            }

        # 'dev_stage' or 'production_stage'?
        default_branch = manifest["default_branch"]
        fallback_stage_info = {
            "checkout": default_branch or "",  # Could be None
            "checkout_type": DEFAULT_REPO_STAGE_CHECKOUT_TYPE,
        }
        repo_info.setdefault("dev_stage", fallback_stage_info)
        repo_info.setdefault("production_stage", fallback_stage_info)

        stage = manifest["stage"]  # 'dev_stage' or 'production_stage'
        selected_repo_stage_info = repo_info[stage]
        selected_repo_stage_info.setdefault("checkout", fallback_stage_info["checkout"])
        selected_repo_stage_info.setdefault("checkout_type", fallback_stage_info["checkout_type"])

        if selected_repo_stage_info["checkout"]:
            # This could be 'None'
            selected_repo_stage_info["checkout"] = selected_repo_stage_info["checkout"].replace("\\", "/")

        selected_stage_checkout_branch_or_tag_name = selected_repo_stage_info["checkout"]
        selected_stage_checkout_type = selected_repo_stage_info["checkout_type"]

        has_tag = selected_stage_checkout_type == "tag"
        url = repo_info.get("url", None)
        if not url:
            logger.error(f"Missing 'url' for repo '{repo_name}'")
            raise RepositoryManagementError(f"\nMissing 'url' for repo '{repo_name}'")

        if url.endswith(".git"):
            url = url[:-4]

        repo_info["url"] = url
        repo_info.setdefault("skip_repo_updates", DEFAULT_SKIP_REPO_UPDATES)
        tag = selected_stage_checkout_branch_or_tag_name if has_tag else None

        repo_name = url.split("/")[-1]
        repo_info.setdefault("symlink_path", repo_name)

        repo_info.setdefault("active", True)
        repo_info.setdefault("repo_sparse_path_override", None)
        base_clone_path_root_symlink_src = manifest["base_clone_path_root_symlink_src"]
        repo_info.setdefault(
            "base_clone_path_root_symlink_src_override",
            base_clone_path_root_symlink_src,
        )

        _meta = repo_info["_meta"]
        _meta["has_tag"] = has_tag
        _meta["repo_name"] = repo_name

        # Is this a local file path?
        repo_url_dotgit_is_file_url = not url.startswith("http") and not url.startswith("ssh")
        if repo_url_dotgit_is_file_url:
            abs_normalized_file_path = Path(os.path.normpath(
                url.replace(".git", "").replace("file://", "").replace("file:", "")
            )).resolve()

            # Prefix "file://", ensure no ".git" suffix
            formatted_repo_url = f"file://{abs_normalized_file_path}"

            _meta["repo_url_dotgit_local_file_abs_path"] = abs_normalized_file_path
            _meta["repo_url_dotgit_is_local_file"] = True
            _meta["url_dotgit"] = formatted_repo_url
        else:
            _meta["url_dotgit"] = f"{url}.git"

        if has_tag:
            _meta["tag_versioned_clone_src_repo_name"] = f"{repo_name}-{tag}"
        else:
            pattern = r"\W+"
            normalized_repo_name_for_dir = selected_stage_checkout_branch_or_tag_name.replace("/", "--")
            normalized_repo_name_for_dir = re.sub(pattern, "_", normalized_repo_name_for_dir)
            _meta["tag_versioned_clone_src_repo_name"] = f"{repo_name}--{normalized_repo_name_for_dir}" \
                if normalized_repo_name_for_dir else repo_name

        symlink_path = repo_info["symlink_path"]
        _meta["abs_symlinked_repo_path"] = os.path.normpath(os.path.join(abs_base_symlink_path, symlink_path))
        tag_versioned_clone_src_repo_name = _meta["tag_versioned_clone_src_repo_name"]
        _meta["tag_versioned_clone_src_path"] = os.path.normpath(
            os.path.join(base_clone_path, tag_versioned_clone_src_repo_name))

    def init_dir_tree(self, manifest):
        """
        Initialize or clear paths based on manifest configuration. Default tree:
        ########################################################################
        - source
          - _repos-available
            - content
        ########################################################################
        """
        logger.info(colorize_action("⚙️ | Crafting dir skeleton from manifest ..."))

        # Setup target symlink path skeleton tree from manifest vals
        rel_base_clone_path = manifest["base_clone_path"]
        rel_base_symlink_path = manifest["base_symlink_path"]

        abs_base_clone_path = os.path.abspath(rel_base_clone_path)
        abs_base_symlink_path = os.path.abspath(rel_base_symlink_path)

        logger.info(colorize_path(f"   - base_clone_path: '{brighten(abs_base_clone_path)}'"))
        logger.info(colorize_path(f"   - base_symlink_path: '{brighten(abs_base_symlink_path)}'"))
        logger.info(colorize_path(f"   - source_static_path: '{brighten(self.source_static_path)}'"))
        logger.info(colorize_path(f"   - source_doxygen_path: '{brighten(self.source_doxygen_path)}'"))

        self.setup_directory_skeleton(abs_base_clone_path)
        self.setup_directory_skeleton(abs_base_symlink_path)
        self.setup_directory_skeleton(self.source_static_path)
        self.setup_directory_skeleton(self.source_doxygen_path)

    def check_is_enabled_ext(self, manifest):
        """
        Checks whether the repository manager extension is enabled according to the manifest settings.
        - Returns: Boolean indicating if the extension is enabled.
        """
        enable_repo_manager = manifest.get("enable_repo_manager", True)
        if not enable_repo_manager:
            logger.warning(
                f"\nDisabled in manifest ({brighten('enable_repo_manager')}) - skipping extension!"
            )
            return False  # Extension is not enabled

        enable_repo_manager_local = manifest.get("enable_repo_manager_local", True)
        if not self.read_the_docs_build and not enable_repo_manager_local:
            logger.warning(
                f"\nDisabled in manifest ({brighten('enable_repo_manager_local')}) - skipping extension!"
            )
            return False  # Extension is not enabled locally

        return True  # Extension is enabled

    def get_normalized_manifest(self):
        """
        Handle the repository cloning and updating process when Sphinx initializes.
        - Read/normalize/validate the manifest
        - Initialize the directory tree skeleton
        - Manage the repositories (cloning, updating, and symlinking)
        - returns: manifest
        """
        logger.info(colorize_success(f"\n══{brighten('BEGIN SPHINX_REPO_MANAGER')}══\n"))

        self.source_static_path = Path(self.abs_confdir, "_static")
        self.source_doxygen_path = Path(self.abs_confdir, "_doxygen")

        manifest_path = Path(self.repo_manager_manifest_path).absolute()
        manifest = self.read_normalize_manifest(manifest_path)

        return manifest

    @staticmethod
    def setup_directory_skeleton(create_path_to):
        try:
            os.makedirs(create_path_to, exist_ok=True)
        except OSError as e:
            raise RepositoryManagementError(f"\nFailed to create directory '{create_path_to}': {str(e)}")

    def manage_repositories(self, manifest):
        if not manifest:
            raise RepositoryManagementError("No manifest found (or failed when normalizing)")

        self.init_dir_tree(manifest)
        stash_and_continue_if_wip = manifest["stash_and_continue_if_wip"]
        stage = manifest["stage"]
        repositories = list(manifest["repositories"].items())
        log_queue = queue.Queue()

        max_num_workers = manifest["max_workers_local"] if not self.read_the_docs_build else manifest["max_workers_rtd"]
        logger.info(colorize_action(f"🤖 | Using {max_num_workers} worker(s) for multi-threading\n"))

        # Use self.live context to manage output positioning
        with self.live:
            worker_tasks = {
                repo_name: self.progress.add_task(
                    description=f"{repo_name}",
                    total=1,
                    status="Pending",
                )

                for repo_name, _ in repositories
            }

            total_task_id = self.progress.add_task(
                description="[bold magenta]Processing...",
                total=len(repositories),
            )

            # Use ThreadPoolExecutor to submit worker tasks (for total % progress bar)
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_num_workers) as executor:
                futures = [
                    executor.submit(
                        self.process_repo,
                        stage,
                        repo_info,
                        stash_and_continue_if_wip,
                        log_queue,
                        worker_tasks[repo_name],
                        repo_name
                    )
                    for repo_name, repo_info in repositories
                ]

                # Monitor each future as it completes
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                        self.progress.update(total_task_id, advance=1)
                        if self.progress.tasks[total_task_id].completed == len(repositories):
                            self.progress.update(
                                total_task_id,
                                description="[bold magenta]Done",
                            )
                    except Exception as e:
                        logger.error(f"Failed to process repository - {e}")
                        self.progress.update(total_task_id, description="[bold magenta](!) Failed")

    @staticmethod
    def redact_url_secret(str_containing_url, reveal_first_char=False):
        """
        Redact the secret in the URL, optionally revealing the first character of the secret.
        
        Args:
            str_containing_url (str): The URL string to redact.
            reveal_first_char (bool): If True, show the first character of the secret.
        
        Returns:
            str: The redacted URL.
        """
        try:
            # Match any scheme (http, https, ssh, etc.), username, and secret
            def mask_secret(match):
                secret = match.group(2)  # Extract the secret part
                if reveal_first_char and len(secret) > 1:
                    masked_secret = f"{secret[0]}{'*' * (len(secret) - 1)}"
                else:
                    masked_secret = "*" * len(secret)
                return f"{match.group(1)}{masked_secret}@"

            url_pattern = re.compile(r"(^[a-zA-Z]+://[^:/]+:)([^@]+)@")
            return url_pattern.sub(mask_secret, str_containing_url)
        except Exception:
            return str_containing_url

    def process_repo(
            self,
            stage,
            repo_info,
            stash_and_continue_if_wip,
            log_queue,
            worker_task_id,
            repo_name
    ):
        """
        Processes an individual repository, performing tasks such as cloning, symlinking,
        and updating the progress bar.
        """
        log_entries = []
        _meta = repo_info["_meta"]
        tag_versioned_clone_src_repo_name = _meta["tag_versioned_clone_src_repo_name"]
        abs_symlinked_repo_path = _meta["abs_symlinked_repo_path"]
        active = repo_info["active"]

        # Update progress for the specific worker task in progress bar
        if not active:
            log_entries.append(
                colorize_action(
                    f"{abs_symlinked_repo_path} Repository '{brighten(repo_name)}' is inactive; skipping ...")
            )
            log_queue.put((f"Skipping {repo_name}", repo_name))  # Queue for progress updates
            self.progress.update(worker_task_id, status="Skipped")
            return

        abs_tag_versioned_clone_src_path = Path(_meta["tag_versioned_clone_src_path"])
        rel_repo_sparse_path = Path(self.manifest["repo_sparse_path"])

        repo_sparse_path_override = Path(repo_info["repo_sparse_path_override"]) if repo_info[
            "repo_sparse_path_override"] else None
        has_repo_sparse_path_override = bool(repo_sparse_path_override)
        rel_selected_repo_sparse_path = repo_sparse_path_override if has_repo_sparse_path_override \
            else rel_repo_sparse_path

        _meta["rel_selected_repo_sparse_path"] = rel_selected_repo_sparse_path

        rel_base_clone_path_root_symlink_src_override = Path(repo_info["base_clone_path_root_symlink_src_override"])
        has_base_clone_path_root_symlink_src_override = bool(rel_base_clone_path_root_symlink_src_override)

        if has_base_clone_path_root_symlink_src_override:
            repo_info["base_clone_path_root_symlink_src_override"] = str(
                repo_info["base_clone_path_root_symlink_src_override"]
            ).replace("{repo_sparse_path}", str(rel_selected_repo_sparse_path))
            rel_base_clone_path_root_symlink_src_override = Path(repo_info["base_clone_path_root_symlink_src_override"])

        rel_selected_clone_path_root_symlink_src = Path(
            rel_base_clone_path_root_symlink_src_override if has_base_clone_path_root_symlink_src_override \
                else rel_repo_sparse_path
        )

        # Report override if any
        if has_repo_sparse_path_override:
            log_entries.append(
                colorize_path(f"  - (!) Overriding repo_sparse_path: '{brighten(repo_sparse_path_override)}'"))

        repo_task = None
        try:
            repo_task = RepoTask(
                stage=stage,
                repo_info=repo_info,
                repo_name=repo_name,
                tag_versioned_clone_src_repo_name=tag_versioned_clone_src_repo_name,
                abs_tag_versioned_clone_src_path=abs_tag_versioned_clone_src_path,
                abs_symlinked_repo_path=abs_symlinked_repo_path,
                stash_and_continue_if_wip=stash_and_continue_if_wip,
                rel_selected_repo_sparse_path=rel_selected_repo_sparse_path,
                rel_selected_clone_path_root_symlink_src=rel_selected_clone_path_root_symlink_src,
                log_entries=log_entries,
                worker_task_id=worker_task_id,
            )

            self.run_repo_git_ops(repo_task)
            self.repo_add_symlinks(repo_task)

            # While thread may not yet be done, await self.is_done
            while not repo_task.is_done:
                time.sleep(0.1)  # Only affects this thread

            log_queue.put((f"Completed {repo_name}", repo_name))

        except Exception as e:
            self.errored_repo_name = repo_name
            stacktrace = traceback.format_exc()  # Includes e
            main_err = colorize_error(f"Error processing repository '{brighten(repo_name)}':\n")
            error_message = (
                    main_err +
                    f"{colorize_action(stacktrace)}"
                    f"  - Git Stage: {repo_task.current_git_stage_num + 1}/{repo_task.total_num_git_stages}\n"
            )

            sanitized_err_msg = self.redact_url_secret(error_message)
            raise RepositoryManagementError(sanitized_err_msg) from e
        finally:
            # Log all collected log entries for the repo
            for entry in log_entries:
                logger.info(entry)
                log_queue.put((entry, repo_name))  # Queue individual log entries for progress tracking

    def try_git_sparse_clone(self, repo_task):
        # TODO: Log?

        is_file_url = repo_task.repo_url_dotgit_is_local_file
        if not is_file_url and self.has_env_repo_auth_token:
            # Inject auth
            formatted_repo_url = repo_task.repo_url_dotgit.replace(
                "://",
                f"://{self.env_repo_auth_user}:{self.env_repo_auth_token}@")
        else:
            formatted_repo_url = repo_task.repo_url_dotgit

        colored_repo_name = self.get_colored_repo_name(repo_task)
        colored_branch_name = self.get_colored_branch_name_or_default_in_parentheses(repo_task)
        cloning = "[cyan]→ Cloning"

        self.progress.update(
            repo_task.worker_task_id,
            description=f"{colored_repo_name} {colored_branch_name} {cloning}",
        )

        # Prep the progress bar update callback
        def update_clone_progress(
                my_worker_task_id,
                progress,
                description,
                is_new_stage,
        ):
            nonlocal repo_task
            """
            Handles updating the progress bar and performing additional actions.
            Callback from git_helper.git_sparse_clone_with_progress().update_progress().
            """
            self.progress.update(
                my_worker_task_id,
                description=description,
                advance=1 if (is_new_stage or progress >= 100) else 0,
            )

            if is_new_stage:
                repo_task.current_git_stage_num += 1

        # Clone now: Stashes if wip and stash_and_continue_if_wip
        GitHelper.git_sparse_clone_with_progress(
            clone_to_path=repo_task.abs_tag_versioned_clone_src_path,
            repo_url_dotgit=formatted_repo_url,
            branch_or_tag=repo_task.checkout_branch_or_tag_name,
            branch_is_tag=repo_task.has_tag,
            repo_sparse_path=repo_task.rel_selected_repo_sparse_path,
            stash_and_continue_if_wip=repo_task.stash_and_continue_if_wip,
            repo_name=repo_task.repo_name,
            worker_task_id=repo_task.worker_task_id,
            log_entries=repo_task.log_entries,
            update_obj=update_clone_progress,
            debug_extra_logs=self.debug_mode,
        )

        if repo_task.stash_and_continue_if_wip:
            repo_task.already_stashed = True

        repo_task.cloned = True
        if self.shutdown_flag:
            raise SystemExit

    def run_repo_git_ops(self, repo_task):
        if self.shutdown_flag:
            raise SystemExit

        self.progress.update(
            repo_task.worker_task_id,
            completed=0,
            total=repo_task.progress_total,
        )

        # Since we started with stages + 1, active workers will init with a small % for "started"
        self.advance_repo_task_stage(repo_task)

        if repo_task.should_clone_repo:
            # Sparse cloning will also change the branch to the correct one
            self.try_git_sparse_clone(repo_task)  # Sets repo_task.cloned
            self.try_git_clean_sparse_docs_after_clone(repo_task, self.debug_mode)
        else:
            if repo_task.has_tag:
                self.try_git_fetch(repo_task)  # Forces to get new tags
                self.try_git_checkout_for_tag_updates(repo_task)  # Failure to switch won't affect success
            else:
                self.try_git_pull(repo_task)

        if self.shutdown_flag:
            raise SystemExit

        self.set_repo_task_done(repo_task)

    def repo_add_symlink1_content_dir(self, repo_task):
        # Target symlink path to create: "source/content/{repo_name}/"
        abs_existing_nonsym_inner_sparse_dir_path = Path(
            repo_task.abs_tag_versioned_clone_src_path,
            repo_task.rel_selected_clone_path_root_symlink_src,
        ).resolve()

        # Target symlink path to create: "source/content/-/"
        abs_target_new_symlink_repo_content_dir_path = Path(
            repo_task.abs_symlinked_repo_path,
            repo_task.repo_info["base_clone_path_root_symlink_src_override"]
        ).resolve()

        # Existing real dir path: 'source/_repos-available/{tagged_repo_name}/docs/source/content'
        self.create_symlink(
            abs_existing_nonsym_inner_sparse_dir_path,
            repo_task.abs_symlinked_repo_path,
            repo_task.log_entries,  # New symlink to be created at dir path
        )

    def repo_add_symlink2_release_notes(self, repo_task):        
        # Locate the first existing file
        release_notes_file_name = next(
            (name for name in CANDIDATE_RELEASE_NOTE_FILE_NAMES
             if Path(repo_task.abs_tag_versioned_clone_src_path, name).exists()),
            None
        )
        
        # Resolve the absolute path if a file was found
        abs_existing_nonsym_release_notes_file_path = (
            Path(repo_task.abs_tag_versioned_clone_src_path, release_notes_file_name).resolve()
            if release_notes_file_name else None
        )
        
        # Validate
        if abs_existing_nonsym_release_notes_file_path is None:
            return

        # Check if the source existing "real" file exists before attempting to create a symlink
        # Target symlink path to create; eg: "source/content/account_services/RELEASE_NOTES.[rst|.md]"
        abs_symlinked_repo_path = self.abs_confdir.joinpath(repo_task.abs_symlinked_repo_path)
        abs_new_symlink_release_notes_path = abs_symlinked_repo_path.joinpath(release_notes_file_name)

        # Create the symlink
        self.create_symlink(
            abs_existing_nonsym_release_notes_file_path,
            abs_new_symlink_release_notes_path,
            repo_task.log_entries,
        )

    def repo_add_symlink3_static_images_dir(self, repo_task):
        # Log + Validate clone src path to _static/{repo_name}
        abs_existing_nonsym_repo_static_images_dir_path = Path(
            repo_task.abs_tag_versioned_clone_src_path,
            repo_task.rel_selected_repo_sparse_path,
            "source",
            "_static",
            "images",
            repo_task.repo_name,
        ).resolve()

        # OPTIONAL target symlink creation path
        if not abs_existing_nonsym_repo_static_images_dir_path.exists():
            return

        # Target symlink path to create: "source/_static/images/{repo_name}/"
        abs_target_new_symlink_static_images_dir_path = self.source_static_path.joinpath("images", repo_task.repo_name)
        self.create_symlink(
            abs_existing_nonsym_repo_static_images_dir_path,
            abs_target_new_symlink_static_images_dir_path,
            repo_task.log_entries,
        )

    def repo_add_symlink4_static_blobs_dir(self, repo_task):
        abs_src_existing_nonsym_static_blobs_dir_path = Path(
            repo_task.abs_tag_versioned_clone_src_path,
            repo_task.rel_selected_repo_sparse_path,
            "source",
            "_static",
            "blobs",
            repo_task.repo_name,
        ).resolve()

        # OPTIONAL target symlink creation path
        if not abs_src_existing_nonsym_static_blobs_dir_path.exists():
            return

        # Target symlink path to create: "source/_static/blobs/{repo_name}/"
        abs_target_new_symlink_static_blobs_dir_path = self.source_static_path.joinpath("blobs", repo_task.repo_name)
        self.create_symlink(
            abs_src_existing_nonsym_static_blobs_dir_path,
            abs_target_new_symlink_static_blobs_dir_path,
            repo_task.log_entries,
        )

    def repo_add_symlink5_doxygen_dir(self, repo_task):
        # Src real path
        abs_src_existing_nonsym_static_doxygen_dir_path = Path(
            repo_task.abs_tag_versioned_clone_src_path,
            repo_task.rel_selected_repo_sparse_path,
            "source",
            "_doxygen",
            repo_task.repo_name,
        ).resolve()

        # OPTIONAL target symlink creation path
        if not abs_src_existing_nonsym_static_doxygen_dir_path.exists():
            return

        # Target symlink path to create
        abs_target_new_symlink_static_doxygen_dir_path = self.source_doxygen_path.joinpath(repo_task.repo_name)
        self.create_symlink(
            abs_src_existing_nonsym_static_doxygen_dir_path,
            abs_target_new_symlink_static_doxygen_dir_path,
            repo_task.log_entries,
        )

    def repo_add_symlink6_source_docs(self, repo_task):
        # Src real path: "source/_static-docs/"
        abs_src_existing_nonsym_local_static_docs_dir_path = self.abs_confdir.joinpath(STATIC_DOCS_DIR_NAME)

        # OPTIONAL src dir
        if not abs_src_existing_nonsym_local_static_docs_dir_path.exists():
            return

        # Target symlink path to create: "source/content/-/"
        abs_target_new_symlink_content_dash_dir_path = Path(
            self.base_symlink_path,
            DEFAULT_STATIC_DOCS_SYMLINKED_CONTENT_DIR_NAME,
        ).resolve()

        self.create_symlink(
            abs_src_existing_nonsym_local_static_docs_dir_path,
            abs_target_new_symlink_content_dash_dir_path,
            repo_task.log_entries,
        )

    def create_symlink(
            self,
            src_existing_nonsym_path,
            new_symlink_target_path,
            log_entries,
    ):
        """
        - Create or update a symlink using relative paths. 
        - Creates dirs leading up to symlink_target_new_sym_path if !exists
        - (!) In Windows, symlinking is the *opposite* src and destination of Unix
          - symlink_src_path     # eg: "source/_repos-available/account_services-v2.1.0/docs/source"
          - symlink_target_path  # eg: "source/content/account_services"
                                 # eg: "source/content/account_services/RELEASE_NOTES.md"
        """
        if not src_existing_nonsym_path:
            raise SymlinkError("!symlink_src_existing_real")
        if not new_symlink_target_path:
            raise SymlinkError("!symlink_target_new_sym_path")

        # Ensure directories leading up to the symlink target exist
        try:
            target_dir = os.path.dirname(new_symlink_target_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            os.symlink(src_existing_nonsym_path, new_symlink_target_path)
        except Exception as e:
            # raise SymlinkError(f"Error creating symlink: {str(e)}\n"
            #                    f"- symlink_src_existing_real_path: {src_existing_nonsym_path}\n"
            #                    f"- symlink_target_new_sym_path: {new_symlink_target_path}") from None
            pass

    @staticmethod
    def try_git_clean_sparse_docs_after_clone(repo_task, debug_extra_logs):
        try:
            GitHelper.git_clean_sparse_docs_after_clone(
                repo_task.abs_tag_versioned_clone_src_path,
                repo_task.rel_selected_repo_sparse_path,
                log_entries=repo_task.log_entries,
                debug_extra_logs=debug_extra_logs,
            )
        except Exception as e:
            additional_info = f"Error cleaning up sparse clone '{brighten(repo_task.repo_name)}':\n- {str(e)}"
            raise Exception(f"{additional_info}") from e

    def repo_add_symlinks(self, repo_task):
        abs_tag_versioned_clone_src_nested_path = repo_task.abs_tag_versioned_clone_src_path.joinpath(
            repo_task.rel_selected_clone_path_root_symlink_src,
        ).resolve()

        self.repo_add_symlink1_content_dir(repo_task)  # Req'd
        self.repo_add_symlink2_release_notes(repo_task)
        self.repo_add_symlink3_static_images_dir(repo_task)
        self.repo_add_symlink4_static_blobs_dir(repo_task)
        self.repo_add_symlink5_doxygen_dir(repo_task)
        self.repo_add_symlink6_source_docs(repo_task)

        # Done with this repo; TODO: Log?
        if self.shutdown_flag:
            raise SystemExit

    def _init_main(self):
        try:
            manifest = self.get_normalized_manifest()
            enabled = self.check_is_enabled_ext(manifest)
            if not enabled:
                return

            self.manage_repositories(manifest)

            if not self.read_the_docs_build and self.debug_mode and self.debug_stop_build_on_extension_done:
                raise RepositoryManagementError("\nManifest 'debug_mode' flag enabled: Stopping build for log review.")
        except Exception as e:
            self.shutdown_flag = True
            if e:
                raise RepositoryManagementError(f"\nsphinx_repo_manager failure: {e}")
            else:
                raise RepositoryManagementError(f"\nsphinx_repo_manager failure.")
        finally:
            if self.shutdown_flag:
                repo_name_hint = (
                    f" @ '{brighten(self.errored_repo_name)}'" if self.errored_repo_name else "")
                logger.error(f"\n(!) Error: Ended early (likely CTRL+C || error){repo_name_hint}")

            logger.info(colorize_success(f"\n══{brighten('END SPHINX_REPO_MANAGER')}══\n"))

    def try_git_checkout_for_tag_updates(self, repo_task):
        """ git checkout wrapper for tags to ensure the tag wasn't. """
        try:
            self.progress.update(
                repo_task.worker_task_id,
                description=f"[bold blue]{repo_task.repo_name} [cyan]→ Ensuring Latest Tag",
            )

            GitHelper.git_checkout_tag(
                repo_task.abs_tag_versioned_clone_src_path,
                repo_task.checkout_branch_or_tag_name,
                log_entries=repo_task.log_entries,
            )

            self.advance_repo_task_stage(repo_task)
        except Exception as e:
            additional_info = (
                f"Error fetching updates for '{brighten(repo_task.repo_name)}':\n- {str(e)}"
            )
            raise Exception(f"{additional_info}") from e

    def try_git_fetch(self, repo_task):
        try:
            colored_repo_name = self.get_colored_repo_name(repo_task)
            colored_branch_name = self.get_colored_branch_name_or_default_in_parentheses(repo_task)
            cloning = "[cyan]→ Fetching"

            self.progress.update(
                repo_task.worker_task_id,
                description=f"{colored_repo_name} {colored_branch_name} {cloning}",
            )

            GitHelper.git_fetch(
                repo_task.abs_tag_versioned_clone_src_path,
                log_entries=repo_task.log_entries,
            )

            self.advance_repo_task_stage(repo_task)
            repo_task.fetched = True
        except Exception as e:
            additional_info = (
                f"Error fetching updates for '{brighten(repo_task.repo_name)}':\n- {str(e)}"
            )
            raise Exception(f"{additional_info}") from e

    def advance_repo_task_stage(self, repo_task):
        self.progress.update(
            repo_task.worker_task_id,
            advance=1,
        )

    @staticmethod
    def get_colored_repo_name(repo_task):
        return f"[bold blue]{repo_task.repo_name}[/bold blue]"

    @staticmethod
    def get_colored_branch_name_or_default_in_parentheses(repo_task):
        return f"[blue]({repo_task.checkout_branch_or_tag_name or 'default'})"

    def set_repo_task_done(self, repo_task):
        colored_repo_name = self.get_colored_repo_name(repo_task)
        colored_branch_name = self.get_colored_branch_name_or_default_in_parentheses(repo_task)
        colored_done = f"[green]→ Done"

        self.progress.update(
            repo_task.worker_task_id,
            description=f"{colored_repo_name} {colored_branch_name} {colored_done}",
            completed=repo_task.progress_total,
        )

        repo_task.current_git_stage_num += 1
        repo_task.is_done = True

    def try_git_pull(self, repo_task):
        """ git pull wrapper. """
        try:
            colored_repo_name = self.get_colored_repo_name(repo_task)
            colored_branch_name = self.get_colored_branch_name_or_default_in_parentheses(repo_task)
            pulling = "[cyan]→ Pulling"

            self.progress.update(
                repo_task.worker_task_id,
                description=f"{colored_repo_name} {colored_branch_name} {pulling}",
            )

            GitHelper.git_pull(
                repo_task.abs_tag_versioned_clone_src_path,
                repo_task.should_stash,
                log_entries=repo_task.log_entries,
                debug_extra_logs=self.debug_mode,
            )

            self.advance_repo_task_stage(repo_task)

        except Exception as e:
            additional_info = (
                f"Error pulling updates for '{brighten(repo_task.repo_name)}':\n- {str(e)}"
            )
            raise Exception(f"{additional_info}") from e

        if repo_task.stash_and_continue_if_wip:
            repo_task.already_stashed = True

        if self.shutdown_flag:
            raise SystemExit
