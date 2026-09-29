"""Fetch HLS-equivalent 6-band chips per site, before and after the event date
(O8). Source: Sentinel-2 L2A COGs via the public Earth Search STAC API (the
S30 source sensor of HLS; same six HLS bands). Cloud-screened via
eo:cloud_cover sorting plus an SCL-window check.

Writes demonstrator/out/chips.npz (git-ignored raw arrays) and
demonstrator/out/chips_meta.json (committed provenance).

Usage: python3 demonstrator/fetch_chips.py
"""

from __future__ import annotations

import datetime as dt
import json
import urllib.request
from pathlib import Path

import numpy as np
import rasterio
from rasterio.warp import transform as warp_transform
from rasterio.windows import from_bounds

STAC = "https://earth-search.aws.element84.com/v1/search"
BANDS = ["blue", "green", "red", "nir08", "swir16", "swir22"]  # HLS six
SIZE = 224          # pixels
EXTENT_M = 2240.0   # 10 m grid

CLOUD_SCL = {3, 8, 9, 10}  # shadow, cloud med/high, cirrus


def stac_search(lat, lon, start, end, limit=6):
    body = {
        "collections": ["sentinel-2-l2a"],
        "intersects": {"type": "Point", "coordinates": [lon, lat]},
        "datetime": f"{start}T00:00:00Z/{end}T23:59:59Z",
        "limit": limit,
        "sortby": [{"field": "properties.eo:cloud_cover", "direction": "asc"}],
    }
    req = urllib.request.Request(
        STAC, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "User-Agent": "geovlm-demonstrator"},
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)["features"]


def read_window(href, lat, lon):
    with rasterio.open(href) as src:
        xs, ys = warp_transform("EPSG:4326", src.crs, [lon], [lat])
        x, y = xs[0], ys[0]
        half = EXTENT_M / 2
        win = from_bounds(x - half, y - half, x + half, y + half,
                          src.transform)
        return src.read(1, window=win, out_shape=(SIZE, SIZE),
                        boundless=True, fill_value=0)


def chip_for(item, lat, lon):
    assets = item["assets"]
    scl = read_window(assets["scl"]["href"], lat, lon)
    cloud_frac = float(np.isin(scl, list(CLOUD_SCL)).mean())
    nodata_frac = float((scl == 0).mean())
    if cloud_frac > 0.25 or nodata_frac > 0.20:
        return None, cloud_frac
    bands = [
        read_window(assets[b]["href"], lat, lon).astype(np.float32) / 10000.0
        for b in BANDS
    ]
    return np.stack(bands), cloud_frac


def best_chip(lat, lon, start, end):
    for item in stac_search(lat, lon, start, end):
        try:
            chip, cf = chip_for(item, lat, lon)
        except Exception as e:  # noqa: BLE001
            print(f"    read failed {item['id']}: {str(e)[:60]}")
            continue
        if chip is not None:
            return chip, {
                "scene": item["id"],
                "datetime": item["properties"]["datetime"][:10],
                "scene_cloud_cover": item["properties"].get("eo:cloud_cover"),
                "window_cloud_fraction": round(cf, 4),
            }
    return None, None


def main() -> None:
    here = Path(__file__).resolve().parent
    sites = json.loads((here / "out" / "sites.json").read_text())
    chips, meta = {}, []
    for s in sites:
        ev = dt.date.fromisoformat(s["event_date"])
        windows = {
            "before": (ev - dt.timedelta(days=150), ev - dt.timedelta(days=10)),
            "after": (ev + dt.timedelta(days=5), ev + dt.timedelta(days=100)),
        }
        rec = {"site_id": s["site_id"], "kind": s["kind"], "scenes": {}}
        ok = True
        for phase, (a, b) in windows.items():
            chip, m = best_chip(s["lat"], s["lon"], a.isoformat(), b.isoformat())
            if chip is None:
                ok = False
                print(f"  {s['site_id']} {phase}: no clean scene")
                break
            chips[f"{s['site_id']}_{phase}"] = chip
            rec["scenes"][phase] = m
        if ok:
            meta.append(rec)
            print(f"  {s['site_id']}: ok "
                  f"({rec['scenes']['before']['datetime']} -> "
                  f"{rec['scenes']['after']['datetime']})")
    np.savez_compressed(here / "out" / "chips.npz", **chips)
    (here / "out" / "chips_meta.json").write_text(
        json.dumps(meta, indent=1), "utf-8"
    )
    n_ev = sum(1 for m in meta if m["kind"] == "event")
    print(f"complete sites: {n_ev} event / {len(meta) - n_ev} control")


if __name__ == "__main__":
    main()
