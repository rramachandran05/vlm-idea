"""Collect GeoVLM candidate papers from the arXiv API (D1, Task 3).

Runs the logged query set against the arXiv export API, dedupes by canonical
ID, and writes `data/corpus/candidates.json` (id, title, abstract, dates,
categories, per-query provenance). Screening/curation into `papers.json` is a
separate, human-reviewed step; this script does retrieval only — no judgment.

Usage: python3 analysis/collect_corpus.py [--max-per-query 40]
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom"}

# GeoVLM query set — modeled on Operations-Work/skills/geoai_landscape_analysis
# context/arxiv_query_reference.md, retargeted from foundation models to
# vision-language pairing, with per-domain coverage queries.
QUERIES = [
    # core GeoVLM
    "remote sensing vision language model",
    "remote sensing image captioning",
    "remote sensing visual question answering",
    "satellite image text retrieval",
    "geospatial multimodal large language model",
    "remote sensing visual grounding",
    "remote sensing instruction tuning",
    "remote sensing change captioning",
    # per-domain coverage
    "agriculture satellite vision language",
    "crop monitoring visual question answering",
    "disaster damage assessment vision language model",
    "flood satellite image text",
    "wildfire remote sensing language",
    "urban satellite imagery question answering",
    "OpenStreetMap vision language",
    "map text alignment model",
    "infrastructure monitoring satellite language model",
    "building damage caption satellite",
    "overhead imagery analyst language model",
    "aerial reconnaissance visual question answering",
    "weather forecast language model multimodal",
    # round 2 — recall sanity check found round 1 thin on seminal VLMs and
    # applied domains; anchor + rephrased queries (results still verified by
    # construction: only papers the API returns enter the pool).
    "RemoteCLIP",
    "GeoChat",
    "RS5M",
    "SkyScript",
    "EarthGPT",
    "LHRS-Bot",
    "ChatEarthNet",
    "GeoPixel",
    "vision language model earth observation",
    "image-text dataset remote sensing",
    "contrastive language image pretraining satellite",
    "crop type classification text",
    "agricultural monitoring multimodal language",
    "flood mapping vision language",
    "earthquake damage multimodal",
    "hurricane damage assessment deep learning text",
    "geo-localization natural language description",
    "text-to-image retrieval geographic",
    "urban perception street view language",
    "scene graph remote sensing",
    "weather climate multimodal foundation model",
    "poverty mapping satellite imagery",
    # round 3 — exact-phrase domain queries all returned 0; use AND-of-phrases
    # (" && " separator) for applied-domain coverage instead.
    "vision language && flood",
    "vision language && wildfire",
    "vision language && disaster",
    "visual question answering && damage",
    "captioning && disaster && satellite",
    "vision language && agriculture",
    "vision language && crop",
    "multimodal && crop monitoring",
    "vision language && OpenStreetMap",
    "language model && map && geographic",
    "image-text && urban && satellite",
    "street view && language model",
    "vision language && infrastructure && satellite",
    "vision language && weather",
    "language model && climate && satellite",
    "vision language && target recognition",
    "geo-localization && language",
    # round 4 — v2 reframe (science-data → language beyond geodata-text pairs):
    # medicine, scientific agents, FM-embedding+LLM systems, evidence-grounded
    # generation. Scope extension logged in methods/schema-v2.md.
    "radiology report generation",
    "chest x-ray && report generation && language model",
    "clinical && evidence && report generation && multimodal",
    "ECG && language model && diagnosis",
    "electronic health record && multimodal && language model",
    "scientific discovery && large language model && agent",
    "AI scientist && hypothesis",
    "hypothesis generation && scientific && language model",
    "foundation model && embedding && retrieval && scientific",
    "time series && language model && explanation && anomaly",
    "sensor data && large language model && reasoning",
    "astronomy && large language model && transient",
    "grounded generation && evidence && scientific",
    "structured report && findings && vision language && medical",
]

WINDOW = (2021, 2026)


def canonical_id(raw: str) -> str:
    """'http://arxiv.org/abs/2306.11300v2' -> '2306.11300'."""
    tail = raw.rsplit("/", 1)[-1]
    return re.sub(r"v\d+$", "", tail)


def to_search_query(query: str) -> str:
    """'a b && c' -> 'all:"a b" AND all:c'; plain phrases stay quoted."""
    parts = [p.strip() for p in query.split("&&")]
    return " AND ".join(
        f'all:"{p}"' if " " in p else f"all:{p}" for p in parts
    )


def fetch(query: str, max_results: int) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "search_query": to_search_query(query),
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
        }
    )
    with urllib.request.urlopen(f"{API}?{params}", timeout=30) as r:
        root = ET.fromstring(r.read())
    out = []
    for e in root.findall("a:entry", NS):
        pub = e.findtext("a:published", "", NS)  # v1 date
        out.append(
            {
                "id": canonical_id(e.findtext("a:id", "", NS)),
                "title": " ".join(e.findtext("a:title", "", NS).split()),
                "abstract": " ".join(e.findtext("a:summary", "", NS).split()),
                "year": int(pub[:4]) if pub[:4].isdigit() else None,
                "month": int(pub[5:7]) if pub[5:7].isdigit() else None,
                "categories": [
                    c.get("term") for c in e.findall("a:category", NS)
                ],
                "url": f"https://arxiv.org/abs/{canonical_id(e.findtext('a:id', '', NS))}",
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-per-query", type=int, default=40)
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    outdir = root / "data" / "corpus"
    outdir.mkdir(parents=True, exist_ok=True)

    merged: dict[str, dict] = {}
    log = []
    for q in QUERIES:
        rows = fetch(q, args.max_per_query)
        kept_window = 0
        for row in rows:
            if row["year"] is None or not (
                WINDOW[0] <= row["year"] <= WINDOW[1]
            ):
                continue
            kept_window += 1
            rec = merged.setdefault(row["id"], {**row, "matched_queries": []})
            rec["matched_queries"].append(q)
        log.append(
            {"query": q, "returned": len(rows), "in_window": kept_window}
        )
        time.sleep(3)  # arXiv API politeness

    candidates = sorted(merged.values(), key=lambda r: r["id"])
    (outdir / "candidates.json").write_text(
        json.dumps(candidates, indent=1), encoding="utf-8"
    )
    (outdir / "query-log.json").write_text(
        json.dumps(log, indent=1), encoding="utf-8"
    )
    print(
        f"queries={len(QUERIES)} unique_candidates={len(candidates)} "
        f"-> {outdir / 'candidates.json'}"
    )


if __name__ == "__main__":
    main()
