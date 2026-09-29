Status: Approved

# Plan: GeoVLM Data–Language Opportunity Framework

## Repo conventions used

Probed 2026-09-29:

- **Target repo (`Projects/vlm-idea/`):** contains only `resources/research-requirements.txt` and `specs/geovlm-opportunity-framework/`. No git init, no README/CLAUDE.md, no language or test-framework signal. → Per the spec-driven-development skill, the **default applies: Python with built-in tests (pytest)**. This plan therefore *proposes* the repo layout below rather than inheriting one.
- **No test suite found** in the target repo — nothing to sanity-run there. (Not a pre-existing-failure risk; there is simply nothing yet.)
- **Reusable asset 1 — `Projects/python_landscape_analysis/`** (read directly): a deterministic collection tool, invoked as `python -m landscape collect --theme ... --query ... --since ... --sources arxiv,github,openalex[,semanticscholar]`, writing a durable per-theme manifest. Python ≥ 3.10, sole runtime dep `requests`, pytest suite at `tests/`. **Verified this run: `python3 -m pytest tests/ -q` → 24 passed.** Its README's field-ownership rule matters here: the tool writes only objective fields; judgment fields (relevance, dimensions, clusters) are agent-owned — which maps cleanly onto our D1 (objective) vs. D2/D3 (judgment) split.
- **Reusable asset 2 — `Operations-Work/skills/geoai_landscape_analysis/`** (read directly): an arXiv-MCP-based survey skill with `context/scope_definition.md`, `context/arxiv_query_reference.md`, `context/synthesis_framework.md`, and a tested `scripts/build_landscape.py` (`--selftest`). Its guardrails (verify every ID via paper-details lookup; never memory-cite; null ≠ zero) are adopted below. Its scope (EO/weather-climate *foundation models*) is narrower than ours (GeoVLMs across seven domains), so its query set and scope definition need a GeoVLM-specific replacement, not verbatim reuse.
- **arXiv MCP availability:** this session exposes `arXivPaper` MCP tools (search, paper-info, recent-by-category, trends) — the retrieval/verification path the geoai skill requires is available.

## Proposed repo layout (all new — nothing exists yet)

```
vlm-idea/
├── README.md                  # project purpose, how to reproduce
├── CLAUDE.md                  # project-level instructions
├── .gitignore                 # excludes .landscape-cache/, private/, raw dumps
├── pyproject.toml             # package `geovlm_framework`, pytest config (modeled on python_landscape_analysis/pyproject.toml)
├── resources/                 # exists (research-requirements.txt)
├── specs/                     # exists (this folder)
├── methods/
│   ├── inclusion-rules.md     # D1: corpus boundary, window, in/out criteria
│   ├── schema.md              # D1–D3: record schema + controlled vocabularies + rubrics
│   ├── maturity-ladder.md     # D3: six-level definitions
│   └── qc-protocol.md         # D2: LLM-extraction verification protocol
├── data/
│   ├── corpus/                # D1 output: manifest + per-paper records (JSON)
│   ├── characterization/      # D2–D3 output: characterized records (JSON)
│   └── demos/                 # D6 output: constructed pair samples per candidate
├── analysis/
│   └── (analysis scripts)     # counts, distributions, score tables — every number cited traces here
├── patterns/
│   ├── metapatterns.md        # D4: ≥5 patterns, ten-element chain, ≥2 citations each
│   ├── anti-patterns.md       # D3: ≥5 negative cases
│   └── spec-card-template.md  # D4: GeoData–Language Pair Spec Card + field defs + worked example
├── opportunities/
│   ├── holdings-inventory.md  # D5: NASA / Earth-science holdings examined
│   └── cards/                 # D5: ≥10 filled spec cards (one file each)
├── prioritization/
│   └── scoring.md             # D6: rubrics, score table, selection rationale
└── tests/
    └── (pytest suite)         # schema validation, analysis reproducibility
```

## Phases

### Phase 0 — Repo bootstrap
Initialize git; add `README.md`, `CLAUDE.md`, `.gitignore`, `pyproject.toml` (modeled on `python_landscape_analysis/pyproject.toml`: setuptools, `requests`, `pytest` dev-dep, `testpaths = ["tests"]`).

