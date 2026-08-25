"""Carte d'Annecy pavee d'ellipses de covariance.

Chaque ellipse est la trace du tenseur de structure du MNT :
    J_rho = G_rho * (grad h  grad h^T)
matrice 2x2 SPD dont le vecteur propre dominant donne la direction de plus
forte pente. On dessine l'ellipse allongee le long des lignes de niveau
(vecteur propre de la plus petite valeur propre), d'excentricite egale a
l'anisotropie du tenseur : ronde en terrain isotrope, effilee sur les
cretes et les rives.

Le semis de points suit un Lloyd pondere (weighted Voronoi stippling,
Secord 2002) de densite proportionnelle a la pente : dense sur la
Tournette et le Semnoz, lache dans la plaine, calme sur le lac.
"""
import argparse, os
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.spatial import cKDTree
from matplotlib.path import Path

import dem

HERE = os.path.dirname(os.path.abspath(__file__))
BBOX = (6.05, 45.74, 6.36, 45.96)   # bassin annecien : lac + Semnoz + Tournette


# ---------------------------------------------------------------- geometrie
def assemble_rings(ways, tol=1e-6):
    """Recolle les ways OSM bout a bout en anneaux fermes."""
    ways = [w.copy() for w in ways]
    rings, cur = [], ways.pop(0)
    while True:
        merged = False
        for k, w in enumerate(ways):
            for a, b in ((0, 1), (1, 0)):
                seg = w if a == 0 else w[::-1]
                if np.allclose(cur[-1], seg[0], atol=tol):
                    cur = np.vstack([cur, seg[1:]]); ways.pop(k); merged = True; break
            if merged:
                break
        if not merged:
            rings.append(cur)
            if not ways:
                break
            cur = ways.pop(0)
    return rings


def lake_mask(shape, extent):
    lon0, lon1, lat0, lat1 = extent
    rings = assemble_rings(dem.fetch_lake())
    ny, nx = shape
    lon = np.linspace(lon0, lon1, nx)
    lat = np.linspace(lat1, lat0, ny)          # ligne 0 = nord
    X, Y = np.meshgrid(lon, lat)
    pts = np.column_stack([X.ravel(), Y.ravel()])
    m = np.zeros(pts.shape[0], dtype=bool)
    for r in rings:
        m |= Path(r).contains_points(pts)
    return m.reshape(shape), rings


# ------------------------------------------------------- tenseur de structure
def structure_tensor(h, sigma=1.5, rho=4.0):
    hs = gaussian_filter(h, sigma)
    gy, gx = np.gradient(hs)
    Jxx = gaussian_filter(gx * gx, rho)
    Jxy = gaussian_filter(gx * gy, rho)
    Jyy = gaussian_filter(gy * gy, rho)
    return Jxx, Jxy, Jyy


def tensor_ellipse(Jxx, Jxy, Jyy):
    """Renvoie (angle du petit vecteur propre, anisotropie dans [0,1])."""
    tr = Jxx + Jyy
    d = np.sqrt(np.maximum((Jxx - Jyy) ** 2 + 4 * Jxy ** 2, 0.0))
    l1, l2 = 0.5 * (tr + d), 0.5 * (tr - d)          # l1 >= l2 >= 0
    # vecteur propre dominant (direction de la pente)
    theta_max = 0.5 * np.arctan2(2 * Jxy, Jxx - Jyy)
    # grand axe de l'ellipse = orthogonal : le long de la ligne de niveau
    theta = theta_max + np.pi / 2
    aniso = np.where(tr > 1e-12, (l1 - l2) / (l1 + l2 + 1e-12), 0.0)
    return theta, aniso, l1


