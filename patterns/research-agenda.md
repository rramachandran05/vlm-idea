# Research Agenda (O10)

Where the structured-evidence architecture creates genuinely new scientific or
operational capability — versus producing another image-caption/VQA dataset.
Each direction is tied to evidence from O1–O9 and names its fastest-path
demonstration.

## RA-1 — The reasoning-operation frontier: discriminate, hypothesize, abstain
**Evidence:** the corpus trains `describe` in 46/76 systems but `discriminate`
in 2, `test-hypotheses` in 2, `retrieve-analogs` in 1; the demonstrator's
question generator produced discrimination/attribution questions for every
changed-event card and abstention questions for every insufficiency —
automatically, from evidence state.
**New capability:** supervision that teaches evidence weighting and rejection,
not description (requirements §12's list: uncertainty, discrimination,
evidence weighting, rejection, abstention).
**Fastest path:** catalog C8 (counterfactual curriculum builder) — mine
FM-similar / cause-different site pairs (fire vs harvest vs drought NDVI
declines) at scale; every pair is a discrimination or abstention example with
deterministic ground truth.

## RA-2 — Representation-trajectory science, honestly evaluated
**Evidence:** the ablation shows the naive FM configuration (single-frame,
mean-pooled) *loses* to ΔNBR for burn detection (0.54 vs 0.63 AUC) while
being the only source of analogs. The FM's temporal-change role is untested
in the literature (0/76 records).
**New capability:** if Prithvi trajectories over true HLS time series carry
state information beyond climatology (catalog C2), that is a new observable;
if they don't, that is a decision-relevant null result NASA should have.
**Fastest path:** re-run the demonstrator's ablation with Prithvi-EO-2.0 on
3-frame sequences against a climatology baseline — the harness already
exists (`demonstrator/ablation.py`).

## RA-3 — Evidence-composition transfer from medicine to Earth science
**Evidence:** medicine already runs the full composition — MAIRA-2 (grounded
context-conditioned reports), MMRad-22K (structured multimodal evidence units
beat text-only and box-only evidence), RetiBridge (quantified biomarkers →
sub-inferences → conclusions), MEETI (four synchronized evidence classes).
Earth science has no equivalent of any of these.
**New capability:** the EO "structured findings" dataset — cards as the EO
analog of structured radiology reporting, with region-grounded findings and
report targets.
**Fastest path:** extend the demonstrator's cards with per-region (not
chip-mean) evidence and generate structured disturbance reports; MMRad-22K's
evidence-format ablation is the evaluation template.

## RA-4 — Text-does-not-exist supervision as NASA's comparative advantage
**Evidence:** v1 found the strong pairings harvest *existing* expert text;
v2's inventory shows the far larger asset is authoritative evidence with **no
text at all** (CMR variables, derived products, event catalogs, model runs).
The demonstrator generated 240 grounded language products from holdings that
contained zero captions — at ~zero marginal human cost (measured per-card
cost in `demonstrator/README.md`).
**New capability:** supervision volume decoupled from annotation budgets and
from web-text licensing, with provenance NASA controls end-to-end.
**Fastest path:** archive back-fill of catalog C1 (the demonstrated
disturbance-explanation pipeline) across EONET history → 10⁵-card scale,
then a fine-tuning pilot evaluating the §13 capability question.

## RA-5 — The card as an auditability standard, not just a data format
**Evidence:** every generated statement in the demonstrator carries a trace
to evidence fields and an epistemic tag (evidence-supported /
derived-interpretation / hypothesis / retrieved-knowledge) — enforced by
tests; the QC found 0 numeric grounding mismatches in the sampled products.
The corpus shows the counterpart risk: LLM-generated language is the single
most common language source (30+/76) usually *without* hallucination control
(AP-5).
**New capability:** scientific generation whose sentences are machine-checkable
against their evidence — a prerequisite for any operational adoption (v1's
maturity-cliff lesson) and for AI-scientist claims to be verifiable
([2410.05080](https://arxiv.org/abs/2410.05080)'s critique).
**Fastest path:** publish the card schema + traceability test harness as a
standalone standard; adopt it as the intake requirement for any proposed
dataset (the v1 Spec Card already plays this role for opportunities).

## What this is *not*
Another large caption/VQA dataset would add to the 30-at-benchmark pile v1
documented. The agenda above is scoped so each direction either creates a
reasoning capability the corpus shows to be missing (RA-1, RA-3), answers a
model-value question with a falsifiable test (RA-2), exploits an asset class
nobody else holds (RA-4), or hardens the trust layer operations require
(RA-5).
