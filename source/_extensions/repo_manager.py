"""
Sphinx Extension: Repository Manager
------------------------------------

Description:
This Sphinx extension is designed to automate the management of multiple documentation repositories as part
of building a larger, unified documentation system. It facilitates the cloning and updating of external
repositories specified in a YAML manifest file, ensuring that each repository is checked out to the specified
tag before Sphinx documentation generation proceeds.

How it Works:
1. The extension reads a manifest file (`repo_manifest.yml`) that lists repositories with their respective
clone URLs and tags.
2. It checks if each repository is already cloned at the specified location.
3. If a repository is not found, it clones the repository from the provided URL to an initial clone path.
4. Symlinks are created from the clone path to the base symlink path specified in the YAML.
5. Regardless of the initial presence, it checks out the specified tag to align the documentation state
with the desired version.

Usage:
1. Place the `repo_manifest.yml` file two levels up from this script, typically at the project root.
2. Ensure each repository listed in the manifest includes a `url` and a `tag`.
3. Optionally, specify `init_clone_path` and `base_symlink_path` in the manifest to manage where repositories
are cloned and how they are accessed.
4. Include this extension in your Sphinx `conf.py` file by adding the extension's path to `sys.path`
and including `'repo_manager'` in the `extensions` list.

Requirements:
- Python 3.6 or higher
- Sphinx 1.8 or higher
- PyYAML library

Ensure that the Python environment where Sphinx is running includes PyYAML to parse the YAML configuration.

Entry point: setup(app) | This script is executed during the 'builder-inited' event of Sphinx,
which is triggered after Sphinx initialization but before the build process begins.
"""
import os
import yaml
import subprocess
import shutil
from sphinx.util import logging
from colorama import init, Fore, Style

init(autoreset=True)  # Initializes Colorama and auto-resets styles after each print
STOP_BUILD_ON_ERROR = True
logger = logging.getLogger(__name__)


class RepositoryManagementError(Exception):
    """ Custom exception for repository management errors. """
    pass


def setup(app):
    """ Connect the 'builder-inited' event from Sphinx to our custom function. """
    app.connect('builder-inited', clone_update_repos)


def init_dir_tree(manifest):
    """
    Initialize or clear paths based on manifest configuration. Default tree:
    ########################################################
    - source
        - _reposAvailable
        - content
            - {macro_version[x]} // Contains symlinked repos
    ########################################################
    """
    print(f"{Fore.CYAN}🧹 Crafting expected hierarchy from manifest...{Fore.RESET}")

    # init_clone_path
    init_clone_path = os.path.abspath(manifest.get('init_clone_path', '../_reposAvailable'))
    print(f"{Fore.CYAN}   - init_clone_path: '{Style.BRIGHT}{init_clone_path}{Style.NORMAL}'{Fore.RESET}")
    setup_directories(init_clone_path, clear=False)

    # base_symlink_path
    base_symlink_path = os.path.abspath(manifest.get('base_symlink_path', '../source'))
    print(f"{Fore.CYAN}   - base_symlink_path: '{Style.BRIGHT}{base_symlink_path}{Style.NORMAL}'{Fore.RESET}")
    setup_directories(base_symlink_path, clear=False)

    # macro_versions
    macro_versions = manifest['macro_versions'].items()
    for macro_version, details in macro_versions:
        version_path = os.path.abspath(os.path.join(base_symlink_path, macro_version))
        setup_directories(version_path, clear=False)

    print()


def clone_update_repos(app):
    """ Handle the repository cloning and updating process when Sphinx initializes. """
    print(f"\n{Fore.GREEN}══BEGIN REPO_MANAGER══\n{Fore.RESET}")
    try:
        manifest, manifest_path = read_manifest()
        init_dir_tree(manifest)

        manage_repositories(manifest)
    except Exception as e:
        logger.error(f"Failed to manage_repositories {Style.BRIGHT}*See `Extension error` below*{Style.NORMAL}")
        if STOP_BUILD_ON_ERROR:
            raise RepositoryManagementError(f"Critical repository management failure: {e}")
    finally:
        print(f"\n{Fore.GREEN}══END REPO_MANAGER══\n{Fore.RESET}")


