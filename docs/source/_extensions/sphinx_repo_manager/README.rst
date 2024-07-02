====================================
Sphinx Extension: Repository Manager
====================================

Description
-----------
This Sphinx extension automates the management of multiple documentation repositories as part of building a larger, unified documentation system. It facilitates the cloning and updating of external repositories specified in a YAML manifest file, ensuring each repository is checked out to the specified tag before Sphinx documentation generation proceeds.

How it Works
------------
#. The extension reads a manifest file (`repo_manifest.yml`) that lists repositories with their respective clone URLs and tags.
#. It checks if each repository is already cloned at the specified location.
#. If a repository is not found, it clones the repository from the provided URL to an initial clone path.
#. Symlinks are created from the clone path to the base symlink path specified in the YAML.
#. Regardless of the initial presence, it checks out the specified tag to align the documentation state with the desired version.

Usage
-----
#. Place the `repo_manifest.yml` file two levels up from this script, typically at the project root.
#. Ensure each repository listed in the manifest includes a `url` and a `tag`.
#. Optionally, specify `init_clone_path` and `base_symlink_path` in the manifest to manage where repositories are cloned and how they are accessed.
#. Include this extension in your Sphinx `conf.py` file by adding the extension's path to `sys.path` and including `'repo_manager'` in the `extensions` list.

Requirements
------------
- Python 3.6 or higher
- Sphinx 1.8 or higher
- PyYAML>6.0
- colorama>=0.4.5

This may work with older versions, but have not been tested.

Entry Point
-----------
The `setup(app)` function is executed during the 'builder-inited' event of Sphinx, which is triggered after Sphinx initializes but before the build process begins.

Tested in
---------
- Windows 11 via PowerShell 7
- Ubuntu 22.04 via ReadTheDocs (RTD) CI

Notes
-----
* `__init__.py` can remain empty but is necessary for Python to treat the directory as a pkg
