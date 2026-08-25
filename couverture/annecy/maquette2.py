"""Registre juste : une texture regulière et pâle, le lac laissé en blanc.

Le contraste ne vient pas de la quantite d'encre mais du vide : le semis est
uniforme sur la terre, nul sur l'eau. Au premier regard, un grain ; ensuite,
la silhouette du lac ; enfin, les cretes, portees par l'orientation du
tenseur de structure.
"""
import os
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection

import lac as L, variantes as V

HERE = os.path.dirname(os.path.abspath(__file__))
BLEU = np.array(matplotlib.colors.to_rgb("#1e3c78"))
ENCRE = np.array(matplotlib.colors.to_rgb("#2d2d2d"))


def ls(s, n=3):
    return (" " * n).join(s)


def texte(ax, ny, nx):
    k = dict(ha="center")
    ax.text(nx / 2, 0.085 * ny, ls("AMMAR MIAN"), color="#6e6e6e", fontsize=6.5, **k)
    ax.text(nx / 2, 0.142 * ny, ls("HABILITATION À DIRIGER DES RECHERCHES", 2),
            color="#1e3c78", fontsize=10.5, **k)
    ax.text(nx / 2, 0.192 * ny, "Matrices de covariances :", color="#2d2d2d", fontsize=9, **k)
    ax.text(nx / 2, 0.218 * ny, "des statistiques multivariées à l'apprentissage profond",
            color="#2d2d2d", fontsize=9, **k)
    ax.text(nx / 2, 0.283 * ny, ls("UNIVERSITÉ SAVOIE MONT-BLANC"), color="#6e6e6e",
            fontsize=5.5, **k)


def champ(f, n, seed=17, rmax=11.0, k=0.40):
    """Semis uniforme sur la terre ferme, ellipses de taille bornee."""
    d = np.ones(f["h"].shape); d[f["mask"]] = 1e-9
    p = V.weighted_lloyd(d, n, seed=seed)
    th, an, alt, lake = V.at(f, p[:, 0], p[:, 1])
    r = np.minimum(k * cKDTree(p).query(p, k=2)[0][:, 1], rmax)
    keep = ~lake
    return p[keep], th[keep], an[keep], alt[keep], r[keep]


def pose(ax, f, p, r, an, th, rgb, encre, lw=None):
    """encre = opacite par ellipse ; lw None => aplats."""
    ratio = np.clip(1 - 0.88 * an, 0.22, 1.0)
    a, b = r / np.sqrt(ratio), r * np.sqrt(ratio)
    col = np.column_stack([np.tile(rgb, (len(p), 1)), np.clip(encre, 0, 1)])
    kw = dict(facecolors="none", edgecolors=col, linewidths=lw) if lw else \
         dict(facecolors=col, edgecolors="none", linewidths=0)
    ax.add_collection(EllipseCollection(2 * a, 2 * b, np.degrees(-th), units="xy",
                                        offsets=p, transOffset=ax.transData, **kw))


def haut(p, ny, seuil=0.31, doux=0.13):
    """Fondu vers le haut de page, pour degager le titre."""
    return np.clip((p[:, 1] / ny - seuil) / doux, 0, 1)


# ------------------------------------------------------------------ variantes
def T1(ax, f):
    """Contours fins, encre modulee par la pente."""
    p, th, an, alt, r = champ(f, 2000)
    ny = f["h"].shape[0]
    s = np.clip(an / np.quantile(an, 0.9), 0, 1)
    pose(ax, f, p, r, an, th, ENCRE, (0.20 + 0.45 * s) * haut(p, ny), lw=0.32)
    V.frame(ax, f["h"].shape); texte(ax, *f["h"].shape)


def T2(ax, f):
    """Aplats gris tres clairs : un grain de papier."""
    p, th, an, alt, r = champ(f, 2600, rmax=9.5)
    ny = f["h"].shape[0]
    s = np.clip(an / np.quantile(an, 0.9), 0, 1)
    pose(ax, f, p, r * 0.92, an, th, ENCRE, (0.16 + 0.36 * s) * haut(p, ny))
    V.frame(ax, f["h"].shape); texte(ax, *f["h"].shape)


def T3(ax, f):
    """Bichromie : terre en gris, filet de rive en CTtitle."""
    p, th, an, alt, r = champ(f, 2000)
    ny = f["h"].shape[0]
    s = np.clip(an / np.quantile(an, 0.9), 0, 1)
    pose(ax, f, p, r, an, th, ENCRE, (0.18 + 0.40 * s) * haut(p, ny), lw=0.3)
    L.contour_lac(ax, f, color="#1e3c78", lw=0.5, alpha=0.55)
    V.frame(ax, f["h"].shape); texte(ax, *f["h"].shape)


def T4(ax, f):
    """Vignettage : l'encre s'eteint aussi vers les bords, le lac reste au centre."""
    p, th, an, alt, r = champ(f, 2400, rmax=10)
    ny, nx = f["h"].shape
    dx = np.abs(p[:, 0] / nx - 0.5) * 2
    vig = np.clip(1.25 - dx ** 2 * 1.35, 0, 1)
    s = np.clip(an / np.quantile(an, 0.9), 0, 1)
    pose(ax, f, p, r, an, th, BLEU, (0.20 + 0.42 * s) * haut(p, ny) * vig, lw=0.32)
    V.frame(ax, f["h"].shape); texte(ax, *f["h"].shape)


if __name__ == "__main__":
    f = L.field()
    for nom, fn in (("T1-contours", T1), ("T2-grain", T2),
                    ("T3-bichromie", T3), ("T4-vignettage", T4)):
        fig, ax = plt.subplots(figsize=(21 / 2.54, 29.7 / 2.54), dpi=150)
        fig.subplots_adjust(0, 0, 1, 1)
        fn(ax, f)
        out = os.path.join(HERE, nom + ".png")
        fig.savefig(out, facecolor="white"); plt.close(fig)
        print("ecrit", out)