def setup_directories(path, clear=False):
    """
    Ensure directory exists and optionally clear its contents.
    TODO: Utilize `clear` - getting perm denied errs, so may require admin
    """
    if not os.path.exists(path):
        os.makedirs(path)
    elif clear:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)


def manage_symlinks(repo_name, source_path, target_path, overwrite=True):
    """Create or update a symlink."""
    logger.info(f"[{repo_name}] {Fore.CYAN}🔗 | Symlinking...{Fore.RESET}")

    if os.path.islink(target_path):
        if overwrite:
            os.remove(target_path)
            os.symlink(source_path, target_path)
    elif not os.path.exists(target_path):
        os.symlink(source_path, target_path)


def normalize_manifest_set_meta(manifest):
    """
    Normalize the manifest values, such as removing .git from URLs, +injects hidden '_meta' prop:
    - Adds to repositories.x: { url_dotgit, is_default, repo_name }
    """
    repo_i = 0
    for version, details in manifest['macro_versions'].items():
        for repo_name, repo_info in details['repositories'].items():
            # Inject '_meta' placeholders; can technically be overridden in yml for debugging
            if '_meta' not in repo_info:
                repo_info['_meta'] = {
                    'is_default': repo_i == 0,  # 1st entry
                    'url_dotgit': ''
                }
            _meta = repo_info['_meta']

            # Default `active` to True
            repo_info.setdefault('active', True)

            # Strip ".git" from urls
            url = repo_info['url']
            if url.endswith('.git'):
                repo_info['url'] = url[:-4]
                _meta['url_dotgit'] = f"{url}.git"

            # Default branch == parent {default_branch}
            if 'default_branch' not in repo_info:
                repo_info.setdefault('branch', manifest['default_branch'])

            # Default symlink_path == repo name (the end of url after the last slash/)
            repo_name = url.split('/')[-1]
            repo_info.setdefault('symlink_path', repo_name)
            _meta["repo_name"] = repo_name

            repo_i += 1
    return manifest


def read_manifest():
    """ Read and return the repository manifest from YAML file, along with its path. """
    base_path = os.path.abspath(os.path.dirname(__file__))
    manifest_path = os.path.abspath(os.path.join(base_path, '..', '..', 'repo_manifest.yml'))
    manifest_path = os.path.normpath(manifest_path)  # Normalize
    print(f"{Fore.CYAN}📜 Reading manifest: '{Style.BRIGHT}{manifest_path}{Style.NORMAL}'...{Fore.RESET}")

    with open(manifest_path, 'r') as file:
        manifest = yaml.safe_load(file)

    # Remove .git from urls; inject hidden _meta prop per repo { url_dotgit, is_default }
    manifest = normalize_manifest_set_meta(manifest)

    # Initialize or clear paths based on manifest configuration
    init_clone_path = os.path.abspath(manifest.get('init_clone_path', '../_reposAvailable'))
    base_symlink_path = os.path.abspath(manifest.get('base_symlink_path', '../source'))
    setup_directories(init_clone_path, manifest.get('clear_clone_path', False))
    setup_directories(base_symlink_path, manifest.get('clear_base_symlink_path', False))

    return manifest, manifest_path


def manage_repositories(manifest):
    """ Manage the cloning and checking out of repositories as defined in the manifest. """
    relative_init_clone_path = manifest.get('init_clone_path', '../_reposAvailable')
    relative_base_symlink_path = manifest.get('base_symlink_path', '../source')

    init_clone_path = os.path.abspath(relative_init_clone_path)
    base_symlink_path = os.path.abspath(relative_base_symlink_path)

    total_repos = sum(len(details['repositories']) for version, details in manifest['macro_versions'].items())
    current_repo = 1

    for version, details in manifest['macro_versions'].items():
        for repo_name, repo_info in details['repositories'].items():
            line_break = "" if current_repo == 1 else "\n"
            logger.info(f"{line_break}[{current_repo}/{total_repos}]")

            # Ensure repo is active
            active = repo_info.get('active', True)
            if not active:
                logger.info(f"{Fore.YELLOW}[{repo_name}] Repository !active; skipping...{Fore.RESET}")
                total_repos -= 1
                continue

            # Gather paths to clone + symlink
            symlink_path = repo_info.get('symlink_path', repo_name)
            repo_path = os.path.join(init_clone_path, symlink_path)
            symlink_target_path = os.path.join(base_symlink_path, symlink_path)

            clone_and_symlink(repo_name,
                              repo_info,
                              repo_path,
                              symlink_target_path)
            current_repo += 1


