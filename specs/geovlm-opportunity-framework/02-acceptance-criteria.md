Status: Approved

# Acceptance Criteria: GeoVLM Data–Language Opportunity Framework

Criteria are grouped by the six deliverables (D1–D6) defined in the approved [01-spec.md](01-spec.md). Each criterion is an observable condition that can be checked against an artifact in this repo.

## Criteria

### D1 — GeoVLM landscape survey
- [ ] A survey corpus exists as a structured dataset (one record per surveyed work) with a documented schema, not free-form prose.
- [ ] Every record carries at minimum: identifier (arXiv ID or DOI), title, year, venue/source, and at least one domain tag from the defined domain list (Earth observation, agriculture, disasters, urban systems, mapping, infrastructure, defense/intelligence).
- [ ] The corpus inclusion rules (time window, source boundary, in/out criteria) are written down in a methods note, and every record satisfies them; works added from outside arXiv are flagged by source.
- [ ] All seven named domains are represented in the corpus, or a written justification exists for any domain with zero entries.

### D2 — Supervision-construction characterization
- [ ] Every corpus record is characterized on all six axes: geospatial data type, language source/type, semantic relationship, alignment basis (spatial/temporal/entity/event), pair-generation method, and scalability assessment — each drawn from a controlled vocabulary defined in the schema.
- [ ] The language-source vocabulary distinguishes at least the six spec-named categories: labels-converted-to-language, structured observations, expert interpretations, scientific knowledge, reports, decision/workflow information.
- [ ] The pair-generation vocabulary distinguishes at least the six spec-named mechanisms: deterministic generation, templates, combinatorial construction, LLM-assisted synthesis, weak supervision, knowledge-based generation.
- [ ] Fields that could not be determined from the paper are marked with an explicit `unknown` value rather than left blank or guessed.
- [ ] A documented quality-control pass exists: a stated sample fraction of LLM-assisted extractions was human-verified, with the observed error rate recorded.

### D3 — Capability, use, maturity, and novelty assessment
- [ ] Every record states the capability created by the pairing in its own field, distinct from the nominal ML task field (VQA/captioning/retrieval/classification/etc.).
- [ ] Every record states the scientific or operational use enabled, or explicitly `none identified`.
- [ ] Every record is placed on the six-step maturity ladder defined in the Spec (benchmark research → deployed application), using written level definitions.
- [ ] Every record carries four novelty scores (data, task, science, application) on a defined scale with written scoring rubrics.
- [ ] At least 5 negative cases are documented, each with the pattern that limited its value stated as a reusable anti-pattern.

### D4 — Metapatterns + Spec Card
- [ ] At least 5 distinct metapatterns are documented, each instantiating the full ten-element chain from the Spec (application need → … → application evaluation) with no element skipped.
- [ ] Every metapattern cites ≥ 2 corpus records as evidence it recurs (a pattern with one instance is not "recurring").
- [ ] A GeoData–Language Pair Spec Card template exists as a standalone document, is model-independent (no field requires naming a specific VLM), and every field has a definition and a worked example.
- [ ] The Spec Card is validated by back-filling it for at least 2 existing published datasets from the corpus without needing fields not in the template.

### D5 — Opportunity discovery
- [ ] A documented inventory of searched information holdings exists (NASA and related Earth-science ecosystems), listing each holding examined and the geodata/language assets it contains.
- [ ] At least 10 candidate opportunities are generated, each expressed as a filled Spec Card.
- [ ] Each candidate identifies authoritative information that exists today but has not been used as multimodal supervision, with a citation or link to the actual holding (no hypothetical data sources).
- [ ] Each candidate documents which combination generated it: application need × geospatial observation × information source × alignment/pair-generation mechanism.

### D6 — Prioritization and demonstration selection
- [ ] Every candidate is scored on all seven Spec-named dimensions (application value, scientific relevance, novelty, scalability, data availability, grounding quality, construction feasibility) using written rubrics, and the scores are recorded in a comparable table.
- [ ] 2–4 candidates are selected for demonstration, each with a written rationale referencing its scores.
- [ ] For each selected candidate, a demonstration exists: a small constructed sample of geodata–language pairs (target ≥ 100 pairs, or a written justification if the data grain makes that infeasible) produced by the mechanism named in its Spec Card.
- [ ] Each demonstration sample includes a grounding-quality check: a stated fraction of pairs manually inspected, with the pass rate recorded.

### Cross-cutting
- [ ] Any analysis code produced ships with tests, and the test suite passes at time of delivery.
- [ ] Every quantitative claim in summary artifacts (counts, distributions, scores) is reproducible from the structured dataset by re-running the analysis code.

## Out of scope for verification

Success explicitly does **not** require:
- Any VLM being trained or fine-tuned, or any model-performance numbers.
- Demonstration datasets at production scale, or production ETL pipelines.
- Exhaustive coverage of all GeoVLM literature — coverage is bounded by the documented inclusion rules, not completeness.
- A drafted paper or publication-ready prose.
- The selected candidates being funded, approved, or adopted by any external stakeholder.
