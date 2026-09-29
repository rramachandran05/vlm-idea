# Demo: pager-shakemap-impact-briefs

**200 pairs** built 2026-09-29 by `analysis/build_demo_pager.py` per the
card's mechanism (deterministic per-event pairing, M6+ events with losspager
since 2022).

- **Geodata side:** USGS ShakeMap intensity images (`download/intensity.jpg`)
  per event — authoritative product URLs.
- **Language side:** impact briefs rendered from PAGER alert level, event
  parameters, and estimated maximum intensity (template over structured PAGER
  fields; alert-level meanings follow published PAGER definitions).
- **Grounding QC (see `qc.json`):** seeded 20-pair sample —
  **20/20 image references resolve**; all 20 sampled briefs manually
  reviewed: **20/20 consistent** with the event's alert level and title.
- **Known limitations:** briefs use the latest product version (the card
  specifies version-matched pairing for production); the deeper PAGER prose
  (onePAGER commentary) is in PDFs not yet parsed — structured fields only in
  this demo.
