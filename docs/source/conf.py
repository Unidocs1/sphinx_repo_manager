##############################################################################
# Configuration file for the Sphinx documentation builder.
# (!) THIS FILE IS IGNORED IF PULLED BY THE MAIN DOC - USED FOR LOCAL TESTING
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
##############################################################################
import os
import shutil
import sys
import git
from pathlib import Path
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# -- Path setup --------------------------------------------------------------
# The absolute path to the directory containing conf.py.
documentation_root = Path(os.path.dirname(__file__)).absolute()
sys.path.insert(0, os.path.abspath(""))

# -- Read normalized repo_manifest.yml ---------------------------------------
# This in-house extension clones repos from repo_manifest.yml and symlinks them into the content directory.
# This allows us to build documentation for multiple versions of the same service.

from sphinx_repo_manager import SphinxRepoManager

# Initialize the RepoManager instance with the manifest path
repo_manager_manifest = Path("..", "repo_manifest.yml").resolve()
repo_manager = SphinxRepoManager()
manifest = repo_manager.get_normalized_manifest(repo_manager_manifest)

# Extract common props
manifest_stage = manifest["stage"]  # 'dev_stage' or 'prod_stage'
manifest_stage_is_production = manifest_stage == "prod_stage"
manifest_repos = manifest[
    "repositories"
]  # repos[repo_name] = { url, tag, symlink_path, branch, active, ... }
xbe_static_docs_repo = manifest_repos["xbe_static_docs"]
macro_ver = xbe_static_docs_repo["production_stage"]["checkout"]  # eg: "v2024.07.0"
print("")
print(f"[conf.py::repo_manifest.yml] Manifest num repos found: {len(manifest_repos)}")
print(f"[conf.py::repo_manifest.yml] Manifest stage: '{manifest_stage}'")
print(f"[conf.py::repo_manifest.yml] Manifest macro ver: '{macro_ver}'")
print("")

# TODO: Use these below for dynamic info pulled from repo_manifest.yaml
base_symlink_path = manifest["base_symlink_path"]  # eg: "source/content"
repo_sparse_path = manifest["repo_sparse_path"]  # eg: "docs"

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "XBE Docs"
copyright = "Xsolla (USA), Inc. All rights reserved"
author = "Xsolla"
release = macro_ver  # eg: "v2024.08.0"
version = release  # Used by some extensions
html_context = {}  # html_context.update({}) to pass data to extensions & themes

# Set the project URL and branch from the environment variables
project_url = os.environ.get("PROJECT_URL", None)
current_branch = os.environ.get("PROJECT_BRANCH", None)
project_name = os.environ.get("PROJECT_NAME", "xbe_example")


# If not set, try to get the project URL and branch from the git repo
if not project_url or not current_branch:
    try:
        project_name = "xbe_example"
        repo = git.Repo(search_parent_directories=True)
        current_branch = repo.active_branch.name
        project_url = repo.remotes.origin.url
    except Exception as e:
        print(
            "Please set the `PROJECT_URL` and `PROJECT_BRANCH` environment variables."
        )

project_brief = "XBE Doxygen Template"
project_group = "Xsolla"
project_repo = f"{project_name}"
api_src_input = "src"


# -- ReadTheDocs (RTD) Config ------------------------------------------------

# Check if we're running on Read the Docs' servers
is_read_the_docs_build = os.environ.get("READTHEDOCS", None) == "True"

rtd_version = is_read_the_docs_build and os.environ.get(
    "READTHEDOCS_VERSION"
)  # Get the version being built
rtd_version_is_latest = (
    is_read_the_docs_build and rtd_version == "latest"
)  # Typically the 'master' branch

# Set canonical URL from the Read the Docs Domain
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")
html_context["READTHEDOCS"] = is_read_the_docs_build

# --- Breathe configuration ---

breathe_projects = {}
doxygen_root = "_doxygen"


def configure_doxygen_breathe(app):
    base_dir = Path(app.srcdir, doxygen_root)
    print(f"\n[conf.py::breathe] Configuring Breathe projects from {base_dir}...")
    for project_name in os.listdir(base_dir):
        path = base_dir.joinpath(project_name)
        if os.path.isdir(path):
            print(
                f"[conf.py::breathe] Registering Breathe project: '{project_name}': '{path}'"
            )
            breathe_projects[project_name] = path
    print("Done.\n")


# --- End of Breathe configuration ---

