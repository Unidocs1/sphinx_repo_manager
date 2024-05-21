"""
repo_cleaner.py
- This migrates repos to the correct architecture for the new doc system.
After cleaning, check git diff to ensure the correct architecture is in place.
- Script to hook into repo_manager and git_manager tooling,
and reading the ../repo_manifest.yml file
- (!) Be sure you're using version control before running this script.
- (!) There's a lot going on here: Absolutely check git diff post-run.
- (!) This is untested against !default manifest paths.

----------------------------------------------------------------------

PREREQS:
1. Follow the prerequisites from ../README.md
1. Run `make html` at proj root, pulling prefs from repo_manifest.yml

----------------------------------------------------------------------

For each repo:
1. Wipe deprecated files that may exist at path:
    - docs
        - conf.py
        - make.bat
        - Makefile

2. Get list of remaining dir paths at the top level docs (to mv later 1 down to /source)

3. Ensure dir tree at target repo path:
    - docs
        - source
            - _static
            - _templates
            - content  # Actual dir here pulled from {repo_sparse_paths}

4. If any dirs existed from step #2 at docs/, mv 1 down (docs/source)

3. Copy from TEMPLATE_REPO_PATH (overwriting, if exists; but keep existing "content"):
    - docs
        - .gitignore
        - make.bat
        - Makefile
        - README.md
        - requirements.txt
        - source
            - _static
                - images
                  - _images go here
            - _static content goes here
            - _templates
            - content  # Actual dir here pulled from {base_symlink_path}
            - conf.py

4. Check for the 1st index.rst found at the following dirs (that may or may not exist):
    - docs
        - content

5. If index.rst found, ensure it's +1 up from repo_sparse_paths; eg: "docs/source/index.rst" (mv, if not there)

6. Ensures the following %PLACEHOLDERS% are replaced:
    - docs
    - README.md
        * %REPO_NAME%
    - source
        - conf.py
            * %REPO_NAME%
            * %REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH%
"""

import os
import re  # Regex
from pathlib import Path  # Path manipulation
import shutil  # File/path manipulation
import sys
# import yaml

# Add the path to the repo_manager extension
repo_manager_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './repo_manager'))
sys.path.insert(0, repo_manager_path)

# Import the RepoManager and GitHelper from the repo_manager package
from repo_manager import RepoManager
# from repo_manager import GitHelper

TOP_DOCS_DIR_NAME = 'docs'  # TODO: Parse from repo_manifest
TOP_DOCS_SOURCE_DIR_NAME = 'source'  # TODO: Parse from repo_manifest
TEMPLATE_REPO_PATH = os.path.normpath('./template-doc')
MANIFEST_PATH = '../repo_manifest.yml'
ABS_MANIFEST_PATH = os.path.normpath(
    os.path.abspath(MANIFEST_PATH))


def wipe_file_if_exists(path_to_file):
    """ Wipes a file at the repo path. """
    if os.path.exists(path_to_file):
        os.remove(path_to_file)


def ensure_dir_tree_exists(rel_tagged_repo_path):
    """ Ensures the expected dir tree is in place. """
    for dir_name in [
        'docs',
        'docs/source',
        'docs/source/_static',
        'docs/source/_templates',
        'docs/source/content'
    ]:
        os.makedirs(os.path.join(rel_tagged_repo_path, dir_name), exist_ok=True)


def mv_existing_index_rst_to_docs_src_if_exists_else_copy_from_template(
        rel_tagged_repo_docs_path,
        rel_tagged_repo_docs_source_path
):
    """ Check for index.rst -- if exists, mv to docs/source; else, copy from template. """
    for root, _, files in os.walk(rel_tagged_repo_docs_path):
        for file in files:
            if file == 'index.rst':
                # Move to docs/source
                src_index_rst_path = os.path.normpath(os.path.join(
                    root, file))
                dst_index_rst_path = os.path.normpath(os.path.join(
                    rel_tagged_repo_docs_source_path, file))

                os.system(f"mv {src_index_rst_path} {dst_index_rst_path}")
                return

    # Copy from template
    index_rst_template_path = os.path.normpath(os.path.join(
        TEMPLATE_REPO_PATH, 'docs/source/index.rst'))
    index_rst_path = os.path.normpath(os.path.join(
        rel_tagged_repo_docs_source_path, 'index.rst'))
    os.system(f"cp {index_rst_template_path} {index_rst_path}")


