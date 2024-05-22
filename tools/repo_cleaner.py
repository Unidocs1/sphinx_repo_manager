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
"""
# INIT ###############################################################################
from colorama import Fore, Style
from colorama import init
import logging
import re  # Regex
from pathlib import Path  # Path manipulation/normalization; allows / slashes for path
import shutil  # File/path manipulation
import sys  # System-specific params/funcs

# Constants
ABS_SCRIPT_PATH = Path(__file__).resolve()
ABS_PROJECT_ROOT_PATH = ABS_SCRIPT_PATH.parent  # Assuming the script is in 'tools', and we need the parent directory

REL_MANIFEST_PATH = Path('../repo_manifest.yml')  # For logging only
ABS_MANIFEST_PATH = ABS_PROJECT_ROOT_PATH / 'repo_manifest.yml'

DOCS_DIR_NAME = 'docs'  # TODO: Parse from repo_manifest
DOCS_SOURCE_DIR_NAME = 'source'  # TODO: Parse from repo_manifest
DOCS_SOURCE_CONTENT_DIR_NAME = 'content'  # TODO: Parse from repo_manifest

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


def mv_existing_index_rst_to_docs_src_if_exists(
        rel_tagged_repo_docs_source_content_path,
        rel_tagged_repo_docs_source_path
):
    """ Check for docs/source/content/index.rst -- if exists, mv docs/source; else, copy from template. """
    abs_tagged_repo_docs_source_content_path = Path(rel_tagged_repo_docs_source_content_path).resolve()
    abs_tagged_repo_docs_source_path = Path(rel_tagged_repo_docs_source_path).resolve()

    # Check for index.rst @ docs/source/content
    index_rst_path = abs_tagged_repo_docs_source_content_path / 'index.rst'
    if index_rst_path.is_file():
        # Remove existing index.rst in the target location if it exists
        target_index_rst_path = abs_tagged_repo_docs_source_path / 'index.rst'
        if target_index_rst_path.is_file():
            target_index_rst_path.unlink()

        # Move index.rst to docs/source
        shutil.move(str(index_rst_path), str(abs_tagged_repo_docs_source_path / 'index.rst'))
        return

    # Copy index.rst from template to docs/source
    index_rst_template_path = ABS_TEMPLATE_REPO_PATH / 'docs/source/index.rst'
    shutil.copy2(
        str(index_rst_template_path),
        str(abs_tagged_repo_docs_source_path / 'index.rst'))

    # Copy content dir (itself) from template to docs/source
    content_template_path = ABS_TEMPLATE_REPO_PATH / 'docs/source/content'
    shutil.copytree(
        content_template_path,
        abs_tagged_repo_docs_source_path / 'content',
        dirs_exist_ok=True)


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
    """
    repo_name_dashed = repo_name.replace('_', '-')

    # Replace %REPO_NAME% @ docs/README.md
    readme_path = (Path(rel_tagged_repo_docs_path).resolve() / 'README.md').resolve()

    # Validate
    if not readme_path.exists():
        logger.info(f"README.md not found: {readme_path}")
        return

    # Read the file content -> Replace %REPO_NAME% in the file README.md -> Write back
    content = readme_path.read_text(encoding='utf-8')
    new_content = re.sub(r"%REPO_NAME%", repo_name_dashed, content)
    readme_path.write_text(new_content, encoding='utf-8')

    # ------------------------------
    # Replace %REPO_NAME% in conf.py
    conf_path = (Path(rel_tagged_repo_docs_source_path).resolve() / 'conf.py').resolve()

    # Validate
    if not conf_path.exists():
        logger.info(f"conf.py not found: {conf_path}")
        return

    # Read the file content -> Replace %REPO_NAME% in the file conf.py -> Write back
    content = conf_path.read_text(encoding='utf-8')
    new_content = re.sub(r"%REPO_NAME%", repo_name, content)
    conf_path.write_text(new_content, encoding='utf-8')

    # ------------------------------
    # Replace %REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH% in conf.py
    # Read the file content -> Replace %REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH% in the file conf.py -> Write back
    content = conf_path.read_text(encoding='utf-8')
    new_content = re.sub(r"%REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH%", repo_name_dashed, content)
    conf_path.write_text(new_content, encoding='utf-8')


