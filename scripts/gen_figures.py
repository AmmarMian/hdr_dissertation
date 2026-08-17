#!/usr/bin/env python3
"""Regenerate figures.toml and figures_parameters.tex from prov.json files."""

import json
from pathlib import Path


DOCS_BASE_URL = "https://ammarmian.fr/simulations_hdr"
INFRA_PARAMS = {"storage_path", "export_path", "output_dir"}


def to_camel(fig_id: str) -> str:
    return "".join(w.capitalize() for w in fig_id.replace("_", "-").split("-"))


def tex_escape(s: str) -> str:
    return s.replace("_", r"\_")


def main():
    gen = Path("gfx/generated")
    prov_files = sorted(gen.rglob("prov.json"))

    # --- figures.toml ---
    toml_lines = [
        "# figures.toml — registered figures for the HDR dissertation",
        "# Auto-generated from prov.json files — do not edit by hand.",
        "",
    ]

    # --- figures_parameters.tex ---
    tex_lines = [
        "% Auto-generated figure provenance commands — do not edit by hand.",
        r"% Usage: \provMyFigId expands to formatted provenance string.",
        r"% Customise the look by redefining \provStyle, \provKey, \provVal, \provSep.",
        "",
        r"\providecommand{\provStyle}[1]{\begingroup\footnotesize\color{gray}\ttfamily #1\endgroup}",
        r"\providecommand{\provKey}[1]{#1=}",
        r"\providecommand{\provVal}[1]{#1}",
        r"\providecommand{\provSep}{\,\textperiodcentered\,}",
        r"\providecommand{\provLink}[2]{\href{#1}{#2}}",
        r"\providecommand{\provQR}[1]{\protect\qrcode[height=1cm]{#1}}",
        r"\providecommand{\provMarginQR}[2][0pt]{\marginnote{\centering\provQR{#2}\\[2pt]\provStyle{Code}}[#1]}",
        "",
    ]

    for pf in prov_files:
        d = json.loads(pf.read_text())
        h = d.get("hdr", {})
        fid = h.get("id", pf.parent.name)
        exp = h.get("exp", "")
        sha = h.get("sha_short", "")
        run_date = h.get("run_date", "")
        seed = h.get("seed", "")
        run_id = h.get("run_id", "?")
        embed = str(h.get("embed_npy", False)).lower()

        toml_lines += [
            f"[figures.{fid}]",
            f'exp       = "{exp}"',
            f'sha       = "{sha}"',
            f'run_date  = "{run_date}"',
            f'seed      = "{seed}"',
            f"embed_npy = {embed}",
            "",
        ]

        cmd_name = "prov" + to_camel(fid)
        exp_url = f"{DOCS_BASE_URL}/experiments/{exp}/"
        items = [
            ("sha", tex_escape(sha)),
            ("date", tex_escape(run_date)),
        ]
        if seed and seed != "deterministic":
            items.append(("seed", tex_escape(seed)))

        run_args = d.get("args", {})
        for key, value in run_args.items():
            if key in INFRA_PARAMS or key == "seed":
                continue
            items.append((tex_escape(key), tex_escape(str(value))))

        inner = r" \provSep ".join(
            r"\provKey{" + k + "}" + r"\provVal{" + v + "}"
            for k, v in items
        )
        tex_lines.append(
            r"\providecommand{" + "\\" + cmd_name + "}"
            + r"{\provStyle{" + inner + "}}"
        )
        tex_lines.append(
            r"\providecommand{" + "\\" + cmd_name + "QR}[1][0pt]"
            + r"{\provMarginQR[#1]{" + exp_url + "}}"
        )

    (gen / "figures.toml").write_text("\n".join(toml_lines) + "\n")
    (gen / "figures_parameters.tex").write_text("\n".join(tex_lines) + "\n")
    print(f"figures.toml + figures_parameters.tex: {len(prov_files)} figure(s)")


if __name__ == "__main__":
    main()
