from sphinx.application import Sphinx
from sphinx.config import Config
from pathlib import Path
from .sphinx_repo_manager import SphinxRepoManager


def configure_doxygen(app: Sphinx, config: Config, repo_manager: SphinxRepoManager):
    """
    Configure Breathe extension based on the repo manager configuration.
    """
    breathe_local: bool = repo_manager.manifest["enable_breathe_local"]
    rtd_build: bool = repo_manager.read_the_docs_build
    do_breathe: bool = breathe_local or rtd_build
    print(
        f"\n[sphinx_repo_manager::configure_breathe] Configuring Breathe extension - active: {do_breathe} (breathe enabled? {breathe_local}, is rtd? {rtd_build})"
    )
    if do_breathe:
        enable_breathe(app, config)
    else:
        exclude_breathe(app, config)


def enable_breathe(app: Sphinx, config: Config):
    """
    Enable Breathe extension based on the repo manager configuration.
    """
    # Configure Breathe extension
    base_dir = Path(app.srcdir, "_doxygen")
    print(
        f"[sphinx_repo_manager::enable_breathe] Configuring breathe projects from {base_dir}..."
    )
    if not hasattr(config, "breathe_projects"):
        config.breathe_projects = {}

    for proj in base_dir.iterdir():
        if not proj.is_dir():
            continue
        proj_name = proj.parts[-1]
        path = base_dir.joinpath(proj_name)
        if path.is_dir():
            posix_path = path.as_posix()
            print(
                f"[sphinx_repo_manager::enable_breathe] Registering project: '{proj_name}' at posix path '{posix_path}'"
            )
            config.breathe_projects[proj_name] = posix_path


def exclude_breathe(app: Sphinx, config: Config):
    """
    Exclude Breathe input content files based on the repo manager configuration.
    """
    # Exclude Breathe api paths
    base_dir = Path(app.srcdir, "_doxygen")
    content_root = Path(app.srcdir, "content")
    print(
        f"[sphinx_repo_manager::exclude_breathe] Exclude breathe from {base_dir} {base_dir.is_dir()}..."
    )

    for proj in base_dir.iterdir():
        if not proj.is_dir():
            continue
        proj_name = proj.parts[-1]
        path = content_root.joinpath(proj_name, "api")
        if path.is_dir():
            posix_pattern = f"content/{proj_name}/api/*"
            print(
                f"[sphinx_repo_manager::exclude_breathe] Excluding project reference for: '{proj_name}' with posix pattern '{posix_pattern}'"
            )
            config.exclude_patterns.append(posix_pattern)