def wipe_deprecated_files(repo_path):
    """ Wipe deprecated files at the repo path. """
    deprecated_files = [
        'conf.py',
        'make.bat',
        'Makefile',
    ]
    for file in deprecated_files:
        wipe_file_if_exists(Path(repo_path).resolve() / file)


def mv_dirs_and_files(src_paths, dst_dir):
    """ Move multiple directories and/or files to a single destination directory using shutil. """
    for src_path in src_paths:
        dst_path = Path(dst_dir) / src_path.name
        shutil.move(str(src_path), str(dst_path))


def copytree_no_overwrite(src, dst):
    """
    Recursively copy a directory tree from src to dst, without overwriting existing files.
    """
    src = Path(src)
    dst = Path(dst)
    if not dst.exists():
        dst.mkdir(parents=True)
    for item in src.iterdir():
        s = src / item.name
        d = dst / item.name
        if s.is_dir():
            copytree_no_overwrite(s, d)
        else:
            if not d.exists():
                shutil.copy2(s, d)


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
    logger.info(f'{Fore.YELLOW}[wipe_deprecated_files]{Fore.RESET}\n'
                f"- rel_tagged_repo_docs_path: '{rel_tagged_repo_docs_path}'")
    wipe_deprecated_files(rel_tagged_repo_docs_path)

    # --------------------------------------
    # Get list of remaining files+dir paths at the top level docs (to mv later 1 down to /source/content),
    # ensuring we exclude [ source, tools ]
    logger.info(f'{Fore.YELLOW}[ensure_dir_tree_exists]{Fore.RESET}\n'
                f"- rel_tagged_repo_path: '{rel_tagged_repo_path}'")
    files_or_dirs_before_ensure_dir_tree = [
        item for item in Path(rel_tagged_repo_docs_path).iterdir()
        if item.name not in ['source', 'tools']
    ]

    ensure_dir_tree_exists(rel_tagged_repo_path)  # /docs, itself, may not even exist yet

    # --------------------------------------
    # Move dirs_before_ensure_dir_tree 1 down to /source/content
    logger.info(f'{Fore.YELLOW}[dirs_before_ensure_dir_tree]{Fore.RESET} {files_or_dirs_before_ensure_dir_tree}')
    if files_or_dirs_before_ensure_dir_tree:
        mv_dirs_and_files(
            files_or_dirs_before_ensure_dir_tree,
            rel_tagged_repo_docs_source_content_path)

    # --------------------------------------
    # Copy TEMPLATE_REPO_PATH/* to rel_tagged_repo_path/
    logger.info(f'{Fore.YELLOW}[Copy TEMPLATE_REPO_PATH/* to rel_tagged_repo_path/]{Fore.RESET}\n'
                f"- From: '{REL_TEMPLATE_REPO_PATH}'\n"
                f"- To: '{rel_tagged_repo_path}'")

    copytree_no_overwrite(ABS_TEMPLATE_REPO_PATH, rel_tagged_repo_path)

    # --------------------------------------
    # If there's an existing index.rst @ docs/source/content,
    # rm placeholder there, then mv +1 to docs/source
    logger.info(f'{Fore.YELLOW}[mv_existing_index_rst_to_docs_src_if_exists_else_copy_from_template]{Fore.RESET}\n'
                f"- rel_tagged_repo_docs_path: '{rel_tagged_repo_docs_path}'\n"
                f"- rel_tagged_repo_docs_source_path: '{rel_tagged_repo_docs_source_path}'")

    mv_existing_index_rst_to_docs_src_if_exists(
        rel_tagged_repo_docs_source_content_path, rel_tagged_repo_docs_source_path)

    # --------------------------------------
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
