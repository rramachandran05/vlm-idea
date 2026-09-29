# Spec Card: nass-crop-condition-scenes

**Generating combination:** in-season crop monitoring need × HLS/Sentinel county composites (H3) × USDA NASS weekly Crop Progress & Condition reports (H12) × deterministic spatio-temporal join + template rendering.

| # | Field | Value |
|---|---|---|
| 0 | Card ID / name | `nass-crop-condition-scenes` — official crop condition language for satellite scenes |
| 1 | Application need | Crop analysts (USDA, NASA Harvest, insurers, traders) need in-season condition assessment; NASS publishes authoritative weekly condition/progress language per state/crop that has never been paired with imagery as supervision |
| 2 | Required capability | From a county/state-week satellite composite, state crop progress stage and condition distribution ("45% good, 20% excellent; harvest 30% complete") in NASS idiom |
| 3 | Geospatial evidence | Weekly HLS/Sentinel-2 composites clipped to crop masks (USDA CDL) per county/state; growing-season coverage |
| 4 | Information source | NASS Quick Stats weekly Crop Progress & Condition records (structured-observations produced by enumerator/reporter networks — ground-sourced official statistics); API verified this run (key required, free) |
| 5 | Semantic relationship | Language asserts officially measured crop state for the imaged area-week — measured ground condition, not pixel aesthetics |
| 6 | Alignment | Spatial (state/county × CDL crop mask) + temporal (report week ↔ composite week) + entity (crop) |
| 7 | Supervision generation | Deterministic join + template rendering of records into statements/QA; multi-week sequences give trajectory supervision; QC: NDVI-vs-condition sanity screens, sample audits |
| 8 | Scaling strategy | ~20 years × 48 states × ~10 crops × weekly → 10^5+ area-week records; refreshed every season; zero marginal cost beyond compositing |
| 9 | Grounding-quality risks | State-level aggregates over heterogeneous pixels (AP-4) → prefer county granularity where published, patch-to-aggregate framing made explicit; clouds → composite QC; condition is partly non-visual (soil moisture) → include ancillary bands |
| 10 | Negative-control plan | Blind baseline from climatology+calendar alone (strong in agriculture!) — imagery must add skill; report condition-distribution error vs NASS truth |
| 11 | VLM adaptation family | Instruction tuning on composite stacks → condition statements; regression-style structured output for distributions |
| 12 | Application evaluation | Weekly condition nowcast skill vs NASS in held-out seasons/states; analyst adoption in monitoring workflows; target maturity: workflow-relevant (NASS/Harvest monitoring) |
| 13 | Novelty assessment | data 3 (NASS condition language unexploited in corpus; AgriBench used EU LUCAS differently), task 2 (area-week condition assessment), science 2 (links spectral trajectories to surveyed condition), application 3 (market/policy-relevant weekly product) |
| 14 | Feasibility notes | Free API key; CDL masks open; compositing is standard; US-only initially (generalizes to other national statistics services) |
| 15 | Metapattern lineage | MP-4 (structured observation rendering), trajectory variant |
