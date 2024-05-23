"""
repo_cleaner.py
- This migrates repos to the correct architecture for the new doc system.
- This could theoretically be used for mass repo changes (beyond just migration).
- Set constant prefs below (all True, by default).
After cleaning, check git diff to ensure the correct architecture is in place.
- Script to hook into repo_manager and git_manager tooling,
and reading the ../repo_manifest.yml file
- (!) Be sure you're using version control before running this script.
- (!) There's a lot going on here: Absolutely check git diff post-run.
- (!) This is untested against !default manifest paths.

----------------------------------------------------------------------

PREREQS:
1. Follow the prerequisites from ../README.md
2. Run `make html` at proj root, pulling prefs from repo_manifest.yml

----------------------------------------------------------------------

For each repo:
1. Wipe deprecated files that may exist at path:
    - docs
        - conf.py
        - make.bat
        - Makefile

2. Get list of remaining dir paths at the top level docs (to mv later 1 down to /source),
   with the EXCEPTION of:
    - docs
        - source
        - tools

3. Ensure dir tree at target repo path:
    - docs
        - source
            - _static
            - _templates
            - content  # Actual dir here pulled from {repo_sparse_paths}

4. If any dirs (minus the exceptions) existed from step #2 at docs/, mv 1 down (docs/source)

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

6. If !index.rst found:
    - Copy `{TEMPLATE_REPO_PATH}/docs/source/index.rst` to `docs/source/`
    - Copy `{TEMPLATE_REPO_PATH}/docs/source/content` to `docs/source/`

7. Ensures the following %PLACEHOLDERS% are replaced:
    - docs
    - README.md
        * %REPO_NAME%
    - source
        - conf.py
            * %REPO_NAME%
            * %REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH%
            * %GIT_TAG%
"""
# CUSTOMIZE ACTIONS ##################################################################
DOCS_DIR_NAME = 'docs'  # TODO: Parse from repo_manifest
DOCS_SOURCE_DIR_NAME = 'source'  # TODO: Parse from repo_manifest
DOCS_SOURCE_CONTENT_DIR_NAME = 'content'  # TODO: Parse from repo_manifest
ENSURE_DIR_TREE_IGNORED_DIRS = [  # Requires: ACTION_ENSURE_DIR_TREE_SKELETON
    'source',
    'build',
    'tools',
]
DEPRECATED_DOC_ROOT_FILES_TO_RM_REPLACED = [  # Requires: ACTION_WIPE_DEPRECATED_FILES
    'conf.py',
    'make.bat',
    'Makefile',
    '.gitignore',
    'README.md',
    'requirements.txt',
]
GIT_TAG_OVERRIDE = 'latest'  # None == We'll search for the latest ver tag [with optional regex whitelist pattern below + append optional suffix]
GIT_TAG_REGEX_PATTERN = None  # None == Grab the latest tag of any syntax # v1.2.3 == r"^v\d+\.\d+\.\d+$"`
GIT_TAG_SUFFIX = '-doc'  # If we use tag 'v1.0.0-lts' and this val is "-doc", result == "v1.0.0-lts-doc"

# ------------------------------
# Shown in order of execution >>
ACTION_WIPE_DEPRECATED_FILES = True
ACTION_ENSURE_DIR_TREE_SKELETON = True
ACTION_MV_DIRS_AND_FILES = True
ACTION_MV_DOCS_ROOT_TO_SRC_DIR = True # Requires: ACTION_MV_DIRS_AND_FILES
COPY_FILES_FROM_TEMPLATE_NO_OVERWRITE = True
CP_CONTEXT_FROM_TEMPLATE_NO_OVERWRITE = True  # Requires: COPY_FILES_FROM_TEMPLATE_REPO_IF_NOT_EXISTS
MV_EXISTING_SRC_CONTENT_INDEX_TO_SRC = True  # Requires: COPY_FILES_FROM_TEMPLATE_REPO_IF_NOT_EXISTS; if this triggers
REPLACE_PLACEHOLDERS_IN_FILES = True


# INIT ###############################################################################
from colorama import Fore, Style
from colorama import init
import logging
import re  # Regex
import os
from pathlib import Path  # Path manipulation/normalization; allows / slashes for path
import shutil  # File/path manipulation
import sys  # System-specific params/funcs

