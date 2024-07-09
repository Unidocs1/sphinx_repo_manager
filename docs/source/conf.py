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
from pathlib import Path  # Path manipulation/normalization; allows / slashes for path
import requests  # To download openapi.yaml
import sys
import yaml  # To process openapi.yaml
# import subprocess  # for Doxyfile


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

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

sys.path.insert(0, os.path.abspath(''))


# -- ReadTheDocs (RTD) Config ------------------------------------------------

# Check if we're running on Read the Docs' servers
read_the_docs_build = os.environ.get("READTHEDOCS", None) == 'True'

# # Warn if GITLAB_ACCESS_TOKEN is !set; it's only required for private docs on !business RTD plan (eg: test acct)
# if read_the_docs_build:
#     gitlab_access_token = os.getenv('GITLAB_ACCESS_TOKEN')
#     if not gitlab_access_token:
#         print("Warning: GITLAB_ACCESS_TOKEN .env !set (ok if public repo or RTD business acct)")


# # TODO: Look into Doxygen / Breathe integration
# def configure_doxyfile(input_dir, output_dir):
#     with open("Doxyfile.in", "r") as file:
#         filedata = file.read()
#
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# The absolute path to the directory containing conf.py.
documentation_root = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_repo_manager')))
sys.path.append(os.path.abspath('.'))

# -- Extension: sphinx_repo_manager --------------------------------------------------------------
# This in-house extension clones repos from repo_manifest.yml and symlinks them into the content directory.
# This allows us to build documentation for multiple versions of the same service.

from _extensions.sphinx_repo_manager import SphinxRepoManager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'tools', 'sphinx_repo_manager')))

# Initialize the RepoManager instance with the manifest path
manifest_path = Path('..', 'repo_manifest.yml').resolve()
repo_manager = SphinxRepoManager(manifest_path)
manifest = repo_manager.read_normalize_manifest()

# Extract common props
repos = manifest['repositories']  # repos[repo_name] = { url, tag, symlink_path, branch, active }
print(f'[conf.py::sphinx_repo_manager] Num repos found: {len(repos)}')

# TODO: Use these below for dynamic info pulled from repo_manifest.yaml
base_symlink_path = manifest['base_symlink_path']  # eg: "source/content"
repo_sparse_path = manifest['repo_sparse_path']  # eg: "docs"


# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    'myst_parser',  # recommonmark successor
    'sphinx.ext.intersphinx',
    'sphinx_tabs.tabs',
    'sphinx_repo_manager',  # Our own custom extension
    'sphinx_new_tab_link',  # https://pypi.org/project/sphinx-new-tab-link
    'sphinx_copybutton',  # https://pypi.org/project/sphinx-copybutton
    'sphinxcontrib.redoc',  # OpenAPI Docgen: Similar to sphinxcontrib-openapi, but +1 column for example responses; https://sphinxcontrib-redoc.readthedocs.io/en/stable 
    # 'breathe',  # Doxygen API docs
    # 'sphinx_csharp',  # CSharp markdown
    # 'sphinx.ext.autodoc',  # More API docgen tools
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'venv',
    'requirements.txt',
    'README.*',
    '_repos-available',  # We'll be using the symlinked `content` dir, instead
]

master_doc = 'index'

# Tell sphinx what the primary language being documented is + code highlighting
primary_domain = "cpp"
highlight_language = "cpp"


# -- OpenAPI Local Download ----------------------------------------------
# The target server host is blocking CORS, so we grab it locally
# Used for the sphinxcontrib.redoc extension

# Define the target yaml + path to save the downloaded OpenAPI spec
openapi_spec_url_noext = 'https://api.dev.xbe.xsolla.cloud/v1/openapi'
openapi_spec_path_noext = os.path.join('_static', 'openapi')
openapi_rst_path_noext = os.path.join('content', '-', 'api_ref', 'openapi')


# Download the spec to source/_static/openapi.yaml
def download_file(url, save_to_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_to_path, 'wb') as f:
            f.write(response.content)
        print(f'[conf.py] Successfully downloaded {url}')
    else:
        print(f'[conf.py] Failed to download {url}: {response.status_code}')
    print('')


def verify_openapi_files_exist():
    files = {
        'openapi.yaml': openapi_spec_path_noext + '.yaml',
        'openapi.json': openapi_spec_path_noext + '.json',
        'openapi.rst': openapi_rst_path_noext + '.rst',
    }

    for name, path in files.items():
        print(f'[conf.py] Validating {name} ...')
        if os.path.exists(path):
            print(f'- {name} found at {path}')
        else:
            print(f'- {name} NOT found at {path}')
    print('')


print('')
download_file(openapi_spec_url_noext + '.yaml', openapi_spec_path_noext + '.yaml')
download_file(openapi_spec_url_noext + '.json', openapi_spec_path_noext + '.json')
verify_openapi_files_exist()


