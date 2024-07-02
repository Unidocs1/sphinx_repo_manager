# acceleratxr.io (Master Doc)

Master doc to create help docs from other repos with `make html` (`sphinx-build`). 

This guide focuses on Windows 11 instructions, but supports other OS (bash, Ubuntu, etc).

## Quickstart

1. Configure `docs/repo_manifest.yaml` (or leave defaults)
2. Run `start-docker.ps1`
3. Upon success, your browser will launch with `index.html` and stop the Docker instance.

## Prerequisites

You may either run via Docker (recommended) or locally (legacy):

### Docker Prereqs (Recommended)

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Local Prereqs (Legacy)

1. [Chocolatey](https://chocolatey.org/) CLI tool
	- Once you have Choco, install `make` in an **ADMIN** terminal:
	  ```powershell
      choco install make --yes
      ```

2. [Python 3.10](https://apps.microsoft.com/detail/9pjpw5ldxlz5)
	- See a recommended path to installing Python [below](#python-install-path)

3. Run `tools/requirements-install.ps1`
		
## Setup

* Configure `docs/repo_manifest.yml` to configure repos/prefs (defaults are recommended)

* **[Required for Xsolla repos]** If Docker tooling with _private_ repos:
	1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) -> Run
	2. Copy `.env.template` to `.env`
	3. Fill the `GITLAB_ACCESS_KEY` field

* **[Required for ReadTheDocs Private Repos]** For proper macro versioning:
    1. [create an account](https://about.readthedocs.com/?ref=readthedocs.org)
    2. At RTD web dashboard, create a new env var named `GITLAB_ACCESS_TOKEN` (⚠️ be aware this _may_ add plaintext server logs)
	3. Update the `.readthedocs.yaml` -> `$READTHEDOCS_PROJECT` name

## Build

### Docker (Recommended)

1. Run `start-docker.ps1`

### Local Build (Legacy)

1. Run `tools/requirements-install.ps1`
2. Run `docs/start.ps1`

### Speedy Rebuild

If you _just_ updated and want to build without going through `sphinx_repo_manager`, set either
`repo_manifest.yml` field: 

1. `enable_repo_manager` to `false` to disable for all repos
2. OR set individual repo `active` to false (notably useful for actively updating the `xbe_static_docs` repo).

### Debugging a Build

1. Slow down the logs and ensure chronological stability: Set the `max_workers_local` of `repo_manifest.yml` to `1` (default `5`).
2. Set `debug_mode` of `repo_manifest` to `true` (default `false`).
3. Comment out all repositories in your `repo_manifest` except 1 or 2.

## Typical Structure

### Main Doc

In this repo, we want to merge multiple docs into a single doc:

Open the built index via `build/html/index.html`

### Single Doc

Source repo docs/  layout tree should be structured as follows, with example content:

```
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

### Template Doc

See tools/[template-doc](tools/template-doc). Be sure to replace the `%PLACEHOLDERS%` (either via a script or manually) at:

* docs/README.md
* docs/source/conf.py

## Apps & Extensions

To describe what is installed, including extensions:

The `requirements.txt` file includes dependencies necessary for building and managing the documentation of our project
using Sphinx. **Overview:**

### Sphinx

- **Purpose**: [`sphinx`] Powerful doc generator that converts reStructuredText (.rst) files into HTML websites and other formats. It is highly customizable and supports numerous extensions.
- **Documentation**: [Sphinx Documentation](https://www.sphinx-doc.org/en/master/)

### Sphinx Read The Docs Theme

- **Purpose**: [`sphinx_rtd_theme`] Popular theme for Sphinx provided by Read the Docs. It offers a clean, mobile-friendly, and well-structured layout for documentation.
- **Documentation**: [sphinx_rtd_theme on GitHub](https://github.com/readthedocs/sphinx_rtd_theme)

### MyST-Parser

- **Purpose**: [`myst_parser`] Spiritual successor to recommonmark: Extended Markdown parser for Sphinx, allowing the use of Markdown with Sphinx documentation. It supports all Markdown features and provides additional syntax for roles and directives typically available in reStructuredText, making it a robust choice for Sphinx-based documentation projects that prefer Markdown.
- **Installation**: 
- **Documentation**: [MyST-Parser on GitHub](https://github.com/executablebooks/MyST-Parser)

### Sphinx Tabs

- **Purpose**: [`sphinx_tabs`] Sphinx extension that enables tabbed content in your documentation. This can be useful for separating content into different context-specific tabs on the same page without clutter.
- **Documentation**: [sphinx_tabs on GitHub](https://github.com/djungelorm/sphinx-tabs)

### PyYAML

- **Purpose**: [`PyYAML`] YAML parser and emitter for Python. It is used to handle YAML-formatted files within your documentation project, which can be useful for configuration files or other data-driven content.
- **Documentation**: [PyYAML on PyPI](https://pypi.org/project/PyYAML/)

### sphinx-copybutton

- **Purpose**: [`sphinx-copybutton`] Sphinx extension that adds a copy button to code blocks in your documentation. This allows users to easily copy code snippets to their clipboard with a single click.
- **Documentation**: [sphinx-copybutton on PyPI](https://pypi.org/project/sphinx-copybutton)

### sphinx-new-tab-lnk

- **Purpose**: [`sphinx-new-tab-lnk`] Sphinx extension that adds a target="_blank" attribute to external links in your documentation. This ensures that external links open in a new tab by default, preventing users from navigating away from your site.
- **Documentation**: [sphinx-new-tab-lnk on PyPI](https://pypi.org/project/sphinx-new-tab-lnk)

### DocGen Tools

#### breathe

TODO

#### sphinx_csharp

TODO

#### sphinx.ext.autodoc

TODO

## Legacy Additional Troubleshooting

### Clearing Cache

Delete these to regenerate them when you build again:

1. Delete `build` (or `make clean` via CLI)
2. Delete `source/content` (symlinks from `source/_repos-available`
3. Delete `source/_repos-available` (for use with `repo_manager`)

### Python Install Path (Legacy - Without Docker)

As this can easily get error-prone, especially for new Python users, see below to install Python 3.10 from scratch:

1. Open PowerShell in ADMIN
2. Install from:
	- Choco:
		- Should work, but not covered in this guide
		- ⚠️ Does not auto-alias `python` to `python3`
		- ⚠️ May handle PATHs differently
		- **TODO:** Update this part, if someone finds a good way
		
	- Windows Store - Either:
		- Install via the [Microsoft Store GUI]([Python 3.10](https://apps.microsoft.com/detail/9pjpw5ldxlz5))
		- Install via `winget` CLI:
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

See tools/[README.md](tools/README.md)

## License

TODO
