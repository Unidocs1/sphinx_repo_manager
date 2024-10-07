# sphinx_repo_manager/tools

## Contents

[TOC]

## Scripts

| Docker Helpers | |
|--------|-------------|
| [`docker-build.ps1`](docker-build.ps1) | Build Docker images for the project. |
| [`docker-start.ps1`](docker-start.ps1) | Start Docker containers for the project. |
| [`docker-destroy.ps1`](docker-destroy.ps1) | Destroy Docker containers and clean up resources. |

| Python VENV Helpers | |
|--------|-------------|
| [`venv-activate.ps1`](venv-activate.ps1) | Activate a new or existing virtual environment called `xbe-venv`. |
| [`venv-destroy.ps1`](venv-destroy.ps1) | Destroy the virtual environment called `xbe-venv`. |

| Python Conda Helpers| |
|--------|-------------|
| [`conda-activate.ps1`](conda-activate.ps1) | Activate a new or existing conda environment called `xbe-docs` at Python 3.10. |
| [`conda-destroy.ps1`](conda-destroy.ps1) | Destroy the conda environment called `xbe-docs`. |

| Python Requirements Install  | |
|--------|-------------|
| [`requirements-install.ps1`](requirements-install.ps1) | Install requirements into the active environment. Equivalent to `cd docs && make install`. |

| Cleanup | |
|--------|-------------|
| [`clean-build.ps1`](clean-build.ps1) | Clean the build directory to ensure a fresh build environment. |
| [`clean-cache.ps1`](clean-cache.ps1) | Clear the cache to resolve potential issues with stale data. |

| Miscellaneous | |
|--------|-------------|
| [`mass-repo-cmds.ps1`](mass-repo-cmds.ps1) | Execute mass commands across multiple repositories for maintenance tasks. |

## Python Scripts

| Script | |
|--------|-------------|
| [`production_prep.py`](production_prep.py) | Prepare the project for production deployment. |
| [`tool_template.py`](tool_template.py) | Start here for tooling -- a minimal template to read the manifest file, then leave you to it. |

## Templates

| Template | |
|----------|-------------|
| [`template-doc/`](template-doc/) | Paste this to new repos for a `docs/` template. <br>Replace the `%PLACEHOLDERS%` in: `docs/README.md` and `docs/source/conf.py` |
