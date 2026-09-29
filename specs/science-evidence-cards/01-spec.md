Status: Draft (execution pre-authorized by Rahul in-session, 2026-09-29 — "update specs … and go ahead and execute; you don't need to stop for permission")

# Spec: Structured Science Evidence Cards (v2 reframe)

## Relationship to the completed v1 effort

Supersedes-and-builds-on `specs/geovlm-opportunity-framework/` (v1, fully
executed 2026-09-29). The unit of analysis changes from **geodata–text pair**
to the pipeline **scientific observations → derived/inferred evidence →
Structured Science Card → grounded language → scientific/operational
capability**. v1's central empirical finding — pairings stall at benchmarks
unless they import expert interpretation or workflow grounding — becomes this
effort's **central hypothesis** (stated as the Core Research Question below).
v1 assets carried forward: the 59-work characterized corpus (extended, not
rebuilt), the holdings inventory (extended), the QC protocol, the maturity
ladder, the anti-patterns, and the repo/test infrastructure. v1's Spec Card is
**replaced** by the Science Evidence Card specification (O3).

## Core research question (verbatim from requirements)

Can a structured evidence layer transform scientific observations and Science
Foundation Model representations into grounded language supervision that
teaches LLMs not merely to describe geospatial imagery, but to compare
observations, recognize state changes, integrate heterogeneous evidence,
evaluate hypotheses, and support scientific and operational reasoning?

## What this effort should produce (10 outputs, per requirements §OUTPUT)

- **O1. Landscape analysis v2** — extend the v1 corpus beyond
  VQA/captioning-framed work into multimodal scientific AI, scientific
  agents, and medicine (report generation from images + measurements +
  context); re-characterize **all** records on three new axes:
  (a) **evidence types provided to the LM** (observed / deterministically
  derived / AI-inferred / learned-representation / external-contextual),
  (b) **Science-FM role** (encoder, feature extractor, embeddings,
  similarity/retrieval, anomaly, temporal-change representation, task head,
  semantic inference, not-required),
  (c) **reasoning operation** trained/evaluated (describe, compare, detect,
  integrate, explain, discriminate, retrieve-analogs, hypothesize,
  test-hypotheses, recommend-analysis).
- **O2. Evidence-composition metapatterns** — recurring strategies for
  combining evidence sources into capabilities unavailable from any single
  source (observation+temporal → change interpretation; observation+FM →
  anomaly/similarity; observation+physics+events → attribution; etc.),
  following the revised 13-element chain (application need → … → operational
  capability).
- **O3. Structured Science Card specification** — model-independent schema
  (document + machine-readable JSON Schema + validator) whose fields preserve
  **observed → computed → inferred → learned-representation →
  retrieved/contextual** distinctions, and per-field
  **value + source + method + provenance + uncertainty**. Covers single
  observations, before/after pairs, sequences, anomalies vs climatology,
  representation trajectories, neighborhoods, cross-location comparisons,
  and analogs.
- **O4. Science FM contribution taxonomy** — when a Science FM (e.g.,
  Prithvi-EO) contributes information not obtainable more transparently from
  metadata, physical variables, or deterministic algorithms — grounded in
  both the corpus and the demonstrator's ablation.
- **O5. Evidence → language generation framework** — methods for producing a
  *family* of language products from one card (factual description, change
  description, comparison, anomaly explanation, evidence-based QA,
  competing-hypothesis evaluation, uncertainty statements, analog
  descriptions, recommended follow-ups, decision-support narratives), each
  statement traceable to card fields and tagged
  evidence-supported / derived-interpretation / hypothesis /
  retrieved-knowledge / speculation.
- **O6. Evidence-driven question generator** — rules that derive
  scientifically interesting questions from the card's evidence state
  (abrupt representation shift + ΔNBR + drought context → discrimination
  questions), not generic image questions.
- **O7. NASA opportunity catalog v2** — candidate datasets from combining
  NASA observations × algorithms × FMs × contextual data × knowledge, where
  **the text does not yet exist** but is generatable from authoritative
  evidence; expressed as filled Science Cards + composition recipes.
- **O8. HLS + Prithvi demonstrator** — end-to-end: HLS-class time-series
  observations → spectral/physical computation + Prithvi-EO embeddings +
  representation-change metrics + analogs + event context → Science Cards →
  multiple grounded language products + evidence-driven questions.
- **O9. Ablation study** — quantitative comparison of evidence tiers for a
  concrete task (event vs stable-site discrimination and attribution):
  raw-imagery proxy vs deterministic variables vs FM representation vs full
  card vs card+external knowledge.
- **O10. Research agenda** — where this architecture creates genuinely new
  capability vs another caption/VQA dataset.

## Why

v1 established *empirically* that semantic pairing alone stalls: 30/59 works
at benchmark maturity, zero deployed, and the works that climb import expert
or workflow evidence. The reframe operationalizes that finding: instead of
mining text that already co-exists with geodata, **construct the evidence
state** (with provenance and uncertainty) and generate the text — turning
authoritative-but-textless NASA holdings into supervision, and making the
LLM's job a defined reasoning operation over auditable evidence rather than
open-ended description.

## Out of scope

- Training or fine-tuning any LLM/VLM (the demonstrator generates and
  evaluates supervision; model training is follow-on).
- Production pipelines and full-archive card construction (demonstrator scale:
  tens of sites, hundreds of language products).
- Paper writing (feeds `write_paper` later).
- GPU-scale FM experimentation — demonstrator runs CPU-scale Prithvi
  inference on chips.

## Open questions / assumptions (noted inline, per skill rules)

- **HLS access:** LP DAAC HLS granules require Earthdata login, and this
  session neither creates accounts nor handles credentials. *Assumption:*
  demonstrator uses **Sentinel-2 L2A COGs (public AWS Earth Search, no
  auth)** — the S30 source sensor of HLS — with the same six HLS bands
  (B02/B03/B04/B8A/B11/B12), documented as the HLS-equivalent testbed; the
  card schema and code treat the sensor as a provenance field so true HLS
  slots in when credentials exist.
- **Prithvi variant:** *Assumption:* Prithvi-EO v1 100M (public Hugging Face
  weights, ~400 MB, runnable on CPU with its published MAE implementation);
  Prithvi-EO-2.0 is preferable when GPU/terratorch is available — recorded as
  an upgrade path, and the FM is a pluggable component per requirement §15.
- **Medicine survey depth:** *Assumption:* focused additions (~10–20 works,
  radiology report generation + evidence-integration systems), not a full
  medical-AI survey — enough to extract composition patterns per §1.
- **"Millions of cards" (§9):** answered analytically (per-field
  constructibility table + measured per-card cost in the demonstrator), not
  by constructing millions.
- **Corpus re-characterization QC:** same protocol as v1
  (`methods/qc-protocol.md`), applied to the three new axes.
