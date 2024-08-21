# Sphinx Extension: Sphinx Algolia Crawler

## Description

This Sphinx extension (that can also be run standalone) uses Algolia's v1 Crawler API 
to trigger a crawl, for either our dev or production stage:

https://www.algolia.com/doc/rest-api/crawler/#tag/actions/operation/crawlUrls

## Sphinx Setup

## Set Secret

In ReadTheDocs' env var dashboard, set `ALGOLIA_CRAWLER_SECRET_API_KEY`.

💡 Add this to your root proj `.env` to test locally

### conf.py

Ensure the following are set:

```py
import sys, os

sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_algolia_crawler')))
extensions = [ 'sphinx_algolia_crawler' ]

algolia_crawler_enabled = True  # Crawling is slow; you may only want this for RTD CI
docsearch_app_id = 'TODO'
algolia_crawler_id = 'TODO'  # Not to be confused with index name
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
