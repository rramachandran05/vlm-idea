Status: Approved (completed; superseded for new work by `specs/science-evidence-cards/` — the v2 reframe per `resources/research-requirements-updated.txt`)

# Spec: GeoVLM Data–Language Opportunity Framework

## What this feature should do

Produce a systematic research framework — with concrete, reviewable artifacts — that moves from a survey of the current GeoVLM (geospatial vision-language model) literature to a prioritized, demonstrable set of novel geodata–language dataset opportunities. The work decomposes into six sequential deliverables:

### D1. GeoVLM landscape survey
A structured survey of current GeoVLM work (arXiv holdings) across Earth observation and adjacent geospatial domains: agriculture, disasters, urban systems, mapping, infrastructure, and defense/intelligence. Each surveyed work is captured as a structured record, not free-form prose.

### D2. Supervision-construction characterization
For every surveyed work, characterize how geodata–language supervision was constructed along these axes:
- **Geospatial data type** used (sensor, modality, resolution class).
- **Language source and type** — distinguishing labels-converted-to-language, structured observations, expert interpretations, scientific knowledge, reports, and decision/workflow information.
- **Semantic relationship** between the geodata and the language.
- **Alignment basis** — spatial, temporal, entity, or event.
- **Pair-generation method** — deterministic generation, templates, combinatorial construction, LLM-assisted synthesis, weak supervision, or knowledge-based generation.
- **Scalability assessment** of the construction approach, especially where it exploits existing authoritative information.

### D3. Capability, use, maturity, and novelty assessment
For each surveyed work:
- Identify the **capability created** by the geodata–language pairing (beyond the nominal ML task of VQA / captioning / retrieval / classification).
- Identify the **scientific or operational use enabled**, with emphasis on decision-support prototypes and operational applications.
- Rate **application maturity** on a defined ladder: benchmark research → domain research → workflow-relevant system → decision-support prototype → operational prototype → deployed application.
- Score **four novelty dimensions**: data, task, science, application.
- Capture **negative cases** — novel datasets or VLM methods that produced limited scientific/operational value — and the anti-patterns they reveal.

### D4. Metapattern abstraction + Spec Card
- Abstract recurring data-construction strategies into reusable **metapatterns** of the form:
  *Application need → required capability → geospatial evidence → information source → semantic relationship → alignment → supervision generation → scaling strategy → VLM adaptation → application evaluation.*
- Develop a model-independent **GeoData–Language Pair Spec Card** — a formal template for describing any candidate multimodal supervision opportunity.

### D5. Opportunity discovery
- Apply the literature-derived metapatterns to search existing geospatial and Earth-science information holdings for previously unexploited geodata–language relationships — especially authoritative information within NASA and related Earth-science ecosystems that has not yet been transformed into multimodal supervision.
- Generate candidate GeoVLM research opportunities by systematically combining: real-world application needs × available geospatial observations × available scientific/operational information sources × scalable alignment and pair-generation mechanisms.
- Each candidate is expressed as a filled-in Spec Card (from D4).

### D6. Prioritization and demonstration selection
- Score all candidates on: application value, scientific relevance, novelty, scalability, data availability, grounding quality, and dataset-construction feasibility.
- Select a small number (assumed 2–4; see Open questions) of high-value candidates for demonstration — showing the framework can produce novel, grounded, application-driven geodata–language datasets and VLM capabilities.

## Why

GeoVLM research today is largely dataset-and-benchmark driven: pairings are built from whatever language is easy to attach to imagery, and the resulting capabilities often have unclear scientific or operational value. Meanwhile, large stores of authoritative Earth-science information (NASA and related ecosystems) already encode expert interpretation, scientific knowledge, and decision/workflow information that has never been exploited as multimodal supervision. A systematic framework — literature-derived patterns, a formal spec card, and a combinatorial opportunity search — turns "what dataset could we build?" from an ad-hoc guess into a repeatable, prioritized pipeline, and steers effort toward capabilities with demonstrable application value.

## Out of scope

- **Training or fine-tuning any VLM.** The demonstration phase (D6) shows that candidate datasets *can* be constructed and are well-grounded; model training is a follow-on effort.
- **Building production data pipelines** for the selected candidates — the deliverable is spec cards plus demonstration-scale evidence, not operational ETL.
- **A comprehensive survey of general (non-geospatial) VLM literature.** Adjacent-domain work enters only where it informs geodata–language supervision construction.
- **Novel VLM architecture research.** The framework is model-independent by design (D4).
- **Publication/paper writing.** The artifacts here feed a paper, but drafting one is a separate effort (a `write_paper` skill exists in Operations-Work for that step).

## Open questions / TBD

- **Survey corpus boundary:** arXiv is named as the primary holding. Include peer-reviewed venues not on arXiv (e.g., RSE, TGRS) opportunistically, or arXiv-only for reproducibility? *Assumed: arXiv-primary with opportunistic additions, flagged by source.*
- **Survey time window:** TBD — assumed roughly 2021–present (CLIP-era onward), since geospatial VLM work predating contrastive/instruction-tuned VLMs is of limited pattern value.
- **Expected corpus size:** TBD — affects whether characterization (D2/D3) is fully manual, LLM-assisted, or hybrid. Assumed hybrid: LLM-assisted extraction into the structured schema, human-spot-checked.
- **Number of demonstration candidates (D6):** "a small number" — assumed 2–4, pending Rahul's call.
- **What "demonstration" concretely means:** a filled spec card + a small constructed sample of pairs (e.g., hundreds) with grounding-quality checks? Or spec card only? *Assumed: spec card + small constructed sample.*
- **Tooling form:** are D1–D3 captured in a structured dataset (CSV/JSON + Python analysis code with tests) versus markdown tables? *Assumed: structured data + Python analysis, per Rahul's Python-with-tests preference, since the repo itself has no conventions yet.*
- **Repo state:** `Projects/vlm-idea/` is not yet a git repository. Assumed it should be initialized before implementation begins (noted for the Plan; not done under this skill).
- **Related existing work:** an Operations-Work skill `geoai_landscape_analysis` and a prior project `python_landscape_analysis` exist in this workspace and may share survey machinery. Whether to reuse them is a Plan-stage question.

## Related existing specs

None — `specs/` did not exist in this repo prior to this document.
