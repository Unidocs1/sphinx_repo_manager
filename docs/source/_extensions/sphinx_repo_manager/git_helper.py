import os
import re  # Regex
import shutil
import subprocess
import shlex  # CLI helper
from pathlib import Path

import logging
from log_styles import *


# Configure the logger
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Save the original format
        original_format = self._style._fmt

        # Check if the log level is INFO and adjust the format accordingly
        if record.levelno == logging.INFO:
            self._style._fmt = '%(message)s'
        else:
            self._style._fmt = '(levelname)s: %(message)s'

        # Format the record using the updated format
        result = logging.Formatter.format(self, record)

        # Restore the original format
        self._style._fmt = original_format

        return result


handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False


def log_pretty_cli_cmd(cmd_arr, log_entries=None):
    """ Log a pretty CLI command to logs. """
    pretty_cmd = shlex.join(cmd_arr)
    message = colorize_cli_cmd(f"  - CLI: `{brighten(pretty_cmd)}`")
    if log_entries is not None:
        log_entries.append(message)
    else:
        logger.info(message)


def redact_url_secret(url):
    """ Redact any credentials in the URL. """
    url_pattern = re.compile(r'https://([^:/]*:[^@]*)@')
    return url_pattern.sub('https://REDACTED-SECRET@', url)


