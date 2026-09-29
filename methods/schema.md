# Record Schema & Controlled Vocabularies (D1–D3)

One JSON record per surveyed work. D1 fields live in `data/corpus/papers.json`;
D2/D3 fields in `data/characterization/records.json`, joined on `id`.
Enum fields take **only** the values defined here, plus `unknown` where noted.
`unknown` means "the paper (abstract + skimmed text) does not say" — never a guess.

## D1 — identification (corpus)

| Field | Type | Rule |
|---|---|---|
| `id` | string | arXiv ID (`2306.11300`) or `doi:<doi>` for non-arXiv; unique |
| `source` | enum | `arxiv` \| `other:<venue>` |
| `title` | string | as returned by lookup |
| `year`, `month` | int | from v1 date; year ∈ [2021, 2026] |
| `venue` | string | arXiv primary category, or venue name; may be `unknown` |
| `domains` | list | ⊆ the 7 tags in `inclusion-rules.md`, ≥1 |
| `url` | string | resolvable abstract page |

## D2 — supervision construction (characterization)

| Field | Type | Values |
|---|---|---|
| `geodata_type` | list | open but normalized: `optical-satellite`, `sar`, `hyperspectral`, `aerial`, `street-level`, `weather-climate-field`, `dem-terrain`, `map-vector`, `multi-source`, `non-geospatial` (v2: medical images, lab experiments, literature — science-adjacent records), `in-situ-timeseries` (v2: ground sensor series), `unknown` |
| `language_source` | list | `labels-as-language` (class labels/annotations verbalized) \| `structured-observations` (measurements, event records, metadata rendered as text) \| `expert-interpretation` (analyst/scientist-written descriptions of the specific scene) \| `scientific-knowledge` (domain knowledge not tied to one scene: encyclopedic text, ATBDs, ontologies) \| `reports` (operational documents: damage assessments, bulletins, news) \| `decision-workflow` (task guidance, alerts, recommended actions) \| `crowd-caption` (crowdworker/volunteer free-text written for the dataset) \| `web-text` (alt-text/co-occurring web text) \| `llm-generated` (language authored by an LLM, from whatever seed) \| `unknown` |
| `semantic_relationship` | string | free text, one line: what the language *says about* the geodata (describes contents / explains cause / assesses impact / instructs action / names entities / quantifies state …) |
| `alignment` | list | `spatial` \| `temporal` \| `entity` \| `event` \| `unknown` |
| `pair_generation` | list | `deterministic` (rule-based from structured data) \| `template` (slot-filled text) \| `combinatorial` (systematic composition of QA/instructions) \| `llm-synthesis` \| `weak-supervision` (noisy/heuristic pairing, e.g. co-location) \| `knowledge-based` (from KGs/ontologies/authoritative documents) \| `manual` (humans wrote pairs one by one) \| `unknown` |
| `scalability` | enum | `high` (grows with existing authoritative/structured data at ~zero marginal human cost) \| `medium` (automated but capped by source coverage or needs human QC per batch) \| `low` (per-pair human effort) \| `unknown` |
| `scalability_note` | string | one line justifying the rating |

## D3 — capability, use, maturity, novelty

| Field | Type | Values |
|---|---|---|
| `nominal_task` | list | `vqa`, `captioning`, `retrieval`, `classification`, `grounding`, `change-description`, `instruction-following`, `detection`, `segmentation`, `forecasting`, `other` |
| `capability` | string | what the pairing lets a model *do* that it couldn't before — must not be a restatement of `nominal_task` |
| `use_enabled` | string | scientific/operational use, or `none identified` |
| `maturity` | enum | `benchmark-research` \| `domain-research` \| `workflow-relevant` \| `decision-support-prototype` \| `operational-prototype` \| `deployed` — per `maturity-ladder.md` |
| `novelty_data` / `novelty_task` / `novelty_science` / `novelty_application` | int 0–3 | rubric below |
| `negative_case` | bool | true when a novel dataset/method yields limited scientific or operational value |
| `negative_reason` | string | required when `negative_case`; else `""` |
| `note` | string | anything load-bearing that fields can't hold |

### Novelty rubric (each dimension, 0–3)
- **0** — none: replicates existing data/task/science/application with minor variation.
- **1** — incremental: same kind, new instance (another captioning set on another city).
- **2** — substantive: new source type, new task formulation, new science question, or new application setting for VLM pairing.
- **3** — first-of-kind: no prior geodata–language work does this; opens a line of research or use.

Dimension meanings — **data**: novelty of the geodata–language pairing itself;
**task**: of the formulated capability/task; **science**: of the Earth-science
question the pairing can address; **application**: of the operational/decision
use it serves.

## Schema-change rule
Extending any vocabulary requires editing this file in the same commit as the
data that first uses the new value, with a one-line rationale in the commit
message. Inline improvisation is a schema violation (caught by tests).
