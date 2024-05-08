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
from colorama import init, Fore, Style

init(autoreset=True)  # Initializes Colorama + auto-resets styles after each print (Style.RESET_ALL)
STOP_BUILD_ON_ERROR = True
logger = logging.getLogger(__name__)


class RepositoryManagementError(Exception):
    """ Custom exception for repository management errors. """
    pass


def setup(app):
    """ Connect the 'builder-inited' event from Sphinx to our custom function. """
    app.connect('builder-inited', clone_update_repos)


def clone_update_repos(app):
    """ Handle the repository cloning and updating process when Sphinx initializes. """
    print(f"\n{Fore.GREEN}══BEGIN REPO_MANAGER══\n")
    try:
        manifest, manifest_path = read_manifest()
        print(f"{Fore.CYAN}Manifest path: {manifest_path}\n")  # Display the fully resolved path
        manage_repositories(manifest, manifest_path)
    except Exception as e:
        logger.error(f"Failed to manage repositories:\n{e}")
        if STOP_BUILD_ON_ERROR:
            raise RepositoryManagementError(f"Critical repository management failure: {e}")
    finally:
        print(f"\n{Fore.GREEN}══END REPO_MANAGER══\n")


def read_manifest():
    """ Read and return the repository manifest from YAML file, along with its path. """
    base_path = os.path.abspath(os.path.dirname(__file__))
    manifest_path = os.path.abspath(os.path.join(base_path, '..', '..', 'repo_manifest.yml'))  # Normalize early
    with open(manifest_path, 'r') as file:
        return yaml.safe_load(file), manifest_path


def manage_repositories(manifest, manifest_path):
    """ Manage the cloning and checking out of repositories as defined in the manifest. """
    # Use the directory of the manifest file to calculate the base clone path
    base_clone_path = os.path.abspath(os.path.join(os.path.dirname(manifest_path),
                                                   manifest.get('base_clone_path', '../')))

    # Calculate the total number of repositories to process
    total_repos = sum(len(details['repositories']) for version, details in manifest['macro_versions'].items())
    current_repo = 1  # Initialize the current repository counter

    for version, details in manifest['macro_versions'].items():
        for repo_name, repo_info in details['repositories'].items():
            clone_path = repo_info.get('clone_path', repo_name)
            repo_path = os.path.join(base_clone_path, clone_path)
            clone_and_checkout(repo_name, repo_info, repo_path, total_repos, current_repo)
            current_repo += 1


def clone_and_checkout(repo_name, repo_info, repo_path, total_repos, current_repo):
    """ Clone the repository if it does not exist and checkout the specified branch and tag, with less verbosity. """
    if not os.path.exists(repo_path):
        logger.info(f"[{repo_name}]{Fore.CYAN} Cloning '{repo_name}' into '{repo_path}'...")
        subprocess.run(['git', 'clone', '-q', repo_info['url'], repo_path], check=True)
        subprocess.run(['git', '-C', repo_path, 'fetch', '--all'], check=True)

    try:
        logger.info(f"[{current_repo}/{total_repos}] {Fore.CYAN}{repo_path}")

        if 'branch' in repo_info:
            logger.info(f"{Fore.YELLOW}[{repo_name}] Checking out branch '{repo_info['branch']}'...")
            subprocess.run(['git', '-C', repo_path, 'checkout', '-q', repo_info['branch']], check=True)

        if 'tag' in repo_info:
            logger.info(f"{Fore.YELLOW}[{repo_name}] Checking out tag '{repo_info['tag']}'...")
            subprocess.run(['git', '-C', repo_path, 'checkout', '-q', repo_info['tag']], check=True)

        logger.info(f"{Fore.GREEN}Ok.\n")
    except subprocess.CalledProcessError as e:
        error_url = f"{repo_info['url']}/tree/{repo_info['tag']}"
        error_message = f"Failed to checkout branch/tag for repository '{repo_name}'. Does it exist? {error_url}"
        logger.error(error_message)
        raise RepositoryManagementError(error_message)
