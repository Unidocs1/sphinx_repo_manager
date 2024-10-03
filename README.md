# sphinx_repo_manager (docs.goxbe.io)

Master doc to create help docs from other repos with `make html` (`sphinx-build`).

This guide focuses on Windows 11 docker desktop instructions, but supports other OS (bash, Ubuntu, etc).

This currently combines content, but is slowly being transitioned to a generalized, official plugin.

## Contents

[TOC]

## Prerequisites

* Ensure to have already [unlocked max file paths](#unlock-max-char-paths)

## Quickstart

> **Warning:**
> Docker quickstart is currently experiencing write-issues for some; see legacy setup if affected.
> This will be addressed soon.

1. Copy [`.env.template`](.env.template) -> to `.env` and set `REPO_AUTH_PREFIX`.
    - If deploying to RTD, you should also set this env var in their web dashboard.
2. Configure [`docs/repo_manifest.yml`](docs/repo_manifest.yml) (ok to leave defaults).
3. Run [`tools/docker-start.ps1`](tools/docker-start.ps1) at the root of the project.
4. Upon success, your browser will launch with `index.html`.

You may either run via [Docker (beta)](#docker-setup) or [Locally (recommended)](#local-setup).

## Docker Setup

### Docker Requirements

* Minimum `Docker Engine` version: 20.10.0
  * Install [Docker Desktop](https://www.docker.com/products/tools/docker-desktop/)
      or [Docker Engine](https://docs.docker.com/engine/install/)

### Docker Scripts

* [`tools/docker-start.ps1`](tools/docker-start.ps1)
  * Start a preview container and launch the docs in your browser.
  * Exit the process to kill the container, it will clean itself up.
  * If there is no html build output (`docs/build/html`), this will run `tools/docker-build.ps1` first - but only if
      there is no existing output. To rebuild docs, run `tools/docker-build.ps1` manually before running this.

* [`tools/docker-build.ps1`](tools/docker-build.ps1)
  * Clear and rebuild the local html build folder (`docs/build/html`).
  * This will also build the required `base` and `sphinx` builder images if necessary.
  * If you've run `tools/docker-start.ps1` ensure the preview container is stopped before running this, or it will
      fail.

* [`tools/docker-destroy.ps1`](tools/clean-cache.ps1)
  * Destroy all containers and local images matching the `NAME` configured in `docker/.env`.
  * Also runs `tools/clean-cache.ps1` to clear the local filesystem.

* [`tools/clean-build.ps1`](tools/clean-build.ps1)
  * Clear all unversioned local files from `docs/build`.

* [`tools/clean-cache.ps1`](tools/clean-cache.ps1)
  * Clear all unversioned local files from `docs/build` and `docs/source`.

## Local Setup

### Local Requirements

1. Build Tool: `make`

   | OS      | Package Manager | Command                 |
   |---------|-----------------|-------------------------|
   | Windows | Chocolatey      | `choco install make -y` |
   | macOS   | Homebrew        | `brew install make`     |
   | Ubuntu  | APT             | `apt-get install make`  |

2. `Python v3.10` (or `conda`)

   | OS      | Package Manager | Command                                      |
   |---------|-----------------|----------------------------------------------|
   | Windows | Chocolatey      | `choco install python3 -y`                   |
   | macOS   | Homebrew        | `brew install python@3.10`                   |
   | Ubuntu  | APT             | `sudo apt-get install python3.10`            |

### Activate Python Environment

Activate the build environment, creating a new one if necessary.

#### With venv

* With `venv` ([`tools/venv-activate.ps1`](tools/venv-activate.ps1)).

    ```powershell
    ./tools/venv-activate.ps1
    ```

* Then proceed to [Installing Dependencies](#installing-dependencies).

#### With Conda

* With `conda` ([`tools/conda-activate.ps1`](tools/conda-activate.ps1)). This will create a new conda environment called `xbe-docs` using the `environment.yml` file.

    ```powershell
    ./tools/conda-activate.ps1
    ```

* Then proceed to [Building the Documentation](#building-the-documentation).

### Installing Dependencies

Local extensions located in the `docs/extensions` directory are referenced by `docs/requirements.txt` by relative 
path **from the project root** to mimic the runtime layout on ReadTheDocs servers.

* Installing `docs/requirements.txt` manually should be done from the project root like so:

    ```powershell
    pip install -r docs/requirements.txt
    ```

* Running the `make install` command from the `docs` directory does this automatically:

    ```powershell
    cd docs
    make install
    ```

* Or you can run the [`tools/requirements-install.ps1`](tools/requirements-install.ps1) script from any directory:

    ```powershell
    ./tools/requirements-install.ps1
    ```

### Building the Documentation

* The `make` command is a wrapper for `sphinx-build` that simplifies the build process. It reads the `Makefile` in the
  `docs` directory and executes the commands specified in it. The `html` target builds the HTML documentation:

    ```powershell
    make html
    ```

* ...while the `clean` target removes the build directory:

    ```powershell
    make clean
    ```

### Teardown Python Environment

Destroy the environment and dependencies, if desired.

* With `venv` ([`tools/venv-destroy.ps1`](tools/venv-destroy.ps1))

    ```powershell
    ./tools/venv-destroy.ps1
    ```

* with `conda`([`tools/conda-destroy.ps1`](tools/conda-destroy.ps1))

    ```powershell
    ./tools/conda-destroy.ps1
    ```

## Build Notes & Tips

❗If you recently updated your `repo_manifest.yml` file, you may want to 1st wipe these `source/` dirs
to ensure a clean build:

1. `_repos-available`
2. `content`

### Speedy Rebuild

If you _just_ updated and want to build without going through `sphinx_repo_manager`, set either
`repo_manifest.yml` field:

1. `enable_repo_manager` to `false` to disable for all repos
2. OR set individual repo `active` to false (notably useful for actively updating the `xbe_static_docs` repo).

### Debugging a Build

1. Slow down the logs and ensure chronological stability: Set the `max_workers_local` of `repo_manifest.yml` to `1` (
   default `5`).
2. Set `debug_mode` of `repo_manifest` to `true` (default `false`).
3. Comment out all repositories in your `repo_manifest` except 1 or 2.

## Typical Structure

### Main Doc

In this repo, we want to merge multiple docs into a single doc:

Open the built index via `build/html/index.html`

### Single Doc

Source repo docs/ layout tree should be structured as follows, with example content:

```text
- .git
- RELEASE_NOTES.rst
- <repo root>/docs/
   - source/
      - _extensions/
     - sphinx_repo_manager/
      - _static/
         - images/
            - foo.png
         - css/
            - someStyle.css
      - _templates/
      - content/
         - foo.rst (pointed to from index.rst)
      - RELEASE_NOTES.rst (symlink to root)
      - conf.py (entry point setup)
   - index.rst (entry point)
```

## Apps & Extensions

To describe what is installed, including extensions:

The `docs/requirements.txt` file includes dependencies necessary for building and managing the documentation of 
our project using Sphinx. __Overview:__

### Sphinx

* __Purpose__: [`sphinx`] Powerful doc generator that converts reStructuredText (.rst) files into HTML websites and
  other formats. It is highly customizable and supports numerous extensions.
* __Documentation__: [Sphinx Documentation](https://www.sphinx-doc.org/en/master/)

### Sphinx Read The Docs Theme

* __Purpose__: [`sphinx_rtd_theme`] Popular theme for Sphinx provided by Read the Docs. It offers a clean,
  mobile-friendly, and well-structured layout for documentation.
* __Documentation__: [sphinx_rtd_theme on GitHub](https://github.com/readthedocs/sphinx_rtd_theme)

### MyST-Parser

* __Purpose__: [`myst_parser`] Spiritual successor to recommonmark: Extended Markdown parser for Sphinx, allowing the
  use of Markdown with Sphinx documentation. It supports all Markdown features and provides additional syntax for roles
  and directives typically available in reStructuredText, making it a robust choice for Sphinx-based documentation
  projects that prefer Markdown.
* __Installation__:
* __Documentation__: [MyST-Parser on GitHub](https://github.com/executablebooks/MyST-Parser)

### Sphinx Tabs

* __Purpose__: [`sphinx_tabs`] Sphinx extension that enables tabbed content in your documentation. This can be useful
  for separating content into different context-specific tabs on the same page without clutter.
* __Documentation__: [sphinx_tabs on GitHub](https://github.com/djungelorm/sphinx-tabs)

### PyYAML

* __Purpose__: [`PyYAML`] YAML parser and emitter for Python. It is used to handle YAML-formatted files within your
  documentation project, which can be useful for configuration files or other data-driven content.
* __Documentation__: [PyYAML on PyPI](https://pypi.org/project/PyYAML/)

### sphinx-copybutton

* __Purpose__: [`sphinx-copybutton`] Sphinx extension that adds a copy button to code blocks in your documentation. This
  allows users to easily copy code snippets to their clipboard with a single click.
* __Documentation__: [sphinx-copybutton on PyPI](https://pypi.org/project/sphinx-copybutton)

### sphinx-new-tab-lnk

* __Purpose__: [`sphinx-new-tab-lnk`] Sphinx extension that adds a target="_blank" attribute to external links in your
  documentation. This ensures that external links open in a new tab by default, preventing users from navigating away
  from your site.
* __Documentation__: [sphinx-new-tab-lnk on PyPI](https://pypi.org/project/sphinx-new-tab-lnk)

### Local Extensions

Local extensions are located in the `docs/extensions` directory:

* [docs/extensions/sphinx_algolia_crawler/README.md](docs/extensions/sphinx_algolia_crawler/README.md)
* [docs/extensions/sphinx_feature_flags/README.md](docs/extensions/sphinx_feature_flags/README.md)
* [docs/extensions/sphinx_image_min/README.md](docs/extensions/sphinx_image_min/README.md)
* [docs/extensions/sphinx_openapi/README.md](docs/extensions/sphinx_openapi/README.md)
* [docs/extensions/sphinx_repo_manager/README.md](docs/extensions/sphinx_repo_manager/README.md)

## Troubleshooting

### Known Issues

#### Smooth-Scroll Navigation Issue

`sphinx_book_theme` and `pydata_sphinx_theme` has a right-column smooth scroll navigation issue where a click will
sometimes scroll 1 above or below your target list item.

#### Unlock Max Char Paths

> **Note:**
> As a repo manager, there may be deeply-nested directories and may need to unlock the 256-char limit in some envs

With **elevated** privileges:

#### Git

```bash
git config --system core.longpaths true
```

#### Windows

```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" `
    -Value 1 `
    -PropertyType DWORD `
    -Force
```

### Legacy Additional Troubleshooting

### Requirements Install - Invalid Requirement

If you see this error:

```bash
ERROR: Invalid requirement: './docs/extensions/sphinx_repo_manager': Expected package name at the start of dependency specifier
    ./docs/extensions/sphinx_repo_manager
    ^ (from line 20 of .\requirements.txt)
```

You probably tried to install `requirements.txt` from the wrong directory specified in the instructions: 

Be sure to run requirements.txt install commands **from project root**.

### sphinx-build `Error 2`

If you see this error:

```bash
process_begin: CreateProcess(NULL, sphinx-build -M clean source build, ...) failed.
make (e=2): The system cannot find the file specified.
make: *** [Makefile:20: clean] Error 2
```

This simply means `sphinx-build` command doesn't exist:

* If using venv/conda, did you activate your correct env? See [Activate Python Environment](#activate-python-environment).
* If manually installing reqs, did you forget to `pip install -r docs/requirements.txt`? See [Installing Dependencies](#installing-dependencies).

#### Clearing Cache

Delete these to regenerate them when you build again:

1. Delete `build` (or `make clean` via CLI)
2. Delete `source/content` (symlinks from `source/_repos-available`)
3. Delete `source/_repos-available` (for use with `repo_manager`)
4. Delete `source/_static/<any repo symlinks>` (for use with `repo_manager`)

#### Python Install Path (Legacy - Without Docker)

As this can easily get error-prone, especially for new Python users, see below to install Python 3.10 from scratch:

1. Open PowerShell in ADMIN
2. Install from:
    * Choco:
    * Should work, but not covered in this guide
    * ⚠️ Does not auto-alias `python` to `python3`
    * ⚠️ May handle PATHs differently
    * __TODO:__ Update this part, if someone finds a good way
    * Windows Store - Either:
    * Install via the [Microsoft Store GUI]([Python 3.10](https://apps.microsoft.com/detail/9pjpw5ldxlz5))
    * Install via `winget` CLI:

        ```powershell
        winget install "Python 3.10" --accept-package-agreements
        ```

3. Verify installation:

    ```powershell
    python --version
    pip --version
    ```

4. Add Python `/Scripts` to env PATH (`pip` installs tools here)

    ```powershell
    # Get the installation path of Python 3.10
    $pythonPath = (Get-Command python.exe).Source

    # Set the PYTHON_SCRIPTS_HOME environment variable
    $env:PYTHON_SCRIPTS_HOME = Join-Path $pythonPath "Scripts"

    # Add the Scripts directory to the user's PATH
    $env:Path += ";$env:PYTHON_SCRIPTS_HOME"

    # Display a message
    Write-Host "PYTHON_SCRIPTS_HOME set to: $env:PYTHON_SCRIPTS_HOME"
    Write-Host "Scripts directory added to PATH."
    ```

## Tools

### Template Doc

See tools/[template-doc](tools/template-doc). Be sure to replace the `%PLACEHOLDERS%` (either via a script or manually)
at:

* docs/README.md
* docs/source/conf.py

### More Tools

See tools/[README.md](tools/README.md)

## License

TODO
