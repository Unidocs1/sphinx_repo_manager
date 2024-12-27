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
from pathlib import Path

sys.path.insert(0, os.path.abspath("."))

# -- Path setup --------------------------------------------------------------
# The absolute path to the directory containing conf.py.
confdir = Path(__file__).parent.resolve()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx_repo_manager",  # Xsolla Backend (XBE)'s extension to manage repos via repo_manifest.yml
    "myst_parser",  # Auto-converts .md to .rst
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_repos-available",  # We'll be using the symlinked `content` dir, instead
    "_static-docs",  # We'll be using the symlinked `content` dir, instead
    "**/_build",
    "**/build",
    "**/.DS_Store",
    "**/README*",
    "**/requirements.txt",
    "**/Thumbs.db",
    "**/venv",
]

# -- Extensions Setup --------------------------------------------------------

source_suffix = [".rst", ".md"]  # Use MyST to auto-convert .md

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Sphinx Repo Manager"
copyright = "2024, Xsolla (USA), Inc. All rights reserved"
author = "Xsolla"
release = "v1.0.0"
version = release  # Used by some extensions
html_context = {}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = [str(confdir / "_static")]
html_theme_options = {}
