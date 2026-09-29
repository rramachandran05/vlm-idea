# Spec Card: eonet-advisory-source-briefs

**Generating combination:** storm situational-awareness need × GIBS storm imagery (H3) × agency advisories linked from EONET sources (H2→NHC-class products) × deterministic event-keyed pairing.

| # | Field | Value |
|---|---|---|
| 0 | Card ID / name | `eonet-advisory-source-briefs` — pairing storm imagery with the advisories agencies issued about it |
| 1 | Application need | Emergency-management briefers need advisory-grade storm summaries (position, intensity, expected impacts) tied to the imagery they're looking at; EONET already keys events to the issuing agency's advisory pages |
| 2 | Required capability | From storm-centered satellite imagery sequences, produce advisory-style situation text: position/track, intensity in operational units (kts), and hazard framing consistent with the responsible agency's product |
| 3 | Geospatial evidence | GIBS true-color/IR imagery cut around EONET storm track points per advisory time; global storms since 2015 |
| 4 | Information source | Agency advisories reachable via EONET source links (verified this run: TS Hanna → NOAA NHC archive) — official position/intensity/impact text (reports + decision-workflow), plus EONET's structured magnitudes |
| 5 | Semantic relationship | Language states operational storm parameters and expected hazards for the depicted system at that time |
| 6 | Alignment | Event (EONET id ↔ advisory number) + temporal (advisory time ↔ imagery time) + spatial (track point) |
| 7 | Supervision generation | Deterministic: EONET geometry timestamps select imagery; advisory text scraped from the linked official archive; template QA from structured magnitudes; QC: advisory-image time-offset audit |
| 8 | Scaling strategy | Every named storm × advisory cadence (6-hourly) × basins × 10 years → 10^5 pairs; grows every season; zero marginal cost |
| 9 | Grounding-quality risks | Intensity is partly non-visual (aircraft/dropsonde data behind advisories) → scope capability to imagery-consistent statements + cite uncertainty; advisory prose includes inland-impact text beyond the image frame (AP-4) → segment text into frame-evidenced vs contextual |
| 10 | Negative-control plan | Blind baseline from climatology + prior advisory (persistence is strong in TC forecasting); Dvorak-style intensity error reported against best-track truth, not just advisory echo |
| 11 | VLM adaptation family | Instruction tuning on image sequences → advisory-style structured text |
| 12 | Application evaluation | Position/intensity error vs best-track; briefer-judged usefulness; target maturity: decision-support-prototype (briefing drafts, never autonomous advisories) |
| 13 | Novelty assessment | data 2 (advisory-imagery pairing at scale unexploited in corpus), task 2 (operational-parameter narration), science 1, application 2 |
| 14 | Feasibility notes | All-open sources; advisory scraping per agency format is the main engineering; human-in-loop framing mandatory for anything advisory-shaped |
| 15 | Metapattern lineage | MP-3 (operational product harvesting) + MP-4 (structured magnitudes), keyed through H2's event graph |
