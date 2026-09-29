# Schema v2 — Evidence, FM-Role, and Reasoning Axes (O1)

Extends `schema.md` (v1 axes unchanged). Three new controlled-vocabulary
fields, stored in `data/characterization/records-v2.json` joined on `id`.
`unknown` is explicit everywhere; the v1 QC protocol applies.

## `evidence_to_lm` (list) — what information sits between raw observation and generated language

Counts information injected **anywhere** in the pipeline — inference-time
inputs *or* supervision-construction injections (e.g., curated class knowledge
baked into instruction data) — since both shape what the generated language
can be grounded in. (Clarified during the v2 QC pass, 2026-09-29.)
| Value | Definition |
|---|---|
| `observed` | raw sensor measurements, bands, acquisition metadata, coordinates fed (as pixels or values) to the LM |
| `derived-deterministic` | spectral indices, physical quantities, anomalies, change metrics, statistics from established algorithms |
| `ai-inferred` | task-model outputs: segmentation, classification, detections, predicted variables |
| `learned-representation` | FM embeddings, similarity scores, anomaly/novelty scores, representation trajectories, nearest-neighbor analogs |
| `external-contextual` | weather, terrain, land cover, event databases, historical records, forecasts, knowledge graphs, literature |
| `unknown` | the paper does not say |

## `fm_role` (list) — how a science/domain foundation model participates
`direct-multimodal-encoder` | `feature-extractor` | `embedding-generator` |
`similarity-retrieval` | `anomaly-detector` | `temporal-change-representation` |
`downstream-task-backbone` | `semantic-inference` | `none` | `unknown`

(`none` = the system uses no science-FM component beyond a generic LLM/VLM;
generic CLIP-style backbones trained in-domain count as `feature-extractor`/
`embedding-generator` per their use.)

## `reasoning_ops` (list) — the semantic operation the LM is trained/evaluated to perform
| Value | Probe question |
|---|---|
| `describe` | What is observed here? |
| `compare` | How does this differ from its historical/reference state? |
| `detect` | What changed, and when? |
| `integrate` | What do heterogeneous observations collectively indicate? |
| `explain` | What processes are consistent with the evidence? |
| `discriminate` | Which evidence supports cause A over cause B? |
| `retrieve-analogs` | Where have similar states occurred? |
| `hypothesize` | What plausible processes could explain this? |
| `test-hypotheses` | What additional observation would distinguish explanations? |
| `recommend-analysis` | What analysis/action should follow? |
| `unknown` | not determinable from the source |

## Inclusion-rule extension (v2, logged)
For the science-data→language pattern class, the v1 geospatial restriction is
lifted: works from **medicine, scientific agents, and other observational
sciences** are in scope when they connect scientific observations/measurements/
model outputs to language generation or language-mediated reasoning — the
survey question is the *evidence pipeline*, not the sensor. Records from this
extension are domain-tagged `science-adjacent` (new tag) and, where geospatial,
also carry v1 domain tags. Pure-NLP work with no observational evidence stays
out of scope.
