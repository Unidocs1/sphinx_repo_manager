# Sphinx Extension: Sphinx Algolia Crawler

## Description

This Sphinx extension (if .env exists) wraps around Docker to scrape our site
for Algolia AI search. This should be run locally; NOT in ReadTheDocs(RST)
since it invokes Docker.

## Setup

1. Edit `config.json`
2. Copy `.env.template` to `.env` and set

## Usage

### Standalone

```bash
python3 sphinx_algolia_crawler.py
```

### Sphinx Ext

Add the following to your `conf.py`:

```py
import sys, os

sys.path.append(os.path.abspath(os.path.join('_extensions', 'sphinx_algolia_crawler')))
extensions = [ 'sphinx_algolia_crawler' ]
```


## Requirements

- Python>=3.6
- Sphinx>=1.8
- Docker Desktop
- jq:
```bash
# Bash
sudo apt-get install jq
```
```powershell
# PowerShell
winget install jqlang.jq
```

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
- (!) RTD is unlikely to run a Docker container

## Notes

- `__init__.py` is required for both external pathing and to treat the directory as a pkg
