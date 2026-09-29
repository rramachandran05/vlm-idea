Status: Draft
Execution note: Rahul pre-authorized implementation in-session on 2026-09-29 ("Implement and run"); these tasks are being executed in the same session that drafted them. The file remains valid as a standalone brief for a fresh Claude Code session if any task needs re-running.

# Tasks: GeoVLM Data–Language Opportunity Framework

Repo: `Projects/vlm-idea/`. All paths relative to repo root. Approved context: `specs/geovlm-opportunity-framework/01-spec.md` (deliverables D1–D6), `02-acceptance-criteria.md` (AC), `03-plan.md` (layout, reuse decisions).

## Task 1: Bootstrap the repo
- Files: `.gitignore`, `README.md`, `CLAUDE.md`, `pyproject.toml`; `git init`
- Change: Initialize git. Write `.gitignore` excluding `.landscape-cache/`, `private/`, `daily-notes/`, `*.local.md`, `.DS_Store`, `__pycache__/`, `*.egg-info/`, raw data dumps (`data/**/raw/`). Write `README.md` (project purpose: framework for discovering novel geodata–language supervision opportunities; how to run tests and reproduce analysis). Write `CLAUDE.md` (project conventions: Python ≥3.10, pytest, numbers only from `analysis/` scripts, `unknown` ≠ blank ≠ zero, never memory-cite a paper). Write `pyproject.toml` modeled on `Projects/python_landscape_analysis/pyproject.toml`: package name `geovlm-framework`, deps `requests`, dev-dep `pytest`, `testpaths = ["tests"]`.
- Done when: `git log` shows an initial commit containing these four files; `python3 -m pytest` runs (collects 0 tests, exits cleanly).

## Task 2: Write D1 methods docs
- Files: `methods/inclusion-rules.md`, `methods/schema.md` (D1 section)
- Change: Inclusion rules per approved Spec: window 2021-01→2026-09, arXiv-primary (non-arXiv opportunistic, flagged by `source`), in-scope = models/datasets/benchmarks pairing geospatial data with natural language (GeoVLMs, EO captioning/VQA/retrieval/grounding, geo instruction-tuning, geodata–text datasets); out-of-scope = pure-vision geo foundation models, generic VLMs with no geospatial component, geo-LLMs with no visual/observational modality (note as adjacent). Domain tags (≥1 per record): earth-observation-general, agriculture, disasters, urban, mapping, infrastructure, defense-intelligence. Schema D1 fields: `id`, `source` (arxiv|other:<name>), `title`, `year`, `month`, `venue`, `domains[]`, `url`.
- Done when: both files exist; every rule in them is checkable against a record (no vague criteria).

