"""Deux maquettes A4 : le champ de covariances avec le texte de couverture."""
import os
import numpy as np
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import lac as L, variantes as V

HERE = os.path.dirname(os.path.abspath(__file__))


def ls(s, n=3):
    return (" " * n).join(s)


def texte(ax, ny, nx, couleur="#1e3c78", gris="#6e6e6e"):
    k = dict(ha="center", transform=ax.transData)
    ax.text(nx / 2, 0.085 * ny, ls("AMMAR MIAN"), color=gris, fontsize=7.5, **k)
    ax.text(nx / 2, 0.145 * ny, ls("HABILITATION À DIRIGER DES RECHERCHES", 2),
            color=couleur, fontsize=13, **k)
    ax.text(nx / 2, 0.195 * ny, "Matrices de covariances :", color="#2d2d2d", fontsize=10, **k)
    ax.text(nx / 2, 0.222 * ny, "des statistiques multivariées à l'apprentissage profond",
            color="#2d2d2d", fontsize=10, **k)
    ax.text(nx / 2, 0.285 * ny, ls("UNIVERSITÉ SAVOIE MONT-BLANC"), color=gris, fontsize=6.5, **k)


def maquette_sombre(ax, f):
    """Aplats sombres, lac isotrope, densite eteinte sous le titre."""
    p, th, an, alt, lake, r = L.semis(f, 3000, 0.7, 0.45, seed=8)
    ny, nx = f["h"].shape
    fade = np.clip((p[:, 1] / ny - 0.30) / 0.10, 0, 1)     # blanc en haut de page
    ratio = np.where(lake, 1.0, np.clip(1 - .85 * an, .22, 1))
    base = np.where(lake[:, None], np.array([[0.76, 0.83, 0.91]]), np.array([[0.20, 0.22, 0.25]]))
    fc = 1 - (1 - base) * fade[:, None]
    V.draw(ax, f, p, r, ratio, np.where(lake, 0, th), fc, "none", 0)
    V.frame(ax, f["h"].shape)
    texte(ax, ny, nx)


def maquette_claire(ax, f):
    """Aplats gris clairs indexes sur l'altitude, lac vide cerne d'un filet."""
    p, th, an, alt, lake, r = L.semis(f, 3400, 0.4, 0.0, seed=8)
    ny, nx = f["h"].shape
    keep = ~lake
    v = np.clip((alt[keep] - 440) / (1900 - 440), 0, 1)
    fade = np.clip((p[keep, 1] / ny - 0.30) / 0.12, 0, 1)
    fc = np.array(plt.cm.Greys(0.20 + 0.66 * v))[:, :3]
    fc = 1 - (1 - fc) * fade[:, None]
    V.draw(ax, f, p[keep], r[keep] * (0.78 + 0.4 * v),
           np.clip(1 - .85 * an[keep], .22, 1), th[keep], fc, "none", 0)
    L.contour_lac(ax, f, color="#2a4a8a", lw=0.6, alpha=0.85)
    V.frame(ax, f["h"].shape)
    texte(ax, ny, nx)


if __name__ == "__main__":
    f = L.field()
    for nom, fn in (("maquette-sombre", maquette_sombre), ("maquette-claire", maquette_claire)):
        fig, ax = plt.subplots(figsize=(21 / 2.54, 29.7 / 2.54), dpi=150)
        fig.subplots_adjust(0, 0, 1, 1)
        fn(ax, f)
        out = os.path.join(HERE, nom + ".png")
        fig.savefig(out, facecolor="white")
        plt.close(fig)
        print("ecrit", out)
