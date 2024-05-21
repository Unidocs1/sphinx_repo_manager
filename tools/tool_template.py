"""
Script to hook into repo_manager and git_manager tooling,
and reading the ../repo_manifest.yml file
"""
import os
import sys
# import yaml

# Add the path to the repo_manager extension
repo_manager_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './repo_manager'))
sys.path.insert(0, repo_manager_path)

# Import the RepoManager and GitHelper from the repo_manager package
from repo_manager import RepoManager
from repo_manager import GitHelper

MANIFEST_PATH = '../repo_manifest.yml'
ABS_MANIFEST_PATH = os.path.normpath(
    os.path.abspath(MANIFEST_PATH))


def main():
    """ TODO. """
    # Initialize the RepoManager with the path to the manifest file
    manager = RepoManager(ABS_MANIFEST_PATH)
    manifest = manager.read_manifest()

    # TODO: Template starts here!
    # debug_mode = manifest['debug_mode']


# ENTRY POINT
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tool_template.py  # Looks for `../repo_manifest.yml`")
        sys.exit(1)

    # TODO: If you accept args, grab it from `sys.argv[i]`
    main()