# --- C# domain configuration ---
sphinx_csharp_test_links = False
sphinx_csharp_multi_language = True
sphinx_csharp_ignore_xref = [
    "xbe.sdk.Source.Interfaces.IUidHandler",
    "xbe.sdk.IAPIClient",
    "T",
    "Task",
    "Guid",
    "KeyCollection",
    "KeyValuePair",
    "PropertyInfo",
    "FieldInfo",
    "DeleteMemberBinder",
    "GetMemberBinder",
    "SetMemberBinder",
    "DateTime",
    "IDynamicMetaObjectProvider",
    "HttpClientHandler",
    "IEquatable",
    "Callback",
    "JsonReader",
    "xbe.sdk.Network.IConnection",
    "JsonWriter",
    "HttpResponseMessage",
    "IAPIClient",
    "StreamingContext",
    "HttpMethod",
    "xbe.sdk.ILogger",
    "HttpStatusCode",
    "CancellationToken",
    "Uri",
    "JsonConverter",
    "ClientWebSocket",
    "Attribute",
    "DynamicObject",
    "OnUnknownMessage",
    "Exception",
    "SerializationInfo",
    "ILogger",
    "Encoding",
    "HttpClient",
    "JsonSerializer",
    "CancellationTokenSource",
    "ValidationParameters",
    "OnSocketMessage",
    "PushMessage",
    "Vector2",
    "Vector3",
    ">",
    
]
# --- End of C# Domain ----


# -- Inline extensions -------------------------------------------------------
# Instead of making an extension for small things, we can just embed inline
def setup(app):
    app.connect("builder-inited", configure_doxygen_breathe)
    app.connect("build-finished", copy_open_graph_img_to_build)


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "myst_parser",  # recommonmark successor, auto-parsing .md to .rst (skips READMEs)
    "sphinx_docsearch",  # AI-powered docsearch | https://pypi.org/project/sphinx-docsearch/
    "sphinx_tabs.tabs",  # Add tabs to code blocks | https://sphinx-tabs.readthedocs.io/en/latest
    "sphinx_algolia_crawler",  # Our own custom extension to crawl our build site for our AI-powered search indexing
    "sphinx_feature_flags",  # Our own custom extension to add a feature-flag:: directive
    "sphinx_image_min",  # Our own custom extension to minimizer images after build from build/ dir (set to CI only)
    "sphinx_repo_manager",  # Our own custom extension to manage repos via repo_manifest.yml
    "sphinx_new_tab_link",  # https://pypi.org/project/sphinx-new-tab-link
    "sphinx_copybutton",  # https://pypi.org/project/sphinx-copybutton
    "sphinxcontrib.redoc",  # Converts OpenAPI spec json files into API docs
    "sphinxcontrib.sass",  # SASS/SCSS -> CSS | https://pypi.org/project/sphinxcontrib-sass
    "sphinx.ext.todo",  # Allows for todo:: directive
    "sphinxext.opengraph",  # Adds OpenGraph meta tags | https://pypi.org/project/sphinxext-opengraph
    "sphinx_design",  # Adds FontAwesome and more | https://sphinx-design.readthedocs.io/en/latest/get_started.html
    "sphinx_remove_toctrees",  # Remove specific toctrees | https://pypi.org/project/sphinx-remove-toctrees
    "sphinx_openapi",  # Our own custom extension to download and build OpenAPI docs
]

if is_read_the_docs_build:
    print("[conf.py::extensions] Adding breathe + sphinx_csharp extensions since is_read_the_docs_build (+7m build time)")
    extensions.append("breathe")  # Breathe extension for Doxygen XML to Sphinx | https://breathe.readthedocs.io/en/latest/
    extensions.append("sphinx_csharp")  # C# extension for breathe | https://github.com/rogerbarton/sphinx-csharp
else:
    print("[conf.py::extensions] WARNING: [ breathe, sphinx_csharp ] skipped since not is_read_the_docs_build (saves 7m build time)")

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_repos-available",  # We'll be using the symlinked `content` dir, instead
    "**/_build",
    "**/build",
    "**/_recycling_bin",  # Deprecated files organized together
    "**/.DS_Store",
    "**/README*",
    "**/requirements.txt",
    "**/Thumbs.db",
    "**/venv",
]

html_extra_path = [
    "robots.txt",  # Only index latest ver to crawlers
    "sitemap.xml",  # Show latest ver -> release notes -> feats -> api docs
]

master_doc = "index"  # Build entry point: The "home page"
tocdepth = 1  # Default :maxdepth:

# Tell sphinx what the primary language being documented is + code highlighting
primary_domain = "cpp"
highlight_language = "cpp"

# -- Sphinx Extension: sphinxext-opengraph ----------------------------
# For embed preview info, such as when link is dropped into Discord/FB.
# https://github.com/wpilibsuite/sphinxext-opengraph?tab=readme-ov-file#options