# -- Extension: sphinxcontrib.redoc --------------------------------------
# OpenAPI Docgen: Similar to sphinxcontrib-openapi, but +1 column for example responses
# Doc | https://sphinxcontrib-redoc.readthedocs.io/en/stable
# Demo | https://sphinxcontrib-redoc.readthedocs.io/en/stable/api/github/

redoc = [
    {
        'name': 'Xsolla Backend API',
        'page': openapi_rst_path_noext,  # 'content/-/api_ref/openapi'; (!) .rst containing `.. redoc::`
        'spec': openapi_spec_path_noext,
        'embed': True,  # Local file only
        'opts': {
            'lazy-rendering': True,  # Formerly called `lazy`
            'required-props-first': True,  # Useful, (!) but slow
            'expand-responses': ["200", "201"],
            'native-scrollbars': True,  # Improves perf on big specs
        }
    },
]


# -- Extension: Breathe --------------------------------------------------
# Breathe allows you to embed Doxygen documentation into your docs.

# breathe_projects = {"AcceleratXR": "./_doxygen/xml"}  # TODO: Name change
# breathe_default_project = "AcceleratXR"  # TODO: Name change


# -- C# domain configuration ----------------------------------------------

# sphinx_csharp_test_links = read_the_docs_build
# sphinx_csharp_multi_language = True

# # Tell sphinx what the primary language being documented is + code highlighting
# primary_domain = "cpp"
# highlight_language = "cpp"


# -- Extension: Breathe --------------------------------------------------
# Breathe allows you to embed Doxygen documentation into your docs.

# breathe_projects = {"AcceleratXR": "./_doxygen/xml"}  # TODO: Name change
# breathe_default_project = "AcceleratXR"  # TODO: Name change


# -- C# domain configuration ----------------------------------------------

# sphinx_csharp_test_links = read_the_docs_build
# sphinx_csharp_multi_language = True


# -- Intersphinx Mapping -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
# Centralized link constants

# # Link constants shared across multiple docs
# intersphinx_mapping = {
#     'some-link-ref': ('https://some-link-ref.acceleratxr.io/en/latest/', None),
# }

# We recommend adding the following config value.
# Sphinx defaults to automatically resolve *unresolved* labels using all your Intersphinx mappings.
# This behavior has unintended side effects, namely that documentations local references can
# suddenly resolve to an external location.
# See also:
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_disabled_reftypes
# intersphinx_disabled_reftypes = ['*']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# The name of the Pygments (syntax highlighting) style to use.
# `sphinx` works very well with the RTD theme, but you can always change it
pygments_style = "sphinx"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ['_static']
def setup(app):
    app.add_css_file(os.path.normpath('styles/main.css'))

html_logo = 'https://docs.xsolla.cloud/en/latest/_static/logo.png'
html_favicon = 'https://docs.xsolla.cloud/en/latest/_static/favicon.ico'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme_options = {
    'canonical_url': 'https://docs.xsolla.cloud',
    'analytics_id': 'UA-136672390-2',  # Provided by Google in your dashboard
    'logo_only': True,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'style_nav_header_background': '#2D2926',
    # Toc options >>
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 2, # (!) Important
    # 'includehidden': True,
    # 'titles_only': False,
}

# This swaps vals in the actual built HTML (NOT the rst files).
# Eg: This is used with themes and third-party extensions;
# (!) `{{templating}}` in rst files with these *won't* work here:
html_context = {
    'conf_py_path': '/source/',  # Path in the checkout to the docs root
    # Edit on GitLab >>
    'display_gitlab': True,  # Integrate Gitlab
    'gitlab_host': 'gitlab.acceleratxr.com',
    'gitlab_user': 'Core',  # Group
    'gitlab_repo': 'acceleratxr.io',  # Repo name
    'gitlab_version': 'master',  # Version
}

source_suffix = ['.rst', '.md']  # Use MyST to auto-convert .md


# -- MyST configuration ------------------------------------------------------
# recommonmark successor to parse .md to .rst

# Configuration for MyST-Parser
myst_enable_extensions = [
    "amsmath",          # Enable parsing and rendering of AMS math syntax
    "dollarmath",       # Enable dollar math syntax
    "html_admonition",  # Enable HTML admonitions
    "html_image",       # Enable HTML image tags
    "colon_fence",      # Enable colon fences for directives/roles
    "smartquotes",      # Enable smart quotes
    "replacements",     # Enable replacements syntax
    "strikethrough",    # Enable strikethrough syntax
    "tasklist",         # Enable task list syntax
]

# -- Append rst_epilog to the bottom of *every* doc file ---------------------
# rst_epilog = ".. |theme| replace:: ``{0}``".format(html_theme)
