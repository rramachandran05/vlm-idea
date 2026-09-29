# Demo: cmr-summary-product-grounding

**120 pairs** built 2026-09-29 by `analysis/build_demo_cmr.py` per the card's
mechanism (knowledge-based rendering of CMR collection summaries onto granule
browse imagery, across 10 thematic keywords).

- **Geodata side:** granule browse-image URLs (CMR `browse#` links),
  validated at build time by fetching image magic bytes — links that were
  401-gated or non-image were dropped before pairing.
- **Language side:** captions rendered from the collection's authoritative
  CMR summary (product identity, archive center, first two summary
  sentences) plus a product-knowledge QA pair with the summary as answer —
  product-level statements by design (the card's scene-vs-product split).
- **Grounding QC (see `qc.json`):** seeded 20-pair sample —
  **20/20 image references resolve**; all 20 sampled captions manually
  reviewed: **20/20 faithful** to the source summaries (no generation beyond
  extraction, so hallucination risk is nil by construction). First QC round
  (3/20) caught unvalidated browse links; fixed with build-time magic-byte
  validation.
- **Known limitations:** browse renderings vary in colormap/legend (card
  notes legend context as production work); demo skips collections whose
  browse requires Earthdata login.
