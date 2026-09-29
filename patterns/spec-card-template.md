# GeoData–Language Pair Spec Card (D4)

A model-independent template for formally describing a candidate multimodal
supervision opportunity — before any data is built. Every field is mandatory;
`TBD` is allowed only in a Draft card. Vocabulary fields use
`methods/schema.md`. No field names a specific VLM: the card describes the
*pairing*, and item 11 describes an adaptation *family*.

## Template

| # | Field | Definition | Worked example (illustrative) |
|---|---|---|---|
| 0 | **Card ID / name** | Kebab-case slug + one-line name. | `osm-caption-pairs` — OSM-derived captions for open satellite imagery |
| 1 | **Application need** | Who needs to decide/do what, in which workflow. Naming an institution or role is required (AP-6). | Regional planners need land-use screening without per-region annotation budgets |
| 2 | **Required capability** | What a model must be able to do (beyond a nominal ML task) for the need. | Describe land use and man-made features of any scene in open vocabulary |
| 3 | **Geospatial evidence** | Data type(s) (schema vocab), source/archive, resolution, coverage, access & license. | Sentinel-2 L2A, 10 m, global, open (Copernicus) |
| 4 | **Information source** | Language-side source: type (schema vocab), holding institution, size/growth rate, access & license. | OSM tags & geometries; ODbL; global; continuously edited |
| 5 | **Semantic relationship** | One sentence: what the language *says about* the geodata (describes / explains / quantifies / instructs / diagnoses). Must be something the geodata can evidence (AP-4). | Language names features present at the imaged location |
| 6 | **Alignment** | Basis (spatial/temporal/entity/event), the join keys, and tolerances (georegistration error, time window). | Spatial: tile footprint ∩ OSM geometry; capture-vs-edit lag < 2 yr |
| 7 | **Supervision generation** | Mechanism(s) (schema vocab), pipeline sketch, and the QC plan — including a measured hallucination/noise rate if any `llm-synthesis` is involved (AP-5). | Deterministic join → template captions → LLM polish; 5% human-audited |
| 8 | **Scaling strategy** | Expected pair count, growth rate, marginal cost per 1K pairs, and what caps it. | ~10M pairs; grows with both archives; ~$0 marginal |
| 9 | **Grounding-quality risks** | Known noise/bias sources mapped to anti-patterns (AP-1…AP-6) and the mitigation for each. | VGI staleness → date filters; template bias → visual-blind baseline reported |
| 10 | **Negative-control plan** | How the claimed capability will be shown non-illusory: visual-blind baseline, spatially grounded metric, zero-shot lower bound (AP-1/2/3). | Blind-LM baseline on all QA; counting/localization metrics |
| 11 | **VLM adaptation family** | Contrastive pretraining / instruction tuning / agentic-RL / retrieval-augmented — family only, no model names. | Contrastive + instruction tuning |
| 12 | **Application evaluation** | The domain metric and baseline the *owning workflow* accepts, and the maturity level targeted (schema ladder). | Planner time-to-screen vs manual; target: workflow-relevant |
| 13 | **Novelty assessment** | The four 0–3 scores (data/task/science/application) with one-line justifications against the corpus. | data 2, task 1, science 0, application 2 |
| 14 | **Feasibility notes** | Licensing conflicts, compute, required domain expertise, ethical/dual-use constraints. | ODbL share-alike; no PII; export-safe |
| 15 | **Metapattern lineage** | Which metapattern(s) (MP-1…MP-7) this card instantiates, and any deliberate deviation. | MP-1 |

---

## Validation back-fill 1 — SkyScript ([2312.12856](https://arxiv.org/abs/2312.12856))

| # | Field | Value |
|---|---|---|
| 0 | Card ID | `skyscript-backfill` — OSM-tag captions for open RS imagery |
| 1 | Application need | RS researchers/SDG monitors need task-agnostic semantic access to imagery without commissioned annotation (paper motivates SDGs/climate; no institution named — a gap the card format exposes) |
| 2 | Required capability | Open-vocabulary recognition of 29K semantic tags incl. fine-grained object attributes |
| 3 | Geospatial evidence | Open, unlabeled multi-source satellite imagery; global |
| 4 | Information source | OpenStreetMap tags (structured-observations); ODbL; global; continuously growing |
| 5 | Semantic relationship | Tags name objects/attributes present at the imaged coordinates |
| 6 | Alignment | Spatial — geo-coordinates connect image extents to OSM semantics |
| 7 | Supervision generation | deterministic + knowledge-based; automatic connection pipeline; semantic-diversity filtering |
| 8 | Scaling strategy | 2.6M pairs demonstrated; grows with both archives; ~zero marginal human cost |
| 9 | Grounding-quality risks | VGI staleness/incompleteness; density bias toward mapped regions (Global North) |
| 10 | Negative-control plan | zero-shot transfer evaluated across 7 external benchmarks (partial; no blind baseline) |
| 11 | VLM adaptation family | Continual contrastive pre-training |
| 12 | Application evaluation | +6.2% zero-shot scene classification (benchmark only — maturity: benchmark-research) |
| 13 | Novelty | data 3, task 1, science 0, application 1 (per `records.json`) |
| 14 | Feasibility | Open imagery + ODbL; demonstrated by a small team |
| 15 | Metapattern lineage | MP-1 |

**Template check:** every SkyScript property fit an existing field; fields 1
and 12 exposed real weaknesses (unnamed user, benchmark-only evaluation) —
the card works as a diagnostic, not just a description.

## Validation back-fill 2 — WeatherQA ([2406.11217](https://arxiv.org/abs/2406.11217))

| # | Field | Value |
|---|---|---|
| 0 | Card ID | `weatherqa-backfill` — SPC expert analyses paired with convective-ingredient imagery |
| 1 | Application need | Forecasters and at-risk-area residents need severe-convection threat anticipation hours ahead (institution: NOAA SPC workflow) |
| 2 | Required capability | Reason over multi-parameter ingredient maps to judge severe-weather development potential, like a forecaster |
| 3 | Geospatial evidence | Weather-climate fields: instability parameters, surface obs, radar reflectivity imagery; CONUS |
| 4 | Information source | Expert-interpretation — forecaster-written mesoscale analyses (SPC); public; produced continuously |
| 5 | Semantic relationship | Text explains causal ingredients and expected development shown in the paired imagery |
| 6 | Alignment | Temporal + event (+ spatial region): analysis issued about this situation/window |
| 7 | Supervision generation | deterministic pairing of archived product with concurrent imagery; QA tasks derived on top |
| 8 | Scaling strategy | 8K+ pairs built; the SPC archive grows daily and extends back years |
| 9 | Grounding-quality risks | Expert text may reference context outside the paired images (obs history) — bounding required |
| 10 | Negative-control plan | Human-expert comparison + case study with meteorologists (gap to GPT-4o quantified) |
| 11 | VLM adaptation family | Instruction tuning + fine-tuned open VLM evaluation |
| 12 | Application evaluation | Affected-area MCQ and development-potential classification vs meteorologists (maturity: domain-research) |
| 13 | Novelty | data 3, task 2, science 2, application 2 (per `records.json`) |
| 14 | Feasibility | Public government products; no licensing barrier |
| 15 | Metapattern lineage | MP-3 |

**Template check:** all fields filled from the paper's reported properties; no
missing-field gaps found. Two back-fills across two different metapatterns
(MP-1, MP-3) completed without adding fields → template accepted for D5 use.
