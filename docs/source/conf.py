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
import shutil  # Path utils like copy
import sys
from pathlib import Path  # Path manipulation/normalization; allows / slashes for path
from dotenv import load_dotenv
from jinja2 import FileSystemLoader, Environment
from sphinx.jinja2glue import SphinxFileSystemLoader

# Load the .env file
load_dotenv()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'XBE Docs'
copyright = 'Xsolla (USA), Inc. All rights reserved'
author = 'Xsolla'
release = 'v2024.07.0'
version = release

# This should likely match your branch name:
# - EXCEPTION: If a "latest" tracked branch (master/lts/main/some ver tester)
#   - If exception, consider using "latest" or "v{ver_about_to_be_released}-doc"
# release = '%GIT_TAG%'

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

sys.path.insert(0, os.path.abspath(''))

# -- ReadTheDocs (RTD) Config ------------------------------------------------

# Check if we're running on Read the Docs' servers
is_read_the_docs_build = os.environ.get("READTHEDOCS", None) == 'True'  # AKA is_production
fallback_to_production_stage_if_not_rtd = True  # Affects feature flags

rtd_version = is_read_the_docs_build and os.environ.get('READTHEDOCS_VERSION')  # Get the version being built
rtd_version_is_latest = is_read_the_docs_build and rtd_version == 'latest'  # Typically the 'master' branch

# The absolute path to the directory containing conf.py.
documentation_root = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_repo_manager')))
sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_feature_flags')))
sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_openapi')))
sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_image_min')))
sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_algolia_crawler')))
sys.path.append(os.path.abspath('.'))


# -- Inline extensions -------------------------------------------------------
# Instead of making an extension for small things, we can just embed inline
def setup(app):
    app.connect('build-finished', copy_open_graph_img_to_build)

# -- Read normalized repo_manifest.yml ---------------------------------------
# This in-house extension clones repos from repo_manifest.yml and symlinks them into the content directory.
# This allows us to build documentation for multiple versions of the same service.

from _extensions.sphinx_repo_manager import SphinxRepoManager

# Initialize the RepoManager instance with the manifest path
manifest_path = Path('..', 'repo_manifest.yml').resolve()
repo_manager = SphinxRepoManager(manifest_path)
manifest = repo_manager.read_normalize_manifest()

# Extract common props
manifest_stage = manifest['stage']  # 'dev_stage' or 'prod_stage'
manifest_stage_is_production = manifest_stage == 'prod_stage'
manifest_repos = manifest['repositories']  # repos[repo_name] = { url, tag, symlink_path, branch, active, ... }
print(f'[conf.py::repo_manifest.yml] Num repos found: {len(manifest_repos)}')

# TODO: Use these below for dynamic info pulled from repo_manifest.yaml
base_symlink_path = manifest['base_symlink_path']  # eg: "source/content"
repo_sparse_path = manifest['repo_sparse_path']  # eg: "docs"

# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.

html_context = {}  # html_context.update({}) to pass data to extensions & themes
extensions = [
    'myst_parser',  # recommonmark successor
    'sphinx_docsearch',  # AI-powered docsearch | https://pypi.org/project/sphinx-docsearch/
    'sphinx_tabs.tabs',  # Add tabs to code blocks | https://sphinx-tabs.readthedocs.io/en/latest
    'sphinx_algolia_crawler',  # Our own custom extension to crawl our build site for our AI-powered search indexing
    'sphinx_openapi',  # Our own custom extension to download and build OpenAPI docs
    'sphinx_feature_flags',  # Our own custom extension to add a feature-flag:: directive
    'sphinx_image_min',  # Our own custom extension to minimizer images after build from build/ dir (set to CI only)
    'sphinx_repo_manager',  # Our own custom extension to manage repos via repo_manifest.yml
    'sphinx_new_tab_link',  # https://pypi.org/project/sphinx-new-tab-link
    'sphinx_copybutton',  # https://pypi.org/project/sphinx-copybutton
    'sphinxcontrib.redoc',  # Converts OpenAPI spec json files into API docs
    'sphinxcontrib.sass',  # SASS/SCSS -> CSS | https://pypi.org/project/sphinxcontrib-sass
    'sphinx.ext.todo',  # Allows for todo:: directive 
    'sphinxext.opengraph',  # Adds OpenGraph meta tags | https://pypi.org/project/sphinxext-opengraph
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_repos-available',  # We'll be using the symlinked `content` dir, instead
    '**/_build',
    '**/build',
    '**/_recycling_bin',  # Deprecated files organized together
    '**/.DS_Store',
    '**/README.*',
    '**/requirements.txt',
    '**/Thumbs.db',
    '**/venv',
]

