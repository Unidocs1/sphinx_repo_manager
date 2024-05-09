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
        - _repos-available
        - content
            - {macro_version[i]} // Contains symlinked repos
    ########################################################
    """
    logger.info(f"{Fore.CYAN}🧹 Crafting expected hierarchy from manifest...{Fore.RESET}")

    # init_clone_path
    init_clone_path = os.path.abspath(manifest['init_clone_path'])
    logger.info(f"{Fore.CYAN}   - init_clone_path: '{Style.BRIGHT}{init_clone_path}{Style.NORMAL}'{Fore.RESET}")
    setup_directory_skeleton(init_clone_path, clear=False)

    # base_symlink_path
    base_symlink_path = os.path.abspath(manifest['base_symlink_path'])
    logger.info(f"{Fore.CYAN}   - base_symlink_path: '{Style.BRIGHT}{base_symlink_path}{Style.NORMAL}'{Fore.RESET}")
    setup_directory_skeleton(base_symlink_path, clear=False)

    # macro_versions
    macro_versions = manifest['macro_versions'].items()
    logger.info(f"{Fore.CYAN}     - macro_version dirs:{Fore.RESET}")

    # Log macro versions -> Create directory skeleton
    macro_version_i = 0
    for macro_version, details in macro_versions:
        default_str = " (default)" if macro_version_i == 0 else ""
        logger.info(f"{Fore.CYAN}       - {macro_version}{default_str}{Fore.RESET}")
        version_path = os.path.abspath(os.path.join(base_symlink_path, macro_version))

        setup_directory_skeleton(version_path, clear=False)
        macro_version_i += 1
    logger.info("")


def clone_update_repos(app):
    """ Handle the repository cloning and updating process when Sphinx initializes. """
    logger.info(f"\n{Fore.GREEN}══BEGIN REPO_MANAGER══\n{Fore.RESET}")
    try:
        manifest, manifest_path = read_manifest()
        init_dir_tree(manifest)
        manage_repositories(manifest)
    except Exception as e:
        logger.error(f"Failed to manage_repositories {Style.BRIGHT}*See `Extension error` below*{Style.NORMAL}")
        if STOP_BUILD_ON_ERROR:
            raise RepositoryManagementError(f"clone_update_repos failure: {e}")
    finally:
        logger.info(f"\n{Fore.GREEN}══END REPO_MANAGER══\n{Fore.RESET}")


def setup_directory_skeleton(path, clear=False):
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


def validate_normalize_manifest_set_meta(manifest):
    """
    Validates + normalizes manifest vals, such as removing .git from URLs, 
    +injects hidden '_meta' prop, etc.
    - Sets default fallbacks, if any
    - Adds to repositories.x: { url_dotgit, is_default, repo_name, macro_repo }
    """

    # Set root defaults
    manifest.setdefault('default_branch', 'master')
    manifest.setdefault('init_clone_path', 'source/_repos-available')
    manifest.setdefault('base_symlink_path', 'source/content')

    repo_i = 0
    for macro_version, details in manifest['macro_versions'].items():        
        for repo_name, repo_info in details['repositories'].items():
            # Inject '_meta' placeholders; can technically be overridden in yml for debugging
            if '_meta' not in repo_info:
                repo_info['_meta'] = {
                    'is_default': repo_i == 0,  # 1st entry == default
                    'url_dotgit': '',           # eg: "https://gitlab.acceleratxr.com/core/account_services.git"
                    'repo_name': '',            # eg: "account_services"
                    'symlinked_path_to': ''     # "{macro_version}{symlink_path}-{tag}"
                }

            # url: Req'd - Strip ".git" from suffix, if any
            url = repo_info.get('url', None)
            if not url:
                logger.error(f"{Fore.RED}Missing 'url' for repo '{repo_name}'{Fore.RESET}")
                raise RepositoryManagementError(f"Missing 'url' for repo '{repo_name}'")

            if url.endswith('.git'):
                url = url[:-4]
                repo_info['url'] = url

            # Default branch == parent {default_branch}
            if 'default_branch' not in repo_info:
                repo_info.setdefault('branch', manifest['default_branch'])

            # Default symlink_path == repo name (the end of url after the last slash/)
            repo_name = url.split('/')[-1]
            repo_info.setdefault('symlink_path', repo_name)

            # "{macro_version}/{repositories[i].symlink_path}"; eg: "v1.0.0/path/to/account_services"
            symlink_path = repo_info['symlink_path']

            # Other validations
            tag = repo_info['tag']
            if not tag:
                logger.error(f"{Fore.RED}Missing 'tag' for repo '{repo_name}'{Fore.RESET}")
                raise RepositoryManagementError(f"Missing 'tag' for repo '{repo_name}'")

            # Set other defaults
            repo_info.setdefault('active', True)

            # Set dynamic meta
            _meta = repo_info['_meta']
            _meta['url_dotgit'] = f"{url}.git"
            _meta["repo_name"] = repo_name
            _meta['symlinked_path_to'] = f"{macro_version}/{symlink_path}-{tag}"
            print(f"symlinked_path_to: {_meta['symlinked_path_to']}")

            repo_i += 1
    return manifest


def read_manifest():
    """ Read and return the repository manifest from YAML file, along with its path. """
    base_path = os.path.abspath(os.path.dirname(__file__))
    manifest_path = os.path.abspath(os.path.join(base_path, '..', '..', 'repo_manifest.yml'))
    manifest_path = os.path.normpath(manifest_path)  # Normalize
    logger.info(f"{Fore.CYAN}📜 Reading manifest: '{Style.BRIGHT}{manifest_path}{Style.NORMAL}'...{Fore.RESET}")

    with open(manifest_path, 'r') as file:
        manifest = yaml.safe_load(file)

    # Remove .git from urls; inject hidden _meta prop per repo, etc
    manifest = validate_normalize_manifest_set_meta(manifest)

    # Initialize or clear paths based on manifest configuration
    init_clone_path = os.path.abspath(manifest['init_clone_path'])
    base_symlink_path = os.path.abspath(manifest['base_symlink_path'])

    setup_directory_skeleton(init_clone_path, clear=False)
    setup_directory_skeleton(base_symlink_path, clear=False)

    return manifest, manifest_path


def manage_repositories(manifest):
    """ Manage the cloning and checking out of repositories as defined in the manifest. """
    # Read manifest
    rel_init_clone_path = manifest['init_clone_path']
    rel_base_symlink_path = manifest['base_symlink_path']
    macro_versions = manifest['macro_versions'].items()
    repositories = [repo for version, details in macro_versions
                    for repo in details['repositories'].items()]

    base_clone_to = os.path.abspath(rel_init_clone_path)  # eg: "source/repos_available

    # How many macro_versions and repos to manage?
    total_macro_versions = len(macro_versions)
    total_repos_num = len(repositories)
    current_macro_ver = 1
    current_repo_num = 1

    # For each macro version:
    #   - for each repo:
    #       - Prep paths, clone/fetch, checkout tagged version
    for macro_version, details in macro_versions:
        for repo_name, repo_info in details['repositories'].items():
            line_break = "" if current_repo_num == 1 else "\n"
            logger.info(f"{line_break}[MacroVer {current_macro_ver}/{total_macro_versions}, "
                        f"Repo {current_repo_num}/{total_repos_num}]")

            # Ensure repo is active
            symlinked_path_to = repo_info['_meta']['symlinked_path_to']  # eg: "v1.0.0/account_services-v2.1.0"
            active = repo_info['active']
            if not active:
                logger.info(f"{Fore.YELLOW}[{symlinked_path_to}] Repository !active; skipping...{Fore.RESET}")
                total_repos_num -= 1
                continue

            # Get other useful manifest props
            repo_tag = repo_info['tag']  # eg: "v2.1.0"
            base_symlink_path = repo_info['symlink_path']  # eg: "account_services"

            # Prep "repo-{repo_tag}"; eg: "account-services-v2.1.0"
            tag_versioned_repo_name = f"{base_symlink_path}-{repo_tag}"

            #######################################################################
            # Combine "{init_clone_path}\{macro_version}\{repo_name}-{tag_version}"
            # eg: "_repos-available\v1.0.0\account_services-v2.1.0"
            #######################################################################

            print()  # DELETE ME >>
            print("#############################################################")
            print(f"init_clone_path: {base_clone_to}")  # eg: "source/_repos-available"
            print(f"tag_versioned_repo_name: {tag_versioned_repo_name}")  # eg: "account_services-{tag_version}"
            print("#############################################################")
            print()  # << DELETE ME

            symlink_to = os.path.join(
                base_clone_to,            # eg: "source/_repos-available"
                tag_versioned_repo_name)  # eg: "account_services-v2.1.0"

            logger.info(f"[{symlinked_path_to}] {Fore.CYAN}📁 | Repo path: "
                        f"'{Style.BRIGHT}{symlink_to}{Style.NORMAL}'{Fore.RESET}")

            clone_and_symlink(repo_name,
                              repo_info,
                              base_clone_to,
                              tag_versioned_repo_name)

            current_repo_num += 1
        current_macro_ver += 1


def git_fetch(symlinked_path_to, repo_path):
    """ Fetch all branches and tags from the remote repository. """
    logger.info(f"[{symlinked_path_to}] {Fore.YELLOW}🔃 | Fetching updates...{Fore.RESET}")

    # Fetch all branches and tags *from the repo_path working dir (-C)*
    git_submodule_cmd(['fetch', '--all', '--tags'], repo_path)


def validate_is_git_dir(repo_path):
    """ Check if a directory is a valid Git repository. """
    is_git_dir = os.path.exists(os.path.join(repo_path, '.git'))
    return is_git_dir


def git_clone(symlinked_path_to, repo_url_dotgit, repo_path, branch):
    """ Clone the repo+branch from the provided URL to the specified path. """
    logger.info(f"[{symlinked_path_to}] {Fore.YELLOW}⬇️ | Cloning '{repo_path}'...{Fore.RESET}")

    # Clone -> Fetch all
    subprocess.run([
        'git', 'clone',
        '--branch', branch,
        '-q',
        repo_url_dotgit, repo_path], check=True)


def git_checkout(clone_to_path, tag_or_branch):
    """ Checkout the specified tag/branch in the repository. """
    git_submodule_cmd(['checkout', tag_or_branch], clone_to_path)


def git_submodule_cmd(cmd, repo_path):
    """
    Run a git command in the specified sub-repo path, ensuring it's run from that working dir.
    - eg: git_existing_repo_cmd(['checkout', 'v1.0.0'], 'source/_repos-available/v1.0.0/account_services')
    - eg: git_existing_repo_cmd(['fetch', '--all', '--tags'], 'source/_repos-available/v1.0.0/account_services')
    - eg: git_existing_repo_cmd(['pull'], 'source/_repos-available/v1.0.0/account_services')
    """
    subprocess.run(['git', '-C', repo_path] + cmd, check=True)


def clone_and_symlink(repo_name, repo_info, base_clone_to_path, tag_versioned_repo_name):
    """ Clone the repository if it does not exist and create a symlink in the base symlink path. """
    try:
        symlinked_path_to = repo_info['_meta']['symlinked_path_to']  # eg: "v1.0.0/path/to/account_services"

        full_clone_path = os.path.join(base_clone_to_path, tag_versioned_repo_name)  # eg: "_repos-available\account_services"
        branch = repo_info['branch']

        # Clone the repo, if we haven't done so already
        if not os.path.exists(full_clone_path):
            repo_url_dotgit = repo_info['_meta']['url_dotgit']
            git_clone(symlinked_path_to, repo_url_dotgit, base_clone_to_path, branch)
        else:
            git_fetch(symlinked_path_to, base_clone_to_path)

        # Checkout to the specific branch or tag
        if 'branch' in repo_info:
            logger.info(f"[{symlinked_path_to}] {Fore.YELLOW}🔄 | Checking out branch '{branch}'...{Fore.RESET}")
            git_checkout(base_clone_to_path, repo_info['branch'])

        if 'tag' in repo_info:
            logger.info(f"[{symlinked_path_to}] {Fore.YELLOW}🏷️ | Checking out tag '{repo_info['tag']}'...{Fore.RESET}")
            git_checkout(base_clone_to_path, repo_info['tag'])

        # Manage symlinks
        manage_symlinks(repo_name, base_clone_to_path, symlink_to_path)
        logger.info(f"[{symlinked_path_to}] {Fore.GREEN}✅ | Repo symlinked: "
                    f"'{Style.BRIGHT}{symlink_to_path}{Style.NORMAL}'{Fore.RESET}")

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
