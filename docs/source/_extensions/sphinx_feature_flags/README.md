# Sphinx Extension: Feature Flags

## Description

This Sphinx extension allows for the `feature-flag` directive to show (if `True`) or fallback (if `False` and
using the `:fallback:` option).

## Setup

1. Add the following to your `conf.py`:

    ```python
    import sys, os
    
    sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_feature_flags')))
    extensions = ['sphinx_feature_flags']
    
    feature_flags = {
        'production_stage': False,  # Example
    }
    ```

## Usage

In any `.rst` file, wrap the `feature-flag` directive around any block:

    ```rst
    .. feature-flag:: production_stage
    
       This only shows if production_stage = True; it can be an entire toctree, too!
    
    .. feature-flag:: production_stage
       :fallback:
    
       This only shows if production_stage = False.
    ```

## Requirements

- Python 3.6 or higher
- Sphinx 1.8 or higher

This may work with older versions, but has not been tested.

## Entry Point

See `setup(app)` definition at `sphinx_repo_manager.py`.

## Tested in

- Windows 11 via PowerShell 7
- Ubuntu 22.04 via ReadTheDocs (RTD) CI

## Notes

- `__init__.py` is required for both external pathing and to treat the directory as a pkg