def run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True, log_entries=None):
    """ Run a subprocess command and handle errors. """
    redacted_cmd_arr = [redact_url_secret(part) for part in cmd_arr]
    log_pretty_cli_cmd(redacted_cmd_arr, log_entries)

    try:
        result = subprocess.run(cmd_arr, capture_output=True, text=True)

        if result.returncode != 0:
            error_message = result.stderr.strip()
            msg = f"Command failed:\n{brighten(error_message)}"
            if log_entries is not None:
                log_entries.append(msg)
            else:
                logger.error(msg)

            if check_throw_on_cli_err:
                pretty_cmd = shlex.join(redacted_cmd_arr)
                raise Exception(f"Command failed: '{pretty_cmd}'\nError: '{brighten(error_message)}'")

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
        """ Fetch all remote branches and tags *from the repo_path working dir (-C). """
        GitHelper._throw_if_path_not_exists(repo_path)
        cmd_arr = ['git', '-C', repo_path, 'fetch', '--all', '--tags']
        run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries)

    @staticmethod
    def git_validate_is_git_dir(repo_path, validate_has_other_files):
        """ Check if a directory is a valid Git repository """
        if not GitHelper.git_dir_exists(repo_path):
            return False

        # Check if it has a .git folder
        git_dir = os.path.join(repo_path, '.git')
        if not os.path.exists(git_dir):
            return False

        # Check if it has other files
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
        pattern = re.compile(r'(https://[^/]+/)')
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
            pattern = re.compile(rf'{escaped_base_url}([^/]+)/')
            match = pattern.search(repo_url)
            if match:
                group = match.group(1)
                return group.lower() if to_lowercase else group
        else:
            return None

    @staticmethod
    def git_clone(
            rel_init_clone_path,
            repo_url_dotgit,
            branch,
            preserve_gitlab_group,
            log_entries=None,
    ):
        """
        Clone the repo+branch from the provided URL to the specified path.
        - preserve_gitlab_group: If you have "https://gitlab.acceleratxr.com/Core/matchmaking_services",
          "Core" dir will be created
        """
        group = GitHelper.get_gitlab_group(repo_url_dotgit)
        repo_name = os.path.basename(repo_url_dotgit).replace('.git', '')

        if preserve_gitlab_group and group:
            rel_init_clone_path = os.path.join(rel_init_clone_path, str(group), str(repo_name))
        else:
            rel_init_clone_path = os.path.join(rel_init_clone_path, str(repo_name))

        if os.path.exists(rel_init_clone_path):
            raise Exception(f"Tried to clone to path, but dir already exists: '{rel_init_clone_path}'")

        git_clone_cmd_arr = [
            'git', 'clone',
            '--branch', branch,
            '-q',
            repo_url_dotgit, rel_init_clone_path
        ]

        run_subprocess_cmd(
            git_clone_cmd_arr,
            check_throw_on_cli_err=True,
            log_entries=log_entries)

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
        # These dirs/files won't be touched
        preserved_dirs_files = ['.git', 'RELEASE_NOTES.rst', sparse_first_level]

        # Add non-preserved dirs to .git/info/exclude before wiping
        # We don't want it to show on git diff -- this is *just* local to us
        GitHelper.git_add_to_exclude(repo_path, preserved_dirs_files, log_entries=log_entries)

        # Remove all items except preserved_dirs_files
        GitHelper._remove_except(repo_path, preserved_dirs_files, log_entries=log_entries)

    @staticmethod
    def git_clean_sparse_docs_clone(repo_path, repo_sparse_path, log_entries=None):
        """
        Clean up the repo to only keep the specified sparse checkout paths.
        """
        # Ensure the path to exclude exists
        full_path = os.path.join(repo_path, repo_sparse_path)
        os.makedirs(full_path, exist_ok=True)

        # Extract the parts of the sparse path
        sparse_parts = Path(repo_sparse_path).parts
        docs_dir = sparse_parts[0]

        # Remove everything except [.git, docs, RELEASE_NOTES.rst] at root level
        GitHelper._clean_exclude_root_level(repo_path, docs_dir, log_entries=log_entries)

    def git_sparse_clone(
            self,
            clone_to_path,
            repo_url_dotgit,
            branch,
            repo_sparse_path,
            stash_and_continue_if_wip,
            log_entries=None
    ):
        """
        Clone the repo with sparse checkout, only fetching the specified directories.
        (!) repo_sparse_path is a single string that will be combined into an arr.
        (!) You may want to call git_clean_sparse_docs_clone() after this to remove unnecessary files.
        """
        git_clone_filter_nocheckout_cmd_arr = [
            'git', 'clone',
            '--filter=blob:none', '--no-checkout',
            '--branch', branch,
            '-q', repo_url_dotgit, clone_to_path
        ]
        run_subprocess_cmd(git_clone_filter_nocheckout_cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries)

        sparse_checkout_init_cmd_arr = [
            'git', '-C', clone_to_path,
            'sparse-checkout', 'init', '--cone'
        ]
        run_subprocess_cmd(sparse_checkout_init_cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries)

        sparse_checkout_set_cmd_arr = [
            'git', '-C', clone_to_path,
            'sparse-checkout', 'set', repo_sparse_path
        ]
        run_subprocess_cmd(sparse_checkout_set_cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries)

        self.git_checkout(
            clone_to_path,
            branch,
            stash_and_continue_if_wip,
            log_entries=log_entries
        )

    @staticmethod
    def git_check_is_dirty(repo_path, log_entries=None):
        """
        Check if the working directory is dirty (has WIP changes).
        :returns is_dirty
        """
        try:
            GitHelper._throw_if_path_not_exists(repo_path)
            cmd_arr = ['git', '-C', repo_path, 'status', '--porcelain']
            output = run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries)
            is_dirty = bool(output.strip())
            return is_dirty
        except Exception as e:
            msg = f"Failed to check if the repository is dirty: {e}"
            if log_entries is not None:
                log_entries.append(msg)
            else:
                logger.error(msg)
            raise Exception(f"Failed to check if the repository is dirty: {repo_path}\nError: {e}")

    @staticmethod
    def git_reset_hard(repo_path, log_entries=None):
        """
        Reset the working directory to the last commit, removing all new/untracked files.
        """
        GitHelper._throw_if_path_not_exists(repo_path)
        cmd_arr = ['git', '-C', repo_path, 'reset', '--hard']
        run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries)

    @staticmethod
    def git_stash(repo_path, stash_message='repo_mgr-autostash', log_entries=None):
        """
        Stash the working directory. Includes new/untracked files.
        -C == working git dir
        -u == untracked
        -m == message
        """
        GitHelper._throw_if_path_not_exists(repo_path)
        cmd_arr = ['git', '-C', repo_path, 'stash', 'push', '-u', '-m', stash_message]
        run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries)

    @staticmethod
    def git_dir_exists(repo_path):
        """ Check if a .git directory exists within repo_path. """
        git_dir = os.path.join(repo_path, '.git')
        return os.path.exists(git_dir)

    @staticmethod
    def git_pull(repo_path, stash_and_continue_if_wip, log_entries=None):
        """ Pull the latest changes from the remote repository. """
        GitHelper._throw_if_path_not_exists(repo_path)
        if GitHelper.git_check_is_dirty(repo_path, log_entries=log_entries):
            if stash_and_continue_if_wip:
                msg = colorize_path(f"  - Stashing WIP changes for repo: '{brighten(repo_path)}'")
                if log_entries is not None:
                    log_entries.append(msg)
                else:
                    logger.info(msg)
                GitHelper.git_stash(repo_path, log_entries=log_entries)
            else:
                raise Exception(f"Working directory is dirty (!stash_and_continue_if_wip): '{brighten(repo_path)}'")

        cmd_arr = ['git', '-C', repo_path, 'pull']
        run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries)

    @staticmethod
    def git_checkout(
            repo_path,
            tag_or_branch,
            stash_and_continue_if_wip,
            log_entries=None
    ):
        """ Checkout the specified tag/branch in the repository, considering `stash_and_continue_if_wip`. """
        if GitHelper.git_dir_exists(repo_path):
            if GitHelper.git_check_is_dirty(repo_path, log_entries=log_entries):
                if stash_and_continue_if_wip:
                    msg = colorize_path(f"  - Stashing WIP changes for repo: '{brighten(repo_path)}'")
                    if log_entries is not None:
                        log_entries.append(msg)
                    else:
                        logger.info(msg)
                    GitHelper.git_stash(repo_path, log_entries=log_entries)
                else:
                    raise Exception(
                        f"Working directory is dirty and !stash_and_continue_if_wip: "
                        f"'{brighten(repo_path)}'")

        cmd_arr = ['git', '-C', repo_path, 'checkout']
        has_tag_or_branch = (tag_or_branch is not None) and (tag_or_branch != '')
        if has_tag_or_branch:
            cmd_arr += [tag_or_branch]

        run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries)

    @staticmethod
    def git_add_to_exclude(rel_base_path, preserved_dirs, log_entries=None):
        """
        Uses git update-index to prevent git from tracking changes to all paths except the preserved ones.
        """
        # Get all items in the base path
        all_items = os.listdir(rel_base_path)

        # Create a list of items to exclude (all items except the preserved ones)
        items_to_exclude = [item for item in all_items if item not in preserved_dirs]

        # Use git update-index to exclude these items
        for item in items_to_exclude:
            abs_path = (Path(rel_base_path) / item).resolve()
            if abs_path.is_dir():
                for sub_item in abs_path.rglob('*'):
                    cmd_arr = [
                        'git', '-C', rel_base_path,
                        'update-index', '--assume-unchanged', str(sub_item)  # Absolute paths only
                    ]
                    run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries)
            else:
                cmd_arr = ['git', '-C', rel_base_path, 'update-index', '--assume-unchanged', str(abs_path)]
                run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True, log_entries=log_entries)

    @staticmethod
    def git_get_latest_tag_ver(
            working_dir_repo_path,
            version_regex_pattern=None,
            quiet=False,
            log_entries=None
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
        git_cmd_arr = ['tag', '--list']

        try:
            stdout, stderr = GitHelper._git_submodule_cmd(
                git_cmd_arr,
                working_dir_repo_path,
                quiet,
                check_throw_on_cli_err=True,
                log_entries=log_entries
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
                return tuple(map(int, re.findall(r'\d+', tag)))

            filtered_tags.sort(key=_parse_version)

            if filtered_tags:
                return filtered_tags[-1]
            else:
                return None
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"

    @staticmethod
    def _git_submodule_cmd(
            cmd,
            working_dir_repo_path,
            quiet,
            check_throw_on_cli_err=True,
            log_entries=None
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
            cmd += ['--quiet']
        cmd_prefix_arr = ['git', '-C', working_dir_repo_path]
        full_cmd = cmd_prefix_arr + cmd
        result = subprocess.run(
            full_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if check_throw_on_cli_err and result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode,
                full_cmd,
                output=result.stdout,
                stderr=result.stderr
            )
        return result.stdout, result.stderr

    @staticmethod
    def _throw_if_path_not_exists(path):
        """ Throw an exception if the specified path does not exist. """
        if not os.path.exists(path):
            raise Exception(f"Path does not exist: '{brighten(path)}'")