def replace_placeholders(
        repo_name,
        rel_tagged_repo_docs_path,
        rel_tagged_repo_docs_source_path):
    """
    Ensures the following %PLACEHOLDERS% are replaced at files:
    - docs
    - README.md
        * %REPO_NAME%
    - source
        - conf.py
            * %REPO_NAME%
            * %REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH%
    ------------------------
    - repo_name | eg: 'account_services'
    - rel_tagged_repo_docs_path | eg: 'source/_repos-available/{tagged_repo_name}/{TOP_DOCS_DIR_NAME}'
    - rel_tagged_repo_docs_source_path | eg: 'source/_repos-available/{tagged_repo_name}/{TOP_DOCS_DIR_NAME}/{TOP_DOCS_SOURCE_DIR_NAME}'
    """
    repo_name_dashed = repo_name.replace('_', '-')

    # Replace %REPO_NAME% @ docs/README.md
    readme_path = Path(rel_tagged_repo_docs_path) / 'README.md'

    # Validate
    if not readme_path.exists():
        print(f"README.md not found: {readme_path}")
        return

    # Read the file content -> Replace %REPO_NAME% in the file README.md -> Write back
    content = readme_path.read_text()
    new_content = re.sub(r"%REPO_NAME%", repo_name_dashed, content)
    readme_path.write_text(new_content)

    # ------------------------------
    # Replace %REPO_NAME% in conf.py
    conf_path = Path(rel_tagged_repo_docs_source_path) / 'conf.py'

    # Validate
    if not conf_path.exists():
        print(f"conf.py not found: {conf_path}")
        return

    # Read the file content -> Replace %REPO_NAME% in the file conf.py -> Write back
    content = conf_path.read_text()
    new_content = re.sub(r"%REPO_NAME%", repo_name, content)
    conf_path.write_text(new_content)

    # ------------------------------
    # Replace %REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH% in conf.py
    # Read the file content -> Replace %REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH% in the file conf.py -> Write back
    content = conf_path.read_text()
    new_content = re.sub(r"%REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH%", repo_name_dashed, content)
    conf_path.write_text(new_content)


def wipe_deprecated_files(repo_path):
    """ Wipe deprecated files at the repo path. """
    for file in [
        'conf.py',
        'make.bat',
        'Makefile',
    ]:
        wipe_file_if_exists(os.path.join(repo_path, file))


def mv_dirs(src_dirs, single_dst):
    """ Move multiple dirs to a single destination using shutils. """
    for src_dir in src_dirs:
        src_dir_path = os.path.normpath(os.path.join(
            single_dst, src_dir))
        shutil.move(src_dir_path, single_dst)


