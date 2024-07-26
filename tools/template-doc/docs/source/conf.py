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
import subprocess  # for Doxyfile
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '%REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH%'
copyright = 'Xsolla (USA), Inc. All rights reserved'
author = 'Xsolla'

# This should likely match your branch name:
# - EXCEPTION: If a "latest" tracked branch (master/lts/main/some ver tester)
#   - If exception, consider using "latest" or "v{ver_about_to_be_released}-doc"
# release = '%GIT_TAG%'


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
#     filedata = filedata.replace("@DOXYGEN_INPUT_DIRECTORY@", input_dir)
#     filedata = filedata.replace("@DOXYGEN_OUTPUT_DIRECTORY@", output_dir)
#
#     with open("Doxyfile", "w") as file:
#         file.write(filedata)
#
#
# breathe_projects = {}
#
# if read_the_docs_build:
#     input_dir = "../sdk"
#     output_dir = "_doxygen"
#     configure_doxyfile(input_dir, output_dir)
#     subprocess.call("doxygen Doxyfile", shell=True)
#     breathe_projects["AcceleratXR"] = output_dir + "/xml"
#     subprocess.call(
#         "python -m breathe.apidoc -p AcceleratXR -o api ./_doxygen/xml", shell=True
#     )
#     print("---- Doxygen / Breathe Done ----")


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# The absolute path to the directory containing conf.py.
documentation_root = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.abspath('.'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_parser',  # recommonmark successor
    'sphinx.ext.intersphinx',
    'sphinx_tabs.tabs',
    'sphinxcontrib.redoc',
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

# -- Extension: sphinx.ext.todo ------------------------------------------
# Support for `todo` directive, passing it during sphinx builds
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html

todo_include_todos = False  # If this is True, todo and todolist produce output, else they produce nothing. The default is False.
todo_emit_warnings = False  # If this is True, todo emits a warning for each TODO entries. The default is False.
todo_link_only = False  # If this is True, todolist produce output without file path and line, The default is False.

# -- Extension: Breathe --------------------------------------------------
# Breathe allows you to embed Doxygen documentation into your docs.

# breathe_projects = {"AcceleratXR": "./_doxygen/xml"}  # TODO: Name change
# breathe_default_project = "AcceleratXR"  # TODO: Name change

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
    'navigation_depth': 2,  # (!) max depth; NOT default
    'includehidden': True,
    'titles_only': False
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
    'gitlab_repo': '%REPO_NAME%',  # Repo name
    'gitlab_version': 'master',  # Version
}

source_suffix = ['.rst', '.md']  # Use MyST to auto-convert .md

# -- MyST configuration ------------------------------------------------------
# recommonmark successor to parse .md to .rst

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

# -- Append rst_epilog to the bottom of *every* doc file ---------------------
# rst_epilog = ".. |theme| replace:: ``{0}``".format(html_theme)
