# Demo: eonet-worldview-event-narration

**300 pairs** built 2026-09-29 by `analysis/build_demo_eonet.py` per the card's
mechanism (deterministic EONET→GIBS join + template narration).

- **Geodata side:** GIBS WMTS tile URLs (VIIRS SNPP true color, 250m grid,
  level 5) at each event-track point/date — authoritative references, not
  downloaded rasters, as stated in the card.
- **Language side:** template narration from EONET event fields (title,
  category, magnitude, status, date).
- **Grounding QC (see `qc.json`):** seeded 20-pair sample (seed 42) —
  **20/20 image references resolve** (HTTP 200, image content). All 20
  sampled narrations manually reviewed: **20/20 coherent and faithful** to the
  EONET record. (First QC round caught a tile-grid bug — 11/20 — fixed by
  correcting the GIBS 250m matrix dimensions and re-verified.)
- **Known limitations:** tile may be cloud-obscured or the event
  sub-resolution (the card's stated risks — a production build adds
  cloud-fraction filtering); narration asserts event presence per EONET, not
  per-pixel visibility.
