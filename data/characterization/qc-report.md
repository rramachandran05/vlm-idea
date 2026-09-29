# Characterization QC Report (per methods/qc-protocol.md)

Run 2026-09-29 against `records.json` (59 records, all fields characterized
from verified arXiv abstracts).

## Pass 1
- **Sample:** 12 of 59 records (20.3%), deterministic — `random.Random(42).sample(sorted(ids), 12)`:
  2507.16716, 2311.16782, 2302.09208, 2601.01416, 2407.19719, 2406.11217,
  2406.09838, 2312.12222, 2606.13148, 2311.15826, 2509.20628, 2602.20066.
- **Checked:** every D2/D3 field against the stored source abstract
  (~204 field checks).
- **Errors found: 6 fields across 4 records** → overall field-level error rate
  **~2.9%**.
- **Pattern:** every error was on the `pair_generation` axis (with a coupled
  `scalability` judgment in 2 records): a plausible mechanism was inferred
  where the abstract is silent, instead of the required `unknown`
  (2302.09208, 2601.01416, 2312.12222, 2606.13148). Axis-level error rate on
  `pair_generation`: 4/12 = **33% > 10% threshold → full re-pass required**.

## Re-pass (pair_generation axis, all 59 records)
- Re-checked the stated mechanism against each abstract; corrected **15
  records** where the mechanism was inferred rather than stated
  (silent source → `unknown`, partially-stated → stated part + `unknown`):
  2106.10548, 2302.09208, 2312.12222, 2401.17600, 2402.02544, 2410.01407,
  2410.06234, 2411.19325, 2502.08168, 2505.21089, 2601.01416, 2601.19099,
  2605.10772, 2606.13148, 2606.17246. Two coupled `scalability` values reset
  to `unknown` (2302.09208, 2401.17600, 2106.10548); demonstrated-scale
  ratings (e.g., a dataset's published pair count) were kept.
- **Fresh axis check:** 12-record sample, `random.Random(43)` —
  2306.11029, 2408.14744, 2509.21609, 2601.18493, 2312.12856, 2502.08168,
  2411.01511, 2509.01907, 2606.17246, 2311.15826, 2604.16451, 2506.00530.
  **0/12 errors** on the re-passed axis.

## Disclosure
- Final measured field-level error rate after re-pass: **2.9% pre-fix on the
  pass-1 sample; 0% on the post-fix axis re-check**. Quote "abstract-level
  characterization, sampled field error rate ~3%, pair-generation axis
  re-passed to 0% on re-check" wherever corpus statistics are presented.
- **Known limitation:** characterization is abstract-based (plus titles and
  logged metadata); full-text-only details (exact generation prompts, dataset
  licensing) are systematically `unknown` rather than guessed. The frequency
  of `unknown` is reported by the analysis scripts and is itself a finding.

## v2-axis pass (2026-09-29, per methods/schema-v2.md)
- Corpus extended to 76 records (17 new science-adjacent works, live-retrieved
  round-4 queries); new records characterized on v1+v2 axes, all 76 on v2 axes.
- **Sample:** 16 of 76 (21%), `random.Random(99).sample(sorted(ids), 16)`.
- **Checked:** all three v2 axes per sampled record against stored abstracts
  (48 axis-fields). **Errors: 0.** One definitional ambiguity surfaced
  (does `evidence_to_lm` include supervision-construction injections?) —
  resolved as *yes* and the definition clarified in `methods/schema-v2.md`;
  no values changed. No axis exceeded the 10% re-pass threshold.
