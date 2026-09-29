Status: Draft (execution pre-authorized by Rahul in-session, 2026-09-29; executed in the same session)

# Tasks: Structured Science Evidence Cards (v2)

Context: approved-for-execution `01-spec.md` (O1–O10), `02-acceptance-criteria.md`, `03-plan.md`. Repo: `Projects/vlm-idea/`.

## Task 1: v2 vocabularies + corpus extension (O1)
- Files: `methods/schema-v2.md`, `analysis/collect_corpus.py` (round-4 queries), `analysis/curate_corpus.py`, `data/corpus/*`, `data/corpus/collection-log.md`
- Change: define `evidence_to_lm` (observed | derived-deterministic | ai-inferred | learned-representation | external-contextual), `fm_role` (9 values + none | unknown), `reasoning_ops` (10 values + unknown). Add live arXiv queries for radiology/medical report generation, scientific agents, FM-embedding+LLM systems; screen ≥10 keeps under extended inclusion rules (rule change: geospatial restriction lifted for the science-data→language pattern class, logged).
- Done when: corpus ≥69 records, tests green, log updated.

## Task 2: Re-characterize all records on new axes (O1)
- Files: `data/characterization/records-v2.json`, `data/characterization/qc-report.md` (appended), `analysis/corpus_stats.py`, `tests/test_landscape_v2.py`
- Change: every corpus id gets the three new axes (+ v1 axes for new works, in `records.json`); QC protocol on new axes (seeded ≥20% sample, error rate recorded, re-pass rule); stats script tallies the new axes.
- Done when: 1:1 id coverage, vocab-validated by tests, QC appended.

## Task 3: Science Card spec + schema + validator (O3)
- Files: `methods/science-card-spec.md`, `schema/science_card.schema.json`, `tests/test_science_cards.py` (validator part)
- Change: evidence-entry object `{value, class, source, method, provenance, uncertainty}`; card sections per requirements §4; temporal modes per §5; no model names as field names.
- Done when: schema validates a hand-built example card in tests.

## Task 4: Demonstrator — sites and chips (O8)
- Files: `demonstrator/sites.py`, `demonstrator/fetch_chips.py`, `demonstrator/out/chips_meta.json`
- Change: ≥12 EONET wildfire events (2024–2026) + ≥12 offset controls; Earth Search STAC per site: lowest-cloud Sentinel-2 L2A scene ≥30d before and 10–90d after event date; windowed 224×224 reads of B02/B03/B04/B8A/B11/B12 (+SCL cloud screen) → `chips.npz` (git-ignored raw) + committed metadata.
- Done when: ≥10 event + ≥10 control sites with clean before/after chips.

## Task 5: Demonstrator — deterministic + FM evidence (O8)
- Files: `demonstrator/evidence.py`, `demonstrator/prithvi_embed.py`, `demonstrator/out/evidence.json`
- Change: NDVI/NBR means, ΔNDVI/ΔNBR, band statistics per chip; download Prithvi-EO-1.0-100M (`prithvi_mae.py` + `Prithvi_EO_V1_100M.pt`, Apache-2.0, ~400MB — recorded in README); encoder embeddings per chip, cosine representation-change per site, cross-site nearest neighbors.
- Done when: evidence.json holds all quantities for every site with provenance stubs.

## Task 6: Demonstrator — cards, language, questions, counterfactuals (O5, O6, O8)
- Files: `demonstrator/build_cards.py`, `demonstrator/generate_language.py`, `demonstrator/out/cards/*.json`, `demonstrator/out/language/products.json`
- Change: assemble schema-valid cards (event context from EONET for event sites; absence recorded for controls); ≥6 traced+tagged language product types; evidence-state question rules; ≥2 counterfactual/abstention constructions (context-conflict, cloud/insufficient-evidence).
- Done when: all cards validate; ≥100 products, every sentence traced; question logic test passes.

## Task 7: Ablation (O9)
- Files: `demonstrator/ablation.py`, `demonstrator/out/ablation.json`
- Change: event-vs-control separation (rank-based AUC) for tiers: raw band-stat delta proxy / Δ-indices / Prithvi Δ-representation / combined; misclassification lists.
- Done when: ablation.json committed; numbers quoted only from it.

## Task 8: Pattern + taxonomy + catalog + agenda documents (O2, O4, O7, O10)
- Files: `patterns/evidence-composition-metapatterns.md`, `patterns/fm-contribution-taxonomy.md`, `opportunities/catalog-v2.md`, `patterns/research-agenda.md`
- Change: ≥5 composition metapatterns (13-element chain, ≥2 citations each); FM taxonomy citing corpus + ablation, ≥3 deterministic-preferable cases; ≥6 text-does-not-exist catalog entries with §18 rubric mapping; ≥5 agenda directions tied to evidence.
- Done when: all counts met with real citations.

## Task 9: QC, tests, verification, report
- Files: `tests/*`, `data/demos-v2 QC in language products`, updated `reports/geovlm-summary-report.html` (same artifact URL)
- Change: seeded grounding QC on generated language (≥20 sampled, manual review, pass rate recorded in demonstrator README); run full suite; AC-by-AC check; republish report with a v2 section; commit everything.
- Done when: full suite green; AC checklist reported to Rahul.
