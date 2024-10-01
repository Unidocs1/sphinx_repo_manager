# source/_extensions/sphinx_repo_manager/__init__.py
import os
from pathlib import Path, WindowsPath, PosixPath, PurePath
from .sphinx_repo_manager import SphinxRepoManager
from .git_helper import GitHelper

MANIFEST_NAME = "repo_manifest.yml"
ABS_BASE_PATH = os.path.abspath(os.path.dirname(__file__))
ABS_MANIFEST_PATH = os.path.normpath(
    os.path.join(ABS_BASE_PATH, "..", "..", "..", MANIFEST_NAME)
)

# [ENTRY POINT] Set up the Sphinx extension to trigger on a sphinx-build init phase (before building)
def setup(app):
    # Repo manifest file to use
    app.add_config_value(
        "repo_manager_manifest",
        Path(ABS_MANIFEST_PATH).as_posix(),
        "env",
        [str, Path, WindowsPath, PosixPath],
    )

    repo_manager = SphinxRepoManager()
    app.connect("builder-inited", repo_manager.main)
