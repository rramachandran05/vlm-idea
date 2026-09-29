"""Demonstration builder: afd-hydro-outlook-pairs (D6, Task 15).

Pairs the hydrology-relevant sections of the latest AFD from every NWS
forecast office with references to concurrent GIBS imagery. Writes
data/demos/afd-hydro-outlook-pairs/pairs.json.

Usage: python3 analysis/build_demo_afd.py
"""

from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

LOCS = "https://api.weather.gov/products/types/AFD/locations"
PRODS = "https://api.weather.gov/products/types/AFD/locations/{wfo}"
GIBS = (
    "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/"
    "IMERG_Precipitation_Rate/default/{date}/2km/2/{row}/{col}.png"
)

SECTION_RE = re.compile(
    r"^\.(HYDROLOGY|KEY MESSAGES)[.\s]*\n(.*?)(?=\n\.[A-Z][A-Z /()]+\.|\n&&)",
    re.S | re.M,
)


def fetch(url: str):
    req = urllib.request.Request(
        url, headers={"User-Agent": "geovlm-demo (research)",
                      "Accept": "application/ld+json"}
    )
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def extract_sections(text: str) -> list[tuple[str, str]]:
    out = []
    for m in SECTION_RE.finditer(text):
        body = " ".join(m.group(2).split())
        if len(body) > 80:
            out.append((m.group(1), body))
    # fallback: bulleted key messages block near the top
    if not out:
        m = re.search(r"\.KEY MESSAGES\.{3}\n(.*?)\n&&", text, re.S)
        if m:
            body = " ".join(m.group(1).split())
            if len(body) > 80:
                out.append(("KEY MESSAGES", body))
    return out


def main() -> None:
    locs = fetch(LOCS)["locations"]
    wfos = sorted(k for k, v in locs.items() if v)
    pairs = []
    for wfo in wfos:
        try:
            plist = fetch(PRODS.format(wfo=wfo)).get("@graph", [])
            if not plist:
                continue
            prod = fetch(plist[0]["@id"])
        except Exception:
            continue
        sections = extract_sections(prod.get("productText", ""))
        if not sections:
            continue
        # IMERG tiles publish with ~1-day latency; pair with the day before
        # issuance — the antecedent precipitation the discussion reasons over.
        import datetime as _dt
        date = (
            _dt.date.fromisoformat(prod["issuanceTime"][:10])
            - _dt.timedelta(days=1)
        ).isoformat()
        for name, body in sections[:2]:
            pairs.append(
                {
                    "pair_id": f"{prod['id']}_{name.replace(' ', '_')}",
                    "wfo": wfo,
                    "office": prod.get("issuingOffice"),
                    "issuance_time": prod["issuanceTime"],
                    "section": name,
                    "language": body,
                    # CONUS quadrant tiles for the issuance date (zoom 2)
                    "geodata_ref": [
                        GIBS.format(date=date, row=0, col=1),
                        GIBS.format(date=date, row=0, col=2),
                        GIBS.format(date=date, row=1, col=1),
                        GIBS.format(date=date, row=1, col=2),
                    ],
                    "source_url": f"https://api.weather.gov/products/{prod['id']}",
                }
            )
        time.sleep(0.2)

    out = Path(__file__).resolve().parent.parent / "data" / "demos" / \
        "afd-hydro-outlook-pairs"
    out.mkdir(parents=True, exist_ok=True)
    (out / "pairs.json").write_text(json.dumps(pairs, indent=1), "utf-8")
    print(f"{len(pairs)} pairs from {len(wfos)} offices -> {out / 'pairs.json'}")


if __name__ == "__main__":
    main()
