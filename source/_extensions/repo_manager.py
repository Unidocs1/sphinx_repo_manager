"""
Sphinx Extension: Repository Manager
------------------------------------

Description:
This Sphinx extension is designed to automate the management of multiple documentation repositories as part
of building a larger, unified doc system. It facilitates the cloning and updating of external repositories
specified in a YAML manifest file, ensuring that each repository is checked out to the specified
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

Entry point: setup(app) | This script is executed during the 'builder-inited' event of Sphinx,
which is triggered after Sphinx inits but before the build process begins.

# Tested in:
- Windows 11 via PowerShell7
"""
import os
import yaml
import subprocess
from sphinx.util import logging
from colorama import init, Fore, Style

init(autoreset=True)  # Initializes Colorama and auto-resets styles after each print
STOP_BUILD_ON_ERROR = True
logger = logging.getLogger(__name__)


class RepositoryManagementError(Exception):
    """ Custom exception for repository management errors. """
    pass


def brighten(log_str):
    """ Apply bright style to a string. """
    return f"{Style.BRIGHT}{log_str}{Style.NORMAL}"


def colorize(log_str, color):
    """ Apply color to a string, resetting when done. """
    return f"{color}{log_str}{Fore.RESET}"


def colorize_path(log_str):
    """ Apply a path-related color (CYAN) to a string. """
    return f"{Fore.CYAN}{log_str}{Fore.RESET}"


def colorize_action(log_str):
    """ Apply an action-related color (YELLOW) to a string. """
    return f"{Fore.YELLOW}{log_str}{Fore.RESET}"


def colorize_success(log_str):
    """ Apply a success-related color (GREEN) to a string. """
    return f"{Fore.GREEN}{log_str}{Fore.RESET}"


def colorize_error(log_str):
    """ Apply an error-related color (RED) to a string. """
    return f"{Fore.RED}{log_str}{Fore.RESET}"


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
    logger.info(colorize_path("🧹 Crafting expected hierarchy from manifest..."))

    # init_clone_path
    init_clone_path = os.path.abspath(manifest['init_clone_path'])
    logger.info(colorize_path(f"   - init_clone_path: '{brighten(init_clone_path)}'"))
    setup_directory_skeleton(init_clone_path)

    # base_symlink_path
    base_symlink_path = os.path.abspath(manifest['base_symlink_path'])
    logger.info(colorize_path(f"   - base_symlink_path: '{brighten(base_symlink_path)}'"))
    setup_directory_skeleton(base_symlink_path)

    # macro_versions
    macro_versions = manifest['macro_versions'].items()
    logger.info(colorize_path("     - macro_version dirs:"))

    # Log macro versions -> Create directory skeleton
    macro_version_i = 0
    for macro_version, details in macro_versions:
        default_str = f" {brighten('(default)')}" if macro_version_i == 0 else ""
        logger.info(colorize_path(f"       - {macro_version}{default_str}"))
        version_path = os.path.abspath(os.path.join(base_symlink_path, macro_version))

        setup_directory_skeleton(version_path)
        macro_version_i += 1
    logger.info("")


def clone_update_repos(app):
    """ Handle the repository cloning and updating process when Sphinx initializes. """
    logger.info(colorize_success(f"\n══{brighten('BEGIN REPO_MANAGER')}══\n"))
    try:
        manifest, manifest_path = read_manifest()
        init_dir_tree(manifest)
        manage_repositories(manifest)
    except Exception as e:
        logger.error(f"Failed to manage_repositories {brighten('*See `Extension error` below*')}")
        if STOP_BUILD_ON_ERROR:
            raise RepositoryManagementError(f"clone_update_repos failure:\n- {e}")
    finally:
        logger.info(colorize_success(f"\n══{brighten('END REPO_MANAGER')}══\n"))


def setup_directory_skeleton(create_path_to):
    """
    Ensure directory exists and optionally clear its contents.
    (!) Deleting or overriding may require ADMIN
    """
    if not os.path.exists(create_path_to):
        os.makedirs(create_path_to)


