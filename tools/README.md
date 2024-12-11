# Tools

## Global Setup

1. To utilize the deployment tools: copy `.env.template` -> `.env` and set the values.
2. [Optional] Run `conda-activate.ps1` before any CLI
3. Run `pip install -r ../requirements-dev.txt` to install the necessary dependencies

## Scripts

### Environment

* `conda-activate.ps1` - Activates (or creates) the `sphinx-repo-manager` conda environment.

### Build & Deploy

* `1_bump-ver.ps1` - Utilizes `bump2version`, bumping your git tag version up with a *patch*, by default
* `2_build-lint.ps1` - Builds the project with `python -m build`, then lints with `twine`
* `3a_deploy.ps1` - Deploys the project with `twine` to PyPi **dev** environment
* `3b_deploy.ps1` - Deploys the project with `twine` to PyPi **prod** environment

## Questions?

Join the Xsolla Backend official [Discord guild](https://discord.gg/XsollaBackend)!

## License

[MIT](../LICENSE)
