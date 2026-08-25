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
ext-tikz/dissertation-figure12.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure12" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure12.pdf: ext-tikz/dissertation-figure12.md5
ext-tikz/dissertation-figure13.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure13" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure13.pdf: ext-tikz/dissertation-figure13.md5
ext-tikz/dissertation-figure14.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure14" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure14.pdf: ext-tikz/dissertation-figure14.md5
ext-tikz/dissertation-figure15.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure15" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure15.pdf: ext-tikz/dissertation-figure15.md5
ext-tikz/dissertation-figure16.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure16" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure16.pdf: ext-tikz/dissertation-figure16.md5
ext-tikz/dissertation-figure17.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure17" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure17.pdf: ext-tikz/dissertation-figure17.md5
ext-tikz/dissertation-figure18.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure18" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure18.pdf: ext-tikz/dissertation-figure18.md5
ext-tikz/dissertation-figure19.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure19" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure19.pdf: ext-tikz/dissertation-figure19.md5
ext-tikz/dissertation-figure20.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure20" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure20.pdf: ext-tikz/dissertation-figure20.md5
ext-tikz/dissertation-figure21.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure21" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure21.pdf: ext-tikz/dissertation-figure21.md5
ext-tikz/dissertation-figure22.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure22" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure22.pdf: ext-tikz/dissertation-figure22.md5
ext-tikz/dissertation-figure23.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure23" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure23.pdf: ext-tikz/dissertation-figure23.md5
ext-tikz/dissertation-figure24.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure24" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure24.pdf: ext-tikz/dissertation-figure24.md5
ext-tikz/dissertation-figure25.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure25" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure25.pdf: ext-tikz/dissertation-figure25.md5
ext-tikz/dissertation-figure26.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure26" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure26.pdf: ext-tikz/dissertation-figure26.md5
ext-tikz/dissertation-figure27.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure27" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure27.pdf: ext-tikz/dissertation-figure27.md5
ext-tikz/dissertation-figure28.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure28" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure28.pdf: ext-tikz/dissertation-figure28.md5
ext-tikz/dissertation-figure29.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure29" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure29.pdf: ext-tikz/dissertation-figure29.md5
ext-tikz/dissertation-figure30.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure30" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure30.pdf: ext-tikz/dissertation-figure30.md5
ext-tikz/dissertation-figure31.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure31" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure31.pdf: ext-tikz/dissertation-figure31.md5
ext-tikz/dissertation-figure32.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure32" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure32.pdf: ext-tikz/dissertation-figure32.md5
ext-tikz/dissertation-figure33.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure33" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure33.pdf: ext-tikz/dissertation-figure33.md5
ext-tikz/dissertation-figure34.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure34" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure34.pdf: ext-tikz/dissertation-figure34.md5
ext-tikz/dissertation-figure35.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure35" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure35.pdf: ext-tikz/dissertation-figure35.md5
ext-tikz/dissertation-figure36.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure36" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure36.pdf: ext-tikz/dissertation-figure36.md5
ext-tikz/dissertation-figure37.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure37" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure37.pdf: ext-tikz/dissertation-figure37.md5
ext-tikz/dissertation-figure38.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure38" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure38.pdf: ext-tikz/dissertation-figure38.md5
ext-tikz/dissertation-figure39.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure39" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure39.pdf: ext-tikz/dissertation-figure39.md5
ext-tikz/dissertation-figure40.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure40" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure40.pdf: ext-tikz/dissertation-figure40.md5
ext-tikz/dissertation-figure41.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure41" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure41.pdf: ext-tikz/dissertation-figure41.md5
ext-tikz/dissertation-figure42.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure42" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure42.pdf: ext-tikz/dissertation-figure42.md5
ext-tikz/dissertation-figure43.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure43" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure43.pdf: ext-tikz/dissertation-figure43.md5
ext-tikz/dissertation-figure44.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure44" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure44.pdf: ext-tikz/dissertation-figure44.md5
ext-tikz/dissertation-figure45.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure45" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure45.pdf: ext-tikz/dissertation-figure45.md5
ext-tikz/dissertation-figure46.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure46" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure46.pdf: ext-tikz/dissertation-figure46.md5
ext-tikz/dissertation-figure47.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure47" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure47.pdf: ext-tikz/dissertation-figure47.md5
ext-tikz/dissertation-figure48.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure48" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure48.pdf: ext-tikz/dissertation-figure48.md5
ext-tikz/dissertation-figure49.pdf: 
	pdflatex -halt-on-error -interaction=batchmode -jobname "ext-tikz/dissertation-figure49" "\def\tikzexternalrealjob{dissertation}\input{dissertation}"

ext-tikz/dissertation-figure49.pdf: ext-tikz/dissertation-figure49.md5
