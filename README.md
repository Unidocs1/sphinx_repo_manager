# Sphinx Extension: Repository Manager

<!-- Badges go here on the same line; PyPi doesn't support `\` or single-multi-line (it'll stack vertically) -->
[![PyPI](https://img.shields.io/pypi/v/sphinx-repo-manager)](https://pypi.org/project/sphinx-repo-manager/) [![PyPI - License](https://img.shields.io/pypi/l/sphinx-repo-manager)](https://opensource.org/licenses/MIT)

## About

This Sphinx extension by [Xsolla Backend [XBE]](https://docs.goxbe.io) automates the management of multiple
documentation repositories as part of building a larger, unified documentation system. It facilitates multithreaded
cloning and updating of external repositories specified in a YAML manifest file before Sphinx builds.

![Demo (GIF)](https://source.goxbe.io/Core/docs/sphinx_repo_manager/-/raw/master/docs/images/clone-example.gif)

📜 See the XBE [docgen source code](https://source.goxbe.io/Core/docs/xbe_static_docs)
and [demo](https://docs.goxbe.io) doc production site heavily making use of this extension.
Here, you may also find tips for how to utilize this extension to its greatest capabilities.

[See how it works](#how-it-works) or quickstart below >>

## Installation

This guide assumes you have a basic understanding of [Sphinx](https://www.sphinx-doc.org/en/master/) and
[RST](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html)

### Add to Existing Project

1. Install the extension [via pip](https://pypi.org/project/sphinx-repo-manager):

   ```bash
    pip install sphinx-repo-manager
   ```

2. Add extension to your project's
   [docs/source/conf.py](https://source.goxbe.io/Core/docs/sphinx_repo_manager/-/blob/master/docs/source/conf.py)
   (example template):

   ```python
   extensions = [ "sphinx_repo_manager" ] ,  # https://pypi.org/project/sphinx-repo-manager
   ```

3. Ensure a `docs/.env` file exists next to your `Makefile` -> set `REPO_AUTH_TOKEN=`

4. Create a 
   [docs/repo_manifest.yml](https://source.goxbe.io/Core/docs/sphinx_repo_manager/-/blob/master/docs/repo_manifest.yml)
   (example template) next to your `Makefile`

Once setup, sphinx-build as normal (typically via `make html` next to your `Makefile`)!

### Tips
- For Windows users, you may want to unlock your max char paths (admin):

  ```powershell
  Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled"
  ```

- Editing the manifest?
   - Consider purging your `docs/source/_repos-available` and `docs/source/content` dirs
- Looking to speedily build without checking for repo updates?
   - Temporarily set manifest `enable_repo_manager_local: false`

___

## Demos

### Minimal Demo

1. Clone the [source repo](https://source.goxbe.io/Core/docs/sphinx_repo_manager) for a demo:

- Minimal build architecture begins at at `docs/`
- `repo_manifest.yml` contains a minimal [demo_doc](https://source.goxbe.io/Core/docs/demo_doc) repo to be cloned

### Production Demo

Alternately, see `sphinx_repo_manager` used by Xsolla Backend at a production-grade level:

- [Source Code](https://source.goxbe.io/Core/docs/xbe_static_docs)
- [Production Site](https://docs.goxbe.io)

___

## How it Works

1. `repo_manifest.yml` lists repositories with their respective clone URLs [and optional rules].
2. `docs/source/` creates `_repos-available` (src repos) and `content` (symlinked) dirs.
3. Upon running `sphinx-build` (commonly via `make html`), the extension either clones or updates each repo defined
   within the manifest.
4. Source clones will [sparse checkout](https://git-scm.com/docs/git-sparse-checkout) and symlink to the `content`
   dir, allowing for flexibility such as custom entry points and custom names (such as for shorter url slugs).
5. All repos in the manifest will be organized in a monolithic doc.

💡 If you want to store *local* content (eg, static `.rst`), add it to `source/_source-docs/`

💡 The only RST file expected for your monolithic repo is the `index.rst` file (next to your `conf.py`)

⌛ 5 local workers (default) will take only ~50s to process 30 repos with default manifest settings

## Tests

Confirmed compatability with:

- Windows 11 via PowerShell 7, WSL2 (bash)
- Ubuntu 22.04 via ReadTheDocs (RTD) CI, Docker Desktop
- Python 3.10, 3.12
- Sphinx 7.3.7, 8.1.3

## Questions?

Join the Xsolla Backend official [Discord guild](https://discord.gg/XsollaBackend)!

## License

[MIT](LICENSE)
