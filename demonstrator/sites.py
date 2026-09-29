"""Select demonstrator sites (O8): EONET wildfire events + offset controls.

Writes demonstrator/out/sites.json. Controls reuse each event's dates at a
location offset ~0.7 deg east (same climate zone, no reported event), giving a
paired event/control design for the ablation.

Usage: python3 demonstrator/sites.py [--n 14]
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

EONET = (
    "https://eonet.gsfc.nasa.gov/api/v3/events"
    "?category=wildfires&status=all&limit=800"
    "&start=2024-06-01&end=2026-06-30"
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=14)
    args = ap.parse_args()

    with urllib.request.urlopen(EONET, timeout=60) as r:
        events = json.load(r)["events"]

    # collect all eligible candidates first, then stride through them so the
    # selection spans dates and geographies instead of clustering on the
    # newest events
    candidates, seen_cells = [], set()
    for ev in events:
        geoms = [g for g in ev.get("geometry", []) if g["type"] == "Point"]
        if not geoms:
            continue
        g = geoms[0]
        lon, lat = g["coordinates"]
        date = g["date"][:10]
        # need Sentinel-2 coverage, valid coordinates, and room for a
        # post-event window (a few EONET geometries carry wrapped/invalid
        # longitudes — drop rather than guess-correct)
        if not (-55 < lat < 65) or not (-180 <= lon <= 180) or \
                not ("2024-01-01" <= date <= "2026-06-30"):
            continue
        cell = (round(lat / 3), round(lon / 3))  # spread sites out
        if cell in seen_cells:
            continue
        seen_cells.add(cell)
        candidates.append((ev, g, lat, lon, date))

    step = max(1, len(candidates) // args.n)
    sites = []
    for ev, g, lat, lon, date in candidates[::step][: args.n]:
        sid = ev["id"].replace("EONET_", "ev")
        sites.append(
            {
                "site_id": sid, "kind": "event", "lat": lat, "lon": lon,
                "event_date": date, "event_id": ev["id"],
                "event_title": ev["title"],
                "event_url": ev["link"],
            }
        )
        sites.append(
            {
                "site_id": f"{sid}_ctl", "kind": "control",
                "lat": lat, "lon": lon + 0.7, "event_date": date,
                "event_id": None,
                "event_title": None,
                "event_url": None,
                "control_for": sid,
            }
        )
    out = Path(__file__).resolve().parent / "out"
    out.mkdir(exist_ok=True)
    (out / "sites.json").write_text(json.dumps(sites, indent=1), "utf-8")
    n_ev = sum(1 for s in sites if s["kind"] == "event")
    print(f"{n_ev} event + {len(sites) - n_ev} control sites -> {out / 'sites.json'}")


if __name__ == "__main__":
    main()