### Phase 1 — D1: Corpus collection
- Write `methods/inclusion-rules.md` (window 2021→present, arXiv-primary, per approved Spec assumptions) and the D1 portion of `methods/schema.md`.
- Collect candidates two complementary ways:
  1. **Deterministic sweep:** `python -m landscape collect` from `python_landscape_analysis` with GeoVLM queries (new query set — the geoai skill's `context/arxiv_query_reference.md` is the model but targets foundation models, not VLMs), `--base-dir` pointed into `vlm-idea/data/corpus/`.
  2. **arXiv MCP search + verify:** per the geoai skill's Step 1–2 pattern; every kept record confirmed via paper-details lookup. No memory-cited papers.
- Screen candidates against inclusion rules; tag each kept record with ≥1 of the seven domain tags.
- Test: `tests/test_corpus_schema.py` — every record has id/title/year/source/domain-tag; flags non-arXiv sources (maps to AC-D1).

### Phase 2 — D2 + D3: Characterization and assessment
- Finalize `methods/schema.md` controlled vocabularies (6 language-source categories, 6 pair-generation mechanisms, 4 alignment bases, maturity ladder, 4 novelty rubrics) and `methods/maturity-ladder.md`, `methods/qc-protocol.md`.
- Characterize every record on all D2/D3 fields (LLM-assisted reading of abstracts/papers, `unknown` for undeterminable — adopting the geoai skill's "null means unknown, never guess" guardrail).
- QC pass per protocol: human-verify a stated sample; record error rate (maps to AC-D2).
- Identify ≥5 negative cases → `patterns/anti-patterns.md`.
- Tests: `tests/test_characterization.py` — all fields present, values ∈ vocabularies, `unknown` explicit (maps to AC-D2/D3).

### Phase 3 — D4: Metapatterns + Spec Card
- Abstract ≥5 recurring metapatterns (full ten-element chain, ≥2 corpus citations each) → `patterns/metapatterns.md`.
- Draft `patterns/spec-card-template.md`; validate by back-filling ≥2 published datasets from the corpus (maps to AC-D4).

### Phase 4 — D5: Opportunity discovery
- Build `opportunities/holdings-inventory.md` — NASA and related Earth-science holdings examined. Candidate starting points are TBD until examined in-phase (no holding is cited in a card without being checked); the geoai skill's NASA-data list in `context/scope_definition.md` is a seed reference.
- Generate ≥10 candidates via metapattern × holdings combinations; one filled spec card each → `opportunities/cards/` (maps to AC-D5).

### Phase 5 — D6: Prioritization + demonstration
- Write scoring rubrics; score all candidates on the 7 dimensions; select 2–4 → `prioritization/scoring.md`.
- For each selected candidate, construct a demonstration sample (target ≥100 pairs) into `data/demos/<candidate>/`, with a grounding-quality inspection recorded (maps to AC-D6).
- Test: `tests/test_analysis_repro.py` — summary counts/scores regenerate identically from the structured data (maps to AC cross-cutting).

## Files/components to change

Everything below is **new** except the first row; "traced to" cites what was actually read.

- `resources/research-requirements.txt` — unchanged; source of record for scope (read this session).
- `README.md`, `CLAUDE.md`, `.gitignore`, `pyproject.toml` — bootstrap (pyproject modeled on `python_landscape_analysis/pyproject.toml`, read this session).
- `methods/*.md` (4 files) — traced to AC-D1/D2/D3 requirements in approved `02-acceptance-criteria.md`.
- `data/corpus/` manifest — produced by `python -m landscape collect` (CLI contract read from `python_landscape_analysis/README.md`) plus arXiv-MCP verification (pattern read from `geoai_landscape_analysis/SKILL.md` Steps 1–2).
- `data/characterization/`, `patterns/*.md` (3 files), `opportunities/*`, `prioritization/scoring.md`, `data/demos/` — traced to Spec deliverables D2–D6 and their AC sections.
- **No modifications to `python_landscape_analysis` or the geoai skill** — both are consumed as-is; if the collector needs a change (e.g., a query feature), that is a separate scoped request, per workspace scope discipline.

## Tests to add/update

All new, pytest, under `vlm-idea/tests/`:

- `tests/test_corpus_schema.py` — AC-D1: required fields present, domain tags from defined list, non-arXiv flagged, inclusion-window respected.
- `tests/test_characterization.py` — AC-D2/D3: all six D2 axes + capability/use/maturity/novelty fields present; values within controlled vocabularies; `unknown` explicit, never blank.
- `tests/test_spec_cards.py` — AC-D4/D5: every card in `opportunities/cards/` contains every template field; ≥10 cards; each names its generating combination.
- `tests/test_analysis_repro.py` — AC cross-cutting: rerunning analysis scripts reproduces the committed summary numbers byte-for-byte (or within stated tolerance).

## Risks

- **Network dependence:** corpus collection needs live arXiv access (the collector uses `requests`; the MCP path is session-dependent). The geoai skill notes the bash sandbox may lack network — if so in the implementation session, collection must run via the arXiv MCP tools only, and the deterministic-sweep step degrades to MCP-only. Flagged so the Tasks file can carry both paths.
- **LLM-assisted characterization quality:** mitigated by the QC protocol + recorded error rate (AC-D2), but the error rate itself may force a re-pass; budget for it.
- **D5 holdings inventory is open-ended research**, not file-traceable work; the plan bounds it via the "no hypothetical sources" AC rather than by enumerating holdings now.
- **Repo not yet under git** — Phase 0 fixes this before any data lands; until then nothing is version-controlled.
