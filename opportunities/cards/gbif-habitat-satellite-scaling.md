# Spec Card: gbif-habitat-satellite-scaling

**Generating combination:** ecosystem monitoring need × open satellite imagery (H3) × GBIF occurrences + linked habitat knowledge (H11) × weak supervision with noise-aware training.

| # | Field | Value |
|---|---|---|
| 0 | Card ID / name | `gbif-habitat-satellite-scaling` — scaling species-bridged habitat supervision to global satellite imagery |
| 1 | Application need | Ecosystem mappers and biodiversity assessors (GEO BON-class users, NASA biodiversity program) need habitat/ecosystem characterization where field surveys don't reach; EcoWikiRS proved the pattern on Swiss aerial imagery — the global satellite version is unbuilt |
| 2 | Required capability | Zero-shot ecological characterization of satellite scenes (ecosystem type, habitat properties, disturbance sensitivity) via habitat language |
| 3 | Geospatial evidence | Sentinel-2/HLS patches at GBIF occurrence coordinates, seasonally matched; global |
| 4 | Information source | GBIF occurrence records (3B+, geolocated, dated) bridging to species habitat descriptions (Wikipedia/EUNIS/trait databases) (structured-observations + scientific-knowledge); API verified this run |
| 5 | Semantic relationship | Language describes habitat properties implied by observed species presence — weak, ecologically mediated description of the scene |
| 6 | Alignment | Entity (species) + spatial (occurrence point → patch) + temporal (season) |
| 7 | Supervision generation | Weak supervision: occurrence→habitat-text join with noise-aware contrastive training (WINCEL-style); QC: filter to research-grade occurrences, measure text-relevance rate on samples |
| 8 | Scaling strategy | 3B occurrences globally (vs EcoWikiRS's regional aerial scope) → 10^7+ candidate pairs; grows daily; marginal cost ≈ imagery chipping |
| 9 | Grounding-quality risks | 10m pixels vs point occurrences (GPS + niche breadth) → patch-level claims only; observer bias toward roads/richness hotspots; habitat text partially irrelevant per image (the pattern's known noise — needs the noise model, AP-5/MP-5) |
| 10 | Negative-control plan | Zero-shot EUNIS-class accuracy vs label-only baseline (does habitat language beat class names?); geographic-holdout evaluation to catch shortcut learning |
| 11 | VLM adaptation family | Contrastive with weighted/noise-aware objectives |
| 12 | Application evaluation | Ecosystem-map agreement with authoritative national/EUNIS maps in held-out regions; target maturity: domain-research → workflow-relevant (ecosystem accounting) |
| 13 | Novelty assessment | data 2 (extends corpus EcoWikiRS from regional aerial to global satellite + full GBIF), task 1, science 2, application 2 |
| 14 | Feasibility notes | Open APIs; licensing mix (some records CC-BY-NC) needs per-record filtering; compute for global chipping is the main cost |
| 15 | Metapattern lineage | MP-5 (knowledge-bridged weak pairing), scale-out variant of EcoWikiRS ([2504.19742](https://arxiv.org/abs/2504.19742)) |
