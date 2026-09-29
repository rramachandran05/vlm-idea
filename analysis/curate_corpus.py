"""Screen candidates into the D1 corpus (Task 3, curation step).

Applies the keep-list below (curated against methods/inclusion-rules.md by
reading titles/abstracts of all candidates) to data/corpus/candidates.json and
writes data/corpus/papers.json with the D1 schema fields plus
data/corpus/abstracts.json (id -> abstract) for the characterization step.

The keep-list is data, reviewed by a human; this script just applies it
deterministically so the screening is reproducible and diffable.
"""

from __future__ import annotations

import json
from pathlib import Path

# id -> domain tags (methods/inclusion-rules.md vocabulary)
KEEP: dict[str, list[str]] = {
    # earth-observation-general: seminal models, datasets, benchmarks, methods
    "2306.11029": ["earth-observation-general"],                  # RemoteCLIP
    "2306.11300": ["earth-observation-general"],                  # RS5M / GeoRSCLIP
    "2307.15266": ["earth-observation-general"],                  # RSGPT / RSICap
    "2311.15826": ["earth-observation-general"],                  # GeoChat
    "2312.12856": ["earth-observation-general", "mapping"],       # SkyScript (OSM tags)
    "2402.02544": ["earth-observation-general", "mapping"],       # LHRS-Bot (VGI)
    "2402.11325": ["earth-observation-general"],                  # ChatEarthNet (WorldCover+LLM)
    "2410.06234": ["earth-observation-general", "disasters"],     # TEOChat (temporal)
    "2501.13925": ["earth-observation-general"],                  # GeoPixel
    "2408.14744": ["earth-observation-general", "mapping"],       # RSTeller (OSM captions)
    "2312.12222": ["earth-observation-general", "urban"],         # EarthVQA
    "2502.09598": ["earth-observation-general"],                  # GAIA dataset
    "2505.03334": ["earth-observation-general"],                  # OS-W2S labeling engine
    "2507.16716": ["earth-observation-general"],                  # MLLM/LLM data generation
    "2411.19325": ["earth-observation-general"],                  # GEOBench-VLM
    "2401.17600": ["earth-observation-general"],                  # GPT-4V EO benchmark (negative)
    "2502.08168": ["earth-observation-general", "defense-intelligence"],  # SARChat-Bench-2M
    "2606.13148": ["earth-observation-general"],                  # TerraBench (earth-system agents)
    "2504.19742": ["earth-observation-general", "agriculture"],   # EcoWikiRS (species obs, weak sup)
    "2311.16782": ["earth-observation-general"],                  # RSVQA language-bias (negative)
    "2501.14905": ["earth-observation-general"],                  # hallucination in VL dataset gen
    # weather/climate language pairing (tagged EO-general per inclusion rules)
    "2406.09838": ["earth-observation-general", "disasters"],     # ClimateIQA (reanalysis VQA)
    "2406.11217": ["earth-observation-general", "disasters"],     # WeatherQA (SPC outlooks)
    "2512.03623": ["earth-observation-general"],                  # textual weather forecasts
    "2604.16451": ["earth-observation-general"],                  # SynopticBench (AFDs)
    # disasters
    "2106.10548": ["disasters"],                                  # VQA-Aid (post-hurricane)
    "2505.21089": ["disasters", "earth-observation-general"],     # DisasterM3
    "2601.18493": ["disasters", "infrastructure"],                # DisasterInsight
    "2411.01511": ["disasters"],                                  # LVLM damage assessment+reporting
    "2509.20628": ["disasters", "urban"],                         # Recov-Vision (street view recovery)
    "2509.21609": ["disasters"],                                  # VLCE knowledge-enhanced description
    "2608.21529": ["disasters"],                                  # DamageScope retrieval at scale
    "2607.11838": ["disasters"],                                  # HASTE platform
    "2606.17246": ["disasters"],                                  # GeoDisaster operational benchmark
    "2603.17108": ["disasters", "urban"],                         # flood depth from social media
    "2508.01380": ["disasters"],                                  # damage data gen w/ human knowledge
    "2509.01907": ["disasters", "earth-observation-general"],     # RSCC change-caption dataset
    # agriculture
    "2410.08405": ["agriculture"],                                # AgroGPT (expert tuning)
    "2410.01407": ["agriculture"],                                # AgriCLIP
    "2412.00465": ["agriculture"],                                # AgriBench
    "2504.10568": ["agriculture"],                                # AgMMU (user-expert Q&A)
    "2506.20100": ["agriculture"],                                # MIRAGE (expert conversations)
    "2512.15977": ["agriculture"],                                # zero-shot readiness (negative)
    # urban
    "2310.18340": ["urban"],                                      # UrbanCLIP
    "2506.00530": ["urban"],                                      # CityLens socioeconomic
    "2407.19719": ["urban"],                                      # safety perception street view
    "2504.02866": ["urban", "mapping"],                           # OpenFACADES (OSM+street view)
    "2602.20066": ["urban"],                                      # HeatPrompt urban heat
    # mapping / geo-localization
    "2409.00255": ["mapping"],                                    # MAPWise map QA
    "2406.18572": ["mapping", "urban"],                           # GeoReasoner
    "2603.11804": ["mapping", "earth-observation-general"],       # OSMDA
    "2601.19099": ["mapping"],                                    # m2sv (scalable benchmark gen)
    "2512.14228": ["mapping"],                                    # georeferencing locality descriptions
    # infrastructure
    "2504.06785": ["infrastructure"],                             # road pavement monitoring
    "2302.09208": ["infrastructure"],                             # bridge damage VQA
    "2404.12606": ["infrastructure", "disasters"],                # ELEV-VISION-SAM (floor elevation)
    "2505.19358": ["infrastructure", "earth-observation-general"],# RoofNet
    # defense / intelligence
    "2605.10772": ["defense-intelligence"],                       # MSTAR ATR VQA
    "2411.03491": ["defense-intelligence"],                       # application-agnostic ATR VLM
    "2608.00119": ["defense-intelligence", "infrastructure"],     # war infrastructure estimation
    "2601.01416": ["defense-intelligence"],                       # AirSpatialBot
}


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    corpus_dir = root / "data" / "corpus"
    candidates = {
        r["id"]: r
        for r in json.loads((corpus_dir / "candidates.json").read_text())
    }

    missing = sorted(set(KEEP) - set(candidates))
    if missing:
        raise SystemExit(f"keep-list ids not in candidates.json: {missing}")

    papers, abstracts = [], {}
    for pid, domains in sorted(KEEP.items()):
        c = candidates[pid]
        papers.append(
            {
                "id": pid,
                "source": "arxiv",
                "title": c["title"],
                "year": c["year"],
                "month": c["month"],
                "venue": (c["categories"] or ["unknown"])[0],
                "domains": domains,
                "url": c["url"],
            }
        )
        abstracts[pid] = c["abstract"]

    (corpus_dir / "papers.json").write_text(
        json.dumps(papers, indent=1), encoding="utf-8"
    )
    (corpus_dir / "abstracts.json").write_text(
        json.dumps(abstracts, indent=1), encoding="utf-8"
    )
    from collections import Counter

    tally = Counter(d for p in papers for d in p["domains"])
    print(f"kept {len(papers)} of {len(candidates)} candidates")
    for dom, n in tally.most_common():
        print(f"  {dom}: {n}")


if __name__ == "__main__":
    main()
