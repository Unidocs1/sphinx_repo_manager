"""
Script to hook into sphinx_repo_manager and git_manager tooling,
and reading the ../repo_manifest.yml file
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
REL_PROJECT_ROOT_PATH = Path(__file__).parent  # .resolve() turns into abs path
REL_MANIFEST_PATH = Path('../repo_manifest.yml')
ABS_MANIFEST_PATH = REL_PROJECT_ROOT_PATH.parent / REL_MANIFEST_PATH

# Add the path to the sphinx_repo_manager extension
repo_manager_path = REL_PROJECT_ROOT_PATH / 'sphinx_repo_manager'
sys.path.insert(0, str(repo_manager_path))

# Import the RepoManager and GitHelper from the sphinx_repo_manager package
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
        levelno = record.levelno
        if levelno >= logging.ERROR:
            color = Fore.RED
        elif levelno >= logging.WARNING:
            color = Fore.YELLOW
        elif levelno >= logging.INFO:
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


def main():
    """ Reads the manifest -> TODO. """
    # Initialize the RepoManager with the path to the manifest file
    """ Read manifest -> iterate repos to clean. """
    print()
    print(f'{Fore.LIGHTGREEN_EX}== tool_template =={Fore.RESET}')

    # Ensure template path exists
    logger.info(f"Attempting to read manifest: '{REL_MANIFEST_PATH}' ...")
    manager = RepoManager(ABS_MANIFEST_PATH)
    manifest = manager.read_manifest()

    # TODO: Template starts here!
    init_clone_path = manifest['init_clone_path']
    logger.info(f"init_clone_path: '{init_clone_path}'")


# ENTRY POINT
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tool_template.py  # Looks for `../repo_manifest.yml`")
        sys.exit(1)

    # TODO: If you accept args, grab it from `sys.argv[i]`
    try:
        main()
    except Exception as e:
        # For paths, convert double backslashes to single forward slashes
        normalized_e = str(e).replace('\\\\', '/')
        logger.error(normalized_e)  # "ERROR: {normalized_e}" (in red)
        print()
        sys.exit(1)
