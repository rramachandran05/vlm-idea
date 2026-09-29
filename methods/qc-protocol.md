# Characterization QC Protocol (D2/D3)

Characterization is LLM-assisted (records filled from verified abstracts and,
where needed, skimmed full text). This protocol bounds its error rate.

1. **Sample:** after all records are characterized, draw a deterministic random
   sample of **≥20% of records** (seeded RNG, seed logged in the QC report so
   the sample is reproducible).
2. **Verify:** for each sampled record, re-read the source abstract/paper and
   check every D2/D3 enum field and the maturity level against the definitions
   in `schema.md` / `maturity-ladder.md`. A field is an **error** if the source
   supports a different value, or if `unknown` was used where the source states
   the answer (and vice versa: a guessed value where the source is silent).
3. **Record:** `data/characterization/qc-report.md` states sample size, seed,
   per-field error counts, and the overall field-level error rate
   (errors / fields checked).
4. **Re-pass rule:** any single field (axis) with **>10% error rate** across the
   sample triggers a full re-pass of that field over *all* records, followed by
   a fresh sample check of that field. Log each re-pass in the QC report.
5. **Disclosure:** the final error rate is quoted wherever corpus-level
   statistics are presented (analysis outputs, summary artifacts).
