# HDR Dissertation

main_tex := "dissertation"

# -synctex=1 : indispensable pour la recherche avant/arriere entre l'editeur
# et la visionneuse PDF (le .synctex.gz suit toujours la derniere compilation)
latexmk_flags := "-pdf -interaction=nonstopmode -synctex=1"

# List available commands
default:
    @just --list

# Regenerate figures.toml and figures_parameters.tex from prov.json files
figures:
    python3 scripts/gen_figures.py

# Build the dissertation (externalize tikz, then compile)
build: (mode "")
    latexmk {{latexmk_flags}} {{main_tex}}.tex
    make -f {{main_tex}}.makefile
    latexmk {{latexmk_flags}} {{main_tex}}.tex

# Build without the joined papers' pdf (papers/ absent or omitted on purpose)
build-nopapers: (mode "\\def\\NOPAPERS{1}")
    latexmk {{latexmk_flags}} {{main_tex}}.tex
    make -f {{main_tex}}.makefile
    latexmk {{latexmk_flags}} {{main_tex}}.tex

# Ecrit build-mode.tex, lu par le preambule. Passer par un fichier plutot que
# par -usepretex est ce qui permet a latexmk de voir le changement de mode.
[private]
mode code:
    @printf '%s\n' '{{code}}' > build-mode.tex

# Build one or more chapters, e.g. `just chapter 5-Detection` or
# `just chapter 5-Detection,6-Apprentissage` (fast draft).
# Ecrase dissertation.pdf: relancer `just build` pour le document complet.
chapter names:
    #!/usr/bin/env bash
    set -euo pipefail
    # Un nom sans / est cherche dans Chapters/; FrontBackmatter/X reste tel quel
    list=$(echo "{{names}}" | tr ',' '\n' \
      | sed 's|^ *||; s| *$||' \
      | awk 'NF { if ($0 !~ "/") $0 = "Chapters/" $0; print }' \
      | paste -sd, -)
    # Cache tikz propre a cette selection: la numerotation des figures
    # externalisees est positionnelle, donc incompatible avec celle du
    # document complet.
    slug=$(echo "$list" | tr ',' '\n' | sed 's|.*/||' | paste -sd+ -)
    printf '%s\n' "\\def\\NOPAPERS{1}\\def\\TIKZPREFIX{ext-tikz/$slug-}\\includeonly{$list}" > build-mode.tex
    latexmk {{latexmk_flags}} {{main_tex}}.tex
    make -f {{main_tex}}.makefile
    latexmk {{latexmk_flags}} {{main_tex}}.tex

# Quick build (single pdflatex pass)
quick:
    pdflatex -interaction=nonstopmode -synctex=1 {{main_tex}}.tex

# Clean build artifacts
clean:
    latexmk -C {{main_tex}}.tex
