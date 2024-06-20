import os
import sys
import subprocess


TARGET_PATH = "../docs/source/_extensions/sphinx_repo_manager"
LINK_NAME = "sphinx_repo_manager"


def create_symlink(target_path, link_name):
    """
    Create a symbolic link and verify it.
    """
    # Normalize the paths
    target_path = os.path.normpath(target_path)
    link_name = os.path.normpath(link_name)

    # Check if the symbolic link already exists and remove it if it does
    if os.path.islink(link_name):
        print(f"Removing existing symbolic link: {link_name}")
        os.remove(link_name)
    elif os.path.exists(link_name):
        print(f"Error: {link_name} already exists and is not a symbolic link")
        sys.exit(1)

    # Create the symbolic link for a directory
    try:
        os.symlink(target_path, link_name, target_is_directory=True)
        print(f"Creating symbolic link: {link_name} -> {target_path}")
    except OSError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Verify the symbolic link
    if os.path.islink(link_name):
        print(f"Symbolic link created successfully: {link_name} -> {os.readlink(link_name)}")
    else:
        print("Error: Failed to create symbolic link")
        sys.exit(1)

    # Add the symbolic link to git
    try:
        subprocess.run(["git", "add", link_name], check=True)
        print(f"Added {link_name} to git")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add {link_name} to git: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Create the symbolic link
    create_symlink(TARGET_PATH, LINK_NAME)
