"""Demonstration builder: pager-shakemap-impact-briefs (D6, Task 15).

Per-event deterministic pairing of USGS ShakeMap intensity images with
PAGER-derived impact language. Writes
data/demos/pager-shakemap-impact-briefs/pairs.json.

Usage: python3 analysis/build_demo_pager.py [--start 2022-01-01] [--minmag 6.0]
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path

QUERY = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
    "&starttime={start}&minmagnitude={mag}&producttype=losspager"
    "&orderby=time&limit={limit}"
)
DETAIL = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
    "&eventid={eid}"
)

ALERT_TEXT = {
    "green": "no significant casualties or damage are expected",
    "yellow": "some casualties or localized damage are possible",
    "orange": "significant casualties and damage are likely and the disaster is potentially widespread",
    "red": "high casualties and extensive damage are probable and the disaster is likely widespread",
}


def fetch(url: str):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def brief(props: dict, pager: dict, mmi) -> str:
    alert = (pager.get("properties", {}) or {}).get("alertlevel") or \
        props.get("alert") or "unknown"
    a_txt = ALERT_TEXT.get(alert, "impact level could not be assessed")
    mmi_txt = (
        f" Maximum estimated shaking intensity is MMI {mmi:.1f}."
        if isinstance(mmi, (int, float)) else ""
    )
    return (
        f"This ShakeMap shows estimated shaking intensity for {props['title']}. "
        f"USGS PAGER issued a {alert.upper()} alert for this event, meaning "
        f"{a_txt}.{mmi_txt} Populated areas within the higher-intensity "
        f"contours face the greatest risk from vulnerable structures."
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2022-01-01")
    ap.add_argument("--minmag", type=float, default=6.0)
    ap.add_argument("--limit", type=int, default=200)
    args = ap.parse_args()

    feed = fetch(QUERY.format(start=args.start, mag=args.minmag,
                              limit=args.limit))
    pairs = []
    for f in feed["features"]:
        eid = f["id"]
        try:
            detail = fetch(DETAIL.format(eid=eid))
            if detail.get("type") == "FeatureCollection":
                detail = detail["features"][0]
        except Exception:
            continue
        products = detail["properties"].get("products", {})
        sm = products.get("shakemap", [])
        pg = products.get("losspager", [])
        if not sm or not pg:
            continue
        contents = sm[0].get("contents", {})
        img = contents.get("download/intensity.jpg") or \
            contents.get("download/pga.jpg")
        if not img:
            continue
        props = detail["properties"]
        mmi = props.get("mmi")
        pairs.append(
            {
                "pair_id": eid,
                "event_title": props["title"],
                "time_ms": props["time"],
                "magnitude": props["mag"],
                "alert": pg[0].get("properties", {}).get("alertlevel")
                or props.get("alert"),
                "geodata_ref": img["url"],
                "language": brief(props, pg[0], mmi),
                "source_url": props["url"],
            }
        )
        time.sleep(0.4)

    out = Path(__file__).resolve().parent.parent / "data" / "demos" / \
        "pager-shakemap-impact-briefs"
    out.mkdir(parents=True, exist_ok=True)
    (out / "pairs.json").write_text(json.dumps(pairs, indent=1), "utf-8")
    print(f"{len(pairs)} pairs -> {out / 'pairs.json'}")


if __name__ == "__main__":
    main()
