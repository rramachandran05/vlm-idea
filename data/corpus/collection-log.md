# Corpus Collection Log (D1)

Collected 2026-09-29 against `methods/inclusion-rules.md`.

## Retrieval
- **Path:** live arXiv export API via `analysis/collect_corpus.py` (deterministic,
  logged query set). Records are real by construction — every candidate comes
  from an API response this run; nothing was memory-cited. Per-query yields:
  `data/corpus/query-log.json`.
- **Plan deviation, noted:** `03-plan.md` named the arXiv MCP + the
  `python_landscape_analysis` collector as retrieval paths. The sandbox has
  direct network access, so retrieval ran through the arXiv API in-repo instead
  — same source of truth and the same verified-by-retrieval guarantee, with the
  query set and yields fully logged here rather than in MCP call history.
- **Three query rounds** (60 queries total, all in `collect_corpus.py`):
  1. 21 phrase queries (core GeoVLM + per-domain). 89 in-window candidates.
  2. Recall sanity check found seminal VLMs missing → 22 anchor/rephrased
     queries (RemoteCLIP, GeoChat, RS5M, SkyScript, EarthGPT, LHRS-Bot,
     ChatEarthNet, GeoPixel, …). Anchors hit; all round-2 phrase-form domain
     queries returned 0 (arXiv exact-phrase behavior).
  3. 17 AND-of-terms domain queries (flood, wildfire, disaster, agriculture,
     crop, OpenStreetMap, street view, weather, target recognition, …).
- **Final candidate pool:** 448 unique in-window works.

## Screening
- All 448 titles reviewed (abstracts for borderline cases) against the
  in/out-of-scope rules; keep decisions recorded in `analysis/curate_corpus.py`
  (KEEP map) so screening is reproducible and diffable.
- **Kept: 59.** Two records initially kept were dropped at characterization time
  for violating written inclusion rules: 2512.14228 (georeferencing locality
  descriptions — text-only, no observational modality; adjacent) and 2607.11838
  (HASTE — operational disaster mapping platform with no language pairing;
  vision-language is listed only as future work; adjacent, and a useful
  maturity comparator showing operational damage mapping exists without
  language today). Focused-corpus policy (~40–60 target): seminal + representative
  per domain and per construction strategy, deliberately including negative-case
  candidates (bias/hallucination/readiness studies).
- Representative drop reasons: no language pairing (pure-vision EO models,
  pansharpening, image–time-series alignment), no geospatial component (generic
  VLM robustness/weather-corruption work, autonomous driving, document parsing,
  short-drama scripts), geo-LLMs without an observational modality (GeoLLM,
  SpaBERT, GPSBench — adjacent), non-Earth geospatial (MarsRetrieval —
  adjacent), and redundancy with a kept representative (many change-captioning
  architectures, repeated ATR/geo-localization variants).

## Domain coverage (kept records; multi-tag)
earth-observation-general 29 · disasters 16 · urban 9 · mapping 9 ·
agriculture 7 · infrastructure 6 · defense-intelligence 5 — all seven domains
represented. Weather/climate–language works are tagged
`earth-observation-general` (+`disasters` where severe-weather-focused) per
inclusion rules.

## Known coverage limits
- arXiv-only this run (no `other:<venue>` records yet); journal-only GeoVLM
  work (e.g., in TGRS/RSE) is not represented — acceptable under the
  arXiv-primary rule, revisit if a pattern rests on a single arXiv record.
- Defense/intelligence is thin on arXiv (5 kept), consistent with the domain's
  publication practices; noted rather than padded.

## v2 extension (2026-09-29, round 4)
14 additional queries for the science-data→language pattern class (medicine
report generation, scientific agents, sensor/time-series reasoning; scope
extension documented in `methods/schema-v2.md`). Candidate pool grew to 812;
17 new works kept under the extended rules (tag `science-adjacent`), corpus
now 76. Same retrieval guarantees (live API, verified by construction).
