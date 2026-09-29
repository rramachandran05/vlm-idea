Status: Draft (execution pre-authorized by Rahul in-session, 2026-09-29)

# Acceptance Criteria: Structured Science Evidence Cards (v2)

Grouped by output O1–O10 from the approved-for-execution [01-spec.md](01-spec.md).

## Criteria

### O1 — Landscape v2
- [ ] Corpus extended with ≥10 new works from beyond geodata–text framing (medicine report generation, scientific agents, multimodal scientific AI), retrieved and verified live, screened under written v2 inclusion rules.
- [ ] Every corpus record (v1 + new) carries the three new axes — `evidence_to_lm` (5-way vocabulary), `fm_role` (9-way vocabulary), `reasoning_ops` (10-way vocabulary) — with `unknown` explicit; validated by tests.
- [ ] QC pass on the new axes per `methods/qc-protocol.md` (seeded ≥20% sample, recorded error rate, re-pass rule applied).
- [ ] A taxonomy summary (script-generated counts) shows the distribution of evidence types, FM roles, and reasoning operations across the corpus.

### O2 — Evidence-composition metapatterns
- [ ] ≥5 composition metapatterns documented on the full 13-element v2 chain (application need → scientific question → reasoning capability → observations → deterministic evidence → FM evidence → contextual evidence → card → generation strategy → grounding/verification → adaptation → scientific evaluation → operational capability), each citing ≥2 corpus records.
- [ ] Each metapattern names the capability unavailable from any single evidence source.

### O3 — Science Card specification
- [ ] A written spec plus machine-readable JSON Schema exist; every field is classed as observed | computed | inferred | learned-representation | contextual, and evidence entries carry value + source + method + provenance + uncertainty (uncertainty may be `null` with a stated reason).
- [ ] The schema supports at minimum: single observation, before/after pair, temporal sequence, anomaly-vs-baseline, representation trajectory, and analog references.
- [ ] A validator runs in the test suite; all demonstrator cards validate.
- [ ] Model-independence: no schema field names Prithvi, HLS, or a specific LLM (they appear only as provenance *values*).

### O4 — Science FM contribution taxonomy
- [ ] A taxonomy document classifies when an FM adds information beyond metadata/deterministic variables, citing ≥5 corpus records and the demonstrator ablation numbers.
- [ ] It explicitly lists cases where deterministic science is preferable (≥3, evidence-cited).

### O5 — Evidence → language framework
- [ ] Implemented generators produce ≥6 distinct language-product types from the same card (including description, temporal-change, comparison, anomaly/attribution QA, uncertainty statement, recommended follow-up).
- [ ] Every generated sentence carries a machine-readable trace to the card field(s) it uses and an epistemic tag (evidence-supported | derived-interpretation | hypothesis | retrieved-knowledge); tests verify traceability.

### O6 — Evidence-driven question generation
- [ ] Questions are generated from evidence-state rules (thresholds/conflicts/absences over card fields), not templates attached to imagery regardless of content; the rule set is documented.
- [ ] On demonstrator cards, event-state cards yield discrimination/attribution questions while stable-state cards yield baseline/monitoring questions — verified by a test on the generated outputs.
- [ ] Negative/counterfactual supervision exists: ≥2 counterfactual constructions (e.g., similar spectral decline with conflicting context; evidence-insufficient cases) generating discrimination or abstention supervision.

### O7 — NASA opportunity catalog v2
- [ ] ≥6 new opportunity entries where the text does not yet exist but is generatable from authoritative evidence composition; each names its full composition (need × observation × deterministic measurement × FM representation × contextual data × knowledge × reasoning op × language product) and cites live-verified holdings.
- [ ] Entries are prioritized with rubrics covering the 12 ranking factors of requirements §18 (grouped is acceptable; mapping stated).

### O8 — HLS + Prithvi demonstrator
- [ ] End-to-end pipeline runs from real satellite observations (HLS if credentials available, else the documented Sentinel-2 HLS-equivalent) for ≥10 event sites and ≥10 stable control sites, ≥2 time points each.
- [ ] Each site yields a validated Science Card containing: observed band statistics, deterministic indices (NDVI/NBR + deltas), Prithvi embedding descriptors and representation-change metric, nearest-neighbor analog references, external event context (from a verified holding), provenance and uncertainty per evidence entry.
- [ ] ≥100 grounded language products are generated across cards, each traceable per O5.
- [ ] A grounding QC (seeded sample, manual review, recorded pass rate) covers the generated products.

### O9 — Ablation
- [ ] A quantitative comparison on the same sites reports discrimination performance (event vs stable) for at least: deterministic variables only; FM representation-change only; combined card evidence — with the metric and n stated.
- [ ] The Science-FM-contribution question is answered explicitly from the numbers (what the FM adds and where deterministic evidence suffices), including a null/negative result if that is what the data shows.

### O10 — Research agenda
- [ ] A document identifies ≥5 directions where the architecture creates new capability, each tied to evidence from O1–O9, with a stated fastest-path demonstration for each.

### Cross-cutting
- [ ] All new analysis/pipeline code ships with tests; the full suite passes at delivery.
- [ ] Every quantitative claim regenerates from committed data via scripts.
- [ ] All external model weights/data sources are named with source, size, and license in the demonstrator README.

## Out of scope for verification
- LLM/VLM training or fine-tuned-model performance numbers.
- Statistical significance at scale — demonstrator n is tens of sites; the ablation is a demonstration-grade signal, stated as such.
- True HLS granule access if Earthdata credentials are unavailable (the equivalent-sensor path is acceptance-equivalent, per Spec assumption).
- Millions of constructed cards (per-field constructibility + measured per-card cost stand in).