ogp_site_url = "https://docs.goxbe.io/"  # Full https:// url with lingering slash/
ogp_use_first_image = False  # We want to always use our consistent banner; we can potentially per-page override this
ogp_title = project  # "XBE Docs"

# EXTERNAL og:banner @ 1200x630 (minimized) url; TODO: Change this to /latest next patch
ogp_image = "https://docs.goxbe.io/en/v2024.07.0/_images/xbe-banner-og-1200x630.min.png"

ogp_custom_meta_tags = [
    # Image
    '<meta property="og:image:type" content="image/png">',
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
    # '<meta name="description" content="The most complete online gaming platform">',
    # FB
    '<meta property="og:url" content="https://docs.goxbe.io/">'
    '<meta property="og:type" content="website">',
    # f'<meta property="og:title" content="{project}">',
    # f'<meta property="og:description" content={ogp_description}>',
    # '<meta property="og:image" content="https://external/link.png">',
    # Twitter / X
    '<meta name="twitter:card" content="summary_large_image">',
    '<meta name="twitter:domain" content="docs.goxbe.io">',
    # '<meta name="twitter:title" content="Xsolla Backend [XBE] Docs">',
    # '<meta name="twitter:description" content="The most complete online gaming platform">',
    # '<meta name="twitter:image" content="https://external/link.png">',
]


# [post-build::low priority] If we don't use the open graph image directly (we use a smaller variant in the root index),
# We need to manually mv it to the build images dir
def copy_open_graph_img_to_build(app, exception):
    html_og_image = (
        Path(app.srcdir)
        / "_static"
        / "images"
        / "_local"
        / "xbe-banner-og-1200x630.min.png"
    )
    build_images_dir = Path(app.outdir) / "_images"

    print(
        f"\n[conf.py::sphinxext.opengraph] Copying og:image locally "
        f"from\n'{html_og_image}'\n"
        f"to\n'{build_images_dir}'\n..."
    )

    shutil.copy(html_og_image, build_images_dir)
    print("Done.\n")


# -- Sphinx Extension: sphinx-remove-toctrees ------------------------------
# Remove specific toctrees from the sidebar; supports wildcards

remove_from_toctrees = [
    # "content/-/welcome/release_notes/current/service_updates-partial.rst",
]

# -- Sphinx Extension: sphinxcontrib-sass ----------------------------------
# SCSS->CSS; doc | https://pypi.org/project/sphinxcontrib-sass

sass_targets = {
    "main.scss": "main.css",
    "redoc.scss": "redoc.css",
    "algolia.scss": "algolia.css",
}
sass_src_dir = "_sass"
sass_out_dir = "_static/styles/css"
# -- End of sphinxcontrib-sass configuration -------------------------------

# -- Sphinx Extension: sphinx_image_min -----------------------------------
# Optimizes ../build/_images/ if RTD CI using Pillow

# Configuration for the image optimizer extension
img_optimization_enabled = bool(is_read_the_docs_build)
img_optimization_max_width = 1920

# -- OpenAPI Shared: Used in multiple extensions --------------------------

# Downloads json|yaml files to here
openapi_dir_path = Path("_static", "specs").absolute().as_posix()

# Link here from rst with explicit ".html" ext (!) but NOT from a doctree
openapi_generated_file_posix_path = Path(
    "content", "-", "api", "index"
).as_posix()  # Parses to forward/slashes/

# -- Extension: sphinx_openapi (OpenAPI Local Download/Updater) -----------
# Used in combination with the sphinxcontrib.redoc extension
# Use OpenAPI ext to download/update -> redoc ext to generate

# Define the target json|yaml + path to save the downloaded OpenAPI spec
openapi_spec_url_noext = "https://api.demo.goxbe.cloud/v1/openapi"

# 'json' or 'yaml' (we'll download them both, but generate from only 1)
# (!) Currently, only json is fully functional and, additionally, supports preprocessing in the ext
openapi_file_type = "json"

# Set the config values for the extension
html_context.update(
    {
        "openapi_spec_url_noext": openapi_spec_url_noext,
        "openapi_dir_path": openapi_dir_path,
        "openapi_generated_file_posix_path": openapi_generated_file_posix_path,
        "openapi_file_type": openapi_file_type,
    }
)

# -- Extension: sphinxcontrib.redoc --------------------------------------
# OpenAPI Docgen: Similar to sphinxcontrib-openapi, but +1 column for example responses
# (!) Prereq: OpenAPI Local Download (above)
# Doc | https://sphinxcontrib-redoc.readthedocs.io/en/stable
# Demo | https://sphinxcontrib-redoc.readthedocs.io/en/stable/api/github/

