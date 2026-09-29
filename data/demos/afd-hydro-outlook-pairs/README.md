# Demo: afd-hydro-outlook-pairs

**116 pairs** built 2026-09-29 by `analysis/build_demo_afd.py` per the card's
mechanism (deterministic issuance-time pairing of AFD sections with
precipitation imagery references), from the latest AFD of every NWS forecast
office (123 offices, 116 yielded a parseable HYDROLOGY or KEY MESSAGES
section).

- **Geodata side:** GIBS IMERG precipitation-rate tile URLs (zoom-2 CONUS
  quadrants) for the day before issuance — the antecedent precipitation the
  discussion reasons over (IMERG publishes with ~1-day latency; the first QC
  round's 0/20 caught same-day URLs).
- **Language side:** verbatim forecaster-written `.HYDROLOGY` / `.KEY
  MESSAGES` section text per office (expert-interpretation, unmodified).
- **Grounding QC (see `qc.json`):** seeded 20-pair sample —
  **20/20 image references resolve**; all 20 sampled sections manually
  reviewed: **20/20 genuine forecaster prose faithful to the product; 6/20
  carry a timestamp header fragment** ("Updated at…"/"Issued at…" — known
  noise; production parsing strips update stamps).
- **Known limitations:** demo pairs CONUS-wide tiles rather than
  CWA-clipped imagery (the card's per-office clipping is production
  engineering); single-day snapshot — the archive back-fill is the scaling
  step.
