"""Cadrage serre sur le lac : quatre traitements du plan d'eau."""
import os
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import dem, stipple, variantes as V

HERE = os.path.dirname(os.path.abspath(__file__))
# Le lac (6.128-6.232 E, 45.793-45.906 N) tient au centre, avec Semnoz a
# l'ouest et Tournette a l'est. Proportions calees sur l'A4 portrait.
BBOX = (6.088, 45.762, 6.288, 45.952)


def field(z=13, rho=7.0):
    V.BBOX = BBOX
    return V.field(z=z, rho=rho)


def semis(f, n, gamma, lake_floor, seed=4):
    d = np.clip((f["slope"] / f["slope"].max()) ** gamma, 0.02, None)
    d = gaussian_filter(d, 3.0)
    d[f["mask"]] = lake_floor * d.max() if lake_floor > 0 else 1e-9
    p = V.weighted_lloyd(d, n, seed=seed)
    th, an, alt, lake = V.at(f, p[:, 0], p[:, 1])
    r = 0.48 * cKDTree(p).query(p, k=2)[0][:, 1]
    return p, th, an, alt, lake, r


def contour_lac(ax, f, **kw):
    ny, nx = f["h"].shape
    lon0, lon1, lat0, lat1 = f["extent"]
    for r in stipple.assemble_rings(dem.fetch_lake()):
        x = (r[:, 0] - lon0) / (lon1 - lon0) * nx
        y = (lat1 - r[:, 1]) / (lat1 - lat0) * ny
        ax.plot(x, y, **kw)


def P1(ax, f):
    """Lac vide : la silhouette se lit en negatif."""
    p, th, an, alt, lake, r = semis(f, 2400, 0.7, 0.0)
    keep = ~lake
    V.draw(ax, f, p[keep], r[keep], np.clip(1 - .85 * an[keep], .22, 1), th[keep],
           "#33383f", "none", 0)
    V.frame(ax, f["h"].shape); ax.set_title("1 — lac vide", fontsize=7)


def P2(ax, f):
    """Lac pave d'ellipses rondes et pales : l'eau comme covariance isotrope."""
    p, th, an, alt, lake, r = semis(f, 2600, 0.7, 0.45)
    th2 = np.where(lake, 0.0, th)
    ratio = np.where(lake, 1.0, np.clip(1 - .85 * an, .22, 1))
    V.draw(ax, f, p, r, ratio, th2, np.where(lake, "#c3d3e8", "#33383f"), "none", 0)
    V.frame(ax, f["h"].shape); ax.set_title("2 — lac isotrope pâle", fontsize=7)


def P3(ax, f):
    """Aplats d'altitude, lac vide et cerne d'un filet."""
    p, th, an, alt, lake, r = semis(f, 3200, 0.35, 0.0)
    keep = ~lake
    v = np.clip((alt[keep] - 440) / (1900 - 440), 0, 1)
    fc = plt.cm.Greys(0.22 + 0.70 * v)
    V.draw(ax, f, p[keep], r[keep] * (0.75 + 0.4 * v),
           np.clip(1 - .85 * an[keep], .22, 1), th[keep], fc, "none", 0)
    contour_lac(ax, f, color="#2a4a8a", lw=0.7)
    V.frame(ax, f["h"].shape); ax.set_title("3 — valeur ∝ altitude, filet sur la rive", fontsize=7)


def P4(ax, f):
    """Contours seuls, lac en ellipses bleues : la version legere."""
    p, th, an, alt, lake, r = semis(f, 1500, 0.6, 0.5)
    ratio = np.where(lake, 1.0, np.clip(1 - .80 * an, .28, 1))
    V.draw(ax, f, p, r, ratio, np.where(lake, 0, th), "none",
           np.where(lake, "#3a6090", "#2d2d2d"), 0.45)
    V.frame(ax, f["h"].shape); ax.set_title("4 — contours seuls", fontsize=7)


if __name__ == "__main__":
    f = field()
    print("MNT", f["h"].shape, "lac", f["mask"].mean())
    fig, axes = plt.subplots(1, 4, figsize=(16, 6.2), dpi=170)
    for ax, v in zip(axes, (P1, P2, P3, P4)):
        v(ax, f)
    fig.tight_layout()
    out = os.path.join(HERE, "lac.png")
    fig.savefig(out, facecolor="white", bbox_inches="tight")
    print("ecrit", out)
