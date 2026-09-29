# Spec Card: eonet-worldview-event-narration

**Generating combination:** disaster-monitoring need × GIBS daily imagery (H3) × EONET curated events (H2) × deterministic spatio-temporal join + template rendering.

| # | Field | Value |
|---|---|---|
| 0 | Card ID / name | `eonet-worldview-event-narration` — event-grounded narration of daily satellite imagery |
| 1 | Application need | Disaster-monitoring analysts (e.g., NASA Disasters program, situational-awareness desks) need plain-language "what is happening here" summaries tied to imagery of ongoing natural events |
| 2 | Required capability | Given a satellite scene and date, state which curated natural event is present, its category, magnitude, and evolution vs prior days |
| 3 | Geospatial evidence | GIBS/Worldview daily global layers (VIIRS/MODIS true color, thermal anomalies, aerosol), tile-addressable by date+bbox; open |
| 4 | Information source | EONET event records: title, category, timestamped point/polygon track, magnitude, authoritative source links (structured-observations); open API |
| 5 | Semantic relationship | Language asserts the identity, category, magnitude, and temporal evolution of the event visible at the imaged location/date |
| 6 | Alignment | Spatial (event geometry ∩ tile bbox) + temporal (same UTC day) + event (EONET id); tolerance: buffer event point by category-typical extent |
| 7 | Supervision generation | Deterministic join EONET→GIBS tiles; template rendering of event fields into captions/QA; multi-day sequences give change statements; QC: manual inspection sample with recorded pass rate |
| 8 | Scaling strategy | EONET holds tens of thousands of events since 2015, each × multiple days × multiple layers → 10^5–10^6 pairs; grows automatically; ~zero marginal cost |
| 9 | Grounding-quality risks | Cloud-obscured scenes pair with event text the pixels don't show (AP-4) → cloud-fraction filter or "obscured" captions; small events sub-resolution at 250m–1km → magnitude/category floor per layer |
| 10 | Negative-control plan | Visual-blind baseline on event-presence QA; negative pairs from event-free dates at the same location; report both |
| 11 | VLM adaptation family | Instruction tuning (event QA + change narration); retrieval-augmented variant using EONET as the index |
| 12 | Application evaluation | Event detection/attribution accuracy vs held-out EONET; analyst time-to-brief; target maturity: workflow-relevant (Disasters program situational reports) |
| 13 | Novelty assessment | data 2 (EONET unexploited as supervision in corpus), task 1 (event narration ≈ change captioning), science 1, application 2 (live-feed grounding for situational awareness) |
| 14 | Feasibility notes | All-open, key-free APIs; compute-light (tile fetch + templating); no licensing or PII constraints |
| 15 | Metapattern lineage | MP-4 (structured observation rendering) + MP-1's coordinate join; sequences borrow MP-6's event framing |
