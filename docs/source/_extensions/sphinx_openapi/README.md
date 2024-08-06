# Sphinx Extension: OpenAPI

## Description

This Sphinx extension allows for downloading updated OpenAPI json + yaml specs for use with the
[sphinxcontrib.redoc](https://pypi.org/project/sphinxcontrib-redoc/) extension.

## Setup

Add the following to your `conf.py` (includes `redoc` extension setup):

 ```python
import sys, os
from pathlib import Path

html_context = {}  # This is usually already defined for other themes/extensions
sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_openapi')))
extensions = ['sphinx_openapi', 'sphinxcontrib.redoc']

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
 ```

## Requirements

- Python>=3.6
- Sphinx>=1.8

This may work with older versions, but has not been tested.

## Entry Point

See `setup(app)` definition at `sphinx_openapi.py`.

## Tested in

- Windows 11 via PowerShell 7
- Ubuntu 22.04 via ReadTheDocs (RTD) CI

## Notes

- `__init__.py` is required for both external pathing and to treat the directory as a pkg