html_extra_path = [
    'robots.txt',  # Only index latest ver to crawlers
    'sitemap.xml',  # Show latest ver -> release notes -> feats -> api docs
]

master_doc = 'index'  # Build entry point: The "home page"
tocdepth = 1  # Default :maxdepth:

# Tell sphinx what the primary language being documented is + code highlighting
primary_domain = "cpp"
highlight_language = "cpp"

# -- Sphinx Extension: sphinxext-opengraph ----------------------------
# For embed preview info, such as when link is dropped into Discord/FB.
# https://github.com/wpilibsuite/sphinxext-opengraph?tab=readme-ov-file#options

ogp_site_url = "https://docs.xsolla.cloud/"  # Full https:// url with lingering slash/
ogp_use_first_image = False  # We want to always use our consistent banner; we can potentially per-page override this
ogp_title = project  # "XBE Docs"

# EXTERNAL og:banner @ 1200x630 (minimized) url; TODO: Change this to /latest next patch
ogp_image = 'https://docs.xsolla.cloud/en/v2024.07.0/_images/xbe-banner-og-1200x630.min.png'

ogp_custom_meta_tags = [
    # Image
    '<meta property="og:image:type" content="image/png">',
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
    # '<meta name="description" content="The most complete online gaming platform">',

    # FB
    '<meta property="og:url" content="https://docs.xsolla.cloud/">'
    '<meta property="og:type" content="website">',
    # f'<meta property="og:title" content="{project}">',
    # f'<meta property="og:description" content={ogp_description}>',
    # '<meta property="og:image" content="https://external/link.png">',

    # Twitter / X
    '<meta name="twitter:card" content="summary_large_image">',
    '<meta property="twitter:domain" content="docs.xsolla.cloud">',
    '<meta property="twitter:url" content="https://docs.xsolla.cloud/">',
    # '<meta name="twitter:title" content="Xsolla Backend [XBE] Docs">',
    # '<meta name="twitter:description" content="The most complete online gaming platform">',
    # '<meta name="twitter:image" content="https://external/link.png">',
]


# If we don't use the open graph image directly (we use a smaller variant in the docs),
# We need to manually mv it to the build images dir
def copy_open_graph_img_to_build(app, exception):
    html_og_image = os.path.abspath('source/_static/images/_local/xbe-banner-og-1200x630.min.png')
    build_images_dir = os.path.abspath(os.path.join(app.outdir, '_images'))

    print(f"\n[conf.py::sphinxext.opengraph] Copying og:image locally "
          f"from\n'{html_og_image}'\n"
          f"to\n'{build_images_dir}'\n...")
    shutil.copy(html_og_image, build_images_dir)
    print('Done.\n')


# -- Sphinx Extension: sphinxcontrib-sass ----------------------------------
# SCSS->CSS; doc | https://pypi.org/project/sphinxcontrib-sass

sass_targets = {
    "main.scss": "main.css",
    "redoc.scss": "redoc.css",
    "algolia.scss": "algolia.css",
}
sass_src_dir = "_static/styles/sass"
sass_out_dir = "_static/styles/css"

# -- Sphinx Extension: Image Minimizer -------------------------------------
# Optimizes ../build/_images/ if RTD CI using Pillow

# Configuration for the image optimizer extension
img_optimization_enabled = bool(is_read_the_docs_build)
img_optimization_max_width = 1920

# -- OpenAPI Shared: Used in multiple extensions --------------------------

openapi_dir_path = os.path.abspath(os.path.join('_static', 'specs'))  # Downloads json|yaml files to here

# Link here from rst with explicit ".html" ext (!) but NOT from a doctree
openapi_generated_file_posix_path = Path(os.path.join(
    'content', '-', 'api', 'index')).as_posix()  # Parses to forward/slashes/

