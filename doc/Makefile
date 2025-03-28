## Makefile for Sphinx documentation
##

# You can set these variables from the command line.
SPHINXOPTS    = -W
SPHINXBUILD   = python3 -m sphinx
SOURCEDIR     = src
BUILDDIR      = build
PYTHON        = python3


# Put it first so that "make" without argument is like "make help".
#help:
#	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

help:  ## Show this help message
	@egrep -h '^##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "## "}; {printf "%s\n", $$2}'
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m %-20s\033[0m %s\n", $$1, $$2}'

.PHONY: help Makefile

#######################################################################
#                           Sphinx targets                            #
#######################################################################
# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
#%: Makefile
#	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html: src/*.rst  ## Generate HTML documentation
	@mkdir -p $(BUILDDIR)
	$(SPHINXBUILD) -b html $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/html
	@echo "Build done in $(BUILDDIR)/html"

pdf: src/*.rst   ## Generate a PDF documentation (with pdflatex)
	@mkdir -p $(BUILDDIR)
	$(SPHINXBUILD) -M latexpdf $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/pdf
	@echo "Build done in $(BUILDDIR)/pdf"

latex: src/*.rst ## Generate a latex documentation (do not compile it)
	@mkdir -p $(BUILDDIR)
	$(SPHINXBUILD) -b latex $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/latex
	@echo "Build done in $(BUILDDIR)/latex"

man: src/*.rst   ## Generate a unix man format documentation
	@mkdir -p $(BUILDDIR)
	$(SPHINXBUILD) -b man $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/man
	@echo "Build done in $(BUILDDIR)/man"

#######################################################################
#                                Clean                                #
#######################################################################
clean:   ## Clean the all build directories
	rm -rf $(BUILDDIR)/html
	rm -rf $(BUILDDIR)/latex
	rm -rf $(BUILDDIR)/pdf
	rm -rf $(BUILDDIR)/man
