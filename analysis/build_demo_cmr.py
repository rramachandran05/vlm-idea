"""Demonstration builder: cmr-summary-product-grounding (D6, Task 15).

Pairs a browse image per NASA collection with knowledge captions rendered
from the CMR collection summary. Writes
data/demos/cmr-summary-product-grounding/pairs.json.

Usage: python3 analysis/build_demo_cmr.py [--target 120]
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

COLLS = (
    "https://cmr.earthdata.nasa.gov/search/collections.json"
    "?has_granules=true&page_size=100&page_num={page}&keyword={kw}"
)
GRANS = (
    "https://cmr.earthdata.nasa.gov/search/granules.json"
    "?collection_concept_id={cid}&browse_only=true&page_size=1"
)
KEYWORDS = ["flood", "fire", "vegetation", "snow", "ocean color", "aerosol",
            "land cover", "precipitation", "temperature", "soil moisture"]


def fetch(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "geovlm-demo"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


IMAGE_MAGIC = (b"\xff\xd8", b"\x89PNG", b"GIF8")


def browse_is_image(url: str) -> bool:
    """Fetch the first bytes and check image magic — some DAAC browse links
    serve octet-stream content types or require Earthdata login (401)."""
    req = urllib.request.Request(url, headers={"User-Agent": "geovlm-demo"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            head = r.read(8)
        return any(head.startswith(m) for m in IMAGE_MAGIC)
    except Exception:  # noqa: BLE001
        return False


def caption(coll: dict) -> str:
    summary = " ".join(coll.get("summary", "").split())
    # first two sentences of the authoritative summary
    parts = summary.split(". ")
    lead = ". ".join(parts[:2]).rstrip(".") + "."
    return (
        f"This browse image is a granule of {coll.get('short_name', 'unknown')} "
        f"({coll.get('dataset_id', '')}), archived by "
        f"{coll.get('archive_center') or coll.get('data_center', 'NASA')}. "
        f"{lead}"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=120)
    args = ap.parse_args()

    pairs, seen = [], set()
    for kw in KEYWORDS:
        if len(pairs) >= args.target:
            break
        colls = fetch(COLLS.format(page=1, kw=urllib.parse.quote(kw)))
        for coll in colls["feed"]["entry"]:
            if len(pairs) >= args.target:
                break
            cid = coll["id"]
            if cid in seen or not coll.get("summary"):
                continue
            seen.add(cid)
            try:
                grans = fetch(GRANS.format(cid=cid))["feed"]["entry"]
            except Exception:
                continue
            if not grans:
                continue
            g = grans[0]
            browse = [
                l["href"] for l in g.get("links", [])
                if "browse#" in l.get("rel", "") and l.get("href", "")
                .lower().startswith("http")
            ]
            if not browse or not browse_is_image(browse[0]):
                continue
            pairs.append(
                {
                    "pair_id": g["id"],
                    "collection": coll.get("short_name"),
                    "collection_id": cid,
                    "keyword": kw,
                    "granule_title": g.get("title"),
                    "geodata_ref": browse[0],
                    "language": caption(coll),
                    "qa": {
                        "q": "What does the data product shown in this image measure?",
                        "a": " ".join(coll["summary"].split())[:400],
                    },
                    "source_url": f"https://cmr.earthdata.nasa.gov/search/concepts/{cid}",
                }
            )
            time.sleep(0.2)

    out = Path(__file__).resolve().parent.parent / "data" / "demos" / \
        "cmr-summary-product-grounding"
    out.mkdir(parents=True, exist_ok=True)
    (out / "pairs.json").write_text(json.dumps(pairs, indent=1), "utf-8")
    print(f"{len(pairs)} pairs -> {out / 'pairs.json'}")


if __name__ == "__main__":
    main()