# (!) Works around a critical bug that default grabs old 1.x ver (that !supports OpenAPI 3+)
redoc_uri = "https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"

# Intentional forward/slashes/ for html; eg: "_static/specs/openapi.json"
xbe_spec = Path(openapi_dir_path, "openapi.json")

redoc = [
    {
        "name": "Xsolla Backend API",
        "page": openapi_generated_file_posix_path,  # content/-/api/index
        "spec": "_static/specs/openapi.json",
        "embed": True,  # Local file only (!) but embed is less powerful
        "template": "_templates/redoc.j2",
        "opts": {
            "lazy-rendering": True,  # Formerly called `lazy`; almost required for giant docs
            "required-props-first": True,  # Useful, (!) but slower
            "native-scrollbars": False,  # Improves perf on big specs when False
            "expand-responses": [],  # "200", "201",
            "suppress-warnings": False,
            "hide-hostname": False,
            "untrusted-spec": False,
        },
    },
]

print(f'[conf.py::sphinxcontrib.redoc] Build from redoc[0].spec: {redoc[0]["spec"]}')
print(f'[conf.py::sphinxcontrib.redoc] Displaying at redoc[0].page: {redoc[0]["page"]}')
print("")

# -- Extension: sphinx.ext.todo ------------------------------------------
# Support for `todo` directive, passing it during sphinx builds
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html

todo_include_todos = False  # If this is True, todo and todolist produce output, else they produce nothing. The default is False.
todo_emit_warnings = False  # If this is True, todo emits a warning for each TODO entries. The default is False.
todo_link_only = False  # If this is True, todolist produce output without file path and line, The default is False.

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_book_theme"

# The name of the Pygments (syntax highlighting) style to use.
# `sphinx` works very well with the RTD theme, but you can always change it
pygments_style = "monokai"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ["_static"]

html_css_files = [
    "styles/css/main.css",
    # 'https://cdn.jsdelivr.net/npm/@docsearch/css@3',
    "styles/css/algolia.css",
    # "styles/css/redoc.css",
]

html_js_files = [
    # 'https://cdn.jsdelivr.net/npm/@docsearch/js@3',
    ("js/algolia.js", {"defer": "defer"}),
]

html_logo = "_static/images/_local/logo.png"
html_favicon = "_static/images/_local/favicon.ico"

html_context.update(
    {
        # SPHINX BOOK THEME (based on Sphinx PyData theme) >>
        # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/light-dark.html#configure-default-theme-mode
        "default_mode": "dark",
    }
)

# The theme to use for HTML and HTML Help pages
html_theme_options = {
    # Use OS light/dark theme prefs? https://pydata-sphinx-theme.readthedocs.io/en/latest/user_guide/light-dark.html
    "show_toc_level": 2,
    "show_nav_level": 1,  # Collapsable toctree :caption:
    "max_navbar_depth": 2,
    "show_navbar_depth": 1,  # How deep should we initially auto-expand the left navbar?
    "collapse_navbar": 1,  # 1 == collapse the initial homepage navbar, stopping the tree from being expanded
    "home_page_in_toc": False,
    "path_to_docs": "docs/source/",
    "repository_provider": "gitlab",
    "repository_url": "https://source.goxbe.io/Core/docs/sphinx_repo_manager",
    "repository_branch": "main",
    "pygments_dark_style": "monokai",  # May get overwritten by pygments_style
    "pygments_light_style": "monokai",  # May get overwritten by pygments_style
    "use_fullscreen_button": False,  # Redundant in modern browsers
    "use_download_button": False,  # Redundant in modern browsers
    "use_repository_button": True,
    "use_edit_page_button": False,
    "use_issues_button": True,
    "icon_links": [  # TODO: Perhaps add something from https://shields.io ?
        {
            "name": "API Docs",
            "url": (
                "https://docs.goxbe.io/en/"
                + ("latest" if manifest_stage_is_production else "dev")
                + "/content/-/api/index.html"
            ),
            "icon": "fa-solid fa-book-open",
            "attributes": {"target": "_self"},
        },
        {
            "name": "Discord",
            "url": "https://discord.gg/XsollaBackend",
            "icon": "fa-brands fa-discord",
            "attributes": {"target": "_blank"},  # Blank target seems to be default
        },
    ],
    "article_header_end": [
        "navbar-icon-links",
        "article-header-buttons",
    ],
}

html_sidebars = {
    "**": [
        "navbar-logo",
        "search-button-field",
        "sbt-sidebar-nav",
    ],
}

