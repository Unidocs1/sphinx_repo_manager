# Sphinx Extension: Sphinx Algolia Crawler

## Description

This Sphinx extension (that can also be run standalone) uses Algolia's v1 Crawler API 
to trigger a crawl. RTD uses Production stage, but Dev stage can be triggered either 
via standalone Python CLI call or by setting project root `.env` (see `.env.template`).

See [Algolia Crawler API Doc](https://www.algolia.com/doc/rest-api/crawler/#tag/actions/operation/crawlUrls)

## Sphinx Setup

## Set RTD Env

In ReadTheDocs' env var dashboard, set:

1. `ALGOLIA_CRAWLER_USER_ID`
2. `ALGOLIA_CRAWLER_API_KEY`
3. `ALGOLIA_CRAWLER_ID`

💡 Add this to your root proj `.env` to test locally (or as a standalone Python app)

### conf.py

```py
import sys, os

sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_algolia_crawler')))
extensions = [ 'sphinx_algolia_crawler' ]

# While this example merely turns it on, you probably want to check if RTD /latest production
# See `sphinx_repo_manager` `conf.py` for examples of how we checked for this
algolia_crawler_enabled = True
```

## Usage

### Standalone

See the `-h` (help) command:

```bash
python3 .\sphinx_algolia_crawler.py -h
```

### Sphinx Ext

If `conf.py` setup is set and `algolia_crawler_enabled`, this will automatically trigger when the build is done.

## Requirements

- Python>=3.6
- Sphinx>=1.8

This may work with older versions, but has not been tested.

## Entry Points

At `sphinx_algolia_crawler.py`:

### Sphinx Extension

See `setup(app)` definition.

### Standalone

See `if is_standalone:` block.

## Tested in

- Windows 11 via PowerShell 7
- Ubuntu 22.04 WSL2 Shell
- ReadTheDocs (RTD) CI Deployment (Ubuntu 22.04)

## Notes

- `__init__.py` is required for both external pathing and to treat the directory as a pkg