# Constants
ABS_SCRIPT_PATH = Path(__file__).resolve()
ABS_PROJECT_ROOT_PATH = ABS_SCRIPT_PATH.parent  # Assuming the script is in 'tools', and we need the parent directory

REL_MANIFEST_PATH = Path('../repo_manifest.yml')  # For logging only
ABS_MANIFEST_PATH = ABS_PROJECT_ROOT_PATH / 'repo_manifest.yml'

REL_TEMPLATE_REPO_PATH = Path('./template-doc')  # For logging only
ABS_TEMPLATE_REPO_PATH = (ABS_PROJECT_ROOT_PATH / REL_TEMPLATE_REPO_PATH).resolve()

# Add the path to the repo_manager extension
repo_manager_path = ABS_PROJECT_ROOT_PATH / 'repo_manager'
sys.path.insert(0, str(repo_manager_path))

# Add the path to the log_styles module
log_styles_path = ABS_PROJECT_ROOT_PATH / 'log_styles'
sys.path.insert(0, str(log_styles_path))

# Import the RepoManager and GitHelper from the repo_manager package
from repo_manager import RepoManager
from repo_manager import GitHelper


# Remove the spammy/redundant "INFO: " from logger
class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            self._style._fmt = "%(message)s"
        else:
            self._style._fmt = "%(levelname)s: %(message)s"
        return super().format(record)


# Create a formatter that includes color codes
class ColorFormatter(logging.Formatter):
    def format(self, record):
        level_num = record.levelno
        if level_num >= logging.ERROR:
            color = Fore.RED
        elif level_num >= logging.WARNING:
            color = Fore.YELLOW
        elif level_num >= logging.INFO:
            color = Fore.WHITE
        else:
            color = Fore.WHITE
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


# Initialize colorama
init(autoreset=True)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a console handler (for the logger)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Set the custom formatter to the handler
formatter = ColorFormatter()
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)
# /INIT ##################################################################################


def wipe_file_if_exists(path_to_file):
    """ Wipes a file at the repo path. """
    file_path = Path(path_to_file).resolve()
    if file_path.exists():
        file_path.unlink()


def ensure_dir_tree_exists(rel_tagged_repo_path):
    """ Ensures the expected dir tree is in place. """
    dirs_to_create = [
        'docs',
        'docs/source',
        'docs/source/_static',
        'docs/source/_templates',
        'docs/source/content'
    ]
    for dir_name in dirs_to_create:
        Path(rel_tagged_repo_path.resolve(), dir_name).resolve().mkdir(parents=True, exist_ok=True)


def cp_dir(src, dest, overwrite):
    """
    Copy a directory from src to dest.

    Parameters:
    - src: Source directory path.
    - dest: Destination directory path.
    - overwrite: If True, overwrite existing files. If False, do not overwrite existing files.
    """
    src_path = Path(src)
    dest_path = Path(dest)

    if overwrite:
        # Copy the entire directory tree and overwrite existing files
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
    else:
        # Walk through the source directory
        for root, dirs, files in os.walk(src_path):
            for file_name in files:
                src_file = Path(root) / file_name
                relative_path = src_file.relative_to(src_path)
                dest_file = dest_path / relative_path

                # If the destination file does not exist, copy the file
                if not dest_file.exists():
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dest_file)


def mv_existing_docs_src_content_index_up_one(
        rel_tagged_repo_docs_source_content_path,
        rel_tagged_repo_docs_source_path
):
    """
    Check for existing docs/source/content/index.rst.
    - if exists, mv it +1 to docs/source
    - else, copy from template
    """
    abs_tagged_repo_docs_source_content_path = Path(rel_tagged_repo_docs_source_content_path).resolve()
    abs_tagged_repo_docs_source_path = Path(rel_tagged_repo_docs_source_path).resolve()
    content_index_rst_path = abs_tagged_repo_docs_source_content_path / 'index.rst'

    # Check for an old index.rst @ docs/source/content
    if content_index_rst_path.is_file():
        if MV_EXISTING_SRC_CONTENT_INDEX_TO_SRC:
            logger.info("💡 Found existing 'docs/source/content/index.rst' to be moved +1 up")

            # Remove placeholder index.rst @ docs/source (before moving the docs/source/content one)
            target_index_rst_path = abs_tagged_repo_docs_source_path / 'index.rst'
            if target_index_rst_path.is_file():
                target_index_rst_path.unlink()  # Delete

            # Move docs/source/content/index.rst to docs/source/
            shutil.move(
                str(content_index_rst_path),
                str(abs_tagged_repo_docs_source_path / 'index.rst'))


