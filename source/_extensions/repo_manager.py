"""
Sphinx Extension: Repository Manager
------------------------------------

Description:
This Sphinx extension is designed to automate the management of multiple documentation repositories as part
of building a larger, unified documentation system. It facilitates the cloning and updating of external
repositories specified in a YAML manifest file, ensuring that each repository is checked out to the specified
tag before Sphinx documentation generation proceeds.

How it Works:
1. The extension reads a manifest file (`repo_manifest.yml`) that lists repositories with their respective
clone URLs and tags.
2. It checks if each repository is already cloned at the specified location.
3. If a repository is not found, it clones the repository from the provided URL.
4. Regardless of the initial presence, it checks out the specified tag to align the documentation state
with the desired version.

Usage:
1. Place the `repo_manifest.yml` file two levels up from this script, typically at the project root.
2. Ensure each repository listed in the manifest includes a `url` and a `tag`.
3. Optionally, specify `baseClonePath` in the manifest to change the default cloning location from two
directories up from this script.
4. Include this extension in your Sphinx `conf.py` file by adding the extension's path to `sys.path`
and including `'repo_manager'` in the `extensions` list.

Manifest Format Example:
repo_manifest.yml should look like this:

    version: "v1.0.0"
    baseClonePath: "../"  # Optional: Default base path for cloning repositories
    repositories:
      example_repo:
        url: "https://github.com/example/example_repo"
        tag: "v1.0"
        clonePath: "example_repo"  # Optional: Specific path relative to baseClonePath

Requirements:
- Python 3.6 or higher
- Sphinx 1.8 or higher
- PyYAML library

Ensure that the Python environment where Sphinx is running includes PyYAML to parse the YAML configuration.

Entry point: setup(app) | This script is executed during the 'builder-inited' event of Sphinx,
which is triggered after Sphinx initialization but before the build process begins.
"""
import os
import yaml
import subprocess
from sphinx.util import logging

STOP_BUILD_ON_ERROR = True
LOG_PREFIX = "[repo_manager]"
END_REPO_MGR = "\n--END REPO_MANAGER--\n"
logger = logging.getLogger(__name__)


class RepositoryManagementError(Exception):
    """Custom exception for repository management errors."""
    pass


def setup(app):
    # Connect the 'builder-inited' event from Sphinx to our custom function.
    app.connect('builder-inited', clone_update_repos)


def clone_update_repos(app):
    print("\n--BEGIN REPO_MANAGER--\n")
    try:
        manifest = read_manifest()
        manage_repositories(manifest)
    except Exception as e:
        logger.error(f"{LOG_PREFIX} Failed to manage repositories:\n{e}")
        if STOP_BUILD_ON_ERROR:
            raise RepositoryManagementError(f"{LOG_PREFIX} Critical repository management failure: {e}")
    finally:
        print(END_REPO_MGR)


def read_manifest():
    """Read and return the repository manifest file."""
    base_path = os.path.abspath(os.path.dirname(__file__))
    manifest_path = os.path.join(base_path, '..', '..', 'repo_manifest.yml')
    print(f"{LOG_PREFIX} Manifest path:", manifest_path)

    with open(manifest_path, 'r') as file:
        return yaml.safe_load(file)


def manage_repositories(manifest):
    """Manage the cloning and checking out of repositories as defined in the manifest."""
    base_path = os.path.abspath(os.path.dirname(__file__))
    base_clone_path = os.path.abspath(os.path.join(base_path, manifest.get('baseClonePath', '../')))

    for repo_name, repo_info in manifest['repositories'].items():
        clone_path = repo_info.get('clonePath', repo_name)
        repo_path = os.path.join(base_clone_path, clone_path)
        clone_and_checkout(repo_name, repo_info, repo_path)


def clone_and_checkout(repo_name, repo_info, repo_path):
    """Clone the repository if it does not exist and checkout the specified tag."""
    if not os.path.exists(repo_path):
        logger.info(f"Cloning {repo_name} into {repo_path}...")
        subprocess.run(['git', 'clone', repo_info['url'], repo_path], check=True)
        subprocess.run(['git', '-C', repo_path, 'fetch', '--tags'], check=True)

    try:
        logger.info(f"Checking out {repo_name} to tag {repo_info['tag']}...")
        subprocess.run(['git', '-C', repo_path, 'checkout', repo_info['tag']], check=True)
    except subprocess.CalledProcessError:
        error_url = f"{repo_info['url']}/tree/{repo_info['tag']}"
        error_message = (f"- Failed to checkout tag '{repo_info['tag']}' for repository '{repo_name}'.\n"
                         f"   - Does the tag exist? {error_url}")
        raise RepositoryManagementError(error_message)
