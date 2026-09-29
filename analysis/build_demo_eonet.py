"""Demonstration builder: eonet-worldview-event-narration (D6, Task 15).

Deterministic join of EONET events to GIBS daily tile URLs + template
narration. Writes data/demos/eonet-worldview-event-narration/pairs.json.

Usage: python3 analysis/build_demo_eonet.py [--limit-events 400] [--max-pairs 300]
"""

from __future__ import annotations

import argparse
import json
import math
import urllib.request
from pathlib import Path

EONET = "https://eonet.gsfc.nasa.gov/api/v3/events?limit={n}&status=all"
GIBS = (
    "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/"
    "VIIRS_SNPP_CorrectedReflectance_TrueColor/default/{date}/"
    "250m/{z}/{row}/{col}.jpg"
)
ZOOM = 5  # EPSG:4326 level 5: 0.15625 deg/tile-pixel block, tile = 5 deg


def tile_for(lat: float, lon: float, z: int = ZOOM) -> tuple[int, int]:
    """GIBS EPSG:4326 250m tile grid: level z has 1.25*2^z cols, half as many
    rows (verified against the WMTS TileOutOfRange bound: level 5 = 40x20)."""
    n_rows = (5 * 2 ** z) // 8
    n_cols = 2 * n_rows
    col = int((lon + 180.0) / 360.0 * n_cols)
    row = int((90.0 - lat) / 180.0 * n_rows)
    return min(row, n_rows - 1), min(col, n_cols - 1)


def narrate(ev: dict, geom: dict) -> str:
    cat = ev["categories"][0]["title"] if ev["categories"] else "natural event"
    mag = ""
    if geom.get("magnitudeValue") is not None:
        mag = f" with reported magnitude {geom['magnitudeValue']} {geom.get('magnitudeUnit') or ''}".rstrip()
    status = "ongoing" if ev.get("closed") is None else "since closed"
    return (
        f"This satellite view of {geom['date'][:10]} covers the location of "
        f"{ev['title']}, a {cat.lower()} event tracked by NASA EONET"
        f"{mag}. The event was {status} at the time of this observation."
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-events", type=int, default=400)
    ap.add_argument("--max-pairs", type=int, default=300)
    args = ap.parse_args()

    with urllib.request.urlopen(
        EONET.format(n=args.limit_events), timeout=60
    ) as r:
        events = json.load(r)["events"]

    pairs = []
    for ev in events:
        for geom in ev.get("geometry", []):
            if geom.get("type") != "Point":
                continue
            lon, lat = geom["coordinates"]
            if not (math.isfinite(lat) and math.isfinite(lon)):
                continue
            date = geom["date"][:10]
            if date < "2015-11-24":  # VIIRS SNPP GIBS availability floor
                continue
            row, col = tile_for(lat, lon)
            pairs.append(
                {
                    "pair_id": f"{ev['id']}_{geom['date']}",
                    "event_id": ev["id"],
                    "event_title": ev["title"],
                    "category": ev["categories"][0]["id"]
                    if ev["categories"] else "unknown",
                    "date": date,
                    "lat": lat,
                    "lon": lon,
                    "geodata_ref": GIBS.format(date=date, z=ZOOM, row=row, col=col),
                    "language": narrate(ev, geom),
                    "source_url": ev["link"],
                }
            )
            if len(pairs) >= args.max_pairs:
                break
        if len(pairs) >= args.max_pairs:
            break

    out = Path(__file__).resolve().parent.parent / "data" / "demos" / \
        "eonet-worldview-event-narration"
    out.mkdir(parents=True, exist_ok=True)
    (out / "pairs.json").write_text(json.dumps(pairs, indent=1), "utf-8")
    print(f"{len(pairs)} pairs -> {out / 'pairs.json'}")


if __name__ == "__main__":
    main()
