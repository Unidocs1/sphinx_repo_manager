##############################################################################
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
##############################################################################
# XBE Custom Extension: repo_manager
#
# At build time, clones tagged versions from ../repo_manifest.yml into the
# specified directories. This allows us to build documentation for multiple
# versions of the same service.
#
# DEFAULTS:
# - Src clone dir: `./repos_available`
# - Target symlinked content: `./content/{macro_version}/{repo}-{tag}`
#
##############################################################################
import logging
import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'xbe'
copyright = 'Xsolla (USA), Inc. All rights reserved'
author = 'Xsolla'
release = '2024.07.0-TEST'  # This should match your branch name (unless latest/master/main)


# -- Path setup --------------------------------------------------------------
#
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

sys.path.append(os.path.abspath(
    os.path.join('_extensions', 'repo_manager')))
sys.path.insert(0, os.path.abspath('.'))
# sys.path.insert(0, os.path.abspath(f'./multiplayer/account_services/docs/content'))
# sys.path.insert(0, os.path.abspath('./multiplayer/quest_services/docs/content'))


# -- Extension: repo_manager --------------------------------------------------------------
# This in-house extension clones repos from repo_manifest.yml and symlinks them into the content directory.
# This allows us to build documentation for multiple versions of the same service.

# Initialize the RepoManager instance with the manifest path
manifest_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'repo_manifest.yml'))
repo_manager = RepoManager(manifest_path)
manifest = repo_manager.read_normalize_manifest()


# -- ReadTheDocs (RTD) Config ------------------------------------------------

# Check if we're running on Read the Docs' servers
read_the_docs_build = os.environ.get("READTHEDOCS", None) == 'True'

if read_the_docs_build:
    gitlab_access_token = os.getenv('GITLAB_ACCESS_TOKEN')
    if not gitlab_access_token:
        print("Warning: GITLAB_ACCESS_TOKEN .env !set (ok if public repo or RTD business acct)")


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_parser',  # recommonmark successor
    'sphinx.ext.intersphinx',
    'sphinx_tabs.tabs',
    'repo_manager',  # Our own custom extension
    'sphinx_jinja',
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
]

master_doc = 'index'  # Allegedly renamed to root_doc long ago, but it doesn't appear so


# -- Intersphinx Mapping -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
# Centralized link constants

# Link constants shared across multiple docs
intersphinx_mapping = {
    'sdk-cpp': ('https://sdk-cpp.acceleratxr.io/en/latest/', None),
    'sdk-csharp': ('https://sdk-csharp.acceleratxr.io/en/latest/', None)
}

# We recommend adding the following config value.
# Sphinx defaults to automatically resolve *unresolved* labels using all your Intersphinx mappings.
# This behavior has unintended side effects, namely that documentations local references can
# suddenly resolve to an external location.
# See also:
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_disabled_reftypes
intersphinx_disabled_reftypes = ['*']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

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
    'style_nav_header_background': '#2D2926',
    # Toc options >>
    'collapse_navigation': True,
    'sticky_navigation': True,
    'show_nav_level': 1,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
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
    'gitlab_repo': 'acceleratxr.io',  # Repo name
    'gitlab_version': 'master',  # Version
}


# -- Options for Jinja Templating --------------------------------------------
# Swap out {{templated}} vars and {% for % } ops in .rst.
# Declare the vars at `jinja_contexts`.

jinja_contexts = {
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
    },
    'content': {
        ## Repos >> TODO: Swap these out dynamically from repo_manifest.yml
        # 'account_services': f'_repos-available/account_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'achievements_services': '_repos-available/achievements_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'asset_services': '_repos-available/asset_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'backup_services': '_repos-available/backup_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'economy_services': '_repos-available/economy_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'leaderboard_services': '_repos-available/leaderboard_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'matchmaking_services': '_repos-available/matchmaking_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'notification_services': '_repos-available/notification_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'persona_services': '_repos-available/persona_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'progression_services': '_repos-available/progression_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'purchasing_services': '_repos-available/purchasing_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'quest_services': '_repos-available/quest_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'reporting_services': '_repos-available/reporting_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'scripting_services': '_repos-available/scripting_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'server_instance_services': '_repos-available/server_instance_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'social_services': '_repos-available/social_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'telemetry_services': '_repos-available/telemetry_services--dylan--refactor--docs-revamp/docs/source/index',
        # 'validation_services': '_repos-available/validation_services--dylan--refactor--docs-revamp/docs/source/index',
        #
        # # SDKs >>
        # 'cpp_sdk': '_repos-available/sdk_cpp--dylan--refactor--docs-revamp/docs/source/index',
        # 'csharp_sdk': '_repos-available/sdk_csharp--dylan--refactor--docs-revamp/docs/source/index',
        #
        # Static >>
        'commerce': '_repos-available/xbe-static-docs--main/docs/source/content/commerce',
        'content': '_repos-available/xbe-static-docs--main/docs/source/content/content',
        'demo': '_repos-available/xbe-static-docs--main/docs/source/content/demo',
        'eula': '_repos-available/xbe-static-docs--main/docs/source/content/eula/index',
        'features': '_repos-available/xbe-static-docs--main/docs/source/content/features',
        'gameplay': '_repos-available/xbe-static-docs--main/docs/source/content/gameplay',
        'getting_started': '_repos-available/xbe-static-docs--main/docs/source/content/getting_started/index',
        'liveops': '_repos-available/xbe-static-docs--main/docs/source/content/liveops',
        'multiplayer': '_repos-available/xbe-static-docs--main/docs/source/content/multiplayer',
        'samples': '_repos-available/xbe-static-docs--main/docs/source/content/samples_and_tutorials/index',
        'tools': '_repos-available/xbe-static-docs--main/docs/source/content/tools',
        # External links >>
        'discord': 'https://discord.gg/wrfBR2Q',
        'gitlab': 'https://gitlab.acceleratxr.com',
        'company': 'https://xsolla.com/backend',
    }
}

# # For each manifest repo
# for repo in repo_manifest:
#     repo_name = repo['name']
#     repo_url = repo['url']
# 
#     # TODO: Finish this

# Add more dynamic props
jinja_general = jinja_contexts['general']

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


# -- Append rst_epilog to the bottom of *every* doc file ---------------------
# However, it's more-recommended to use the following at the top of your RST files (notice the `_` underscore prefix):
# `.. _company: https://xsolla.com/backend`
# Then to use it: `Company <company>`

# rst_prolog = """
# .. |company| replace:: https://xsolla.com/backend
# """