def git_fetch(repo_name, repo_path):
    """ Fetch all branches and tags from the remote repository. """
    logger.info(f"[{repo_name}] {Fore.YELLOW}🔃 | Fetching updates...{Fore.RESET}")
    subprocess.run(['git', '-C', repo_path, 'fetch', '--all'], check=True)


def validate_is_git_dir(repo_path):
    """ Check if a directory is a valid Git repository. """
    is_git_dir = subprocess.run(['git', '-C', repo_path, 'rev-parse'],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL).returncode == 0
    return is_git_dir


def validate_pull_repo(repo_name, repo_path):
    """ Repo already cloned: Check if it's a valid Git repository. """
    if not validate_is_git_dir(repo_path):
        logger.error(f"{Fore.RED}The directory '{repo_path}' exists but is not a Git repository.{Fore.RESET}")
        raise RepositoryManagementError(f"The directory '{repo_path}' exists but is not a Git repository.")

    git_fetch(repo_name, repo_path)


def clone_repo(repo_name, repo_url_dotgit, repo_path):
    """ Clone the repository from the provided URL to the specified path. """
    logger.info(f"[{repo_name}] {Fore.YELLOW}⬇️ | Cloning '{repo_path}'...{Fore.RESET}")

    subprocess.run(['git', 'clone', '-q', repo_url_dotgit, repo_path], check=True)
    subprocess.run(['git', '-C', repo_path, 'fetch', '--all'], check=True)


def clone_and_symlink(repo_name, repo_info, repo_path, symlink_target_path):
    """ Clone the repository if it does not exist and create a symlink in the base symlink path. """
    try:
        # Clone the repo, if we haven't done so already
        if not os.path.exists(repo_path):
            repo_url_dotgit = repo_info['_meta']['url_dotgit']
            clone_repo(repo_name, repo_url_dotgit, repo_path)
        else:
            validate_pull_repo(repo_name, repo_path)

        # Checkout to the specific branch or tag
        if 'branch' in repo_info:
            logger.info(f"[{repo_name}] {Fore.YELLOW}🔄 | Checking out branch '{repo_info['branch']}'...{Fore.RESET}")
            subprocess.run(['git', '-C', repo_path, 'checkout', '-q', repo_info['branch']], check=True)

        if 'tag' in repo_info:
            logger.info(f"[{repo_name}] {Fore.YELLOW}🏷️ | Checking out tag '{repo_info['tag']}'...{Fore.RESET}")
            subprocess.run(['git', '-C', repo_path, 'checkout', '-q', repo_info['tag']], check=True)

        # Manage symlinks
        manage_symlinks(repo_name, repo_path, symlink_target_path)
        logger.info(f"[{repo_name}] {Fore.GREEN}✅ | Repo symlinked: "
                    f"'{Style.BRIGHT}{symlink_target_path}{Style.NORMAL}'{Fore.RESET}")

    except subprocess.CalledProcessError:
        tag = repo_info['tag']
        repo_url_dotgit = repo_info['url']
        error_url = f"{repo_url_dotgit}/tree/{tag}"
        tags_url = f"{repo_url_dotgit}/-/tags"

        error_message = (f"\n\n{Fore.RED}[repo_manager]{Style.BRIGHT} Failed to checkout branch/tag for "
                         f"repository '{repo_name}':{Style.NORMAL}\n"
                         f"- Does the '{tag}' tag exist? {error_url}\n"
                         f"- Check available tags: {tags_url}{Fore.RESET}\n\n")
        raise RepositoryManagementError(error_message)