# ------------------------------------------------------ Lloyd pondere (2D)
def weighted_lloyd(density, n, iters=25, seed=0, sub=2):
    rng = np.random.default_rng(seed)
    ny, nx = density.shape
    d = density[::sub, ::sub]
    gy, gx = np.mgrid[0:d.shape[0], 0:d.shape[1]].astype(float)
    cells = np.column_stack([gx.ravel(), gy.ravel()])
    w = d.ravel().astype(float)
    keep = w > 0
    cells, w = cells[keep], w[keep]
    # tirage initial proportionnel a la densite
    p = w / w.sum()
    idx = rng.choice(len(cells), size=n, replace=True, p=p)
    pts = cells[idx] + rng.random((n, 2)) - 0.5
    for _ in range(iters):
        lab = cKDTree(pts).query(cells)[1]
        num = np.zeros((n, 2)); den = np.zeros(n)
        np.add.at(num, lab, cells * w[:, None])
        np.add.at(den, lab, w)
        alive = den > 0
        pts[alive] = num[alive] / den[alive, None]
        pts[~alive] = cells[rng.choice(len(cells), size=(~alive).sum(), p=p)]
    return pts * sub   # retour en coordonnees pixel pleine resolution


# --------------------------------------------------------------------- main
def build(n=2600, gamma=0.55, lake_floor=0.10, seed=1, z=12):
    h, extent = dem.fetch_dem(BBOX, z=z)
    mask, rings = lake_mask(h.shape, extent)
    Jxx, Jxy, Jyy = structure_tensor(h)
    theta, aniso, l1 = tensor_ellipse(Jxx, Jxy, Jyy)

    slope = np.sqrt(l1)
    dens = (slope / slope.max()) ** gamma
    dens = gaussian_filter(dens, 2.0)
    dens = np.clip(dens, 0.03, None)
    dens[mask] = lake_floor * dens.max()          # le lac respire

    pts = weighted_lloyd(dens, n, seed=seed)      # (x, y) en pixels
    xi = np.clip(pts[:, 0], 0, h.shape[1] - 1)
    yi = np.clip(pts[:, 1], 0, h.shape[0] - 1)
    c = np.vstack([yi, xi])
    th = np.arctan2(map_coordinates(np.sin(2 * theta), c, order=1),
                    map_coordinates(np.cos(2 * theta), c, order=1)) / 2
    an = map_coordinates(aniso, c, order=1)
    on_lake = map_coordinates(mask.astype(float), c, order=1) > 0.5
    alt = map_coordinates(h, c, order=1)

    # rayon local : moitie de la distance au plus proche voisin
    dd = cKDTree(pts).query(pts, k=2)[0][:, 1]
    r = 0.52 * dd
    ratio = np.clip(1 - 0.92 * an, 0.10, 1.0)     # b/a
    a = r / np.sqrt(np.clip(ratio, 0.1, 1))
    b = a * ratio
    a, b = np.minimum(a, 2.2 * r), np.minimum(b, 2.2 * r)
    an[on_lake] = 0.0
    return dict(x=xi, y=yi, a=a, b=b, theta=th, aniso=an, alt=alt,
                lake=on_lake, shape=h.shape, extent=extent, rings=rings, dem=h)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=2600)
    ap.add_argument("--out", default=os.path.join(HERE, "apercu.png"))
    args = ap.parse_args()
    d = build(n=args.n)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import EllipseCollection

    ny, nx = d["shape"]
    fig, ax = plt.subplots(figsize=(21 / 2.54, 29.7 / 2.54), dpi=160)
    ax.set_xlim(0, nx); ax.set_ylim(ny, 0); ax.set_aspect("equal"); ax.axis("off")
    col = EllipseCollection(2 * d["a"], 2 * d["b"], np.degrees(-d["theta"]),
                            units="xy", offsets=np.column_stack([d["x"], d["y"]]),
                            transOffset=ax.transData, facecolors="none",
                            edgecolors=np.where(d["lake"], "#2a4a8a", "#2d2d2d"),
                            linewidths=0.35)
    ax.add_collection(col)
    fig.savefig(args.out, bbox_inches="tight", facecolor="white")
    print("ecrit", args.out, "-", len(d["x"]), "ellipses")
