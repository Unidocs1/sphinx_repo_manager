# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Doxygen and Exhale options
DOXYGEN ?= False
EXHALE ?= False

DOXYFILE = "$(CURDIR)/Doxyfile"
DOXYGEN_DIR = "$(CURDIR)/$(SOURCEDIR)/_doxygen"
EXHALE_DIR = "$(CURDIR)/$(SOURCEDIR)/content/api"

.PHONY: help clean

ifeq ($(OS),Windows_NT)
    RM_F = del /F /Q
    RM_RF = rd /S /Q
else
    RM_F = rm -f
    RM_RF = rm -rf
endif

# Exports for the Doxygen and Exhale options
export DOXYGEN
export EXHALE

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Clean target: cleans up build directories and Exhale/Doxygen outputs
clean:
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	-@if [ "$(DOXYGEN)" == "True" ]; then \
		echo "Clean up Doxygen outputs (DOXYGEN=True)"; \
		$(RM_RF) $(DOXYGEN_DIR); \
	fi
	-@if [ "$(EXHALE)" == "True" ]; then \
		echo "Clean up Exhale outputs (EXHALE=True)"; \
		$(RM_RF) $(EXHALE_DIR); \
	fi

# Doxygen target: builds the Doxygen xml files
doxygen:
	-@$(RM_RF) $(DOXYGEN_DIR)
	@doxygen $(DOXYFILE)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option. $(O) is meant as a shortcut for $(SPHINXOPTS).
%:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)