def validate_normalize_manifest_set_meta(manifest):
    """
    Validates + normalizes YAML v1.2 manifest vals, such as removing .git from URLs,
    +injects hidden '_meta' prop, etc.
    - Sets default fallbacks, if any
    - Adds to repositories.x: {
        - is_default
        - url_dotgit
        - repo_name
        - rel_symlinked_tagged_repo_path
        - tag_versioned_repo_name
        - tag_versioned_clone_src_path
    }
    """
    # Set root defaults
    manifest.setdefault('debug_mode', False)
    manifest.setdefault('default_branch', 'master')
    manifest.setdefault('init_clone_path', 'source/_repos-available')
    manifest.setdefault('base_symlink_path', 'source/content')

    init_clone_path = manifest['init_clone_path']
    base_symlink_path = manifest['base_symlink_path']
    repo_i = 0
    for macro_version, details in manifest['macro_versions'].items():
        for repo_name, repo_info in details['repositories'].items():
            # Inject '_meta' placeholders; can technically be overridden in yml for debugging
            if '_meta' not in repo_info:
                repo_info['_meta'] = {
                    'is_default': repo_i == 0,             # 1st entry == default
                    'url_dotgit': '',                      # eg: "https://gitlab.acceleratxr.com/core/account_services.git"
                    'repo_name': '',                       # eg: "account_services"
                    'rel_symlinked_tagged_repo_path': '',  # "{base_symlink_path}{macro_version}{symlink_path}-{tag}"
                    'tag_versioned_repo_name': '',         # "Prep "repo-{repo_tag}"; eg: "account-services-v2.1.0"
                    'tag_versioned_clone_src_path': ''     # "{init_clone_path}/{tag_versioned_repo_name}"
                }

            # url: Req'd - Strip ".git" from suffix, if any
            url = repo_info.get('url', None)
            if not url:
                logger.error(colorize_error(f"Missing 'url' for repo '{repo_name}'"))
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

            # Other validations
            tag = repo_info['tag']
            if not tag:
                logger.error(colorize_error(f"Missing 'tag' for repo '{repo_name}'"))
                raise RepositoryManagementError(f"Missing 'tag' for repo '{repo_name}'")

            # Set other defaults
            repo_info.setdefault('active', True)

            # Set dynamic meta
            _meta = repo_info['_meta']
            _meta['url_dotgit'] = f"{url}.git"
            _meta['repo_name'] = repo_name
            _meta['tag_versioned_repo_name'] = f"{repo_name}-{tag}"  # eg: "account-services-v2.1.0"

            tag_versioned_repo_name = _meta['tag_versioned_repo_name']
            _meta['rel_symlinked_tagged_repo_path'] = os.path.normpath(os.path.join(
                base_symlink_path, macro_version, tag_versioned_repo_name))

            # "{init_clone_path}/{tag_versioned_repo_name}"
            _meta['tag_versioned_clone_src_path'] = os.path.normpath(os.path.join(
                init_clone_path, tag_versioned_repo_name))

        repo_i += 1
    return manifest


def create_symlink(rel_symlinked_tagged_repo_path, tag_versioned_clone_src_path):
    """
    Create or update a symlink.
    (!) overwrite only works if running in ADMIN
    (!) In Windows, symlinking is the *opposite* src and destination of Unix
    - tag_versioned_clone_src_path   # eg: "source/_repos-available/account_services-v2.1.0"
    - rel_symlinked_tagged_repo_path # eg: "source/content/v1.0.0/account_services-v2.1.0"
    - ^ We need a lingering /slash on the end
    """
    # Convert to abs paths
    abs_symlinked_tagged_repo_path = os.path.abspath(rel_symlinked_tagged_repo_path)
    abs_tag_versioned_clone_src_path = os.path.abspath(tag_versioned_clone_src_path)
    
    print(f"*Source (real content): {abs_tag_versioned_clone_src_path}")
    print(f"*Destination (symlink): {abs_symlinked_tagged_repo_path}")
    print(f"*PowerShell equivalent command:")
    print(f'New-Item -ItemType SymbolicLink -Path "{abs_symlinked_tagged_repo_path}" -Target "{abs_tag_versioned_clone_src_path}"')

    # Is it already symlinked?
    if os.path.islink(abs_symlinked_tagged_repo_path):
        logger.info(colorize_success(f"  - Already linked."))
        return

    # Path is clean: Symlink now, after we ensure a "/" on the end
    os.symlink(abs_tag_versioned_clone_src_path, abs_symlinked_tagged_repo_path)


