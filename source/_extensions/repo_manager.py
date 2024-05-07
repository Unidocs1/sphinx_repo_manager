import os
import yaml
import subprocess
from sphinx.util import logging

logger = logging.getLogger(__name__)

def setup(app):
    # Connect the 'builder-inited' event from Sphinx to our custom function.
    # This func will run when Sphinx finished initializing the builder.
    app.connect('builder-inited', clone_update_repos)

def clone_update_repos(app):
    # Determine absolute path/to/source/_extensions/repo_manager.py
    base_path = os.path.abspath(os.path.dirname(__file__))

    # Construct the path to the manifest file which defines the repos to manage.
    manifest_path = os.path.join(base_path, '..', '..', 'repo_manifest.yml')

    try:
        # Open and read the manifest file.
        with open(manifest_path, 'r') as file:
            manifest = yaml.safe_load(file)

            # Iterate over each repository defined in the manifest.
            for repo_name, repo_info in manifest['repositories'].items():
                # Construct the path where the repository should be cloned.
                repo_path = os.path.join(base_path, '..', '..', 'source', repo_name)

                # Check if the repository directory already exists.
                if not os.path.exists(repo_path):
                    # If the repository does not exist, clone it using the URL provided in the manifest.
                    logger.info(f"Cloning {repo_name}...")
                    subprocess.run(['git', 'clone', repo_info['url'], repo_path], check=True)

                # Checkout the specific tag for the repository, as defined in the manifest.
                logger.info(f"Checking out {repo_name} to {repo_info['tag']}...")
                subprocess.run(['git', '-C', repo_path, 'checkout', repo_info['tag']], check=True)

    # Catch and log any exceptions that occur during the process.
    except Exception as e:
        logger.error(f"Failed to manage repositories: {e}")
