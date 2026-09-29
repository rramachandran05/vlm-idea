# CLAUDE.md — vlm-idea project conventions

- **Language/tests:** Python ≥ 3.10, pytest (`testpaths = ["tests"]`). Analysis
  code ships with tests; run `python3 -m pytest` before declaring anything done.
- **Every number traces to a script.** Counts, distributions, and scores quoted
  in any artifact must be regenerable from `analysis/` scripts over the
  structured data in `data/` — never hand-computed and pasted.
- **Never memory-cite a paper.** Every arXiv ID in `data/` or `patterns/` was
  retrieved and verified via a live lookup at collection time. A model you
  "know exists" but didn't retrieve is *absent from this corpus*, not citable.
- **`unknown` ≠ blank ≠ zero.** Fields a paper doesn't report are the explicit
  string `unknown` (or `null` for numerics). The frequency of unknowns is
  itself a finding — never backfill with guesses.
- **Controlled vocabularies win.** Characterization fields take values only
  from `methods/schema.md`. Extending a vocabulary is a deliberate, logged
  schema change, not an inline improvisation.
- **No hypothetical data sources.** Opportunity cards cite only holdings
  actually examined (link/retrieval noted in `opportunities/holdings-inventory.md`).
- **Spec-driven:** substantive new features go through
  `specs/<feature-slug>/01-spec.md → 04-tasks.md` (see the
  spec_driven_development skill in Operations-Work) before implementation.
- **Don't modify sibling projects** (`python_landscape_analysis`, workspace
  skills) from here — they're consumed as-is; changes to them are separate,
  scoped requests.
