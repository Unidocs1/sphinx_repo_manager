# Sphinx Extension: Repository Manager

## About

This Sphinx extension by [Xsolla Backend (XBE)](https://docs.goxbe.io) automates the management of multiple
documentation repositories as part of building a larger, unified documentation system. It facilitates multi-threaded
cloning and updating of external repositories specified in a YAML manifest file before Sphinx builds.

![Demo (GIF)](./docs/images/clone-example.gif)

📜 See the Xsolla Backend (XBE) [source code](https://source.goxbe.io/Core/docs/xbe_static_docs)
and [demo](https://source.goxbe.io/Core/docs/xbe_static_docs) production site heavily making use of this extension.
Here, you may also find tips for how to utilize this extension to its greatest capabilities.

## Getting Started

1. Copy the `templates/repo_manifest.template.yml` to a project `docs/repo_manifest.yml`.
2. Ensure each repository listed in the manifest minimally includes a `url`.
3. Ensure the [prerequisites](#prerequisites) (below) are met, such as having a Python env with `make`.
4. Within `docs/` -> Open terminal and `make html`.

❗ If editing the manifest, delete your `docs/source/_repos-available` and `docs/source/content` dirs to wipe cache

## How it Works

1. `repo_manifest.yml` lists repositories with their respective clone URLs [and optional rules].
2. `docs/source/` creates `_repos-available` (src repos) and `content` (symlinked) dirs.
3. Upon running `sphinx-build` (commonly via `make html`), the extension either clones or updates each repo defined
   within the manifest.
4. Source clones will [sparse checkout](https://git-scm.com/docs/git-sparse-checkout) and symlink to the `content` 
   dir, allowing for flexibility such as custom entry points and custom names (such as for shorter url slugs).
5. All repos in the manifest will be organized in a monolithic doc. 

💡 If you want to store *local* content (eg, static `.rst`), add it to `source/_source_docs/`

💡 The only RST file expected for your monolithic repo is the `index.rst` file (next to your `conf.py`), which can
simply be an [include](https://docutils.sourceforge.io/docs/ref/rst/directives.html#include) or 
[toctree](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree) 
directive to your symlinked `docs/source/content/*.rst`.

⌛ 5 local workers (default) will take only ~50s to process 30 repos with default manifest settings

### Demo

If you cloned this repo (rather than just using it as a sphinx extension), see [docs/](docs) 
for a ready-to-go template! We recommend you move `docs/` to a separate repo after testing, leaving this extension 
to simply be imported.

After prerequisite setup, simply `make html` within `docs/` -> the manifest is setup to pull a sample doc repo
at [templates/](templates).

___

## Prerequisites

### Required

This guide assumes you have a basic understanding of [Sphinx](https://www.sphinx-doc.org/en/master/) and
[RST](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html)

#### Python

Ensure `Python >= 3.10` is installed

#### Unlock Max Char Paths

> **Note:**
> As a repo manager, there may be deeply-nested directories and may need to unlock the 256-char limit in some envs

With **elevated** privileges:

#### requirements.txt

Add the following:

```dotenv
# Sphinx Repo Manager by Xsolla Backend (XBE)
git+https://source.goxbe.io/Core/docs/sphinx_repo_manager.git#egg=sphinx_repo_manager
```

💡 This will later be available via [PyPi](https://pypi.org)

Then install: `pip install -r requirements.txt`

### conf.py

Add the extension (already within `docs/`):

```py
extensions = [
    "sphinx_repo_manager",  # Xsolla Backend (XBE)'s extension to manage repos via repo_manifest.yml
]
```

### Optional

#### [Optional] Auth Token

**Using a git host auth token?** Copy `docs/.env.template` -> to `docs/.env`, then minimally set `REPO_AUTH_TOKEN`.

💡 Deploying to [RTD](https://www.readthedocs.com)? Don't forget to dupe these `.env` vals to your RTD project settings!

#### [Optional] Doxygen Support

Want to build API docs from OpenAPI? We natively support that! Docs coming soon.

💡 **Can't wait?** Check out our [xbe_static_docs](https://source.goxbe.io/Core/docs/xbe_static_docs) repo for
integration examples

## Build Requirements

Build requirements for [sphinx-build](https://www.sphinx-doc.org/en/master/man/sphinx-build.html) falls outside the
scope of this guide. However, some high-level instructions follow:

* If Windows, install `make`; perhaps with [choco](https://community.chocolatey.org/packages/make)
* Remember to `pip install -r requirements.txt` within `docs/` before `make html`.
* Our [xbe_static_docs](https://source.goxbe.io/Core/docs/xbe_static_docs) repo contains containerized Docker
  examples and tooling to expand upon building.

## Tested in

- Windows 11 via PowerShell 7
- Windows 11 via WSL2 (bash)
- Ubuntu 22.04 via ReadTheDocs (RTD) CI

## License

[MIT](LICENSE)
