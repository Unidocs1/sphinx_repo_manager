import os
# import yaml
import subprocess
import shlex  # CLI helper
from sphinx.util import logging
from log_styles import *

logger = logging.getLogger(__name__)


def git_fetch(repo_path):
    """ Fetch all branches and tags from the remote repository. """
    # Fetch all branches and tags *from the repo_path working dir (-C)*
    git_submodule_cmd(['fetch', '--all', '--tags'], repo_path)


def git_validate_is_git_dir(repo_path, validate_has_other_files):
    """ Check if a directory is a valid Git repository """
    if not os.path.exists(repo_path):
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


def git_clone(clone_to_path, repo_url_dotgit, branch):
    """
    Clone the repo+branch from the provided URL to the specified path.
    - rel_symlinked_tagged_repo_path # eg: "v1.0.0/account_services"
    """
    # Clone -> Fetch all
    subprocess.run([
        'git', 'clone',
        '--branch', branch,
        '-q',
        repo_url_dotgit, clone_to_path], check=True)


def git_checkout(repo_path, tag_or_branch):
    """ Checkout the specified tag/branch in the repository. """
    git_submodule_cmd(['checkout', tag_or_branch], repo_path)


def git_submodule_cmd(cmd, working_dir_repo_path):
    """
    Run a git command in the specified sub-repo path, ensuring it's run from that working dir.
    - `--quiet` suppresses spammy tips
    - eg: git_existing_repo_cmd(['checkout', 'v1.0.0'], 'source/_repos-available/v1.0.0/account_services')
    - eg: git_existing_repo_cmd(['fetch', '--all', '--tags'], 'source/_repos-available/v1.0.0/account_services')
    - eg: git_existing_repo_cmd(['pull'], 'source/_repos-available/v1.0.0/account_services')
    """
    full_cmd = ['git', '-C', working_dir_repo_path] + cmd + ['--quiet']

    pretty_cmd = shlex.join(full_cmd)
    logger.info(colorize_action(colorize_path(f"  - CLI: `{brighten(pretty_cmd)}`")))

    subprocess.run(full_cmd, check=True)