def get_git_tag_for_confpy_release_var_placeholder_swap(rel_tagged_repo_docs_path):
    """  """
    if GIT_TAG_OVERRIDE:
        return GIT_TAG_OVERRIDE

    latest_git_tag = GitHelper.git_get_latest_tag_ver(rel_tagged_repo_docs_path, GIT_TAG_REGEX_PATTERN)
    logger.info(f"- 🏷️ | Latest git tag: {latest_git_tag}")

    # Add the hard-coded GIT_TAG_SUFFIX const and fallback to '' if no tag
    latest_git_tag_with_suffix = f"{latest_git_tag}{GIT_TAG_SUFFIX}" if latest_git_tag else ''
    return latest_git_tag_with_suffix


def replace_placeholders(
        repo_name,
        rel_tagged_repo_docs_path,
        rel_tagged_repo_docs_source_path
):
    """
    Ensures the following %PLACEHOLDERS% are replaced in files:
    - docs
    - README.md
        * %REPO_NAME%
    - source
        - conf.py
            * %REPO_NAME%
            * %REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH%
            * %GIT_TAG%
    """
    repo_name_dashed = repo_name.replace('_', '-')

    # ------------------------------
    # docs/README.md:
    # - Replace %REPO_NAME%
    readme_path = (Path(rel_tagged_repo_docs_path).resolve() / 'README.md').resolve()

    # Validate
    if not readme_path.exists():
        logger.info(f'README.md not found: {readme_path}')
        return

    # Read the file content -> Replace %REPO_NAME% in the file README.md -> Write back
    content = readme_path.read_text(encoding='utf-8')
    new_content = re.sub(r'%REPO_NAME%', repo_name, content)
    readme_path.write_text(new_content, encoding='utf-8')

    # ------------------------------
    # docs/source/conf.py
    # - Replace %REPO_NAME%
    # - Replace %REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH%
    # - Replace %GIT_TAG%
    conf_path = (Path(rel_tagged_repo_docs_source_path).resolve() / 'conf.py').resolve()

    # Validate
    if not conf_path.exists():
        logger.info(f'conf.py not found: {conf_path}')
        return

    # Read the file content -> Replace %PLACEHOLDERS%
    content = conf_path.read_text(encoding='utf-8')
    new_content = re.sub(r'%REPO_NAME%', repo_name, content)
    new_content = re.sub(r'%REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH%', repo_name_dashed, new_content)

    # Find the latest tag with regex filter -- then apply an optional suffix
    release_tag = get_git_tag_for_confpy_release_var_placeholder_swap(rel_tagged_repo_docs_path)
    new_content = re.sub(r'%GIT_TAG%', release_tag, new_content)

    conf_path.write_text(new_content, encoding='utf-8')


def wipe_deprecated_files(repo_path):
    """ Wipe deprecated files at the repo path; we'll likely replace them from template. """
    for file in DEPRECATED_DOC_ROOT_FILES_TO_RM_REPLACED:
        wipe_file_if_exists(Path(repo_path).resolve() / file)


def mv_sphinx_dirs_and_files(src_paths, dst_dir):
    """
    Move multiple dirs and/or files to a single destination dir using shutil.

    Only moves files ending with .rst or dirs containing .rst files.
    """
    for src_path in src_paths:
        # Check if the path is a file and ends with .rst
        if src_path.is_file() and src_path.suffix == '.rst':
            dst_path = Path(dst_dir) / src_path.name
            shutil.move(str(src_path), str(dst_path))
        elif src_path.is_dir():  # Check if the path is a directory
            # Check if the dir contains any .rst files
            contains_rst = any(f.suffix == '.rst' for f in src_path.rglob('*') if f.is_file())
            if contains_rst:
                dst_path = Path(dst_dir) / src_path.name
                shutil.move(str(src_path), str(dst_path))


