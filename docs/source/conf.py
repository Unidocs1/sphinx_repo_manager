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
import sys
from pathlib import Path  # Path manipulation/normalization; allows / slashes for path

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Xsolla XBE'
copyright = 'Xsolla (USA), Inc. All rights reserved'
author = 'Xsolla'
release = '2024.07.0-TEST'

# This should likely match your branch name:
# - EXCEPTION: If a "latest" tracked branch (master/lts/main/some ver tester)
#   - If exception, consider using "latest" or "v{ver_about_to_be_released}-doc"
# release = '%GIT_TAG%'


# -- Inline extensions -------------------------------------------------------
# Instead of making an extension for small things, we can just embed inline
def setup(app):
    app.add_css_file(os.path.normpath('styles/main.css'))  # Allow for custom styling

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

sys.path.insert(0, os.path.abspath(''))

# -- ReadTheDocs (RTD) Config ------------------------------------------------

# Check if we're running on Read the Docs' servers
read_the_docs_build = os.environ.get("READTHEDOCS", None) == 'True'

# The absolute path to the directory containing conf.py.
documentation_root = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_repo_manager')))
sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_feature_flags')))
sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_openapi')))
sys.path.append(os.path.abspath('.'))

# -- Read normalized repo_manifest.yml ---------------------------------------
# This in-house extension clones repos from repo_manifest.yml and symlinks them into the content directory.
# This allows us to build documentation for multiple versions of the same service.

from _extensions.sphinx_repo_manager import SphinxRepoManager

# Initialize the RepoManager instance with the manifest path
manifest_path = Path('..', 'repo_manifest.yml').resolve()
repo_manager = SphinxRepoManager(manifest_path)
manifest = repo_manager.read_normalize_manifest()

# Extract common props
repos = manifest['repositories']  # repos[repo_name] = { url, tag, symlink_path, branch, active, ... }
print(f'[conf.py::repo_manifest.yml] Num repos found: {len(repos)}')

# TODO: Use these below for dynamic info pulled from repo_manifest.yaml
base_symlink_path = manifest['base_symlink_path']  # eg: "source/content"
repo_sparse_path = manifest['repo_sparse_path']  # eg: "docs"

# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.

