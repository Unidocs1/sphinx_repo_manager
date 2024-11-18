import os
import re
import shutil
import subprocess
import shlex
import logging
from datetime import datetime
from pathlib import Path
from subprocess import CompletedProcess
from .log_styles import *
from rich.console import Console

console = Console()

GIT_DEBUG = False  # Spammy logs, if True - notably for cloning

GIT_SPARSE_PRESERVED_DIRS_FILES = [
    ".git",
    ".gitignore",
    ".gitlab",
    "README.md",
    "RELEASE_NOTES.rst",
]

STAGES = {
    "Receiving": "Receiving objects",
    "Compressing": "Compressing objects",
    "Resolving": "Resolving deltas",
}


# Configure the logger
class CustomFormatter(logging.Formatter):
    def format(self, record):
        original_format = self._style._fmt

        if record.levelno == logging.INFO:
            self._style._fmt = "%(message)s"
        else:
            self._style._fmt = "(levelname)s: %(message)s"

        result = logging.Formatter.format(self, record)
        self._style._fmt = original_format

        return result


handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(handler)
logger.propagate = False


def redact_url_secret(url):
    """ Redact any credentials in the URL. """
    try:
        url_pattern = re.compile(r"https://([^:/]*:[^@]*)@")
        return url_pattern.sub("https://REDACTED-SECRET@", url)
    except Exception:
        return url


def clean_command_array(cmd_arr):
    """Filter out None or empty string values."""
    cmd_arr[:] = [arg for arg in cmd_arr if arg]


def run_subprocess_with_progress(cmd, progress_callback=None):
    """
    Run a subprocess command and display output in real-time, optionally tracking progress.

    Parameters:
    * cmd (list): Command to be executed as a list of arguments.
    * progress_callback (function): Function to handle progress updates, called with each line of output.
    """
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            line = line.strip()
            if progress_callback:
                progress_callback(line)
            if GIT_DEBUG:
                print(line)

        process.stdout.close()
        process.wait()

        # Failed?
        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode, cmd, output="Subprocess error encountered."
            )

    except FileNotFoundError:
        raise Exception(f"Command not found: {' '.join(cmd)}")
    except subprocess.CalledProcessError as e:
        raise Exception(
            f"Command failed with return code {e.returncode}.\nCommand: {' '.join(cmd)}\nError: {e.output}"
        )
    except Exception as e:
        raise Exception(f"An unexpected error occurred while running: {' '.join(cmd)}\nError: {str(e)}")


def prepare_command(cmd):
    """
    Convert all Path objects in a command list to strings for the subprocess.
    """
    return [str(part) if isinstance(part, Path) else part for part in cmd]


def run_subprocess_cmd(
        cmd_arr,
        check_throw_on_cli_err=True,
        log_entries=None,
):
    """Run a subprocess command and handle errors."""
    clean_command_array(cmd_arr)
    redacted_cmd_arr = [redact_url_secret(str(part)) for part in cmd_arr]  # Ensure every part is a string

    try:
        result = subprocess.run(
            cmd_arr,
            capture_output=True, 
            text=True,
        )

        if result.returncode != 0:
            error_message = getattr(result, 'stderr', '').strip() if result.stderr else ""
            msg = f"Command failed:\n{brighten(error_message)}"
            if log_entries is not None:
                log_entries.append(msg)
            else:
                logger.error(msg)

            if check_throw_on_cli_err:
                pretty_cmd = shlex.join(redacted_cmd_arr)
                raise Exception(
                    f"Command failed: '{pretty_cmd}'\nError: '{brighten(error_message)}'"
                )

        return result.stdout
    except FileNotFoundError as e:
        msg = f"Command not found: '{brighten(e)}'"
        if log_entries is not None:
            log_entries.append(msg)
        else:
            logger.error(msg)
        pretty_cmd = shlex.join(redacted_cmd_arr)
        raise Exception(f"Command not found: {pretty_cmd}\nError: '{brighten(e)}'")


