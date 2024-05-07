import os
import yaml
import subprocess
from sphinx.util import logging

logger = logging.getLogger(__name__)

def setup(app):
    app.connect('builder-inited', clone_update_repos)

def clone_update_repos(app):
    base_path = os.path.abspath(os.path.dirname(__file__))
    manifest_path = os.path.join(base_path, '..', '..', 'repo_manifest.yml')

    try:
        with open(manifest_path, 'r') as file:
            manifest = yaml.safe_load(file)
            for repo_name, repo_info in manifest['repositories'].items():
                repo_path = os.path.join(base_path, '..', '..', 'source', repo_name)
                if not os.path.exists(repo_path):
                    logger.info(f"Cloning {repo_name}...")
                    subprocess.run(['git', 'clone', repo_info['url'], repo_path], check=True)
                # Checkout specific tag
                logger.info(f"Checking out {repo_name} to {repo_info['tag']}...")
                subprocess.run(['git', '-C', repo_path, 'checkout', repo_info['tag']], check=True)
    except Exception as e:
        logger.error(f"Failed to manage repositories: {e}")

