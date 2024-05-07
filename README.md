# xbe-docs

Create help docs with `sphinx-build`. This guide is specific to Windows OS.

## Prerequisites

1. [Chocolatey](https://chocolatey.org/) CLI tool
	- Once you have Choco, install `make` in an **ADMIN** terminal:
		```powershell
		choco install make --yes
		```

2. [Python 3.10](https://apps.microsoft.com/detail/9pjpw5ldxlz5)
	- See a recommended path to installing Python [below](#python-install-path)

## Setup

Run `requirements-install.ps1` as a normal user

## Build

To build from source:

```powershell
make html
```

The output will build to the root-level `/Build` dir.

## Typical Structure

### Main Doc

In this repo, we want to merge multiple docs into a single doc:



### Single Doc

```
│   .gitignore
│   index.rst
│   make.bat
│   Makefile
│   README.md
│   requirements.txt
│
├───build
│       _build result of `make html`
│
└───source
    │   conf.py
    │   index.rst
    │
    ├───content
    │   ├───auth
    │   │       index.rst
    │   │       phone.rst
    │   │
    │   ├───concepts
    │   │       index.rst
    │   │       users.rst
    │   │
    │   └───sso
    │           index.rst
    │           steam.rst
    │
    ├───_static
    │       _static content goes here
			images/foo.png
			css/someStyle.css
    │
    └───_templates
            _templates go here
```

## Apps & Extensions

To describe what is installed, including extensions:

The `requirements.txt` file includes dependencies necessary for building and managing the documentation of our project using Sphinx. **Overview:**

### Sphinx

- **Purpose**: Sphinx is a powerful documentation generator that converts reStructuredText files into HTML websites and other formats. It is highly customizable and supports numerous extensions.
- **Installation**: `sphinx>=4.5`
- **Documentation**: [Sphinx Documentation](https://www.sphinx-doc.org/en/master/)

### Sphinx Read The Docs Theme

- **Purpose**: `sphinx_rtd_theme` is a popular theme for Sphinx provided by Read the Docs. It offers a clean, mobile-friendly, and well-structured layout for documentation.
- **Installation**: `sphinx_rtd_theme`
- **Documentation**: [sphinx_rtd_theme on GitHub](https://github.com/readthedocs/sphinx_rtd_theme)

### MyST-Parser

- **Purpose**: Spiritual successor to recommonmark, MyST-Parser is an extended Markdown parser for Sphinx, allowing the use of Markdown with Sphinx documentation. It supports all Markdown features and provides additional syntax for roles and directives typically available in reStructuredText, making it a robust choice for Sphinx-based documentation projects that prefer Markdown.
- **Installation**: `myst_parser`
- **Documentation**: [MyST-Parser on GitHub](https://github.com/executablebooks/MyST-Parser)

### Sphinx Tabs

- **Purpose**: `sphinx_tabs` is an extension for Sphinx that enables tabbed content in your documentation. This can be useful for separating content into different context-specific tabs on the same page without clutter.
- **Installation**: `sphinx_tabs`
- **Documentation**: [sphinx_tabs on GitHub](https://github.com/djungelorm/sphinx-tabs)

### PyYAML

- **Purpose**: PyYAML is a YAML parser and emitter for Python. It is used to handle YAML-formatted files within your documentation project, which can be useful for configuration files or other data-driven content.
- **Installation**: `PyYAML`
- **Documentation**: [PyYAML on PyPI](https://pypi.org/project/PyYAML/)

## Troubleshooting

### Clearing Cache

Delete your `build/` contents, or:

```powershell
make clean
```

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
