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
import subprocess
import sys
import git
import shutil
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project_title = "XBE Docs"
author = "Xsolla"
copyright = "Xsolla (USA), Inc. All rights reserved"

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

release = "v2024.07.0"
version = release  # Used by some extensions

# -- Path setup --------------------------------------------------------------
# The absolute path to the directory containing conf.py.
documentation_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(""))

# -- ReadTheDocs (RTD) Config ------------------------------------------------
# Check if we're running on Read the Docs' servers
is_read_the_docs_build = (
    os.environ.get("READTHEDOCS", None) == "True"
)  # AKA is_production
fallback_to_production_stage_if_not_rtd = True  # Affects feature flags

rtd_version = is_read_the_docs_build and os.environ.get(
    "READTHEDOCS_VERSION"
)  # Get the version being built
rtd_version_is_latest = (
    is_read_the_docs_build and rtd_version == "latest"
)  # Typically the 'master' branch

# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # "myst_parser",
    # "sphinx_tabs.tabs",
    # "sphinx_new_tab_link",
    # "sphinx_copybutton",
    # "sphinxcontrib.sass",
    # "sphinx.ext.todo",
    # "sphinxext.opengraph",
    # "sphinx_design",
    "breathe",
    "sphinx_csharp",
]

html_context = {}
breathe_projects = {}

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

html_extra_path = []
master_doc = "content/index"
tocdepth = 1

primary_domain = "cpp"
highlight_language = "cpp"

# --- Breathe configuration ---
breathe_default_project = project_name
breathe_projects[project_name] = f"_doxygen/{project_name}"
# --- End of Breathe configuration ---

# -- Doxygen configuration ---------------------------------------------------
# Check if we're running Doxygen
run_doxygen = os.environ.get("DOXYGEN", None) == "True"
if run_doxygen:
    # Remove the existing doxygen output
    shutil.rmtree(breathe_projects[project_name], ignore_errors=True)

    # Run doxygen on configured Doxyfile
    subprocess.call("cd .. && doxygen Doxyfile", shell=True)
# --- End of Doxygen configuration ---


# -- Exhale configuration ---------------------------------------------------
# Check if we're running Exhale
run_exhale = os.environ.get("EXHALE", None) == "True"
if run_exhale:
    # Add the exhale extension
    extensions.append("exhale")

    # Remove the existing api rst files
    api_rst_output = "./source/content/api"
    shutil.rmtree(api_rst_output, ignore_errors=True)

    # Setup the exhale extension
    exhale_args = {
        # These arguments are required
        "containmentFolder": api_rst_output,
        "rootFileName": "index.rst",
        "rootFileTitle": f"{project_brief} - API Reference",
        "afterTitleDescription": "",
        "createTreeView": True,
        "fullToctreeMaxDepth": 1,
        "doxygenStripFromPath": f"../{api_src_input}",
        "unabridgedOrphanKinds": {"typedef", "function", "file"},
    }
# --- End of Exhale configuration ---

# --- C# domain configuration ---
sphinx_csharp_test_links = True
sphinx_csharp_multi_language = True

sphinx_csharp_ignore_xref = [
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
    "Vector2",
    "Vector3",
    ">",
]

sphinx_csharp_ext_search_pages = {}
sphinx_csharp_ext_type_map = {}
sphinx_csharp_external_type_rename = {}

# Debug options
sphinx_csharp_debug = False
sphinx_csharp_debug_parse = False
sphinx_csharp_debug_parse_func = False
sphinx_csharp_debug_parse_var = False
sphinx_csharp_debug_parse_prop = False
sphinx_csharp_debug_parse_attr = False
sphinx_csharp_debug_parse_idxr = False
sphinx_csharp_debug_parse_type = False
sphinx_csharp_debug_xref = False
sphinx_csharp_debug_ext_links = False
# --- End of C# Domain ----

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
    "styles/css/algolia.css",
    # "styles/css/redoc.css",
    # 'https://cdn.jsdelivr.net/npm/@docsearch/css@3',
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
        "default_mode": "dark",  # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/light-dark.html#configure-default-theme-mode
    }
)

# The theme to use for HTML and HTML Help pages
html_theme_options = {
    # BOOK THEME >>
    "show_toc_level": 2,
    "home_page_in_toc": False,
    "path_to_docs": "docs/source/",
    "repository_provider": "gitlab",
    "repository_url": f"{project_url}",
    "repository_branch": f"{current_branch}",
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
            "name": "API Docs",
            "url": (
                "https://docs.xsolla.cloud/en/"
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
        "gitlab_repo": project_repo,  # Repo name
        "gitlab_version": current_branch,  # Repo branch
        "conf_py_path": "/docs/source/",  # /path/to/docs/source (containing conf.py)
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
    "production-stage": is_read_the_docs_build
    or fallback_to_production_stage_if_not_rtd,
    # True: [Navbar, Docs] Create Acct -> AXR pricing si te
    # False: New login page @ https://xsolla.cloud
    "use-new-price-page-url": False,
    # True: Show web app libs (xbeapp, react, etc) - False: Hide
    "welcome-release_notes-products_web_apps-libs": False,
    # True: Show new openapi docs & hide old ones - False: Hide new openapi docs, show placeholders
    "new-xbe-openapi-doc": True,
}

# -- Append rst_epilog to the bottom of *every* doc file ---------------------
# rst_epilog = ".. |theme| replace:: ``{0}``".format(html_theme)
