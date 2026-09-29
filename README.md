# vlm-idea — GeoVLM Data–Language Opportunity Framework

A research framework for systematically discovering **novel geodata–language
supervision opportunities** for geospatial vision-language models (GeoVLMs):
survey the literature, characterize how geodata–language pairs get built,
abstract the recurring construction strategies into metapatterns, then apply
those patterns to NASA / Earth-science information holdings to generate and
prioritize new, grounded dataset opportunities.

Requirements of record: [resources/research-requirements.txt](resources/research-requirements.txt)
Spec artifacts (spec-driven): [specs/geovlm-opportunity-framework/](specs/geovlm-opportunity-framework/)

## Layout

| Path | Contents |
|---|---|
| `methods/` | Inclusion rules, record schema + controlled vocabularies, maturity ladder, QC protocol |
| `data/corpus/` | D1 survey corpus (`papers.json`, collection log) |
| `data/characterization/` | D2/D3 characterized records + QC report |
| `data/demos/` | D6 demonstration pair samples (one dir per selected candidate) |
| `patterns/` | Metapatterns, anti-patterns, GeoData–Language Pair Spec Card template |
| `opportunities/` | Holdings inventory + candidate opportunity cards |
| `prioritization/` | Scoring rubrics, score table, selection rationale |
| `analysis/` | Scripts that generate every quantitative claim (reproducible) |
| `tests/` | pytest suite validating schemas, cards, and reproducibility |

## Reproduce

```bash
python3 -m pytest            # validate all data artifacts against their schemas
python3 analysis/score_table.py   # regenerate the prioritization table
```

Python ≥ 3.10. Corpus collection reuses the deterministic collector in
`Projects/python_landscape_analysis` (`python -m landscape collect`) plus
arXiv-verified lookups; every cited paper resolves to a real arXiv record
retrieved at collection time — nothing is memory-cited.
