##############################################################################
# Configuration file for the Sphinx documentation builder.
# (!) THIS FILE IS IGNORED IF PULLED BY THE MAIN DOC - USED FOR LOCAL TESTING
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
##############################################################################

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '%REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH%'
copyright = 'Xsolla (USA), Inc. All rights reserved'
author = 'Xsolla'

# This should likely match your branch name:
# - EXCEPTION: If a "latest" tracked branch (master/lts/main/some ver tester)
#   - If exception, consider using "latest" or "v{ver_about_to_be_released}-doc"
release = '%GIT_TAG%'

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
# import yaml

sys.path.insert(0, os.path.abspath(''))


# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

# Check if we're running on Read the Docs' servers
read_the_docs_build = os.environ.get("READTHEDOCS", None) == 'True'

extensions = [
    'myst_parser',  # recommonmark successor
    'sphinx.ext.intersphinx',
    'sphinx_tabs.tabs',
    'sphinx_jinja2',
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
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
}

# This swaps vals in the actual built HTML (NOT the rst files).
# Eg: This is used with themes and third-party extensions;
# (!) `{{templating}}` in rst files with these *won't* work here:
#     If templating, see `jinja_contexts`
html_context = {
    'conf_py_path': '/source/',  # Path in the checkout to the docs root
    # Edit on GitLab >>
    'display_gitlab': True,  # Integrate Gitlab
    'gitlab_host': 'gitlab.acceleratxr.com',
    'gitlab_user': 'Core',  # Group
    'gitlab_repo': '%REPO_NAME%',  # Repo name
    'gitlab_version': 'master',  # Version
}


# -- Options for Jinja Templating --------------------------------------------
# https://pypi.org/project/sphinx-jinja/
# https://www.sphinx-doc.org/en/master/usage/extensions/jinja.html
# When 'sphinx_jinja' is added to 'extensions' var above (+installed via pip):
# Swap out {{templated}} vars and {% for % } ops in .rst (vars declared below).

# This is passed to .rst files
# USAGE with `jinja_context['general']['release']`
# ----------------------------------------------------
# .. jinja:: general
#    You are now seeing release version: {{ release }}
# ----------------------------------------------------
jinja2_contexts = {
    'general': {
        'release': release,
        'repo_name': html_context['gitlab_repo'],
        'gitlab_domain': 'gitlab.acceleratxr.com',
        'gitlab_org': 'Core',
        # -- Dynamic; set below --
        'gitlab_url': '',
        'badge_base_url': '',  # With no trailing slash
        'coverage_badge_svg_url': '',
        'pipeline_badge_svg_url': '',
    }
}

# Add more dynamic props
jinja_general = jinja2_contexts['general']

# eg: https://gitlab.acceleratxr.com/Core/acceleratxr.io
gitlab_url = ('https://'
              f"{jinja_general['gitlab_domain']}/"
              f"{jinja_general['gitlab_org']}/"
              f"{jinja_general['repo_name']}")
jinja_general['gitlab_url'] = gitlab_url

# eg: https://gitlab.acceleratxr.com/Core/account_services/badges/master/pipeline.svg
badge_base_url = (f"{gitlab_url}/badges/"
                  f"{html_context['gitlab_version']}")
jinja_general['badge_base_url'] = badge_base_url

jinja_general['coverage_badge_svg_url'] = f"{badge_base_url}/coverage.svg"
jinja_general['pipeline_badge_svg_url'] = f"{badge_base_url}/pipeline.svg"
