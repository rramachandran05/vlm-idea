# Spec Card: globe-ground-truth-captions

**Generating combination:** land-cover validation need × co-located satellite imagery (H3) + GLOBE ground photos (H6) × GLOBE observer captions/classifications (H6) × deterministic co-location + weak supervision.

| # | Field | Value |
|---|---|---|
| 0 | Card ID / name | `globe-ground-truth-captions` — citizen ground truth as cross-view language supervision |
| 1 | Application need | Land-cover product teams (NASA GLOBE, LP DAAC validation) need ground-truth-grounded interpretation of satellite pixels; GLOBE's photo+caption archive is collected exactly for this but unused as VLM supervision |
| 2 | Required capability | Describe ground-level land cover and surface conditions of a satellite pixel/patch, calibrated by what citizen observers actually reported there |
| 3 | Geospatial evidence | Satellite patches (HLS/GIBS) centered on GLOBE observation coordinates, matched to observation date; plus the 6-direction ground photos themselves |
| 4 | Information source | GLOBE land_covers records: observer captions, MUC land-cover classifications, dry/wet flags, compass-tagged photos (structured-observations + crowd-caption); open API, sample verified this run |
| 5 | Semantic relationship | Language reports ground-verified surface state (cover type, condition) at the imaged location and date |
| 6 | Alignment | Spatial (GPS point → patch) + temporal (same season/date window) + entity (observation id); cross-view: ground photo ↔ overhead patch |
| 7 | Supervision generation | Deterministic join; template rendering of classifications; captions kept verbatim as weak supervision with noise-aware training (MP-5 style); QC: sample audit of caption-photo-patch consistency |
| 8 | Scaling strategy | Millions of GLOBE observations, growing via the Observer app; ~zero marginal cost; multilingual captions are a feature (multilingual supervision) |
| 9 | Grounding-quality risks | Crowd noise (mislabeled cover, "null" captions — seen in the live sample) → filter completeness, weight by observer history; GPS error vs 30m pixels → patch-level, not pixel-level, claims |
| 10 | Negative-control plan | Hold-out agreement with professionally validated sites (LUCAS-style); blind baseline predicting cover from location prior alone |
| 11 | VLM adaptation family | Contrastive cross-view (ground↔overhead) + instruction tuning for condition description |
| 12 | Application evaluation | Land-cover product validation throughput (auto-screening GLOBE reports vs product disagreements); target maturity: workflow-relevant (GLOBE/LP DAAC validation loop) |
| 13 | Novelty assessment | data 3 (GLOBE captions unexploited in corpus), task 2 (cross-view ground-truth description), science 2 (citizen-science calibration of EO semantics), application 2 |
| 14 | Feasibility notes | Open API; photos have usage-friendly terms; multilingual QC needed; volume manageable |
| 15 | Metapattern lineage | MP-4 (observation rendering) + MP-5 (weak pairing with noise-aware training) |
