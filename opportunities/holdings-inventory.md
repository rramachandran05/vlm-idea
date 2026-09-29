# Holdings Inventory (D5)

NASA and related Earth-science information holdings **examined live on
2026-09-29** (every endpoint probed and a content sample inspected — no
hypothetical sources). Each entry: geodata assets, language/information
assets, access path, availability/license.

| # | Holding | Geodata assets | Language / information assets | Access path (verified) | Availability |
|---|---|---|---|---|---|
| H1 | **NASA CMR / Earthdata** | Metadata + links to every NASA EO collection & granule (all DAACs) | Collection **summaries**: dense scientific prose describing what each product measures, how, and why (sample: HMA2_FGP flood-geomorphic-potential summary) | `cmr.earthdata.nasa.gov/search/collections.json?keyword=…` (HTTP 200, sample read) | Open, no key |
| H2 | **NASA EONET** | Curated natural-event geometries (points/polygons) with timestamps & magnitudes, across 13 categories | Event titles, categories, and **source links** to authoritative agency pages (NHC advisories etc.) | `eonet.gsfc.nasa.gov/api/v3/events` (200, sample read: TS Hanna, NOAA_NHC source) | Open, no key |
| H3 | **NASA Worldview / GIBS** | ~1000 daily global imagery layers (MODIS/VIIRS/etc.), tile API, any date since 2000 | Layer descriptions; pairs with H2 events for before/after views | `gibs.earthdata.nasa.gov` WMTS (via Worldview; layer set documented in the geoai skill's NASA list; imagery access exercised in D6 demos) | Open, no key |
| H4 | **NWS API — forecast products** | (pairs with H3/H7 fields) CONUS coverage by forecast office | **Area Forecast Discussions** — expert forecaster reasoning text, issued several times daily per office (sample read: KHUN AFD 2026-09-29 with key messages, heat-risk levels); plus warnings/watches (CAP) | `api.weather.gov/products/types/AFD/locations/{WFO}` (200, full product text read) | Open, no key |
| H5 | **USGS Earthquake Hazards** | Event epicenters, **ShakeMap** intensity rasters, ground-failure rasters | **PAGER** loss/impact assessments, "Did You Feel It" reports, event pages; product list verified on live M6.6 event (`dyfi, ground-failure, losspager, shakemap`) | `earthquake.usgs.gov/earthquakes/feed/v1.0/…` (200, sample read) | Open, no key |
| H6 | **GLOBE Observer** | Citizen-science **ground photos** (N/E/S/W/up/down) with GPS + compass metadata | Observer **captions** and land-cover classifications per photo (sample read: geolocated 2026-09-05 observation with captions and photo URLs) | `api.globe.gov/search/v1/measurement/…` (200, sample read) | Open, no key |
| H7 | **NASA CMR granule/variable metadata + DAAC product docs** | Granule-level spatial/temporal footprints for every product | Product user-guide/ATBD-derived summaries embedded in CMR umm-json | same H1 API, `…/granules.json` | Open |
| H8 | **NASA Image and Video Library** | Curated EO imagery (Landsat/ISS/airborne) | **Editor-written narrative descriptions** per image (sample read: Salton Sea flood-history narrative) | `images-api.nasa.gov/search?q=…` (200, sample read) | Open, no key |
| H9 | **Gateway to Astronaut Photography (JSC EOL)** | 4M+ geolocated astronaut photos of Earth | Cataloger/scientist captions and feature identifications | `eol.jsc.nasa.gov` PhotosDatabaseAPI (200 probe) | Open |
| H10 | **NASA Earth Observatory / NASA Science feeds** | Image-of-the-day EO scenes (with acquisition metadata) | **Science-writer narratives** explaining each scene's Earth-science story, reviewed by NASA scientists | `earthobservatory.nasa.gov/feeds/…` (301→200, RSS read) | Open |
| H11 | **GBIF occurrences** | (pairs with H3/commercial imagery) 3B+ geolocated species occurrence records | Species identity → linkable habitat/trait text (EcoWikiRS pattern) | `api.gbif.org/v1/occurrence/search` (200, sample read: geolocated record) | Open, CC-BY-NC mix |
| H12 | **USDA NASS Quick Stats** | (pairs with imagery/CDL) county-level crop statistics; weekly **Crop Progress & Condition** categorical reports | Structured crop condition/progress records renderable to language | `quickstats.nass.usda.gov/api` (200 probe; **requires free API key** for data pulls) | Open w/ key |

## Notes
- H3's imagery access is exercised directly in the D6 demonstration builds
  (GIBS tile URLs are constructed per NASA's published WMTS scheme and
  spot-verified there); its *language* assets are thin — GIBS is the imagery
  side of pairings whose language comes from H1/H2/H4/H5/H10.
- **Unexploited-by-the-corpus check:** none of the 59 corpus works uses H1
  collection summaries, H5 PAGER text, H6 GLOBE captions, H8/H9/H10
  narrative archives, or H12 condition reports as supervision. WeatherQA/
  SynopticBench (corpus) already exploit H4-class text for *severe weather
  and synoptic discussion*; other H4 product families (e.g., hydrology
  discussions) remain unexploited.
- Everything listed is examined evidence; anything we could not probe live
  (e.g., Copernicus EMS damage grading) is deliberately **absent** from this
  inventory and from the opportunity cards.
