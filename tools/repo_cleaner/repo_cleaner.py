"""
repo_cleaner.py
This migrates repos to the correct architecture for the new doc system.
After cleaning, check git diff to ensure the correct architecture is in place.
(!) Be sure you're using version control before running this script.

For each repo:
1. Checkout the designated branch
2. Choose path/to/template repo
3. Ensure dir tree:
  - docs
    - .gitignore
    - make.bat
    - Makefile
    - README.md
    - requirements.txt
    - source
      - _static
        - images
          - favicon.png
          - logo.png
        - _static content goes here
      - _templates
      - content
      - conf.py
      - index.rst

4. Ensure the following files/dirs wiped recursively:
  - **/conf.py

5. Check for the 1st index.rst found at the following dirs (that may or may not exist):
  - docs
    - content

5. Ensures the following %PLACEHOLDERS% are replaced:
  - docs
    - README.md
        * %REPO_NAME%
    - source
      - conf.py
        * %REPO_NAME%
        * %REPO_NAME_REPLACE_UNDERSCORE_WITH_DASH%

"""
# TODO: Implement this script
