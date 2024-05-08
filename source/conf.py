# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup --------------------------------------------------------------
#
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
sys.path.append(os.path.abspath('./_extensions'))
sys.path.insert(0, os.path.abspath('.'))
# sys.path.insert(0, os.path.abspath('./multiplayer/account_services/docs/content'))
# sys.path.insert(0, os.path.abspath('./multiplayer/quest_services/docs/content'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'xbe'
copyright = 'Xsolla (USA), Inc. All rights reserved'
author = 'Xsolla'
release = 'v0.0.1'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_parser',  # recommonmark successor
    'sphinx.ext.intersphinx',
    'sphinx_tabs.tabs',
    'repo_manager'  # Our own custom extension
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store'
]

master_doc = 'index'


# -- Intersphinx Mapping -------------------------------------------------

# Link constants shared across multiple docs
intersphinx_mapping = {
    "sdk-cpp": ("https://sdk-cpp.acceleratxr.io/en/latest/", None),
    "sdk-csharp": ("https://sdk-csharp.acceleratxr.io/en/latest/", None)
}

# We recommend adding the following config value.
# Sphinx defaults to automatically resolve *unresolved* labels using all your Intersphinx mappings.
# This behavior has unintended side effects, namely that documentations local references can
# suddenly resolve to an external location.
# See also:
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_disabled_reftypes
intersphinx_disabled_reftypes = ["*"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_logo = '_static/images/logo.png'
html_favicon = '_static/images/favicon.png'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme_options = {
    'canonical_url': 'https://docs.xsolla.cloud',
    'analytics_id': 'UA-136672390-2',  # Provided by Google in your dashboard
    'logo_only': True,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'style_nav_header_background': '#2D2926',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
    'gitlab_url': 'https://gitlab.acceleratxr.com/core/acceleratxr.io'
}

html_context = {
    # Edit on GitLab
    "display_gitlab": True,  # Integrate Gitlab
    "gitlab_host": "gitlab.acceleratxr.com",
    "gitlab_user": "Core",  # Group
    "gitlab_repo": "acceleratxr.io",  # Repo name
    "gitlab_version": "master",  # Version
    "conf_py_path": "/source/",  # Path in the checkout to the docs root
}
