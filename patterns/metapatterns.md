# Metapatterns (D4): recurring geodata–language construction strategies

Seven recurring strategies abstracted from the characterized corpus
(`data/characterization/records.json`). Each instantiates the full ten-element
chain from the Spec: **application need → required capability → geospatial
evidence → information source → semantic relationship → alignment →
supervision generation → scaling strategy → VLM adaptation → application
evaluation**, and cites ≥2 corpus records as evidence of recurrence.
Distribution counts come from `analysis/corpus_stats.py`.

---

## MP-1 — Geo-Registered Knowledge Verbalization
Pair open imagery with a co-located geographic knowledge base and verbalize
what the knowledge base says exists there.

1. **Application need:** broad semantic understanding of anywhere-on-Earth
   imagery without commissioning annotation.
2. **Required capability:** open-vocabulary recognition/description of scene
   contents, attributes, and functions.
3. **Geospatial evidence:** optical satellite/aerial imagery (open archives).
4. **Information source:** geo-registered structured knowledge — OSM/VGI tags,
   geometries, functional attributes.
5. **Semantic relationship:** language names entities/attributes/functions
   present at the imaged location.
6. **Alignment:** spatial, via coordinates/footprints.
7. **Supervision generation:** deterministic join + knowledge-based rendering,
   optionally LLM-polished into prose.
8. **Scaling strategy:** grows with both open archives at ~zero marginal human
   cost; millions of pairs demonstrated.
9. **VLM adaptation:** contrastive pretraining or instruction tuning.
10. **Application evaluation:** mostly zero-shot benchmarks so far — the
    weakest link (see AP-6).

