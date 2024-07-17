# %REPO_NAME%/docs (Single Doc)

Single doc - a content fragment of [the master doc](https://gitlab.acceleratxr.com/Core/acceleratxr.io) - is used to create help docs with `make html` (`sphinx-build`). 

The master doc will pull this repo's root `docs/` dir and use this as part of the content into a single doc.

This guide focuses on Windows 11 instructions, but supports other OS (bash, Ubuntu, etc).

## Prerequisites

### Required

#### Windows

1. [Chocolatey](https://chocolatey.org/) CLI tool
	- Once you have Choco, install `make` in an **ADMIN** terminal:
		```powershell
		choco install make --yes
		```
		
#### Common

2. [Python 3.10](https://apps.microsoft.com/detail/9pjpw5ldxlz5)
	- See a recommended path to installing Python [below](#python-install-path)

## Setup

1. Run `tools/requirements-install.ps1` as a normal user.

2. Configure the `docs/repo_manifest.yml` (well-commented within) with your desired versioning/cloning.

## Build


1. To build from source, either run `make.bat` or run in PowerShell from `docs/`:

```powershell
make html
```

2. Open the built index via `build/html/content/index.html` (`make.bat` will auto-launch this)

### Speedy Build

If you _just_ updated and want to build without going through `repo_manager`, simply set `repo_manifest.yml` property `enable_repo_manager` to `false`.

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

## Apps & Extensions

To describe what is installed, including extensions:

The `requirements.txt` file includes dependencies necessary for building and managing the documentation of our project using Sphinx. **Overview:**

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


### DocGen Tools

#### breathe

TODO

#### sphinx_csharp

TODO

#### sphinx.ext.autodoc

TODO

## Additional Troubleshooting

### Clearing Cache

Delete these to regenerate them when you build again:

1. Delete `build` (or `make clean` via CLI)
2. Delete `source/content`
3. Delete `source/_repos-available` (for use with `repo_manager`)

### Python Install Path

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

## License

TODO
