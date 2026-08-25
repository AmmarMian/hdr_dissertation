"""Registre discret : peu d'encre, beaucoup de blanc, un filet de 0.2 pt.

Le relief ne doit pas s'imposer : il doit se laisser trouver. Six reglages
du meme champ de covariances, du plus efface au presque-rien.
"""
import os
import numpy as np
from scipy.ndimage import gaussian_filter, distance_transform_edt
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import lac as L, variantes as V, stipple, dem

HERE = os.path.dirname(os.path.abspath(__file__))
BLEU = "#1e3c78"        # CTtitle du manuscrit
GRIS = "#6e6e6e"


def semis_libre(f, n, dens, seed=11, k=0.34):
    """Semis de Lloyd sur une densite quelconque ; ellipses plus petites que
    la cellule, pour qu'elles ne se touchent jamais."""
    p = V.weighted_lloyd(dens, n, seed=seed)
    th, an, alt, lake = V.at(f, p[:, 0], p[:, 1])
    r = k * cKDTree(p).query(p, k=2)[0][:, 1]
    return p, th, an, alt, lake, r


def dens_pente(f, gamma=0.5, floor=0.0):
    d = np.clip((f["slope"] / f["slope"].max()) ** gamma, 0.03, None)
    d = gaussian_filter(d, 3.0)
    d[f["mask"]] = floor * d.max() if floor > 0 else 1e-9
    return d


def trace(ax, f, p, r, an, th, couleur, lw=0.25, amax=0.75, alpha=1.0):
    ratio = np.clip(1 - amax * an, 0.30, 1.0)
    V.draw(ax, f, p, r, ratio, th, "none", couleur, lw)
    ax.collections[-1].set_alpha(alpha)


def S1(ax, f):
    """Le champ complet, mais dilue : contour fin, gris pale, semis lache."""
    p, th, an, alt, lake, r = semis_libre(f, 850, dens_pente(f, 0.5, 0.35))
    trace(ax, f, p, r, an, np.where(lake, 0, th), GRIS, 0.25, 0.75, 0.55)
    V.frame(ax, f["h"].shape); ax.set_title("S1 — le champ dilué", fontsize=6)


def S2(ax, f):
    """Seuil d'anisotropie : seules les cretes se dessinent, le reste est blanc."""
    d = np.ones_like(f["slope"]); d[f["mask"]] = 1e-9
    p, th, an, alt, lake, r = semis_libre(f, 3000, d, k=0.40)
    keep = an > np.quantile(an, 0.72)
    trace(ax, f, p[keep], r[keep], an[keep], th[keep], GRIS, 0.3, 0.85, 0.8)
    V.frame(ax, f["h"].shape); ax.set_title("S2 — seuil d'anisotropie", fontsize=6)


def S3(ax, f):
    """Bandeau : le champ n'occupe que le pied de page et se dissout vers le haut."""
    ny, nx = f["h"].shape
    d = dens_pente(f, 0.5, 0.35)
    ramp = np.clip((np.arange(ny) / ny - 0.42) / 0.30, 0, 1)[:, None]
    p, th, an, alt, lake, r = semis_libre(f, 1400, d * ramp)
    a = np.clip((p[:, 1] / ny - 0.45) / 0.22, 0, 1) * 0.75
    for i in range(len(p)):
        pass
    trace(ax, f, p, r, an, np.where(lake, 0, th), GRIS, 0.25, 0.75, 0.7)
    ax.collections[-1].set_alpha(None)
    ax.collections[-1].set_edgecolor(np.column_stack(
        [np.tile(matplotlib.colors.to_rgb(GRIS), (len(p), 1)), a]))
    V.frame(ax, f["h"].shape); ax.set_title("S3 — bandeau de pied de page", fontsize=6)


def S4(ax, f):
    """La rive seule : densite decroissante avec la distance au trait de cote.
    Le lac n'est jamais dessine, il apparait comme un creux."""
    din = distance_transform_edt(f["mask"])
    dout = distance_transform_edt(~f["mask"])
    dist = np.where(f["mask"], din, dout)
    d = np.exp(-dist / 55.0)
    d[f["mask"]] = 0.35 * d[f["mask"]]
    p, th, an, alt, lake, r = semis_libre(f, 1300, d, k=0.38)
    trace(ax, f, p, r, an, np.where(lake, 0, th), BLEU, 0.28, 0.8, 0.7)
    V.frame(ax, f["h"].shape); ax.set_title("S4 — la rive seule", fontsize=6)


def S5(ax, f):
    """Grain : beaucoup d'ellipses minuscules, taille constante, seule
    l'orientation varie. Le relief est une texture, pas un dessin."""
    ny, nx = f["h"].shape
    p = V.hexgrid((ny, nx), 26)
    th, an, alt, lake = V.at(f, p[:, 0], p[:, 1])
    ratio = np.where(lake, 1.0, np.clip(1 - 0.9 * an, 0.18, 1.0))
    V.draw(ax, f, p, np.full(len(p), 6.2), ratio, th, "none", GRIS, 0.22)
    ax.collections[-1].set_alpha(0.6)
    V.frame(ax, f["h"].shape); ax.set_title("S5 — grain régulier", fontsize=6)


def S6(ax, f):
    """Monochrome CTtitle, tres dilue : le relief affleure a peine."""
    p, th, an, alt, lake, r = semis_libre(f, 1100, dens_pente(f, 0.45, 0.30), k=0.32)
    trace(ax, f, p, r, an, np.where(lake, 0, th), BLEU, 0.24, 0.8, 0.38)
    V.frame(ax, f["h"].shape); ax.set_title("S6 — bichromie, encre à 35 %", fontsize=6)


if __name__ == "__main__":
    f = L.field()
    fig, axes = plt.subplots(1, 6, figsize=(19, 5.0), dpi=200)
    for ax, v in zip(axes, (S1, S2, S3, S4, S5, S6)):
        v(ax, f)
    fig.tight_layout()
    out = os.path.join(HERE, "subtil.png")
    fig.savefig(out, facecolor="white", bbox_inches="tight")
    print("ecrit", out)
