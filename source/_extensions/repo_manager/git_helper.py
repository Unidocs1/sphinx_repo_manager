import os
import shutil
import subprocess
import shlex  # CLI helper
from pathlib import Path
from sphinx.util import logging
from log_styles import *

logger = logging.getLogger(__name__)


def log_pretty_cli_cmd(cmd_arr):
    """ Log a pretty CLI command. """
    pretty_cmd = shlex.join(cmd_arr)
    logger.info(colorize_cli_cmd(f"  - CLI: `{brighten(pretty_cmd)}`"))


def run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True):
    """ Run a subprocess command and handle errors. """
    log_pretty_cli_cmd(cmd_arr)
    try:
        result = subprocess.run(cmd_arr, capture_output=True, text=True)
        if result.returncode != 0:
            error_message = result.stderr.strip()
            logger.error(f"Command failed:\n{brighten(error_message)}")
            if check_throw_on_cli_err:
                pretty_cmd = shlex.join(cmd_arr)
                raise Exception(f"Command failed: '{pretty_cmd}'\nError: '{brighten(error_message)}'")
        return result.stdout
    except FileNotFoundError as e:
        logger.error(f"Command not found: '{brighten(e)}'")
        pretty_cmd = shlex.join(cmd_arr)
        raise Exception(f"Command not found: {pretty_cmd}\nError: '{brighten(e)}'")


