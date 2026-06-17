ALL_FIGURE_NAMES=$(shell cat dissertation.figlist)
ALL_FIGURES=$(ALL_FIGURE_NAMES:%=%.pdf)

allimages: $(ALL_FIGURES)
	@echo All images exist now. Use make -B to re-generate them.

FORCEREMAKE:

-include $(ALL_FIGURE_NAMES:%=%.dep)

%.dep:
	mkdir -p "$(dir $@)"
	touch "$@" # will be filled later.

ext-tikz/dissertation-figure0.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure0" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure0.pdf: ext-tikz/dissertation-figure0.md5
ext-tikz/dissertation-figure1.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure1" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure1.pdf: ext-tikz/dissertation-figure1.md5
ext-tikz/dissertation-figure2.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure2" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure2.pdf: ext-tikz/dissertation-figure2.md5
ext-tikz/dissertation-figure3.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure3" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure3.pdf: ext-tikz/dissertation-figure3.md5
ext-tikz/dissertation-figure4.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure4" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure4.pdf: ext-tikz/dissertation-figure4.md5
ext-tikz/dissertation-figure5.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure5" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure5.pdf: ext-tikz/dissertation-figure5.md5
ext-tikz/dissertation-figure6.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure6" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure6.pdf: ext-tikz/dissertation-figure6.md5
ext-tikz/dissertation-figure7.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure7" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure7.pdf: ext-tikz/dissertation-figure7.md5
ext-tikz/dissertation-figure8.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure8" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure8.pdf: ext-tikz/dissertation-figure8.md5
ext-tikz/dissertation-figure9.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure9" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure9.pdf: ext-tikz/dissertation-figure9.md5
ext-tikz/dissertation-figure10.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure10" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure10.pdf: ext-tikz/dissertation-figure10.md5
ext-tikz/dissertation-figure11.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure11" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure11.pdf: ext-tikz/dissertation-figure11.md5
