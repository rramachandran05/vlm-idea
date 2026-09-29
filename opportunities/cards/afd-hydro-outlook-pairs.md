# Spec Card: afd-hydro-outlook-pairs

**Generating combination:** flood-anticipation need × precipitation/satellite fields (H3/H4) × NWS AFD hydrology sections (H4) × deterministic issuance-time pairing.

| # | Field | Value |
|---|---|---|
| 0 | Card ID / name | `afd-hydro-outlook-pairs` — forecaster hydrology reasoning paired with the fields it reads |
| 1 | Application need | WFO forecasters and emergency managers need flood-potential reasoning ("locally heavy rainfall the main concern") drafted from current fields; corpus works cover severe convection (WeatherQA) and synoptic discussion (SynopticBench) — hydrology sections are unexploited |
| 2 | Required capability | From precipitation forecasts, radar/satellite moisture fields, and antecedent conditions, produce flood-risk reasoning at WFO granularity, in forecaster idiom with calibrated uncertainty language ("40-80% chances") |
| 3 | Geospatial evidence | Gridded QPF, GOES water-vapor/precipitable-water imagery, radar mosaics for each WFO area at issuance time |
| 4 | Information source | NWS AFD `.HYDROLOGY`/key-message sections, per WFO, several issuances daily (expert-interpretation + decision-workflow); live product text verified this run (KHUN) |
| 5 | Semantic relationship | Text explains flood-relevant causal reasoning about the paired atmospheric fields and states graded risk |
| 6 | Alignment | Temporal (issuance time ↔ field valid time) + spatial (WFO county-warning area) |
| 7 | Supervision generation | Deterministic pairing by issuance timestamp; section parsing (AFD structure is conventionalized); QC: sample audit that referenced phenomena appear in paired fields (MP-3 bounding rule) |
| 8 | Scaling strategy | ~120 WFOs × ~2-4 AFDs/day × years of archive → 10^5+ sectioned pairs; grows daily; zero marginal cost |
| 9 | Grounding-quality risks | Discussions reference unpaired context (previous days, upstream obs) → include short field history; office-style variance → per-office normalization or style conditioning |
| 10 | Negative-control plan | Blind-LM baseline from location+date alone; skill scored on held-out flood events (did generated reasoning flag them?) |
| 11 | VLM adaptation family | Instruction tuning on multi-image field stacks → discussion text; evaluation with SPACE-style phenomenon-coverage metrics |
| 12 | Application evaluation | Forecaster-judged draft usefulness; phenomenon recall vs issued AFDs on held-out flood days; target maturity: decision-support-prototype (drafting aid in AFD production) |
| 13 | Novelty assessment | data 2 (same archive family as SynopticBench, unexploited section), task 2 (risk reasoning, not description), science 2 (hydrometeorological causality), application 2 |
| 14 | Feasibility notes | Open API, no key; parsing AFD sections is known-solvable; NOAA collaboration path exists via existing WeatherQA-style engagements |
| 15 | Metapattern lineage | MP-3 (expert interpretation harvesting), scoped to an unexploited product family |
