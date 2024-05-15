"""
Script to get repository data and manage repositories.
It utilizes the RepoManager and GitHelper classes from the Sphinx extension.
"""

import os
import sys
import yaml

# Add the path to the repo_manager extension
repo_manager_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './repo_manager'))
sys.path.insert(0, repo_manager_path)

# Import the RepoManager and GitHelper from the repo_manager package
from repo_manager import RepoManager
# from repo_manager import GitHelper


def generate_readthedocs_yaml(manifest, output_path="../.readthedocs.yaml"):
    """
    Generate a .readthedocs.yaml file based on the given manifest.
    Create a backup of the existing .readthedocs.yaml file if it exists.
    -----------------------------------------------------------------------------
    - Overview Doc | https://docs.readthedocs.io/en/stable/config-file/index.html
    - Ref Doc | https://docs.readthedocs.io/en/stable/config-file/v2.html
    -----------------------------------------------------------------------------
    """
    versions = list(manifest['macro_versions'].keys())

    rtd_config = {
        "version": 2,
        "formats": ["htmlzip", "pdf", "epub"],
        "build": {
            "image": "latest"
        },
        "python": {
            "version": 3,
            "install": [
                {
                    "requirements": "requirements.txt"
                }
            ]
        },
        "sphinx": {
            "configuration": "source/conf.py"
        },
        "submodules": {
            "include": ["*"],
            "recursive": True
        },
        "versions": {
            "only": versions
        }
    }

    # Backup the existing .readthedocs.yaml file if it exists
    if os.path.exists(output_path):
        backup_path = output_path + ".bak"
        os.rename(output_path, backup_path)
        print(f"Existing {output_path} backed up as {backup_path}")

    # Generate the new .readthedocs.yaml file
    with open(output_path, "w") as f:
        yaml.dump(rtd_config, f, default_flow_style=False)
    print(f".readthedocs.yaml generated with versions: {versions}")


def main(manifest_path):
    """
    Main function to manage repositories based on the manifest file.
    """
    # Initialize the RepoManager with the path to the manifest file
    manager = RepoManager(manifest_path)

    # Read the manifest
    manifest = manager.read_manifest()

    # Generate the .readthedocs.yaml file
    generate_readthedocs_yaml(manifest)


# Entry point of the script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_repo_data.py <manifest_path>")
        sys.exit(1)

    # Get the path of the manifest file from the command line arguments
    manifest_path = sys.argv[1]

    # Run the main function
    main(manifest_path)
