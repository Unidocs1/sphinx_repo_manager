# acceleratxr.io/tools

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

The successor of `repo_cleaner.py` for more-minimal actions for already-normalized doc repos. Eg: Mass add an entry to `.gitignore` -> commit the change.

## repo_cleaner.py

Somewhat deprecated in favor of the more-minimal `mass-repo-cmds.ps1`, initially used to mass normalize every cloned repo and replace %PLACEHOLDERS%, but can be repurposed to do similar things. Repurpose this script to do more-complex things, even if the files are not yet normalized.

## Deprecated/ dir

Contains CI/CD for gitlab and related test runners. In the end, we did not need this, but could be a useful template for the future.

## symlink_to_repo_manager.py

Called from `requirements-install.ps1`, this creates a 

## License

TODO
