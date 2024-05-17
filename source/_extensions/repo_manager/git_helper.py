import os
import subprocess
import shlex  # CLI helper
from sphinx.util import logging
from log_styles import *

logger = logging.getLogger(__name__)


class GitHelper:
    def __init__(self):
        pass

    @staticmethod
    def git_fetch(repo_path):
        """ Fetch all remote branches and tags *from the repo_path working dir (-C). """
        GitHelper.throw_if_path_not_exists(repo_path)
        cmd_arr = ['fetch', '--all', '--tags']
        GitHelper.git_submodule_cmd(cmd_arr, repo_path, quiet=False)

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
        subprocess.run([
            'git', 'clone',
            '--branch', branch,
            '-q',
            repo_url_dotgit, clone_to_path], check=True)

    @staticmethod
    def git_check_is_dirty(repo_path):
        """ Check if the working directory is dirty (has WIP changes). """
        try:
            GitHelper.throw_if_path_not_exists(repo_path)
            cmd_arr = ['status', '--porcelain']
            output = GitHelper.git_submodule_cmd(cmd_arr, repo_path, quiet=False)
            is_dirty = bool(output.strip())
            return is_dirty
        except Exception as e:
            logger.error(f"Failed to check if the repository is dirty: {e}")
            raise Exception(f"Failed to check if the repository is dirty: {repo_path}\nError: {e}")

    @staticmethod
    def git_stash(repo_path, stash_message='repo_mgr-autostash'):
        """ Stash the working directory. """
        GitHelper.throw_if_path_not_exists(repo_path)
        cmd_arr = ['stash', 'push', '-m', stash_message]
        GitHelper.git_submodule_cmd(cmd_arr, repo_path, quiet=False)

    @staticmethod
    def git_dir_exists(repo_path):
        """ Check if a .git directory exists within repo_path. """
        git_dir = os.path.join(repo_path, '.git')
        return os.path.exists(git_dir)

    @staticmethod
    def git_checkout(repo_path, tag_or_branch, stash_and_continue_if_wip):
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

        cmd_arr = ['checkout', tag_or_branch]
        GitHelper.git_submodule_cmd(cmd_arr, repo_path, quiet=True)

    @staticmethod
    def git_submodule_cmd(cmd, working_dir_repo_path, quiet, check_throw_on_cli_err=True):
        """ Run a git command in the specified sub-repo path, ensuring it's run from that working dir. """
        if quiet:
            cmd += ['--quiet']
        cmd_prefix_arr = ['git', '-C', working_dir_repo_path]
        full_cmd = cmd_prefix_arr + cmd

        pretty_cmd = shlex.join(full_cmd)
        logger.info(colorize_action(colorize_path(f"  - CLI: `{brighten(pretty_cmd)}`")))

        try:
            result = subprocess.run(full_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                error_message = result.stderr.strip()
                logger.error(f"Git command failed:\n{brighten(error_message)}")
                if check_throw_on_cli_err:
                    raise Exception(f"Git command failed: '{pretty_cmd}'\nError: '{brighten(error_message)}'")
            return result.stdout
        except FileNotFoundError as e:
            logger.error(f"Git command not found: '{brighten(e)}'")
            raise Exception(f"Git command not found: {pretty_cmd}\nError: '{brighten(e)}'")

    @staticmethod
    def throw_if_path_not_exists(path):
        """ Throw an exception if the specified path does not exist. """
        if not os.path.exists(path):
            raise Exception(f"Path does not exist: '{brighten(path)}'")

# Example usage:
# git_helper = GitHelper()
# git_helper.git_fetch(repo_path)