def read_manifest():
    """ Read and return the repository manifest from YAML file, along with its path. """
    base_path = os.path.abspath(os.path.dirname(__file__))
    manifest_path = os.path.abspath(os.path.join(base_path, '..', '..', 'repo_manifest.yml'))
    manifest_path = os.path.normpath(manifest_path)  # Normalize
    logger.info(colorize_path(f"📜 Reading manifest: '{brighten(manifest_path)}'..."))

    with open(manifest_path, 'r') as file:
        manifest = yaml.safe_load(file)

    # Remove .git from urls; inject hidden _meta prop per repo, etc
    manifest = validate_normalize_manifest_set_meta(manifest)

    # Initialize or clear paths based on manifest configuration
    init_clone_path = os.path.abspath(manifest['init_clone_path'])
    base_symlink_path = os.path.abspath(manifest['base_symlink_path'])

    setup_directory_skeleton(init_clone_path)
    setup_directory_skeleton(base_symlink_path)

    return manifest, manifest_path


def log_paths(
        debug_mode,
        tag_versioned_repo_name,
        rel_init_clone_path,
        tag_versioned_clone_src_path,
        rel_symlinked_tagged_repo_path):
    """ Log paths for production [and optionally debugging, if debug_mode]. """
    if debug_mode:
        print("###############################################################################")
        print(f"tag_versioned_repo_name:  '{tag_versioned_repo_name}'")                # eg: "account_services-v2.1.0"
        print(f"rel_init_clone_path:  '{rel_init_clone_path}'")                        # eg: "source/_repos-available"
        print(f"tag_versioned_clone_src_path:  '{tag_versioned_clone_src_path}'")      # eg: "source/_repos-available/account_services-v2.1.0"
        print(f"rel_symlinked_tagged_repo_path:  '{rel_symlinked_tagged_repo_path}'")  # eg: "source/content/v1.0.0/account_services-v2.1.0"
        print("###############################################################################")
        print()

    action_str = colorize_action(f"📁 | Working Dirs:")
    logger.info(f"[{tag_versioned_repo_name}] {action_str}")
    logger.info(colorize_path(f"  - Repo clone src path: '{brighten(tag_versioned_clone_src_path)}'"))
    logger.info(colorize_path(f"  - Repo symlink target path: '{brighten(rel_symlinked_tagged_repo_path)}'"))


def manage_repositories(manifest):
    """ Manage the cloning and checking out of repositories as defined in the manifest. """
    # Read manifest
    rel_init_clone_path = manifest['init_clone_path']
    macro_versions = manifest['macro_versions'].items()
    repositories = [repo for version, details in macro_versions
                    for repo in details['repositories'].items()]

    # Track current/max macro_versions & child repos
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
            logger.info(
                colorize_action(f"{line_break}[MacroVer {current_macro_ver}/{total_macro_versions}, Repo {current_repo_num}/{total_repos_num}]"))

            # Get paths from _meta
            _meta = repo_info['_meta']
            rel_symlinked_tagged_repo_path = _meta['rel_symlinked_tagged_repo_path']  # eg: "source/content/v1.0.0/account_services-v2.1.0"
            tag_versioned_repo_name = _meta['tag_versioned_repo_name']  # eg: "account_services-v2.1.0"

            # Ensure repo is active
            active = repo_info['active']
            if not active:
                logger.info(colorize_action(f"[{rel_symlinked_tagged_repo_path}] Repository !active; skipping..."))
                total_repos_num -= 1
                continue

            # eg: "source/_repos-available/account_services-v2.1.0"
            tag_versioned_clone_src_path = _meta['tag_versioned_clone_src_path']
            debug_mode = manifest['debug_mode']
            log_paths(
                debug_mode,
                tag_versioned_repo_name,
                rel_init_clone_path,
                tag_versioned_clone_src_path,
                rel_symlinked_tagged_repo_path)

            clone_and_symlink(
                repo_info,
                tag_versioned_repo_name,
                rel_init_clone_path,
                tag_versioned_clone_src_path,
                rel_symlinked_tagged_repo_path)

            current_repo_num += 1
        current_macro_ver += 1


def git_fetch(repo_path):
    """ Fetch all branches and tags from the remote repository. """
    # Fetch all branches and tags *from the repo_path working dir (-C)*
    git_submodule_cmd(['fetch', '--all', '--tags'], repo_path)


def validate_is_git_dir(repo_path):
    """ Check if a directory is a valid Git repository. """
    is_git_dir = os.path.exists(os.path.join(repo_path, '.git'))
    return is_git_dir


