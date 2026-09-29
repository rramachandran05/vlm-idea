Status: Draft (execution pre-authorized by Rahul in-session, 2026-09-29)

# Plan: Structured Science Evidence Cards (v2)

## Repo conventions and environment (probed 2026-09-29)

- Repo conventions carry over from v1 (Python ≥3.10, pytest `testpaths=["tests"]`, numbers-from-scripts, `unknown` ≠ blank, never memory-cite). 55 v1 tests green at start.
- **Python 3.12.7 (Anaconda).** numpy present; `torch` and `rasterio` absent → installed for the demonstrator (recorded in `demonstrator/README.md`).
- **Earth Search STAC** (`earth-search.aws.element84.com/v1`, Sentinel-2 L2A COGs, public, no auth): probed HTTP 200. This is the HLS-equivalent observation source per the Spec assumption (same S30 bands B02/B03/B04/B8A/B11/B12).
- **Prithvi-EO-1.0-100M** (Hugging Face `ibm-nasa-geospatial/Prithvi-EO-1.0-100M`): probed live. Apache-2.0. Repo contains standalone `prithvi_mae.py`, weights `Prithvi_EO_V1_100M.pt`, `config.json` (patch/band config), and example HLS chips. CPU inference on 224×224×6-band chips is tractable at 100M params.
- **Event/context holdings:** EONET (v1-verified, live) supplies wildfire events with dates/coordinates for demonstrator sites and external-context evidence; the v1 holdings inventory carries into O7.

## Structure (new work under existing layout)

```
methods/schema-v2.md               # O1 new axes vocabularies (+ QC applies)
methods/science-card-spec.md       # O3 written spec
schema/science_card.schema.json    # O3 machine-readable schema
data/characterization/records-v2.json   # all records, three new axes
data/corpus/…                      # extended corpus (collect → curate v2 path)
patterns/evidence-composition-metapatterns.md   # O2
patterns/fm-contribution-taxonomy.md            # O4 (cites ablation)
patterns/research-agenda.md                     # O10
opportunities/catalog-v2.md        # O7 (composition recipes + priorities)
demonstrator/
  README.md                        # sources, sizes, licenses, run order
  sites.py                         # event + control site selection (EONET-driven)
  fetch_chips.py                   # STAC search + windowed COG reads → chips.npz
  evidence.py                      # deterministic indices, band stats, deltas
  prithvi_embed.py                 # Prithvi MAE encoder → embeddings, Δ-representation, analogs
  build_cards.py                   # assemble + validate Science Cards (JSON)
  generate_language.py             # O5 generators (traced, tagged) + O6 questions + counterfactuals
  ablation.py                      # O9 tiered discrimination comparison
  out/                             # cards/, language/, ablation.json (committed)
tests/test_science_cards.py        # schema validation, traceability, question logic
tests/test_landscape_v2.py         # new axes vocab + coverage
```

## Phases

1. **O1 corpus v2** — write `methods/schema-v2.md` (three new axes, vocabularies from requirements §2/§3/§7). Extend collection with medicine/scientific-agent queries (live arXiv API, same logged-query machinery: `analysis/collect_corpus.py` round 4 + curation update). Characterize new works fully (v1 axes + new axes); add the three new axes to all v1 records from stored verified abstracts. QC per protocol on new axes. Script-generated taxonomy counts (`analysis/corpus_stats.py` extended).
2. **O3 card spec first** (it is the interface everything else consumes): written spec + JSON Schema + validator. Evidence entries are `{value, class: observed|computed|inferred|learned-representation|contextual, source, method, provenance, uncertainty}`.
3. **O8 demonstrator** — sites: ~12 wildfire events (EONET, 2024–2026, point-geometry, cloud-checked) + ~12 stable controls (offset locations); chips: 6-band Sentinel-2 L2A windowed reads before/after event date; evidence: NDVI/NBR/ΔNBR/ΔNDVI + band stats; FM: Prithvi encoder mean-pooled embeddings per chip, cosine representation-change, cross-site nearest-neighbor analogs; context: the EONET event record (or its absence, for controls); assemble → validate cards.
4. **O5/O6 language layer** — generators over cards: factual description, temporal-change, comparison-to-analog, attribution QA, uncertainty statement, recommended follow-up (≥6 types); every sentence emitted as `{text, trace: [card field paths], epistemic: …}`. Question rules keyed to evidence state (ΔNBR & Δ-representation & event-context conjunctions); counterfactual/negative constructions: context-conflict cases and evidence-insufficient (cloud/artifact) cases with abstention targets.
5. **O9 ablation** — event-vs-control discrimination with tiered evidence: (raw-band-stat proxy) / deterministic Δ-indices / Prithvi Δ-representation / combined; report AUC-style separation + per-tier misclassifications at demonstrator n; feed numbers into O4.
6. **O2/O4/O7/O10 documents** — composition metapatterns (corpus + demonstrator evidence), FM contribution taxonomy (corpus + ablation), catalog v2 (≥6 text-does-not-exist compositions over verified holdings; rubric mapping to §18's 12 factors), research agenda.
7. **Verification** — new tests + full suite, AC-by-AC check, updated summary report artifact.

## Files/components to change

All new files above, plus: `analysis/collect_corpus.py` (round-4 queries), `analysis/curate_corpus.py` (new keeps), `analysis/corpus_stats.py` (new-axis tallies), `patterns/spec-card-template.md` (add superseded-by note, kept for the v1 record), `specs/geovlm-opportunity-framework/01-spec.md` (superseded-by pointer), `pyproject.toml` (demonstrator deps noted as extras). No modifications to sibling projects.

## Risks

- **Network/scale:** chip fetches are windowed HTTP range reads over ~50 COG assets — bounded, but Earth Search throttling is possible → retry + reduced site count is the fallback (AC floor is 10+10 sites).
- **Prithvi on CPU:** 100M MAE inference is fine; if `prithvi_mae.py` has undeclared deps (einops etc.), install as needed and record.
- **Cloud contamination:** naive before/after chips may be cloudy → per-chip cloud screen via STAC `eo:cloud_cover` + SCL band; contaminated cases become the O6 "artifact" counterfactuals rather than silent noise.
- **Ablation honesty:** at n≈24 the ablation is demonstration-grade; the deliverable states this and reports whatever the numbers show, including "deterministic suffices."
- **v1 tests must stay green** — v2 additions extend, never mutate, v1 data contracts (records-v2 is a separate file joined on id).
