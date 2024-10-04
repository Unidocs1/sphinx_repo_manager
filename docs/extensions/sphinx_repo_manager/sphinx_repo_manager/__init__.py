# source/extensions/sphinx_repo_manager/sphinx_repo_manager/__init__.py
from .sphinx_repo_manager import SphinxRepoManager
from .git_helper import GitHelper
from typing import TypedDict
from pathlib import Path
from typing import cast


# Define the type structure for sphinx_repo_manager config values
class SphinxRepoManagerConfig(TypedDict):
    repo_manager_manifest_path: Path
    source_static_path: Path
    source_doxygen_path: Path
    default_repo_auth_user: str
    default_repo_auth_token: str
    has_default_repo_auth_token: bool
    start_time: float
    end_time: float
    manifest: dict
    # raw_manifest: dict


def set_config_dot_py_vals(app, repo_manager):
    """ Save useful config vals to be accessible from conf.py """
    app.config.sphinx_repo_manager = cast(SphinxRepoManagerConfig, {
        "repo_manager_manifest_path": repo_manager.repo_manager_manifest_path,
        "source_static_path": repo_manager.source_static_path,
        "source_doxygen_path": repo_manager.source_doxygen_path,
        "default_repo_auth_user": repo_manager.default_repo_auth_user,
        "default_repo_auth_token": repo_manager.default_repo_auth_token,
        "has_default_repo_auth_token": repo_manager.has_default_repo_auth_token,
        "start_time": repo_manager.start_time,
        "end_time": repo_manager.end_time,
        "manifest": repo_manager.manifest,
        # "raw_manifest": repo_manager.raw_manifest,
    })


def create_repo_manager(app):
    """ Instantiate the SphinxRepoManager and save config values to app.config """
    repo_manager = SphinxRepoManager(app)
    repo_manager.main(app)
    set_config_dot_py_vals(app, repo_manager)


# [ENTRY POINT] Set up the Sphinx extension to trigger on a sphinx-build init phase (before building)
def setup(app):
    # Connect to the builder-inited event -> and only then instantiate SphinxRepoManager
    app.connect("builder-inited", create_repo_manager)

    return {
        # Retrieve version from pyproject.toml
        'version': '1.0.0',

        # Until determined otherwise, marking as False to be safe
        'parallel_read_safe': False,
        'parallel_write_safe': False,
    }