class GitHelper:
    def __init__(self):
        pass

    @staticmethod
    def git_fetch(repo_path):
        """ Fetch all remote branches and tags *from the repo_path working dir (-C). """
        GitHelper.throw_if_path_not_exists(repo_path)
        cmd_arr = ['git', '-C', repo_path, 'fetch', '--all', '--tags']
        run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True)

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
    def git_clone(clone_to_path, repo_url_dotgit, branch):
        """ Clone the repo+branch from the provided URL to the specified path. """
        git_clone_cmd_arr = [
            'git', 'clone',
            '--branch', branch,
            '-q',
            repo_url_dotgit, clone_to_path
        ]
        run_subprocess_cmd(git_clone_cmd_arr, check_throw_on_cli_err=True)

    @staticmethod
    def remove_except(base_path, exclude_dirs):
        """
        Remove all items in the base_path except those in exclude_dirs.
        """
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if item not in exclude_dirs:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)

    @staticmethod
    def clean_exclude_root_level(repo_path, sparse_first_level):
        """
        Clean the root level of the repo_path, leaving only .git and sparse_first_level directories.
        """
        # These dirs won't be touched
        preserved_dirs = ['.git', sparse_first_level]

        # Add non-preserved dirs to .git/info/exclude before wiping
        # We don't want it to show on git diff -- this is *just* local to us
        GitHelper.git_add_to_exclude(repo_path, preserved_dirs)

        # Remove all items except those in exclude_dirs
        GitHelper.remove_except(repo_path, preserved_dirs)

    @staticmethod
    def git_clean_sparse_docs_clone(repo_path, repo_sparse_path):
        """
        Clean up the repo to only keep the specified sparse checkout paths.
        """
        # Ensure the path to exclude exists
        full_path = os.path.join(repo_path, repo_sparse_path)
        os.makedirs(full_path, exist_ok=True)

        # Extract the parts of the sparse path
        sparse_parts = Path(repo_sparse_path).parts
        docs_dir = sparse_parts[0]

        # Remove everything except the .git and docs dir at root level
        GitHelper.clean_exclude_root_level(repo_path, docs_dir)

    def git_sparse_clone(
            self,
            clone_to_path,
            repo_url_dotgit,
            branch,
            repo_sparse_path,
            stash_and_continue_if_wip,
    ):
        """
        Clone the repo with sparse checkout, only fetching the specified directories.
        (!) repo_sparse_path is a single string that will be combined into an arr.
        (!) You may want to call git_clean_sparse_docs_clone() after this to remove unnecessary files.
        """
        # Clone the repository with no checkout
        git_clone_filter_nocheckout_cmd_arr = [
            'git', 'clone',
            '--filter=blob:none', '--no-checkout',
            '--branch', branch,
            '-q', repo_url_dotgit, clone_to_path
        ]
        run_subprocess_cmd(git_clone_filter_nocheckout_cmd_arr, check_throw_on_cli_err=True)

        # Initialize sparse checkout
        sparse_checkout_init_cmd_arr = [
            'git', '-C', clone_to_path,
            'sparse-checkout', 'init', '--cone'
        ]
        run_subprocess_cmd(sparse_checkout_init_cmd_arr, check_throw_on_cli_err=True)

        # Set the sparse checkout paths
        sparse_checkout_set_cmd_arr = [
            'git', '-C', clone_to_path,
            'sparse-checkout', 'set', repo_sparse_path
        ]
        run_subprocess_cmd(sparse_checkout_set_cmd_arr, check_throw_on_cli_err=True)

        # Pull the changes (checkout the branch)
        self.git_checkout(
            clone_to_path,
            branch,
            stash_and_continue_if_wip)

    @staticmethod
    def git_check_is_dirty(repo_path):
        """
        Check if the working directory is dirty (has WIP changes).
        :returns is_dirty
        """
        try:
            GitHelper.throw_if_path_not_exists(repo_path)
            cmd_arr = ['git', '-C', repo_path, 'status', '--porcelain']
            output = run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True)
            is_dirty = bool(output.strip())
            return is_dirty
        except Exception as e:
            logger.error(f"Failed to check if the repository is dirty: {e}")
            raise Exception(f"Failed to check if the repository is dirty: {repo_path}\nError: {e}")

    @staticmethod
    def git_stash(repo_path, stash_message='repo_mgr-autostash'):
        """ Stash the working directory. """
        GitHelper.throw_if_path_not_exists(repo_path)
        cmd_arr = ['git', '-C', repo_path, 'stash', 'push', '-m', stash_message]
        run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True)

    @staticmethod
    def git_dir_exists(repo_path):
        """ Check if a .git directory exists within repo_path. """
        git_dir = os.path.join(repo_path, '.git')
        return os.path.exists(git_dir)

    @staticmethod
    def git_checkout(
            repo_path,
            tag_or_branch,
            stash_and_continue_if_wip,
    ):
        """ Checkout the specified tag/branch in the repository, considering `stash_and_continue_if_wip`. """
        if GitHelper.git_dir_exists(repo_path):
            if GitHelper.git_check_is_dirty(repo_path):
                if stash_and_continue_if_wip:
                    logger.info(colorize_path(f"  - Stashing WIP changes for repo: '{brighten(repo_path)}'"))
                    GitHelper.git_stash(repo_path)
                else:
                    raise Exception(
                        f"Working directory is dirty and !stash_and_continue_if_wip: "
                        f"'{brighten(repo_path)}'")

        cmd_arr = ['git', '-C', repo_path, 'checkout']
        has_tag_or_branch = (tag_or_branch is not None) and (tag_or_branch != '')
        if has_tag_or_branch:
            cmd_arr += [tag_or_branch]

        run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True)

    @staticmethod
    def git_add_to_exclude(rel_base_path, preserved_dirs):
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
                    run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True)
            else:
                cmd_arr = ['git', '-C', rel_base_path, 'update-index', '--assume-unchanged', str(abs_path)]
                run_subprocess_cmd(cmd_arr, check_throw_on_cli_err=True)

    @staticmethod
    def git_submodule_cmd(
            cmd,
            working_dir_repo_path,
            quiet,
            check_throw_on_cli_err=True,
    ):
        """ Run a git command in the specified sub-repo path, ensuring it's run from that working dir. """
        if quiet:
            cmd += ['--quiet']
        cmd_prefix_arr = ['git', '-C', working_dir_repo_path]
        full_cmd = cmd_prefix_arr + cmd
        run_subprocess_cmd(full_cmd, check_throw_on_cli_err=check_throw_on_cli_err)

    @staticmethod
    def throw_if_path_not_exists(path):
        """ Throw an exception if the specified path does not exist. """
        if not os.path.exists(path):
            raise Exception(f"Path does not exist: '{brighten(path)}'")
