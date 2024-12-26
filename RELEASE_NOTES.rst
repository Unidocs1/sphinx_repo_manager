Sphinx Repo Manager Release Notes
=================================

v1.0.19
-------

* Injected auth via headers instead of URL params for git operations for a more-sanitized approach
* Added ``tools/admin-enable-long-file-paths.ps1``

v1.0.18
-------

* feat: Git sparse checkout whitelist now supports wildcards; notably whitelisting ``README*`` (instead of just .md)
* feat(tool): ``environment.yml`` and ``tools/conda-activate.ps1``
* docs(tool): Initialized a ``tools/README.md``

v1.0.17
-------

* feat: Now shows shows (branch) next to repo name when performing git actions, including when done

v1.0.16
-------

* Potentially fixed a bug that would show a progress bar not reaching 'done' before continuing

v1.0.15
-------

* Updated README with additional performance tips
* Added a small arsenal of `tools/` for PyPi build-lint-deploy

v1.0.13
-------

* Initial Release
