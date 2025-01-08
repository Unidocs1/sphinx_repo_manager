from sphinx.application import Sphinx
from sphinx.config import Config
from .sphinx_repo_manager import SphinxRepoManager
from .git_helper import GitHelper
from .api_reference import configure_doxygen
from pathlib import Path
import importlib.metadata

# Get the version of the extension
try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"


class SphinxRepoManagerConfig:
    """
    Define the type structure for sphinx_repo_manager config values.

    Attributes:
        repo_manager_manifest_path (Path): The path to the repository manager manifest file.
        read_the_docs_build (bool): Whether the build is being executed on Read the Docs.
        source_static_path (Path): The path to the static source directory.
        source_doxygen_path (Path): The path to the Doxygen source directory.
        default_repo_auth_user (str): The default repository authentication username.
        default_repo_auth_token (str): The default repository authentication token.
        has_default_repo_auth_token (bool): Whether the default repository authentication token is set.
        start_time (float): The start time of the build.
        end_time (float): The end time of the build.
        manifest (dict): The repository manager manifest
        raw_manifest (dict): The raw repository manager manifest
    """

    def __init__(self):
        # TODO: Config should be defaulted by env vars in this constructor,
        # and then a new instance should be set as the default config value
        # in `setup` below. This way, the config values can be set in conf.py
        # and then loaded to the SphinxManager instance via its constructor
        # during `create_repo_manager`.
        self.repo_manager_manifest_path: Path = Path()
        self.read_the_docs_build: bool = False
        self.source_static_path: Path = Path()
        self.source_doxygen_path: Path = Path()
        self.default_repo_auth_user: str = ""
        self.default_repo_auth_token: str = ""
        self.has_default_repo_auth_token: bool = False
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.manifest: dict = {}
        self.raw_manifest: dict = {}

    def set_from_repo_manager(self, repo_manager: SphinxRepoManager):
        """
        Set the configuration values from a SphinxRepoManager instance.

        Args:
            repo_manager (SphinxRepoManager): The repository manager to extract values from.
        """
        self.repo_manager_manifest_path = repo_manager.debug_stop_build_on_extension_done
        self.repo_manager_manifest_path = repo_manager.repo_manager_manifest_path
        self.read_the_docs_build = repo_manager.read_the_docs_build
        self.source_static_path = repo_manager.source_static_path
        self.source_doxygen_path = repo_manager.source_doxygen_path
        self.default_repo_auth_user = repo_manager.env_repo_auth_user
        self.default_repo_auth_token = repo_manager.env_repo_auth_token
        self.has_default_repo_auth_token = repo_manager.has_env_repo_auth_token
        self.start_time = repo_manager.start_time
        self.end_time = repo_manager.end_time
        self.manifest = repo_manager.manifest
        self.raw_manifest = repo_manager.raw_manifest


def set_config_dot_py_vals(
        app: Sphinx,
        config: Config,
        repo_manager: SphinxRepoManager,
):
    """
    Save useful config vals to be accessible from conf.py.

    Args:
        app (Sphinx): The Sphinx application instance.
        config (Config): The Sphinx configuration object.
        repo_manager (SphinxRepoManager): The Sphinx repository manager instance containing the configuration values to be saved.
    """
    # TODO: We should avoid modifying `config` values as a way to expose data to external modules. Config
    # should be treated as immutable after config is initialized.
    # 
    # For setting versioned data as environment domains, we should use either the env collector or domain API
    #   - https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_env_collector
    #   - https://www.sphinx-doc.org/en/master/extdev/domainapi.html#module-sphinx.domains
    #
    # For firing off custom events to be caught by other modules, we should use add_event and emit:
    #   - https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_event
    #   - https://www.sphinx-doc.org/en/master/extdev/appapi.html#emitting-events

    # Create a SphinxRepoManagerConfig instance -> set values from repo_manager
    config.sphinx_repo_manager = SphinxRepoManagerConfig()
    config.sphinx_repo_manager.set_from_repo_manager(repo_manager)


def create_repo_manager(app: Sphinx, config: Config):
    """
    Instantiate the SphinxRepoManager and propagate downstream config changes.

    Args:
        app (Sphinx): The Sphinx application instance.
        config (Config): The Sphinx configuration object.
    """
    try:
        # Instantiate the SphinxRepoManager
        repo_manager = SphinxRepoManager(app)
        set_config_dot_py_vals(app, config, repo_manager)
        configure_doxygen(app, config, repo_manager)
    except Exception as e:
        print(f"[sphinx_repo_manager] WARNING: Failed to initialize: {e}")


def setup(app: Sphinx):
    """
    Set up the repo manager extension.

    Args:
        app (Sphinx): The Sphinx application instance.
    
    Returns:
        dict: The extension metadata. See https://www.sphinx-doc.org/en/master/extdev/index.html#extension-metadata
    """
    # Add repo manager manifest path to the Sphinx config - changes to this will trigger a full rebuild
    abs_yml_path = Path(app.confdir, "..", "repo_manifest.yml").resolve()
    app.add_config_value(
        "repo_manager_manifest_path",
        abs_yml_path,
        "env",
        [Path, str],
    )

    # Add repo manager config - no changes to this will trigger a rebuild. Default values are set in the constructor.
    app.add_config_value(
        "sphinx_repo_manager",
        SphinxRepoManagerConfig(),
        "",
        SphinxRepoManagerConfig)

    # Connect to the config-inited event -> and only then instantiate SphinxRepoManager.
    # This fires before `builder-inited` and `env-updated` events.
    # For more info on event lifecycle, see:
    #   - https://www.sphinx-doc.org/en/master/extdev/event_callbacks.html#core-events-overview
    app.connect("config-inited", create_repo_manager)

    # Print the extension version
    print(f"[sphinx_repo_manager::setup] Sphinx Repo Manager extension loaded with version: {__version__}")

    # Return extension metadata.
    # See details here:
    #  - https://www.sphinx-doc.org/en/master/extdev/index.html#extension-metadata
    return {
        # The version of the extension.
        "version": __version__,

        # An integer that identifies the version of env data structure if the extension 
        # stores any data to environment. It is used to detect the data structure has been 
        # changed from last build. The extensions have to increment the version when data 
        # structure has changed. If not given, Sphinx considers the extension does not 
        # stores any data to environment.
        # "env_version": None,

        # Parallel reading of source files can be used when the extension is loaded
        "parallel_read_safe": True,

        # Parallel writing of output files can be used when the extension is loaded
        "parallel_write_safe": True,
    }