**Evidence:** SkyScript [2312.12856](https://arxiv.org/abs/2312.12856),
RSTeller [2408.14744](https://arxiv.org/abs/2408.14744), LHRS-Bot
[2402.02544](https://arxiv.org/abs/2402.02544), OSMDA
[2603.11804](https://arxiv.org/abs/2603.11804), OpenFACADES
[2504.02866](https://arxiv.org/abs/2504.02866), DisasterInsight
[2601.18493](https://arxiv.org/abs/2601.18493).
**Failure mode to avoid:** stale/incomplete VGI injects label noise;
temporal mismatch between map edits and image capture.

---

## MP-2 — Label-to-Language Conversion
Verbalize existing task annotations (classes, boxes, masks) into
captions/QA so legacy supervised datasets become VLM supervision.

1. **Need:** domain VLM where paired text doesn't exist but labeled vision
   datasets do.
2. **Capability:** cross-modal alignment; zero-shot classification/retrieval.
3. **Evidence:** any annotated imagery (optical, SAR, agricultural).
4. **Information source:** the annotations themselves (labels-as-language:
   23/59 records).
5. **Semantic relationship:** language restates annotation semantics.
6. **Alignment:** spatial (annotation is registered to the image).
7. **Generation:** deterministic conversion (Box-to-Caption), templates, or
   LLM seeding from labels.
8. **Scaling:** high — every legacy dataset converts; 5M+ pairs demonstrated.
9. **Adaptation:** CLIP-style contrastive or instruction tuning.
10. **Evaluation:** retrieval/classification benchmarks.

**Evidence:** RemoteCLIP [2306.11029](https://arxiv.org/abs/2306.11029),
RS5M [2306.11300](https://arxiv.org/abs/2306.11300), ChatEarthNet
[2402.11325](https://arxiv.org/abs/2402.11325), EarthVQA
[2312.12222](https://arxiv.org/abs/2312.12222), AgriCLIP
[2410.01407](https://arxiv.org/abs/2410.01407).
**Failure mode:** template QA with tiny vocabularies → AP-1's
self-answering datasets; semantic ceiling is the label taxonomy.

---

## MP-3 — Expert Interpretation Harvesting
Pair observational/forecast data with the expert-written text that
operational institutions already produce about it, every day.

1. **Need:** expert-level interpretation, diagnosis, or advisory text where
   experts are scarce.
2. **Capability:** explain causes, assess significance, and advise like a
   domain expert, grounded in the specific scene/state.
3. **Evidence:** weather/climate fields, radar, satellite imagery, or
   user-submitted photos.
4. **Information source:** authoritative expert products — forecaster
   discussions (SPC, NWS AFDs), extension-service expert answers,
   commissioned expert captions (expert-interpretation: 7/59;
   decision-workflow: 10/59).
5. **Semantic relationship:** language interprets/explains the specific
   observation (causal ingredients, diagnosis, recommended action).
6. **Alignment:** temporal + event (product issued about this time window /
   case), plus spatial extent.
7. **Generation:** deterministic pairing of the archived product with its
   concurrent data; optional LLM restructuring into QA with human
   verification.
8. **Scaling:** high — archives are decades deep and grow daily
   (1.37M AFDs; 116K extension dialogues).
9. **Adaptation:** instruction tuning; evaluation against held-out expert
   text.
10. **Evaluation:** expert-comparison studies; drafting-assistance quality in
    the producing institution's workflow.

**Evidence:** WeatherQA [2406.11217](https://arxiv.org/abs/2406.11217),
SynopticBench [2604.16451](https://arxiv.org/abs/2604.16451), AgMMU
[2504.10568](https://arxiv.org/abs/2504.10568), MIRAGE
[2506.20100](https://arxiv.org/abs/2506.20100), Shipping Forecast
[2512.03623](https://arxiv.org/abs/2512.03623), RSICap
[2307.15266](https://arxiv.org/abs/2307.15266) (commissioned variant).
**Failure mode:** expert text references context outside the paired data
(prior days, unpictured obs) — pairing must bound what the text can see.

---

## MP-4 — Structured Observation Rendering
Render authoritative structured records (surveys, station measurements,
event databases, indicator tables) into language paired with co-located,
co-temporal imagery or fields.

1. **Need:** connect imagery to measured ground truth without new field work.
2. **Capability:** state, quantify, or verify measured conditions from
   imagery.
3. **Evidence:** imagery or gridded fields covering the record's footprint.
4. **Information source:** structured observations (12/59 records): LUCAS
   survey, reanalysis products, official indicators, incident feeds, species
   observations.
5. **Semantic relationship:** language asserts measured/recorded state at a
   location and time.
6. **Alignment:** spatial + temporal (+ entity for per-object records).
7. **Generation:** deterministic join + template rendering into
   captions/QA.
8. **Scaling:** high — record systems are large and refresh on schedule.
9. **Adaptation:** VQA/regression-style tuning.
10. **Evaluation:** agreement with held-out records; domain metrics.

**Evidence:** AgriBench/LUCAS [2412.00465](https://arxiv.org/abs/2412.00465),
ClimateIQA [2406.09838](https://arxiv.org/abs/2406.09838), CityLens
[2506.00530](https://arxiv.org/abs/2506.00530), war-infrastructure estimation
[2608.00119](https://arxiv.org/abs/2608.00119).
**Failure mode:** AP-4 — pairing imagery with aggregates the pixels
underdetermine; keep the mediating observable explicit.

---

## MP-5 — Knowledge-Bridged Weak Pairing
Use an observed entity as a bridge: entity is observed at a location →
attach the entity's encyclopedic/knowledge-graph description to the imagery,
with noise-aware training.

1. **Need:** scientific semantic depth (habitat, function, condition) beyond
   any label taxonomy.
2. **Capability:** science-aware interpretation (e.g., ecosystem type from
   habitat language).
3. **Evidence:** imagery of locations where entities are recorded.
4. **Information source:** entity-linked knowledge — Wikipedia habitat text,
   ConceptNet/WordNet vocab, maps as context.
5. **Semantic relationship:** language describes properties *implied* by the
   entity's presence (weak, partially irrelevant by design).
6. **Alignment:** entity + spatial.
7. **Generation:** weak supervision with robustness mechanisms (weighted
   contrastive losses, hallucination measurement).
8. **Scaling:** high — observation networks (GBIF-class) and knowledge bases
   grow independently.
9. **Adaptation:** contrastive with noise-aware objectives.
10. **Evaluation:** zero-shot science tasks against authoritative
    classifications (EUNIS).

**Evidence:** EcoWikiRS [2504.19742](https://arxiv.org/abs/2504.19742),
VLCE [2509.21609](https://arxiv.org/abs/2509.21609), fMoW-mm
[2501.14905](https://arxiv.org/abs/2501.14905), GeoReasoner
[2406.18572](https://arxiv.org/abs/2406.18572) (human game reasoning as the
bridged knowledge).
**Failure mode:** unbounded noise — requires an explicit noise model and
measured QC (AP-5).

---

## MP-6 — Workflow-Grounded Task Synthesis
Derive tasks, ground truth, and language from executable operational
workflows and published standards, so supervision is verifiable and the
application evaluation is built in.

1. **Need:** decision support inside a named operational workflow (disaster
   response, inspection, routing).
2. **Capability:** evidence-backed operational decisions and reports, not
   just descriptions.
3. **Evidence:** multi-source EO/GIS (optical, SAR, vectors, road networks).
4. **Information source:** the workflow itself — executable geospatial
   procedures, standards (PSCI), triage protocols (decision-workflow:
   10/59).
5. **Semantic relationship:** language specifies the task and asserts the
   decision + rationale.
6. **Alignment:** event + spatial (+ temporal for bi-temporal damage).
7. **Generation:** deterministic — run the workflow to produce ground truth;
   consistency checks replace LLM annotation.
8. **Scaling:** high — workflows re-run on every new event/scene.
9. **Adaptation:** agentic/instruction tuning, RL against workflow-verified
   outcomes.
10. **Evaluation:** operational task success (routing validity, damage
    accuracy vs workflow output), directly meaningful to the owning
    institution.

**Evidence:** GeoDisaster [2606.17246](https://arxiv.org/abs/2606.17246),
TerraBench [2606.13148](https://arxiv.org/abs/2606.13148), Recov-Vision
[2509.20628](https://arxiv.org/abs/2509.20628), PSCI pavement rating
[2504.06785](https://arxiv.org/abs/2504.06785), DisasTeller
[2411.01511](https://arxiv.org/abs/2411.01511).
**Why it matters:** this is the pattern behind every corpus record at
workflow-relevant maturity or above — it is the shortest path past AP-6.

---

## MP-7 — Constructed-Truth Synthesis
Generate the geodata (or the pairing) so ground truth is known by
construction — simulation, physics scaling, or knowledge-steered generation.

1. **Need:** supervision for conditions too rare, dangerous, or unobservable
   to collect (graded flood depths, moderate damage states, embargoed
   scenes).
2. **Capability:** quantitative estimation in long-tail conditions.
3. **Evidence:** synthetic or archival imagery standing in for the rare
   condition.
4. **Information source:** the generator's parameters — simulated depth
   values, physics scaling laws, expert damage taxonomies.
5. **Semantic relationship:** language states the constructed ground-truth
   quantity/state.
6. **Alignment:** spatial + event (constructed).
7. **Generation:** deterministic (truth known by construction) or
   LLM-synthesis steered by domain knowledge.
8. **Scaling:** high — bounded only by compute.
9. **Adaptation:** fine-tuning with curriculum from synthetic to real;
   validation on real cases mandatory.
10. **Evaluation:** accuracy on *real* held-out cases (the synthetic-real gap
    is the metric that matters).

**Evidence:** FloodLlama [2603.17108](https://arxiv.org/abs/2603.17108)
(190K synthetic depth-labeled images, validated on real Detroit floods),
damage-data generation [2508.01380](https://arxiv.org/abs/2508.01380),
war-infrastructure physics projection
[2608.00119](https://arxiv.org/abs/2608.00119).
**Failure mode:** synthetic-only validation; domain shift silently absorbs
the claimed capability.

---

## Cross-cutting observations
- **Scalability concentrates in existing authoritative information.** 49/59
  records rate `high` scalability, and the high-value patterns (MP-1, MP-3,
  MP-4, MP-6) all exploit archives someone else already maintains.
- **The maturity cliff is a construction choice.** Patterns that import the
  application evaluation with the data (MP-3, MP-6) are the ones that reach
  workflow-relevant maturity and beyond; patterns that only import semantics
  (MP-1, MP-2) stall at benchmarks unless combined with a named workflow.
- **LLM synthesis is a polish step, not a source.** 30/59 records use
  llm-generated language, but in the strongest constructions the LLM
  restructures authoritative content rather than inventing it (AP-5).