def clean_repo(
        repo_name,
        rel_tagged_repo_path,
        rel_tagged_repo_docs_path,
        rel_tagged_repo_docs_source_path,
        rel_tagged_repo_docs_source_content_path,
):
    """
    Cleans and normalizes expected per-repo consistency.
    - repo_name | eg: 'account_services'
    - rel_tagged_repo_path | 'source/_repos-available/{tagged_repo_name}
        - If !tag, {tagged_repo_name} eg: 'source/_repos-available/account_services--master'
        - If tag, {tagged_repo_name} eg: 'source/_repos-available/account_services-1.0.0'
    - rel_tagged_repo_docs_path | 'source/_repos-available/{tagged_repo_name}/{DOCS_DIR_NAME}'
    - rel_tagged_repo_docs_source_path | eg: 'source/_repos-available/{tagged_repo_name}/{DOCS_DIR_NAME}/{DOCS_SOURCE_DIR_NAME}'
    - rel_tagged_repo_docs_source_content_path | 'source/_repos-available/{tagged_repo_name}/{DOCS_DIR_NAME}/{DOCS_SOURCE_DIR_NAME}/{DOCS_SOURCE_CONTENT_DIR_NAME}'
    """
    # --------------------------------------
    if ACTION_WIPE_DEPRECATED_FILES:
        logger.info(f'{Fore.YELLOW}[wipe_deprecated_files]{Fore.RESET}\n'
                    f"- rel_tagged_repo_docs_path: '{rel_tagged_repo_docs_path}'")
        wipe_deprecated_files(rel_tagged_repo_docs_path)

    # --------------------------------------
    # Get list of remaining files+dir paths at the top level docs (to mv later 1 down to /source/content),
    # ensuring we exclude [ source, tools ]
    if ACTION_ENSURE_DIR_TREE_SKELETON:
        logger.info(f'{Fore.YELLOW}[ensure_dir_tree_exists]{Fore.RESET}\n'
                    f"- rel_tagged_repo_path: '{rel_tagged_repo_path}'")
        files_or_dirs_before_ensure_dir_tree = [
            item for item in Path(rel_tagged_repo_docs_path).iterdir()
            if item.name not in ENSURE_DIR_TREE_IGNORED_DIRS
        ]

        ensure_dir_tree_exists(rel_tagged_repo_path)  # /docs, itself, may not even exist yet

        # --------------------------------------
        # Move dirs_before_ensure_dir_tree 1 down to /source/content
        if ACTION_MV_DOCS_ROOT_TO_SRC_DIR:
            logger.info(f'{Fore.YELLOW}[dirs_before_ensure_dir_tree]{Fore.RESET}\n'
                        f'- {files_or_dirs_before_ensure_dir_tree}')
            if files_or_dirs_before_ensure_dir_tree:
                mv_sphinx_dirs_and_files(
                    files_or_dirs_before_ensure_dir_tree,
                    rel_tagged_repo_docs_source_content_path)

    # --------------------------------------
    # Copy TEMPLATE_REPO_PATH/* to rel_tagged_repo_path/ for whatever is missing (!overwrite)
    if COPY_FILES_FROM_TEMPLATE_NO_OVERWRITE:
        logger.info(f'{Fore.YELLOW}[Copy TEMPLATE_REPO_PATH/* to rel_tagged_repo_path/]{Fore.RESET}\n'
                    f"- From: '{REL_TEMPLATE_REPO_PATH}'\n"
                    f"- To: '{rel_tagged_repo_path}'")

        cp_dir(
            ABS_TEMPLATE_REPO_PATH,
            rel_tagged_repo_path,
            overwrite=False)

    # --------------------------------------
    # If there's an existing index.rst @ docs/source/content,
    # rm placeholder there, then mv +1 to docs/source
    logger.info(f'{Fore.YELLOW}[mv_existing_index_rst_to_docs_src_if_exists_else_copy_from_template]{Fore.RESET}\n'
                f"- rel_tagged_repo_docs_source_content_path: '{rel_tagged_repo_docs_source_content_path}'\n"
                f"- rel_tagged_repo_docs_source_path: '{rel_tagged_repo_docs_source_path}'")

    mv_existing_docs_src_content_index_up_one(
        rel_tagged_repo_docs_source_content_path,
        rel_tagged_repo_docs_source_path)

    # --------------------------------------
    if REPLACE_PLACEHOLDERS_IN_FILES:
        logger.info(f'{Fore.YELLOW}[replace_placeholders]{Fore.RESET}\n'
                    f"- repo_name: '{repo_name}'\n"
                    f"- rel_tagged_repo_docs_path: '{rel_tagged_repo_docs_path}'\n"
                    f"- rel_tagged_repo_docs_source_path: '{rel_tagged_repo_docs_source_path}'")
        replace_placeholders(
            repo_name,
            rel_tagged_repo_docs_path,
            rel_tagged_repo_docs_source_path)