# -- Extension: sphinx_openapi (OpenAPI Local Download/Updater) -----------
# Used in combination with the sphinxcontrib.redoc extension
# Use OpenAPI ext to download/update -> redoc ext to generate

# Define the target json|yaml + path to save the downloaded OpenAPI spec
openapi_spec_url_noext = 'https://api.demo.goxbe.cloud/v1/openapi'
sys.path.append(openapi_dir_path)  # TODO: Is this redundant?

# 'json' or 'yaml' (we'll download them both, but generate from only 1)
# (!) Currently, only json is fully functional and, additionally, supports preprocessing in the ext
openapi_file_type = 'json'

# Set the config values for the extension
html_context.update({
    'openapi_spec_url_noext': openapi_spec_url_noext,
    'openapi_dir_path': openapi_dir_path,
    'openapi_generated_file_posix_path': openapi_generated_file_posix_path,
    'openapi_file_type': openapi_file_type,
})

# -- Extension: sphinxcontrib.redoc --------------------------------------
# OpenAPI Docgen: Similar to sphinxcontrib-openapi, but +1 column for example responses
# (!) Prereq: OpenAPI Local Download (above)
# Doc | https://sphinxcontrib-redoc.readthedocs.io/en/stable
# Demo | https://sphinxcontrib-redoc.readthedocs.io/en/stable/api/github/

# (!) Works around a critical bug that default grabs old 1.x ver (that !supports OpenAPI 3+)
redoc_uri = 'https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js'

# Intentional forward/slashes/ for html; eg: "_static/specs/openapi.json"
xbe_spec = openapi_dir_path + '/openapi.json'

redoc = [
    {
        'name': 'Xsolla Backend API',
        'page': openapi_generated_file_posix_path,  # content/-/api/index
        'spec': '_static/specs/openapi.json',
        'embed': True,  # Local file only (!) but embed is less powerful
        'template': '_templates/redoc.j2',
        'opts': {
            'lazy-rendering': True,  # Formerly called `lazy`; almost required for giant docs
            'required-props-first': True,  # Useful, (!) but slower
            'native-scrollbars': False,  # Improves perf on big specs when False
            'expand-responses': ["200", "201"],
            'suppress-warnings': False,
            'hide-hostname': False,
            'untrusted-spec': False,
        }
    },
]

print(f'[conf.py::sphinxcontrib.redoc] Build from redoc[0].spec: {redoc[0]["spec"]}')
print(f'[conf.py::sphinxcontrib.redoc] Displaying at redoc[0].page: {redoc[0]["page"]}')
print('')

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
html_theme = 'sphinx_book_theme'

# The name of the Pygments (syntax highlighting) style to use.
# `sphinx` works very well with the RTD theme, but you can always change it
pygments_style = "monokai"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ['_static']

html_css_files = [
    'styles/css/main.css',
    # 'https://cdn.jsdelivr.net/npm/@docsearch/css@3',
    'styles/css/algolia.css',
]

html_js_files = [
    # 'https://cdn.jsdelivr.net/npm/@docsearch/js@3',
    ('js/algolia.js', {'defer': 'defer'}),
]

html_logo = '_static/images/_local/logo.png'
html_favicon = '_static/images/_local/favicon.ico'

