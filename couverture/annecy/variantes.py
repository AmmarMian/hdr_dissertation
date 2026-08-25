"""Quatre traitements de la carte d'Annecy en ellipses, pour comparaison."""
import os
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection

import dem
from stipple import lake_mask, structure_tensor, tensor_ellipse, weighted_lloyd

HERE = os.path.dirname(os.path.abspath(__file__))
BBOX = (6.048, 45.72, 6.332, 46.00)     # cadrage A4 portrait sur le bassin


def field(z=12, rho=6.0):
    h, extent = dem.fetch_dem(BBOX, z=z)
    mask, rings = lake_mask(h.shape, extent)
    hf = h.copy()
    hf[mask] = np.median(h[mask]) if mask.any() else h.min()   # lac plat
    J = structure_tensor(hf, sigma=2.0, rho=rho)
    theta, aniso, l1 = tensor_ellipse(*J)
    return dict(h=h, mask=mask, theta=theta, aniso=aniso, slope=np.sqrt(l1),
                extent=extent, rings=rings)


def sample(f, x, y, arr):
    return map_coordinates(arr, np.vstack([y, x]), order=1)


def at(f, x, y):
    th = np.arctan2(sample(f, x, y, np.sin(2 * f["theta"])),
                    sample(f, x, y, np.cos(2 * f["theta"]))) / 2
    return th, sample(f, x, y, f["aniso"]), sample(f, x, y, f["h"]), \
           sample(f, x, y, f["mask"].astype(float)) > 0.5


def hexgrid(shape, step):
    ny, nx = shape
    pts = []
    dy = step * np.sqrt(3) / 2
    for k, yy in enumerate(np.arange(step, ny, dy)):
        off = (k % 2) * step / 2
        pts += [(xx + off, yy) for xx in np.arange(step / 2, nx - step / 4, step)]
    return np.array(pts)


def draw(ax, f, xy, r, ratio, th, fc, ec, lw):
    a = r / np.sqrt(ratio)
    b = r * np.sqrt(ratio)
    ax.add_collection(EllipseCollection(
        2 * a, 2 * b, np.degrees(-th), units="xy", offsets=xy,
        transOffset=ax.transData, facecolors=fc, edgecolors=ec, linewidths=lw))


def frame(ax, shape):
    ny, nx = shape
    ax.set_xlim(0, nx); ax.set_ylim(ny, 0)
    ax.set_aspect("equal"); ax.axis("off")


# ----------------------------------------------------------------- variantes
def variante_A(ax, f, n=1100):
    """Semis de Lloyd calme, contours fins, lac en bleu."""
    d = np.clip((f["slope"] / f["slope"].max()) ** 0.5, 0.05, None)
    d = gaussian_filter(d, 3.0); d[f["mask"]] = 0.22 * d.max()
    p = weighted_lloyd(d, n, seed=3)
    x, y = p[:, 0], p[:, 1]
    th, an, alt, lake = at(f, x, y)
    r = 0.50 * cKDTree(p).query(p, k=2)[0][:, 1]
    ratio = np.clip(1 - 0.80 * an, 0.30, 1.0)
    draw(ax, f, p, r, ratio, np.where(lake, 0, th), "none",
         np.where(lake, "#2a4a8a", "#2d2d2d"), 0.45)
    frame(ax, f["h"].shape); ax.set_title("A — semis de Lloyd, contours", fontsize=7)


def variante_B(ax, f, step=17):
    """Grille hexagonale, taille constante : la carte comme motif regulier."""
    p = hexgrid(f["h"].shape, step)
    x, y = p[:, 0], p[:, 1]
    th, an, alt, lake = at(f, x, y)
    ratio = np.clip(1 - 0.85 * an, 0.22, 1.0)
    ratio[lake] = 1.0
    draw(ax, f, p, np.full(len(p), 0.46 * step), ratio, th, "none",
         np.where(lake, "#3a6090", "#3a3a3a"), 0.4)
    frame(ax, f["h"].shape); ax.set_title("B — grille hexagonale, contours", fontsize=7)


def variante_C(ax, f, step=15):
    """Grille hexagonale, aplats : la valeur porte l'altitude, le lac est vide."""
    p = hexgrid(f["h"].shape, step)
    x, y = p[:, 0], p[:, 1]
    th, an, alt, lake = at(f, x, y)
    ratio = np.clip(1 - 0.85 * an, 0.20, 1.0)
    v = np.clip((alt - 430) / (1900 - 430), 0, 1)
    fc = plt.cm.Greys(0.18 + 0.72 * v)
    fc[lake] = matplotlib.colors.to_rgba("#e8eef6")
    ratio[lake] = 1.0
    r = np.full(len(p), 0.46 * step) * np.where(lake, 0.55, 0.75 + 0.45 * v)
    draw(ax, f, p, r, ratio, th, fc, "none", 0)
    frame(ax, f["h"].shape); ax.set_title("C — aplats, taille et valeur ∝ altitude", fontsize=7)


def variante_D(ax, f, n=2200):
    """Semis dense en aplats sombres : le relief comme une gravure."""
    d = np.clip((f["slope"] / f["slope"].max()) ** 0.75, 0.02, None)
    d = gaussian_filter(d, 2.5); d[f["mask"]] = 0.02
    p = weighted_lloyd(d, n, seed=5)
    x, y = p[:, 0], p[:, 1]
    th, an, alt, lake = at(f, x, y)
    r = 0.48 * cKDTree(p).query(p, k=2)[0][:, 1]
    ratio = np.clip(1 - 0.85 * an, 0.22, 1.0)
    draw(ax, f, p, r, ratio, th, np.where(lake, "#b9c8dd", "#33383f"), "none", 0)
    frame(ax, f["h"].shape); ax.set_title("D — semis dense, aplats", fontsize=7)


if __name__ == "__main__":
    f = field()
    fig, axes = plt.subplots(1, 4, figsize=(16, 6.2), dpi=170)
    for ax, v in zip(axes, (variante_A, variante_B, variante_C, variante_D)):
        v(ax, f)
    fig.tight_layout()
    out = os.path.join(HERE, "variantes.png")
    fig.savefig(out, facecolor="white", bbox_inches="tight")
    print("ecrit", out)
