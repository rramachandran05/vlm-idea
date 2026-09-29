# Corpus Inclusion Rules (D1)

Governs what enters `data/corpus/papers.json`. Every kept record satisfies all
of these; every drop is attributable to one of them.

## Window
- Published (arXiv v1 date) **2021-01-01 through 2026-09-29** (collection date).

## Sources
- **Primary: arXiv.** Retrieved via live arXiv API / arXiv MCP query this run;
  every kept ID verified by a per-paper metadata lookup.
- **Opportunistic non-arXiv** (journal/venue-only work) allowed when load-bearing
  for a domain, flagged `source: other:<venue>` — never memory-cited; must be
  verified against a resolvable DOI/URL at collection time.

## In scope
A work is in scope if it pairs **geospatial observational data** with **natural
language** in any of these forms:
1. GeoVLM models (remote-sensing / EO vision-language models, geospatial
   multimodal LLMs with an observational modality);
2. Geodata–language **datasets or benchmarks** (EO captioning, VQA, retrieval,
   visual grounding, change description, instruction-tuning corpora);
3. **Supervision-construction methods** for geodata–language pairs (template,
   LLM-assisted, weak supervision, knowledge-based), even if the model is generic;
4. **Applied systems** using vision-language pairing on geospatial data in the
   seven domains below, including decision-support and operational prototypes.

"Geospatial observational data" includes satellite/aerial imagery, SAR,
hyperspectral, weather/climate fields, street-level geo-imagery, and derived
geospatial rasters/vectors when paired at a geographic location.

## Out of scope (drop; note as adjacent if informative)
- Pure-vision geospatial foundation models with **no language pairing**.
- Generic VLM work with **no geospatial component** or evaluation.
- Geo-LLMs over text/coordinates only (**no observational modality**).
- Robotics/indoor VQA, medical imaging, generic scene understanding.
- Pure NLP over Earth-science literature without paired geodata.

## Domain tags (each record gets ≥1)
`earth-observation-general` | `agriculture` | `disasters` | `urban` | `mapping`
| `infrastructure` | `defense-intelligence`

`earth-observation-general` covers cross-domain EO work (generic RS captioning/
VQA/retrieval) not specific to one application domain.

## Corpus size target
Focused corpus: **~40–60 kept works** — seminal + representative per domain,
not exhaustive. Coverage claims are bounded by these rules and the logged
queries in `data/corpus/collection-log.md`, not by completeness.
