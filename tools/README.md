# xbe_docs/tools

From "perfect doc" templates to scripts to get things done:

## requirements-install.ps1

The equivalent of installing ../requirements.txt yourself, but friendlier (and creates a symlink to repo_manager for tooling).

## template-doc/ dir

Paste this to new repos for a `docs/` template. Be sure to replace the `%PLACEHOLDERS%` (either via a script or manually) at:

* docs/README.md
* docs/source/conf.py

## tool_template.py

Start here for tooling -- a minimal template to read the manifest file, then leave you to it.

## mass-repo-cmds.ps1

The successor of `repo_cleaner.py` for more-minimal actions for already-normalized doc repos. Eg: Mass add an entry to `.gitignore` -> commit the change:

1. Copy the script where you your repos are -> set the `$REPOS_AVAIL_DIR` path.
2. Edit between `>> Custom Cmds >>` section at `Start-RepoCmds` func.

## License

TODO
