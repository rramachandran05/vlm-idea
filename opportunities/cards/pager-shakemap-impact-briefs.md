# Spec Card: pager-shakemap-impact-briefs

**Generating combination:** earthquake rapid-response need × USGS ShakeMap intensity rasters (H5) × USGS PAGER expert impact assessments (H5) × deterministic per-event pairing.

| # | Field | Value |
|---|---|---|
| 0 | Card ID / name | `pager-shakemap-impact-briefs` — expert impact briefs from shaking-intensity maps |
| 1 | Application need | Earthquake response coordinators (USGS NEIC/PAGER consumers: OFDA, WHO, national civil protection) need immediate impact framing — exposed population, likely losses, vulnerable structure types — from the first intensity estimates |
| 2 | Required capability | Read a ShakeMap intensity surface (+ exposure context) and produce a PAGER-style impact assessment: alert level, exposure by intensity bin, structure-vulnerability commentary |
| 3 | Geospatial evidence | ShakeMap MMI rasters + ground-failure (landslide/liquefaction) rasters per event; global coverage since ~2007; open |
| 4 | Information source | PAGER onePAGER assessments and event summaries — expert-calibrated impact text and structured loss estimates (expert-interpretation + structured-observations); open, verified on a live M6.6 event this run |
| 5 | Semantic relationship | Language assesses human/structural impact implied by the shaking field — an expert judgment grounded in the raster plus exposure models |
| 6 | Alignment | Event (USGS event id) + spatial (raster extent); versioned products → pair the assessment with the raster version it was issued against |
| 7 | Supervision generation | Deterministic per-event pairing of archived ShakeMap raster with its PAGER text/tables; template rendering of structured exposure tables into QA; QC: version-matching audit sample |
| 8 | Scaling strategy | Thousands of PAGER-processed events, each with versioned raster+text pairs; grows with global seismicity; zero marginal human cost |
| 9 | Grounding-quality risks | Impact depends on exposure/vulnerability data not in the raster (AP-4) → include population-exposure layer as input modality, or scope capability to "conditional on exposure context"; early-version rasters differ from final → pair by version |
| 10 | Negative-control plan | Blind baseline given only event magnitude+location text (no raster) — the raster must add measurable skill; alert-level confusion matrix vs PAGER truth |
| 11 | VLM adaptation family | Instruction tuning on raster-image + exposure-context → assessment text; structured-output decoding for exposure tables |
| 12 | Application evaluation | Alert-level agreement and exposure-bin error vs held-out PAGER; latency vs current pipeline; target maturity: decision-support-prototype (drafting aid inside the existing PAGER workflow) |
| 13 | Novelty assessment | data 3 (PAGER text never used as multimodal supervision in corpus), task 2 (impact assessment ≠ damage captioning), science 1, application 3 (drops into an existing operational alerting workflow) |
| 14 | Feasibility notes | Open USGS products; modest volume; capability is advisory-drafting, not autonomous alerting — human-in-loop framing avoids dual-use concerns |
| 15 | Metapattern lineage | MP-3 (expert interpretation harvesting) + MP-4 (structured exposure tables) |