# This swaps vals in the actual built HTML (NOT the rst files).
# Eg: This is used with themes and third-party extensions;
# Doc | https://docs.readthedocs.io/en/stable/guides/edit-source-links-sphinx.html#gitlab
# (!) `{{templating}}` in rst files with these *won't* work here:
html_context.update(
    {
        # Edit on GitLab >>
        "display_gitlab": True,  # Integrate Gitlab
        "gitlab_host": "source.goxbe.io",
        "gitlab_user": "Core",  # Group
        "gitlab_repo": "sphinx_repo_manager",  # Repo name
        "conf_py_path": "/docs/source/",  # /path/to/docs/source (containing conf.py)
        "gitlab_version": "master",  # Version
        "doc_path": "docs/source",
    }
)

source_suffix = [".rst", ".md"]  # Use MyST to auto-convert .md

# -- Sphinx Extension: Algolia Crawler ----------------------------------------------------------------------------
# Crawling is *slow* and temporarily takes search offline while reindexing: Only trigger @ RTD /latest prod build
# (!) /dev builds can be manually triggered: Use `sphinx_algolia_crawler.py` standalone or see root proj .env.template

algolia_crawler_enabled = rtd_version_is_latest

# -- Sphinx Extension: sphinxext_docsearch ------------------------------------------------------------------------
# Algolia DocSearch support | https://sphinx-docsearch.readthedocs.io/configuration.html

algolia_docsearch_app_id_dev = "DBTSGB2DXO"
algolia_docsearch_app_id_prod = "CKS2O35GXS"

docsearch_app_id = (
    algolia_docsearch_app_id_prod
    if manifest_stage_is_production
    else algolia_docsearch_app_id_dev
)

# Which index to select? 'dev_stage' or 'production_stage' (None skips extension)
docsearch_index_name = "xsolla"  # From Algolia dash "Data Sources" -> "Indices"

# Public read key
docsearch_api_key_dev = "a98b6eb7635b38887be38212d12318fa"
docsearch_api_key_prod = "4ebb45dbcdd78f224f1b24c28ba7fd9e"
docsearch_api_key = (
    docsearch_api_key_prod if manifest_stage_is_production else docsearch_api_key_dev
)

# docsearch_container = ".sidebar-primary-item"  # We want to use our own search bar
docsearch_container = "#search-input"  # Arbitrary - we just want it to spawn "somewhere" since we use our own search bar

docsearch_missing_results_url = (
    f"https://{html_context['gitlab_host']}/{html_context['gitlab_user']}/"
    f"{html_context['gitlab_repo']}/-/issues/new?issue[title]=${{query}}"
)

html_context.update(
    {
        "docsearch_app_id": docsearch_app_id,
        "docsearch_api_key": docsearch_api_key,
        "docsearch_index_name": docsearch_index_name,
    }
)

# -- MyST configuration ------------------------------------------------------
# Recommonmark successor to auto-parse .md to .rst

# Configuration for MyST-Parser
myst_enable_extensions = [
    "amsmath",  # Enable parsing and rendering of AMS math syntax
    "dollarmath",  # Enable dollar math syntax
    "html_admonition",  # Enable HTML admonitions
    "html_image",  # Enable HTML image tags
    "colon_fence",  # Enable colon fences for directives/roles
    "smartquotes",  # Enable smart quotes
    "replacements",  # Enable replacements syntax
    "strikethrough",  # Enable strikethrough syntax
    "tasklist",  # Enable task list syntax
    # Recommended for use with sphinx_design. Doc | https://sphinx-design.readthedocs.io/en/latest/get_started.html
    # Ext | https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
    "colon_fence",
]

# -- Feature Flags -----------------------------------------------------------
# Turn any block of docs on/off - with optional fallbacks. EXAMPLE USE:
"""
.. feature-flag:: dev_toctree

   This will show if True

.. feature-flag:: dev_toctree
   :fallback:

   This will show if False
"""

feature_flags = {
    # True: Nothing - False: Show dev toctree
    "dev-debug-mode": False,
    # True: [Navbar, Docs] Create Acct -> AXR pricing si te
    # False: New login page @ https://xsolla.cloud
    "use-new-price-page-url": False,
    # True: Show web app libs (xbeapp, react, etc) - False: Hide
    "welcome-release_notes-products_web_apps-libs": False,
    # True: Show new openapi docs & hide old ones - False: Hide new openapi docs, show placeholders
    "new-xbe-openapi-doc": True,
}

# -- Globally declare replacement items at the top of *every* doc file -------------
# (!) These do not work in toctrees

rst_prolog = """
.. |docs-wip| replace:: :bdg-info-line:`Docs WIP`
"""