## Task 3: Collect and screen the corpus (D1)
- Files: `data/corpus/papers.json`, `data/corpus/collection-log.md`
- Change: Retrieve candidates via (a) the arXiv MCP (`arXivPaper` server: search + paper-info; verify every kept ID via paper-info lookup) using GeoVLM query set (remote sensing vision-language, EO captioning/VQA, satellite image-text, geospatial instruction tuning, per-domain queries for the seven domains) and (b) if sandbox network allows, `python -m landscape collect` from `Projects/python_landscape_analysis` with the same queries, `--base-dir data/corpus/`. Merge, dedupe by arXiv ID, screen against `methods/inclusion-rules.md`, tag domains. Target a focused corpus (~40–60 kept works: seminal + representative per domain, per the geoai skill's focused-corpus pattern). Log queries run, counts retrieved/kept/dropped in `collection-log.md`. Never memory-cite: every record must come from a live lookup this run.
- Done when: `papers.json` has ≥40 records, all with required D1 fields; all seven domains represented or justified absent in `collection-log.md`.

## Task 4: D1 schema test
- Files: `tests/test_corpus_schema.py`
- Change: pytest validating every `papers.json` record: required fields present and non-empty, `year` ∈ [2021, 2026], `domains` ⊆ the seven-tag list, `source` well-formed, IDs unique.
- Done when: `python3 -m pytest tests/test_corpus_schema.py` passes against the real corpus.

## Task 5: Write D2/D3 vocabularies and rubrics
- Files: `methods/schema.md` (D2/D3 sections), `methods/maturity-ladder.md`, `methods/qc-protocol.md`
- Change: Controlled vocabularies — language-source (labels-as-language | structured-observations | expert-interpretation | scientific-knowledge | reports | decision-workflow), pair-generation (deterministic | template | combinatorial | llm-synthesis | weak-supervision | knowledge-based), alignment (spatial | temporal | entity | event; multi allowed), geodata-type (open list, normalized). D3 fields: `nominal_task`, `capability` (free text, must differ from nominal task), `use_enabled` (or `none identified`), `maturity` (6 levels, each defined by an observable test in maturity-ladder.md), `novelty` scores 0–3 × 4 dimensions with rubric anchors, `negative_case` (bool + reason). Every enum includes `unknown`. QC protocol: verify ≥20% random sample of characterized records against source abstracts; record error rate; re-pass axis if >10% wrong.
- Done when: all three files exist; every vocabulary value has a one-line definition; rubric anchors given for every novelty level.

## Task 6: Characterize the corpus (D2 + D3)
- Files: `data/characterization/records.json`, `data/characterization/qc-report.md`
- Change: For every corpus record, read its verified abstract (paper-info lookup) and fill all D2/D3 fields per `methods/schema.md`. `unknown` where the abstract doesn't say — never guess. Run the QC protocol; write `qc-report.md` (sample size, errors found, error rate, re-passes).
- Done when: every corpus ID has a characterization record; `tests/test_characterization.py` (Task 7) passes; qc-report.md records an error rate.

## Task 7: D2/D3 characterization test
- Files: `tests/test_characterization.py`
- Change: pytest validating: 1:1 ID match with corpus; all D2/D3 fields present; enum values within vocabularies; `capability` ≠ `nominal_task` string; `unknown` explicit (no null/blank).
- Done when: passes against real `records.json`.

## Task 8: Negative cases → anti-patterns (D3)
- Files: `patterns/anti-patterns.md`
- Change: From records flagged `negative_case`, document ≥5 anti-patterns: what was built, why value was limited, the reusable "don't replicate" rule. Cite corpus IDs.
- Done when: ≥5 anti-patterns, each citing ≥1 corpus record.

## Task 9: Metapatterns (D4)
- Files: `patterns/metapatterns.md`
- Change: Abstract ≥5 recurring data-construction strategies, each instantiating the full ten-element chain (application need → required capability → geospatial evidence → information source → semantic relationship → alignment → supervision generation → scaling strategy → VLM adaptation → application evaluation), each citing ≥2 corpus records as evidence of recurrence.
- Done when: ≥5 patterns × 10 elements × ≥2 citations, no element skipped.

## Task 10: Spec Card template + back-fill validation (D4)
- Files: `patterns/spec-card-template.md`
- Change: Model-independent GeoData–Language Pair Spec Card: every field defined with a worked example; no field names a specific VLM. Validate by back-filling 2 published datasets from the corpus; include both back-fills in the file; note any field gaps found and fix the template.
- Done when: template + 2 complete back-fills exist using only template fields.

## Task 11: Holdings inventory (D5)
- Files: `opportunities/holdings-inventory.md`
- Change: Inventory NASA and related Earth-science information holdings actually examined this run (live lookup or verified documentation — no hypothetical sources): candidate ecosystems include NASA CMR/Earthdata collection metadata, EONET, GIBS/Worldview, DAAC user guides and ATBDs, GLOBE observations, USGS/NOAA feeds. For each: geodata assets, language/information assets, access path, license/availability note.
- Done when: every listed holding has all four attributes and was actually examined (link or retrieval noted).

## Task 12: Generate candidate opportunity cards (D5)
- Files: `opportunities/cards/<slug>.md` × ≥10
- Change: Systematically cross metapatterns × holdings × the seven application domains; keep ≥10 viable candidates; fill a complete Spec Card for each; each card names its generating combination (need × observation × information source × mechanism) and cites the real holding.
- Done when: ≥10 cards, every template field filled, no hypothetical sources; `tests/test_spec_cards.py` (Task 13) passes.

## Task 13: Spec-card test
- Files: `tests/test_spec_cards.py`
- Change: pytest validating every file in `opportunities/cards/`: all template sections present, generating-combination line present, ≥10 cards total.
- Done when: passes against the real cards.

## Task 14: Score, prioritize, select (D6)
- Files: `prioritization/scoring.md`, `analysis/score_table.py`
- Change: Rubrics (0–3) for the seven dimensions (application value, scientific relevance, novelty, scalability, data availability, grounding quality, construction feasibility). Score every card; generate the comparison table with `analysis/score_table.py` from a structured scores file (not hand-typed); select 2–4 with written rationale referencing scores.
- Done when: table regenerates from data via the script; 2–4 selections with rationale.

## Task 15: Demonstration samples (D6)
- Files: `data/demos/<candidate>/pairs.json`, `data/demos/<candidate>/README.md`, `analysis/build_demo_<candidate>.py`
- Change: For each selected candidate, construct ≥100 geodata–language pairs by the mechanism named in its card, using the real holding (geodata side may be authoritative references — granule IDs, tile URLs, bboxes, timestamps — rather than downloaded rasters; state this in the README). Deterministic/template generation must be a runnable script. Grounding QC: manually inspect ≥20 pairs per candidate; record pass rate in README. If ≥100 is infeasible for a candidate's data grain or access, write the justification in its README (AC escape hatch).
- Done when: each selected candidate has pairs.json + generating script + README with QC pass rate (or written justification).

## Task 16: Reproducibility test + final verification
- Files: `tests/test_analysis_repro.py`
- Change: pytest that reruns `analysis/` scripts and asserts outputs match committed artifacts. Then run the full suite, check every AC checkbox in `02-acceptance-criteria.md` against the artifacts, and commit.
- Done when: `python3 -m pytest` fully passes; an AC-by-AC verification summary is reported to Rahul.