def clean_repo(
        repo_name,
        rel_tagged_repo_path,
        rel_tagged_repo_docs_path,
        rel_tagged_repo_docs_source_path
):
    """
    Cleans and normalizes expected per-repo consistency.
    - repo_name | eg: 'account_services'
    - rel_tagged_repo_path | eg: 'source/_repos-available/{tagged_repo_name}
        - If !tag, {tagged_repo_name} eg: 'source/_repos-available/account_services--master'
        - If tag, {tagged_repo_name} eg: 'source/_repos-available/account_services-1.0.0'
    - rel_tagged_repo_docs_path | eg: 'source/_repos-available/{tagged_repo_name}/{TOP_DOCS_DIR_NAME}'
    - rel_tagged_repo_docs_source_path | eg: 'source/_repos-available/{tagged_repo_name}/{TOP_DOCS_DIR_NAME}/{TOP_DOCS_SOURCE_DIR_NAME}'
    """
    print(f"Cleaning repo: '{repo_name}' @ '{rel_tagged_repo_docs_path}'")
    wipe_deprecated_files(rel_tagged_repo_docs_path)

    # Get list of remaining dir paths at the top level docs (to mv later 1 down to /source)
    dirs_before_ensure_dir_tree = os.listdir(rel_tagged_repo_docs_path)
    ensure_dir_tree_exists(rel_tagged_repo_path)  # /docs, itself, may not even exist

    # Mv dirs_before_ensure_dir_tree -1 down to /source
    if dirs_before_ensure_dir_tree:
        mv_dirs(dirs_before_ensure_dir_tree, rel_tagged_repo_docs_source_path)

    # Copy TEMPLATE_REPO_PATH/* to rel_tagged_repo_path/
    shutil.copytree(TEMPLATE_REPO_PATH, rel_tagged_repo_path, dirs_exist_ok=True)

    # If there's an existing index.rst, mv it -1 to /source
    # Else, copy from template to /source
    mv_existing_index_rst_to_docs_src_if_exists_else_copy_from_template(
        rel_tagged_repo_docs_path, rel_tagged_repo_docs_source_path)

    replace_placeholders(
        repo_name,
        rel_tagged_repo_docs_path,
        rel_tagged_repo_docs_source_path)


def main():
    """ Read manifest -> iterate repos to clean. """
    print(f"[repo_cleaner@main] Reading manifest: {ABS_MANIFEST_PATH}")
    # Ensure template path exists
    if not os.path.exists(TEMPLATE_REPO_PATH):
        raise FileNotFoundError(f"Template path not found: {TEMPLATE_REPO_PATH}")

    # Initialize the RepoManager with the path to the manifest file
    manager = RepoManager(ABS_MANIFEST_PATH)
    manifest = manager.read_manifest()

    # +1 up to proj root since we're in /tools
    init_clone_path = os.path.normpath(os.path.join(
        '..', manifest.get('init_clone_path', 'source/_repos-available')))

    repositories = manifest.get('repositories', {}).items()
    if not repositories:
        print("No repositories found in manifest.")
        return

    # For each repo, clean it up
    for repo_name, repo_data in repositories:
        normalized_branch = (repo_data.get('branch', 'master')
                             .replace('/', '--')
                             .replace(' ', '-'))
        tag = repo_data.get('tag', None)

        # If tag, dir name == "{repo_name}-{tag}"
        # If no tag, dir name == "{repo_name}--{normalized_branch}"
        tagged_repo_dir_name = f"{repo_name}--{normalized_branch}" if not tag else f"{repo_name}-{tag}"
        rel_tagged_repo_path = os.path.normpath(os.path.join(
            init_clone_path, tagged_repo_dir_name))

        if not os.path.exists(rel_tagged_repo_path):
            print(f"Repo path not found: {rel_tagged_repo_path}")
            continue

        # "{repo_path}/{TOP_DOCS_DIR_NAME}"
        rel_tagged_repo_docs_path = os.path.normpath(os.path.join(
            rel_tagged_repo_path, TOP_DOCS_DIR_NAME))

        rel_tagged_repo_docs_source_path = os.path.normpath(os.path.join(
            rel_tagged_repo_docs_path, TOP_DOCS_SOURCE_DIR_NAME))

        clean_repo(
            repo_name,
            rel_tagged_repo_path,
            rel_tagged_repo_docs_path,
            rel_tagged_repo_docs_source_path)


# ENTRY POINT
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tool_template.py  # Looks for `../repo_manifest.yml`")
        sys.exit(1)

    # TODO: If you accept args, grab it from `sys.argv[i]`
    main()
