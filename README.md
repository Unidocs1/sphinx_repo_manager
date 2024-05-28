# xbe-docs

Create help docs with `sphinx-build`. This guide is specific to Windows OS.

## Prerequisites

### Required

1. [Chocolatey](https://chocolatey.org/) CLI tool
	- Once you have Choco, install `make` in an **ADMIN** terminal:
		```powershell
		choco install make --yes
		```

2. [Python 3.10](https://apps.microsoft.com/detail/9pjpw5ldxlz5)
	- See a recommended path to installing Python [below](#python-install-path)

### Optional
	
1. If you want macro versionining with ReadTheDocs (RTD), [create an account](https://about.readthedocs.com/?ref=readthedocs.org)

2. RTD works best with public repos, but to use _private_ repos:
	1. Login to RTD dashboard and create a new env var named `GITLAB_ACCESS_TOKEN` (be aware this _may_ add plaintext server logs)
	2. Update the .readthedocs.yaml `$READTHEDOCS_PROJECT` name

## Setup

1. Run `tools/requirements-install.ps1` as a normal user

2. Configure the `repo_manifest.yml` with your desired versioning/cloning.

## Build

1. To build from source, either run `make.bat` or run in PowerShell:

```powershell
make html
```

2. Open the built index via `build/html/index.html`

## Typical Structure

### Main Doc

In this repo, we want to merge multiple docs into a single doc:

Open the built index via `build/html/index.html`

### Single Doc

Source repo docs/  layout tree should be structured as follows, with example content:

```
<repo root>/docs
└───source
    │   conf.py
    │   index.rst
    │
    ├───content
    │   ├───foo
    │   │       index.rst
    │   │       arbitrary.rst
    │   │
    │   └───bar.rst
    │
    ├───_static
	│		images/foo.png
	│		css/someStyle.css
    │
    └───_templates
            _templates go here
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

## Troubleshooting

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