# The theme to use for HTML and HTML Help pages
html_theme_options = {
    # # RTD THEME (DEPRECATED) >>
    # 'nav_title': project,  # Appears in opengraph metadata, meta title & top breadcrumbs
    # 'base_url': 'https://docs.xsolla.cloud/',
    # 'color_primary': 'blue', 
    # 'color_accent': 'light-blue',
    # 'repo_url': 'https://gitlab.acceleratxr.com/Core/xbe_docs/',
    # 'repo_name': 'xbe_docs',
    # 'globaltoc_depth': 2,  # Visible levels of the global TOC; Default: 2
    # 'globaltoc_collapse': False,  # Expand the global TOC by default
    # 'globaltoc_includehidden': True,  # Show the TOC in the sidebar
    # 'master_doc': 'index', # Set the master doc for the project

    # BOOK THEME >>
    'show_toc_level': 2,
    'home_page_in_toc': False,
    "path_to_docs": "docs/source/",
    "repository_provider": "gitlab",
    "repository_url": "https://gitlab.acceleratxr.com/Core/xbe_docs",
    "repository_branch": "main",
    "max_navbar_depth": 2,
    "show_navbar_depth": 1,  # Gow deep should we initially auto-expand the left navbar?
    "pygments_dark_style": "monokai",  # May get overwritten by pygments_style
    "pygments_light_style": "monokai",  # May get overwritten by pygments_style
    "use_fullscreen_button": False,  # Redundant in modern browsers
    "use_download_button": False,  # Redundant in modern browsers
    "use_repository_button": True,
    "use_edit_page_button": False,
    "use_issues_button": True,
    "icon_links": [  # TODO: Perhaps add something from https://shields.io ?
        {
            "name": "Discord",
            "url": "https://discord.gg/XsollaBackend",
            "icon": "fa-brands fa-discord",
            "attributes": {"target": "_blank"},
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
html_context.update({
    # Edit on GitLab >>
    'display_gitlab': True,  # Integrate Gitlab
    'gitlab_host': 'gitlab.acceleratxr.com',
    'gitlab_user': 'Core',  # Group
    'gitlab_repo': 'xbe_docs',  # Repo name
    'conf_py_path': '/docs/source/',  # /path/to/docs/source (containing conf.py)
    'gitlab_version': 'master',  # Version
    'doc_path': 'docs/source',
})

source_suffix = ['.rst', '.md']  # Use MyST to auto-convert .md

# -- Sphinx Extension: Algolia Crawler ----------------------------------------------------------------------------
# Crawling is *slow* and temporarily takes search offline while reindexing: Only trigger @ RTD /latest prod build
# (!) /dev builds can be manually triggered: Use `sphinx_algolia_crawler.py` standalone or see root proj .env.template

algolia_crawler_enabled = rtd_version_is_latest

# -- Sphinx Extension: sphinxext_docsearch ------------------------------------------------------------------------
# Algolia DocSearch support | https://sphinx-docsearch.readthedocs.io/configuration.html 

algolia_docsearch_app_id_dev = "DBTSGB2DXO"
algolia_docsearch_app_id_prod = "CKS2O35GXS"

docsearch_app_id = algolia_docsearch_app_id_prod if manifest_stage_is_production \
    else algolia_docsearch_app_id_dev

# Which index to select? 'dev_stage' or 'production_stage' (None skips extension)
docsearch_index_name = "xsolla"  # From Algolia dash "Data Sources" -> "Indices"

# Public read key
docsearch_api_key_dev = "a98b6eb7635b38887be38212d12318fa"
docsearch_api_key_prod = "4ebb45dbcdd78f224f1b24c28ba7fd9e"
docsearch_api_key = docsearch_api_key_prod if manifest_stage_is_production \
    else docsearch_api_key_dev

# docsearch_container = ".sidebar-primary-item"  # We want to use our own search bar
docsearch_container = "#search-input"  # Arbitrary - we just want it to spawn "somewhere" since we use our own search bar

docsearch_missing_results_url = (f"https://{html_context['gitlab_host']}/{html_context['gitlab_user']}/"
                                 f"{html_context['gitlab_repo']}/-/issues/new?issue[title]=${{query}}")

html_context.update({
    "docsearch_app_id": docsearch_app_id,
    "docsearch_api_key": docsearch_api_key,
    "docsearch_index_name": docsearch_index_name,
})

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
    'production-stage': is_read_the_docs_build or fallback_to_production_stage_if_not_rtd,

    # True: [Navbar, Docs] Create Acct -> AXR pricing si te
    # False: New login page @ https://xsolla.cloud 
    'use-new-price-page-url': False,

    # True: Show web app libs (xbeapp, react, etc) - False: Hide
    'welcome-release_notes-products_web_apps-libs': False,

    # True: Show new openapi docs & hide old ones - False: Hide new openapi docs, show placeholders
    'new-xbe-openapi-doc': True,
}

# -- Append rst_epilog to the bottom of *every* doc file ---------------------
# rst_epilog = ".. |theme| replace:: ``{0}``".format(html_theme)
