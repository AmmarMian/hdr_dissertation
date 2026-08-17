# HDR Dissertation

main_tex := "dissertation"

# List available commands
default:
    @just --list

# Regenerate figures.toml and figures_parameters.tex from prov.json files
figures:
    python3 scripts/gen_figures.py

# Build the dissertation (externalize tikz, then compile)
build:
    latexmk -pdf -interaction=nonstopmode {{main_tex}}.tex
    make -f {{main_tex}}.makefile
    latexmk -pdf -interaction=nonstopmode {{main_tex}}.tex

# Quick build (single pdflatex pass)
quick:
    pdflatex -interaction=nonstopmode {{main_tex}}.tex

# Clean build artifacts
clean:
    latexmk -C {{main_tex}}.tex
