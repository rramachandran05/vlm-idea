# Spec Card: astronaut-photo-geocaption

**Generating combination:** oblique-imagery interpretation need × astronaut photography (H9) × EOL cataloger captions + geolocation records (H9) × deterministic catalog pairing.

| # | Field | Value |
|---|---|---|
| 0 | Card ID / name | `astronaut-photo-geocaption` — cataloger-captioned oblique Earth photography as supervision |
| 1 | Application need | EOL catalogers geolocate/describe millions of astronaut photos largely manually; disaster and science teams use these oblique views when nadir satellites miss the angle — both need automated feature ID and geolocation support |
| 2 | Required capability | Identify geographic features and estimate location/orientation in oblique, variably framed Earth photographs, and describe them in cataloger idiom |
| 3 | Geospatial evidence | 4M+ astronaut photos (handheld, oblique, multi-focal-length), subset geolocated with center coordinates; ISS nadir tracks known |
| 4 | Information source | EOL catalog: scientist/cataloger captions, feature names, geolocation fields (expert-interpretation + structured-observations); API probed this run |
| 5 | Semantic relationship | Language names the geographic features visible and their locations — identification under oblique geometry |
| 6 | Alignment | Entity (photo id ↔ catalog record) + spatial (center point, ISS position) + temporal |
| 7 | Supervision generation | Deterministic catalog join; template QA from structured fields (location, features, focal length); captions verbatim; QC: sample audit of caption-photo agreement |
| 8 | Scaling strategy | Millions of photos, continuously captured; captioned/geolocated subset in the hundreds of thousands; grows with every expedition |
| 9 | Grounding-quality risks | Oblique geometry breaks nadir-trained spatial priors (corpus ISS-Geo142 shows this is hard); uncaptioned majority tempts pseudo-labeling — keep human-cataloged subset as gold (AP-5) |
| 10 | Negative-control plan | Geolocation error vs catalog truth (km bins) with ISS-position-only baseline; feature-ID accuracy vs random-region baseline |
| 11 | VLM adaptation family | Contrastive photo↔map/nadir alignment + instruction tuning for feature description; geolocation as structured output |
| 12 | Application evaluation | Cataloging throughput uplift (auto-suggest features/locations for cataloger confirmation); target maturity: decision-support-prototype inside the EOL cataloging workflow |
| 13 | Novelty assessment | data 2 (corpus has ISS-Geo142 benchmark on 142 photos; the full captioned archive is unexploited), task 2 (oblique geolocation + description), science 1, application 2 |
| 14 | Feasibility notes | NASA imagery is public domain; API exists; volume large but samples cheaply; direct NASA JSC stakeholder |
| 15 | Metapattern lineage | MP-2 (catalog labels → language) + MP-3 (cataloger expertise) |