def main():
    """ Read manifest -> iterate repos to clean. """
    print()
    print(f'{Fore.LIGHTGREEN_EX}== repo_cleaner =={Fore.RESET}')

    # Ensure template path exists
    if not ABS_TEMPLATE_REPO_PATH.exists():
        raise FileNotFoundError(f"Template path not found: {ABS_TEMPLATE_REPO_PATH}")

    # Initialize the RepoManager with the path to the manifest file
    logger.info(f"📖 | Attempting to read manifest: '{REL_MANIFEST_PATH}' ...")
    manager = RepoManager(REL_MANIFEST_PATH)
    manifest = manager.read_manifest()

    # +1 up to proj root since we're in /tools
    rel_init_clone_path = (Path('..') / manifest.get('init_clone_path', 'source/_repos-available'))

    repositories = manifest.get('repositories', {}).items()
    if not repositories:
        logger.info("No repositories found in manifest.")
        return

    # Process each repository
    process_repositories(repositories, rel_init_clone_path)

    print(f"-------------------")
    print(f"{Fore.GREEN}✅ | ALL JOBS DONE.{Fore.RESET}")
    print()


def process_repositories(repositories, rel_init_clone_path):
    """ Process each repository defined in the manifest. """
    num_repos = len(repositories)
    for repo_i, (repo_name, repo_data) in enumerate(repositories, start=1):
        # Prep expected repo name, different based on branch or tag with some normalizations
        normalized_branch = (repo_data.get('branch', 'master')
                             .replace('/', '--')
                             .replace(' ', '-'))
        tag = repo_data.get('tag', None)

        # If tag, dir name == "{repo_name}-{tag}"
        # If no tag, dir name == "{repo_name}--{normalized_branch}"
        tagged_repo_dir_name = f"{repo_name}--{normalized_branch}" if not tag else f"{repo_name}-{tag}"
        rel_tagged_repo_path = rel_init_clone_path / tagged_repo_dir_name

        if not rel_tagged_repo_path.exists():
            logger.info(f"Repo path not found: {rel_tagged_repo_path}")
            continue

        # "{repo_path}/{TOP_DOCS_DIR_NAME}"
        rel_tagged_repo_docs_path = (rel_tagged_repo_path / DOCS_DIR_NAME)
        rel_tagged_repo_docs_source_path = (rel_tagged_repo_docs_path / DOCS_SOURCE_DIR_NAME)
        rel_tagged_repo_docs_source_content_path = (rel_tagged_repo_docs_source_path / DOCS_SOURCE_CONTENT_DIR_NAME)

        repo_i_of_max = f"{repo_i}/{num_repos}"
        print()
        logger.info(f"{Fore.CYAN}CLEANING REPO ({repo_i_of_max}): '{repo_name}' "
                    f"@ '{rel_tagged_repo_docs_path}'{Fore.RESET}")
        clean_repo(
            repo_name,
            rel_tagged_repo_path,
            rel_tagged_repo_docs_path,
            rel_tagged_repo_docs_source_path,
            rel_tagged_repo_docs_source_content_path)
        print(f'{Fore.GREEN}🧹 | Finished Repo Clean.{Fore.RESET}')


# ENTRY POINT
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Process optional argument if needed
        arg = sys.argv[1]
        # Use the argument as needed, for example:
        logger.info(f"Optional argument provided: {arg}")

    try:
        main()
    except Exception as e:
        # For paths, convert double backslashes to single forward slashes
        normalized_e = str(e).replace('\\\\', '/')
        logger.error(normalized_e)  # "ERROR: {normalized_e}" (in red)
        print()
        sys.exit(1)
