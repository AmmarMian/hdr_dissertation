"""Recupere le MNT du bassin annecien et le contour OSM du lac.

MNT : tuiles terrarium (AWS elevation-tiles-prod), libres et sans cle.
Lac : relation OSM 2390533, via Overpass.
Tout est mis en cache dans ce repertoire pour ne telecharger qu'une fois.
"""
import json, math, os, urllib.parse, urllib.request
import numpy as np

UA = {"User-Agent": "hdr-cover-sketch/0.1 (amr.mian@gmail.com)"}


def _get(url, timeout=90):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
os.makedirs(CACHE, exist_ok=True)


def _deg2tile(lon, lat, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def fetch_dem(bbox, z=12):
    """bbox = (lon_min, lat_min, lon_max, lat_max). Renvoie (altitudes, extent)."""
    from PIL import Image
    lon0, lat0, lon1, lat1 = bbox
    x0f, y0f = _deg2tile(lon0, lat1, z)   # lat1 = nord = haut
    x1f, y1f = _deg2tile(lon1, lat0, z)
    x0, y0, x1, y1 = int(x0f), int(y0f), int(x1f), int(y1f)
    tiles = np.zeros(((y1 - y0 + 1) * 256, (x1 - x0 + 1) * 256), dtype=np.float64)
    for ty in range(y0, y1 + 1):
        for tx in range(x0, x1 + 1):
            path = os.path.join(CACHE, f"t{z}_{tx}_{ty}.png")
            if not os.path.exists(path):
                url = f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{tx}/{ty}.png"
                open(path, "wb").write(_get(url, 60))
            rgb = np.asarray(Image.open(path).convert("RGB"), dtype=np.float64)
            alt = rgb[:, :, 0] * 256 + rgb[:, :, 1] + rgb[:, :, 2] / 256 - 32768
            tiles[(ty - y0) * 256:(ty - y0 + 1) * 256, (tx - x0) * 256:(tx - x0 + 1) * 256] = alt
    # recadrage exact sur la bbox demandee (en coordonnees de tuile fractionnaires)
    i0 = int(round((y0f - y0) * 256)); i1 = int(round((y1f - y0) * 256))
    j0 = int(round((x0f - x0) * 256)); j1 = int(round((x1f - x0) * 256))
    return tiles[i0:i1, j0:j1], (lon0, lon1, lat0, lat1)


def fetch_lake(rel_id=2390533):
    """Contour exterieur du lac, en (lon, lat)."""
    path = os.path.join(CACHE, f"lac{rel_id}.json")
    if not os.path.exists(path):
        q = f"[out:json][timeout:60];rel({rel_id});out geom;"
        url = "https://overpass-api.de/api/interpreter?data=" + urllib.parse.quote(q)
        open(path, "wb").write(_get(url))
    d = json.load(open(path))
    rings = []
    for m in d["elements"][0]["members"]:
        if m.get("role") == "outer" and "geometry" in m:
            rings.append(np.array([[p["lon"], p["lat"]] for p in m["geometry"]]))
    return rings


if __name__ == "__main__":
    import urllib.parse
    dem, ext = fetch_dem((6.05, 45.74, 6.36, 45.96), z=12)
    print("MNT", dem.shape, dem.min(), dem.max())
    rings = fetch_lake()
    print("lac :", len(rings), "segments,", sum(len(r) for r in rings), "points")