html_context = {}  # html_context.update({}) to pass data to extensions & themes
extensions = [
    'myst_parser',  # recommonmark successor
    'sphinx.ext.intersphinx',
    'sphinx_tabs.tabs',
    'sphinx_openapi',  # Our own custom extension to download and build OpenAPI docs
    'sphinx_feature_flags',  # Our own custom extension to add a feature-flag:: directive
    'sphinx_repo_manager',  # Our own custom extension to manage repos via repo_manifest.yml
    'sphinx_new_tab_link',  # https://pypi.org/project/sphinx-new-tab-link
    'sphinx_copybutton',  # https://pypi.org/project/sphinx-copybutton
    'sphinxcontrib.redoc',  # Converts OpenAPI spec json files into API docs
    'sphinx.ext.todo',  # Allows for todo:: directive 
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

master_doc = 'index'  # Build entry point: The "home page"
tocdepth = 1  # Default :maxdepth:

# Tell sphinx what the primary language being documented is + code highlighting
primary_domain = "cpp"
highlight_language = "cpp"

# -- Extension: sphinx_openapi (OpenAPI Local Download/Updater) -----------
# Used in combination with the sphinxcontrib.redoc extension
# Use OpenAPI ext to download/update -> redoc ext to generate

# Define the target json|yaml + path to save the downloaded OpenAPI spec
openapi_spec_url_noext = 'https://api.dev.xbe.xsolla.cloud/v1/openapi'
openapi_dir_path = '_specs'  # Downloads json|yaml files to here
openapi_file_type = 'json'  # 'json' or 'yaml' (we'll download them both, but generate from only 1)

# Link here from rst with explicit ".html" ext (!) but NOT from a doctree
openapi_generated_file_posix_path = Path(os.path.join(
    'content', '-', 'api', 'index')).as_posix()  # Parses to forward/slashes/

# Set the config values for the extension
html_context.update({
    'openapi_spec_url_noext': openapi_spec_url_noext,
    'openapi_dir_path': openapi_dir_path,
    'openapi_generated_file_posix_path': openapi_generated_file_posix_path,
    'openapi_file_type': openapi_file_type,
})

# -- Extension: sphinx.ext.todo ------------------------------------------
# Support for `todo` directive, passing it during sphinx builds
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html

todo_include_todos = False  # If this is True, todo and todolist produce output, else they produce nothing. The default is False.
todo_emit_warnings = False  # If this is True, todo emits a warning for each TODO entries. The default is False.
todo_link_only = False  # If this is True, todolist produce output without file path and line, The default is False.

# -- Extension: sphinxcontrib.redoc --------------------------------------
# OpenAPI Docgen: Similar to sphinxcontrib-openapi, but +1 column for example responses
# (!) Prereq: OpenAPI Local Download (above)
# Doc | https://sphinxcontrib-redoc.readthedocs.io/en/stable
# Demo | https://sphinxcontrib-redoc.readthedocs.io/en/stable/api/github/

# Intentional forward/slashes/ for html; eg: "_specs/openapi.json"
xbe_spec = openapi_dir_path + '/openapi.json'
github_demo_spec = openapi_dir_path + '/github-demo.yml'

redoc = [
    {
        'name': 'Xsolla Backend API',
        'page': openapi_generated_file_posix_path,  # content/-/api/index
        # 'spec': '_specs/openapi.json',  # (!) Ours Currently won't build due to errs: `/components/schemas/ACLRecordMongo". Token "ACLRecordMongo" does not exist`
        'spec': github_demo_spec,  # DELETE ME AFTER DONE WITH TESTS!
        'embed': True,  # Local file only (!) but embed is less powerful
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

print(f'[conf.py::sphinxcontrib.redoc] redoc[0].page: {redoc[0]["page"]}')
print(f'[conf.py::sphinxcontrib.redoc] redoc[0].spec: {redoc[0]["spec"]}')
print('')

# -- Intersphinx Mapping -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
# Centralized link constants
# TODO(XBND-891): Centralize Discord links, perhaps others

# # Link constants shared across multiple docs
# objs_inv_path = None  # Use default
# intersphinx_mapping = {
#     'xbe-discord': ('https://discord.gg/XsollaBackend', objs_inv_path),
# }

# Ensure we only use intersphinx when we use :ref: role | https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_disabled_reftypes
intersphinx_disabled_reftypes = ['*']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'
# html_theme = 'piccolo_theme'

# The name of the Pygments (syntax highlighting) style to use.
# `sphinx` works very well with the RTD theme, but you can always change it
pygments_style = "monokai"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ['_static']

html_logo = '_static/images/logo.png'
html_favicon = '_static/images/favicon.ico'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme_options = {
    'canonical_url': 'https://docs.xsolla.cloud',
    'analytics_id': 'UA-136672390-2',  # Provided by Google in your dashboard
    'logo_only': True,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'style_nav_header_background': '#18171C',
    # Toc options >>
    'collapse_navigation': True,
    'sticky_navigation': True,  # Keep the navbar fixed to the top
    'navigation_depth': 2,  # (!) Important
    # 'includehidden': True,
    # 'titles_only': False,
}

# This swaps vals in the actual built HTML (NOT the rst files).
# Eg: This is used with themes and third-party extensions;
# (!) `{{templating}}` in rst files with these *won't* work here:
html_context.update({
    'conf_py_path': '/source/',  # Path in the checkout to the docs root
    # Edit on GitLab >>
    'display_gitlab': True,  # Integrate Gitlab
    'gitlab_host': 'gitlab.acceleratxr.com',
    'gitlab_user': 'Core',  # Group
    'gitlab_repo': 'acceleratxr.io',  # Repo name
    'gitlab_version': 'master',  # Version
})

source_suffix = ['.rst', '.md']  # Use MyST to auto-convert .md

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
    'production-stage': False,
    
    # True: [Navbar] New create acct page - False: Pricing page
    'parent-nav-create-your-acct-link-to-new-xbe': False,
    
    # True: [Doc Page] New create acct page - False: Pricing page
    'what-is-xbe-doc-create-link-to-new-xbe': False,
    
    # True: Show web app libs (xbeapp, react, etc) - False: Hide
    'welcome-release_notes-products_web_apps-libs': False,
    
    # True: Show new openapi docs & hide old ones - False: Hide new openapi docs, show placeholders
    'new-xbe-openapi-doc': False,
}

# -- Append rst_epilog to the bottom of *every* doc file ---------------------
# rst_epilog = ".. |theme| replace:: ``{0}``".format(html_theme)