def git_clone(clone_to_path, repo_url_dotgit, branch):
    """
    Clone the repo+branch from the provided URL to the specified path.
    - rel_symlinked_tagged_repo_path # eg: "v1.0.0/account_services"
    """
    # Clone -> Fetch all
    subprocess.run([
        'git', 'clone',
        '--branch', branch,
        '-q',
        repo_url_dotgit, clone_to_path], check=True)


def git_checkout(repo_path, tag_or_branch):
    """ Checkout the specified tag/branch in the repository. """
    git_submodule_cmd(['checkout', tag_or_branch], repo_path)


def git_submodule_cmd(cmd, working_dir_repo_path):
    """
    Run a git command in the specified sub-repo path, ensuring it's run from that working dir.
    - `--quiet` suppresses spammy tips
    - eg: git_existing_repo_cmd(['checkout', 'v1.0.0'], 'source/_repos-available/v1.0.0/account_services')
    - eg: git_existing_repo_cmd(['fetch', '--all', '--tags'], 'source/_repos-available/v1.0.0/account_services')
    - eg: git_existing_repo_cmd(['pull'], 'source/_repos-available/v1.0.0/account_services')
    """
    subprocess.run(['git', '-C', working_dir_repo_path, *cmd, "--quiet"], check=True)


def clone_and_symlink(
        repo_info,
        tag_versioned_repo_name,
        rel_init_clone_path,  # TODO: Unused?
        tag_versioned_clone_src_path,
        rel_symlinked_tagged_repo_path):
    """
    Clone the repository if it does not exist and create a symlink in the base symlink path.
    - repo_name                       # eg: "account_services"
    - tag_versioned_repo_name         # eg: "account_services-v2.1.0"
    - rel_init_clone_path             # eg: "source/_repos-available"
    - tag_versioned_clone_src_path    # eg: "source/_repos-available/account_services-v2.1.0"
    - rel_symlinked_tagged_repo_path  # eg: "source/content/v1.0.0/account_services-v2.1.0"
    """
    tag = repo_info['tag']
    branch = repo_info['branch']
    repo_url_dotgit = repo_info['_meta']['url_dotgit']

    try:

        # Clone the repo, if we haven't done so already
        if not os.path.exists(tag_versioned_clone_src_path):
            action_str = colorize_action(f"📦 | Cloning ({brighten(f'--branch {branch}')}) '{repo_url_dotgit}'...")
            logger.info(f"[{tag_versioned_repo_name}] {action_str}")

            git_clone(tag_versioned_clone_src_path, repo_url_dotgit, branch)
        else:
            action_str = colorize_action(f"🔄 | Fetching updates...")
            logger.info(f"[{tag_versioned_repo_name}] {action_str}")

            git_fetch(tag_versioned_clone_src_path)

        # Checkout to the specific branch or tag
        has_tag = 'tag' in repo_info
        has_branch = 'branch' in repo_info

        if has_branch:
            action_str = colorize_action(f"🔄 | Checking out branch '{brighten(branch)}'...")
            logger.info(f"[{tag_versioned_repo_name}] {action_str}")
            git_checkout(tag_versioned_clone_src_path, branch)

        if has_tag:
            action_str = colorize_action(f"🔄 | Checking out tag '{brighten(tag)}'...")
            logger.info(f"[{tag_versioned_repo_name}] {action_str}")
            git_checkout(tag_versioned_clone_src_path, tag)

        # Manage symlinks
        action_str = colorize_action(f"🔗 | Symlinking...")
        logger.info(f"[{tag_versioned_repo_name}] {action_str}")
        logger.info(colorize_path(f"  - From clone src path: '{brighten(tag_versioned_clone_src_path)}'"))
        logger.info(colorize_path(f"  - To symlink path: '{brighten(rel_symlinked_tagged_repo_path)}'"))
        create_symlink(rel_symlinked_tagged_repo_path, tag_versioned_clone_src_path)

        # Done with this repo
        success_str = colorize_success("✅ | Done.")
        logger.info(f"[{tag_versioned_repo_name}] {success_str}")

    except subprocess.CalledProcessError:
        error_url = f"{repo_url_dotgit}/tree/{tag}"
        tags_url = f"{repo_url_dotgit}/-/tags"

        error_message = (f"\n\n{Fore.RED}[repo_manager] {brighten('Failed to checkout')}"
                         f"branch/tag '{rel_symlinked_tagged_repo_path}'\n"
                         f"- Does the '{tag}' tag exist? {error_url}\n"
                         f"- Check available tags: {tags_url}{Fore.RESET}\n\n")
        raise RepositoryManagementError(error_message)