class GitHelper:
    def __init__(self):
        pass

    @staticmethod
    def git_fetch(repo_path, log_entries=None):
        """ Fetch all remote branches and tags from the repo_path working dir (-C). """
        GitHelper._throw_if_path_not_exists(repo_path)

        # --force works around the potential `rejected: would clobber existing tag` error
        cmd_arr = ["git", "-C", repo_path, "fetch", "--all", "--tags", "--force"]
        run_subprocess_cmd(
            cmd_arr,
            check_throw_on_cli_err=True,
            log_entries=log_entries,
        )

    @staticmethod
    def git_validate_is_git_dir(repo_path, validate_has_other_files):
        """ Check if a directory is a valid Git repository. """
        if not GitHelper.git_dir_exists(repo_path):
            return False

        git_dir = os.path.join(repo_path, ".git")
        if not os.path.exists(git_dir):
            return False

        if validate_has_other_files:
            other_files = os.listdir(repo_path)
            if len(other_files) > 1:
                return False

        return True

    @staticmethod
    def _get_gitlab_base_url(repo_url):
        """
        Extract the GitLab base URL from the given repo URL.
        - @returns empty string if no group.
        """
        pattern = re.compile(r"(https://[^/]+/)")
        match = pattern.search(repo_url)
        if match:
            return match.group(1)
        else:
            return ""

    @staticmethod
    def get_gitlab_group(repo_url, to_lowercase=True):
        """ Extract the GitLab group from the given repo URL. """
        base_url = GitHelper._get_gitlab_base_url(repo_url)
        if base_url:
            escaped_base_url = re.escape(base_url)
            pattern = re.compile(rf"{escaped_base_url}([^/]+)/")
            match = pattern.search(repo_url)
            if match:
                group = match.group(1)
                return group.lower() if to_lowercase else group
        else:
            return None

    @staticmethod
    def git_clone(
            rel_base_clone_path,
            repo_url_dotgit,
            branch,
            branch_is_tag,
            preserve_gitlab_group,
            log_entries=None,
    ):
        """
        Clone the repo+branch from the provided URL to the specified path.
        - preserve_gitlab_group; eg: If you have "https://source.goxbe.io/Core/matchmaking_services",
          "Core" dir will be created
        - (!) Consider git_sparse_clone_with_progress() for docs-only clones
        """
        group_str = str(GitHelper.get_gitlab_group(repo_url_dotgit))
        repo_name_str = str(os.path.basename(repo_url_dotgit).replace(".git", ""))

        if preserve_gitlab_group and group_str:
            rel_base_clone_path = os.path.join(
                rel_base_clone_path, group_str, repo_name_str
            )
        else:
            rel_base_clone_path = os.path.join(rel_base_clone_path, repo_name_str)

        if os.path.exists(rel_base_clone_path):
            raise Exception(
                f"Tried to clone to path, but dir already exists: '{rel_base_clone_path}'"
            )

        single_branch_cmd = (
            "--single-branch" if branch_is_tag else None
        )
        
        git_clone_cmd_arr = [
            "git",
            "clone",
            "--branch",
            branch,
            single_branch_cmd,
            "-q",
            repo_url_dotgit,
            rel_base_clone_path,
        ]

        run_subprocess_cmd(
            git_clone_cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries
        )

    @staticmethod
    def _remove_except(base_path, exclude_dirs_files, log_entries=None):
        """
        Remove all items in the base_path except those in exclude_dirs.
        """
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if item not in exclude_dirs_files:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)

    @staticmethod
    def _clean_exclude_root_level(repo_path, sparse_first_level, log_entries=None):
        """
        Clean the root level of the repo_path, leaving only [.git, docs] at root level and sparse_first_level directories.
        """
        preserved_dirs_files = GIT_SPARSE_PRESERVED_DIRS_FILES + [sparse_first_level]
        if log_entries is not None:
            pass  # TODO: Log?

        # Add non-preserved dirs to .git/info/exclude before wiping
        # We don't want it to show on git diff -- this is *just* local to us
        GitHelper.git_add_to_exclude(
            repo_path, preserved_dirs_files, log_entries=log_entries
        )

        GitHelper._remove_except(
            repo_path, preserved_dirs_files, log_entries=log_entries
        )

    @staticmethod
    def git_clean_sparse_docs_after_clone(repo_path, repo_sparse_path, log_entries=None):
        """
        Clean up the repo to only keep the specified sparse checkout paths.
        """
        full_path = os.path.join(repo_path, repo_sparse_path)
        os.makedirs(full_path, exist_ok=True)

        sparse_parts = Path(repo_sparse_path).parts
        docs_dir = sparse_parts[0]

        # Remove everything except [.git, docs, RELEASE_NOTES.rst] at root level
        GitHelper._clean_exclude_root_level(
            repo_path,
            docs_dir, 
            log_entries=log_entries,
        )

    @staticmethod
    def git_clone_with_progress(repo_url, repo_path):
        """ Clone a Git repository with progress updates. """
        process = subprocess.Popen(
            [
                "git",
                "clone",
                repo_url,
                repo_path,
                "--progress"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
        )

        # Ensure process completes
        process.stdout.close()
        process.wait()

        # Display final confirmation
        if process.returncode != 0:
            pass  # TODO: Log?

    @staticmethod
    def git_sparse_clone_with_progress(
            clone_to_path,
            repo_url_dotgit,
            branch_or_tag,
            branch_is_tag,
            repo_sparse_path,
            stash_and_continue_if_wip,
            repo_name,
            worker_task_id,
            log_entries=None,
            update_obj=None,
    ):
        git_clone_cmd = [
            "git",
            "clone",
            "--filter=blob:none",
            "--no-checkout",
            "--branch",
            branch_or_tag,
            "--progress",
            repo_url_dotgit,
            clone_to_path,
        ]

        if branch_is_tag:
            git_clone_cmd.insert(len(git_clone_cmd) - 2, "--single-branch")

        git_clone_cmd = prepare_command(git_clone_cmd)

        # Define cloning stages
        total_stages = len(STAGES)  # Total stage count to track (3)
        stage_progress = {stage: 0 for stage in STAGES}  # Initialize stage progress tracking
        current_stage_index = 0  # Track the current stage index
        cumulative_progress = 0  # Initialize cumulative progress

        def update_progress(line):
            nonlocal cumulative_progress, current_stage_index, total_stages

            is_new_stage = False  # Flag to indicate if we entered a new stage

            # Detect the current stage based on the line
            for short_name, full_name in STAGES.items():
                if full_name in line:
                    match = re.search(r"(\d+)%", line)
                    if match:
                        percentage = int(match.group(1))
                        if percentage > stage_progress[short_name]:
                            stage_progress[short_name] = percentage
                            cumulative_progress = (current_stage_index * 100 + percentage) // total_stages

                            # Entered a new stage?
                            new_stage_index = list(STAGES.keys()).index(short_name)
                            if current_stage_index < new_stage_index:
                                current_stage_index = new_stage_index
                                is_new_stage = True

                            if update_obj:
                                update_obj(
                                    worker_task_id,
                                    progress=cumulative_progress,  # Progress %
                                    description=f"{repo_name} [cyan]→ Cloning → {short_name}",
                                    is_new_stage=is_new_stage,
                                )

                    # Print spammy CLI output only if GIT_DEBUG is True
                    if GIT_DEBUG:
                        print(line)

                    break

            return is_new_stage

        # Run clone command with progress updates
        run_subprocess_with_progress(git_clone_cmd, update_progress)

        GitHelper.git_sparse_checkout(
            clone_to_path,
            repo_sparse_path,
            branch_or_tag,
            branch_is_tag,
            stash_and_continue_if_wip,
            log_entries=log_entries,
        )

    @staticmethod
    def git_sparse_checkout(
            clone_to_path,
            repo_sparse_path,
            branch_or_tag,
            branch_is_tag,
            stash_and_continue_if_wip,
            log_entries=None,
    ):
        """ Perform a sparse checkout on the specified paths. """
        # Initialize sparse checkout
        sparse_checkout_init_cmd_arr = prepare_command([
            "git", "-C", clone_to_path, "sparse-checkout", "init", "--cone"
        ])
        run_subprocess_cmd(
            sparse_checkout_init_cmd_arr,
            check_throw_on_cli_err=True,
            log_entries=log_entries,
        )

        # Set sparse checkout path
        sparse_checkout_set_cmd_arr = prepare_command([
            "git", "-C", clone_to_path, "sparse-checkout", "set", repo_sparse_path
        ])
        run_subprocess_cmd(
            sparse_checkout_set_cmd_arr,
            check_throw_on_cli_err=True,
            log_entries=log_entries,
        )

        # !Tag can just switch branches
        if not branch_is_tag:
            GitHelper.git_switch_branch(
                clone_to_path,
                branch_or_tag,
                stash_and_continue_if_wip,
                log_entries=log_entries,
            )
        else:
            # Tag needs to checkout the branch
            GitHelper.git_checkout_tag(
                clone_to_path,
                branch_or_tag,
                stash_and_continue_if_wip,
                log_entries=log_entries,
            )

    @staticmethod
    def git_check_is_dirty(repo_path, log_entries=None):
        """
        Check if the working directory is dirty (has WIP changes).
        - Returns is_dirty
        """
        try:
            GitHelper._throw_if_path_not_exists(repo_path)
            cmd_arr = ["git", "-C", repo_path, "status", "--porcelain"]
            output = run_subprocess_cmd(
                cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries
            )
            is_dirty = bool(output and output.strip())
            return is_dirty
        except Exception as e:
            msg = f"Failed to check if the repository is dirty: {e}"
            if log_entries is not None:
                log_entries.append(msg)
            else:
                logger.error(msg)
            raise Exception(
                f"Failed to check if the repository is dirty: {repo_path}\nError: {e}"
            )

    @staticmethod
    def git_reset_hard(repo_path, log_entries=None):
        """
        Reset the working directory to the last commit, removing all new/untracked files.
        """
        GitHelper._throw_if_path_not_exists(repo_path)
        
        cmd_arr = ["git", "-C", repo_path, "reset", "--hard"]
        run_subprocess_cmd(
            cmd_arr, 
            check_throw_on_cli_err=True, 
            log_entries=log_entries,
        )

    @staticmethod
    def git_stash(
            repo_path,
            stash_message=None,
            log_entries=None,
    ):
        """
        Stash the working directory. Includes new/untracked files.
        -C == working git dir
        -u == untracked
        -m == message
        """
        if not os.path.exists(repo_path):
            raise Exception(f"repo_path not found: {repo_path}")

        GitHelper._throw_if_path_not_exists(repo_path)
        if stash_message is None:
            stash_message = f"repo_mgr_wip-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        cmd_arr = ["git", "-C", repo_path, "stash", "push", "-u", "-m", stash_message]
        run_subprocess_cmd(
            cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries
        )

    @staticmethod
    def git_dir_exists(repo_path):
        """ Check if a .git directory exists within repo_path. """
        git_dir = os.path.join(repo_path, ".git")
        return os.path.exists(git_dir)

    @staticmethod
    def git_pull(repo_path, stash_and_continue_if_wip, log_entries=None):
        """ Pull the latest changes from the remote repository. """
        GitHelper._throw_if_path_not_exists(repo_path)
        if GitHelper.git_check_is_dirty(repo_path, log_entries=log_entries):
            if stash_and_continue_if_wip:
                # TODO: Log?
                GitHelper.git_stash(repo_path, log_entries=log_entries)
            else:
                raise Exception(
                    f"Working directory is dirty (!stash_and_continue_if_wip): '{brighten(repo_path)}'"
                )

        cmd_arr = ["git", "-C", repo_path, "pull"]
        run_subprocess_cmd(
            cmd_arr, 
            check_throw_on_cli_err=True, 
            log_entries=log_entries,
        )

    @staticmethod
    def git_checkout_tag(
            repo_path,
            tag,
            stash_and_continue_if_wip=True,
            log_entries=None,
    ):
        """
        Switch to a tagged branch. Technically you can do this without a tag, but you should use git_switch for that.
        """
        if GitHelper.git_dir_exists(repo_path):
            if GitHelper.git_check_is_dirty(repo_path, log_entries=log_entries):
                if stash_and_continue_if_wip:
                    # TODO: Log?
                    GitHelper.git_stash(repo_path, log_entries=log_entries)
                else:
                    raise Exception(
                        f"Working directory is dirty and !stash_and_continue_if_wip: "
                        f"'{brighten(repo_path)}'"
                    )

        cmd_arr = ["git", "-C", repo_path, "checkout", tag]
        run_subprocess_cmd(
            cmd_arr,
            check_throw_on_cli_err=True,
            log_entries=log_entries,
        )

    @staticmethod
    def git_switch_branch(
            repo_path,
            tag_or_branch,
            stash_and_continue_if_wip=True,
            log_entries=None,
    ):
        """ Switch to a non-tagged branch. """
        if not tag_or_branch:
            raise Exception("tag_or_branch is required")

        if GitHelper.git_dir_exists(repo_path):
            if GitHelper.git_check_is_dirty(repo_path, log_entries=log_entries):
                if stash_and_continue_if_wip:
                    # TODO: Log?
                    GitHelper.git_stash(repo_path, log_entries=log_entries)
                else:
                    raise Exception(
                        f"Working directory is dirty and !stash_and_continue_if_wip: "
                        f"'{brighten(repo_path)}'"
                    )

        cmd_arr = ["git", "-C", repo_path, "switch", tag_or_branch]

        run_subprocess_cmd(
            cmd_arr,
            check_throw_on_cli_err=True,
            log_entries=log_entries,
        )

    @staticmethod
    def git_add_to_exclude(rel_base_path, preserved_dirs, log_entries=None):
        """
        Uses git update-index to prevent git from tracking changes to all paths except the preserved ones.
        """
        all_items = os.listdir(rel_base_path)
        items_to_exclude = [item for item in all_items if item not in preserved_dirs]

        # Use git update-index to exclude these items
        for item in items_to_exclude:
            abs_path = (Path(rel_base_path) / item).resolve()
            if abs_path.is_dir():
                for sub_item in abs_path.rglob("*"):
                    cmd_arr = [
                        "git",
                        "-C",
                        rel_base_path,
                        "update-index",
                        "--assume-unchanged",
                        str(sub_item),  # Absolute paths only
                    ]
                    run_subprocess_cmd(
                        cmd_arr, 
                        check_throw_on_cli_err=True, 
                        log_entries=log_entries,
                    )
            else:
                cmd_arr = [
                    "git",
                    "-C",
                    rel_base_path,
                    "update-index",
                    "--assume-unchanged",
                    str(abs_path),
                ]
                run_subprocess_cmd(
                    cmd_arr, 
                    check_throw_on_cli_err=True,
                    log_entries=log_entries
                )

    @staticmethod
    def git_get_latest_tag_ver(
            working_dir_repo_path, 
            version_regex_pattern=None, 
            quiet=False, 
            log_entries=None,
    ):
        """
        Retrieves the latest tag version from the specified Git repository, optionally ignoring
        tags that do not match the regex pattern.

        Args:
            working_dir_repo_path (str): The path to the working directory of the Git repository.
            version_regex_pattern ([str]): A regex pattern to match tag versions. If None or empty, no filtering is applied.
            quiet ([bool]): If True, suppress command output.

        Returns:
            str | None: The latest tag version, `None` if no tags on this repo, or an error message if the command fails.
        """
        git_cmd_arr = ["tag", "--list"]

        try:
            stdout, stderr = GitHelper._git_submodule_cmd(
                git_cmd_arr,
                working_dir_repo_path,
                quiet,
                check_throw_on_cli_err=True,
                log_entries=log_entries,
            )

            tags = stdout.splitlines()

            if version_regex_pattern:
                regex = re.compile(version_regex_pattern)
                filtered_tags = [tag for tag in tags if regex.match(tag)]
            else:
                filtered_tags = tags

            def _parse_version(tag):
                """
                Parses a version string into a tuple of integers.
                Example: 'v1.2.3' -> (1, 2, 3)
                """
                return tuple(map(int, re.findall(r"\d+", tag)))

            filtered_tags.sort(key=_parse_version)

            if filtered_tags:
                return filtered_tags[-1]
            else:
                return None
        except subprocess.CalledProcessError as e:
            return f"Error: {e and e.stderr and e.stderr.strip()}"

    @staticmethod
    def _git_submodule_cmd(
            cmd,
            working_dir_repo_path,
            quiet,
            check_throw_on_cli_err=True,
            log_entries=None,
    ):
        """
        Run a git command in the specified sub-repo path, ensuring it's run from that working dir.

        Args:
            cmd (list): The git command to run.
            working_dir_repo_path (str): The path to the working directory of the Git repository.
            quiet (bool): If True, suppress command output.
            check_throw_on_cli_err (bool): If True, raise an error on CLI error.

        Returns:
            tuple: (output, error) - The stdout and stderr from the command.
        """
        if quiet:
            cmd += ["--quiet"]
        cmd_prefix_arr = ["git", "-C", working_dir_repo_path]
        full_cmd = cmd_prefix_arr + cmd
        result = subprocess.run(
            full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if check_throw_on_cli_err and result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode, full_cmd, output=result.stdout, stderr=result.stderr
            )
        return result.stdout, result.stderr

    @staticmethod
    def _throw_if_path_not_exists(path):
        """ Throw an exception if the specified path does not exist. """
        if not os.path.exists(path):
            raise Exception(f"Path does not exist: '{brighten(path)}'")
