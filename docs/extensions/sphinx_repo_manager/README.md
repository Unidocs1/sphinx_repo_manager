# Sphinx Extension: Repository Manager

## Description

This Sphinx extension automates the management of multiple documentation repositories as part of building a larger,
unified documentation system. It facilitates the cloning and updating of external repositories specified in a YAML
manifest file, ensuring each repository is checked out to the specified tag before Sphinx documentation generation
proceeds.

## How it Works

1. The extension reads a manifest file (`repo_manifest.yml`) that lists repositories with their respective clone URLs and tags.
2. It checks if each repository is already cloned at the specified location.
3. If a repository is not found, it clones the repository from the provided URL to an initial clone path (else, it pulls updates).
4. Symlinks are created from the clone path to the base symlink path specified in the YAML (along with other symlinks, such as RELEASE_NOTES).
5. All repos in the manifest will be organized in a monolithic doc, with [`xbe_static_docs`](https://source.goxbe.io/Core/xbe_static_docs) being the core repo for static docs.

## Usage

1. Place the `repo_manifest.yml` file two levels up from this script, typically at the project root.
2. Ensure each repository listed in the manifest includes a `url` and a `tag`.
3. Optionally, specify `init_clone_path` and `base_symlink_path` in the manifest to manage where repositories are cloned and how they are accessed.
4. Include this extension in your Sphinx `conf.py` file by adding the extension's path to `sys.path` and including `'repo_manager'` in the `extensions` list.

## Requirements

- Python >= 3.8
- Sphinx = 7.3.7
- colorama >= 0.4.6

This may work with older versions, but has not been tested.

## Entry Point

See `setup(app)` definition at `sphinx_feature_flags.py`.

## Tested in

- Windows 11 via PowerShell 7
- Ubuntu 22.04 via ReadTheDocs (RTD) CI

## Notes

- `__init__.py` is required for both external pathing and to treat the directory as a pkg
