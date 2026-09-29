# Spec Card: ground-failure-terrain-explanations

**Generating combination:** post-earthquake infrastructure triage need × ShakeMap + ground-failure rasters over terrain imagery (H5/H3) × USGS ground-failure model outputs and event-page interpretations (H5) × deterministic per-event pairing + knowledge-based rendering.

| # | Field | Value |
|---|---|---|
| 0 | Card ID / name | `ground-failure-terrain-explanations` — explaining landslide/liquefaction likelihood after earthquakes |
| 1 | Application need | Lifeline operators and road-network managers need, within hours of a quake, plain-language triage of where landslides/liquefaction likely cut corridors — USGS publishes the rasters and expert framing, but reading them requires specialists |
| 2 | Required capability | Given terrain imagery/DEM context plus event ground-failure rasters, explain which corridors/areas face landslide vs liquefaction risk and why (slope, saturation, shaking), at triage granularity |
| 3 | Geospatial evidence | USGS ground-failure probability rasters + ShakeMap per event; DEM/terrain and optical basemap context; global events since ~2018 |
| 4 | Information source | USGS ground-failure product summaries, alert statements, and model documentation (structured-observations + scientific-knowledge); product presence verified on a live M6.6 event this run |
| 5 | Semantic relationship | Language explains hazard likelihood and its physical drivers for the depicted terrain — causal, spatially specific interpretation |
| 6 | Alignment | Event (USGS id) + spatial (raster grid ↔ terrain tiles) |
| 7 | Supervision generation | Deterministic per-event pairing; knowledge-based rendering of raster statistics + driver variables into explanation text; QC: driver-attribution audits against model docs |
| 8 | Scaling strategy | Hundreds of ground-failure-processed events × many tiles each; grows with seismicity; zero marginal human cost |
| 9 | Grounding-quality risks | Model outputs are probabilistic estimates, not observations — language must carry uncertainty (mis-stating them as observed slides is an AP-4 variant); raster resolution vs corridor width mismatch |
| 10 | Negative-control plan | Blind baseline from slope+magnitude heuristics; agreement with post-event observed-landslide inventories where published (real-world truth, not just model echo) |
| 11 | VLM adaptation family | Instruction tuning on multi-layer raster+terrain stacks → explanations; structured corridor-risk outputs |
| 12 | Application evaluation | Corridor-triage agreement with expert picks on held-out events; time-to-triage; target maturity: decision-support-prototype (lifeline operators) |
| 13 | Novelty assessment | data 3 (ground-failure products unexploited in corpus), task 2 (causal hazard explanation), science 2 (geotechnical drivers), application 2 |
| 14 | Feasibility notes | Open USGS products; observed-slide inventories exist for validation on major events; modest volume |
| 15 | Metapattern lineage | MP-4 + MP-7 (model-constructed truth with uncertainty carried) |
