# Structured Science Evidence Card — Specification (O3)

The card is the **interface between scientific data/models and language
models**: a normalized, auditable evidence state from which many language
products can be generated. It replaces v1's GeoData–Language Pair Spec Card
(which described *pairing opportunities*; this describes the *evidence object
itself* — the v1 card survives as the opportunity-intake format, see
`patterns/spec-card-template.md`).

Machine-readable schema: [`schema/science_card.schema.json`](../schema/science_card.schema.json)
(enforced in `tests/test_science_cards.py`; all demonstrator cards validate).

## Design rules

1. **Evidence classes never collapse.** Every evidence entry carries `class ∈
   {observed, computed, inferred, learned-representation, contextual}` so
   generation can weight raw measurements differently from model opinions and
   retrieved knowledge. (Requirements §4's observed → computed → inferred →
   retrieved/contextual chain, with learned representations kept separate per
   §2.)
2. **Five-tuple per evidence entry:** `value + source + method + provenance +
   uncertainty` (§9). `uncertainty: null` is legal only with an
   `uncertainty_note` explaining why (schema-enforced) — silence is not an
   option.
3. **Model independence.** No field names Prithvi, HLS, or any LLM; they
   appear only as *values* of `source`/`method` (§15). A different FM or
   sensor changes the payload, not the schema.
4. **Temporal modes are card types** (§5): `single-observation`,
   `before-after`, `temporal-sequence`, `anomaly-vs-baseline`,
   `representation-trajectory`, `cross-location-comparison`.
5. **Phenomenon status is explicit:** `externally-reported` (an authoritative
   catalog reports an event), `candidate` (evidence suggests, nothing
   confirms), `none-expected` (control). This is what lets cards generate
   negative/counterfactual supervision (§12) instead of assuming every card
   depicts something.
6. **Insufficiencies are first-class.** `insufficiencies` records what the
   card *cannot* support (cloud contamination, missing baseline, conflicting
   context) — the hook for abstention supervision.
7. **Reasoning affordances are declared, not implied.** Each card lists the
   reasoning operations its evidence state supports (`describe` … `abstain`),
   which drives both language generation (O5) and question generation (O6):
   a card affords `discriminate` only when it holds evidence for competing
   causes.
8. **Analogs and relationships are references,** never copies — cards link to
   other cards/sites with the similarity method stated, keeping
   retrieval-based reasoning auditable.

## Field walk-through (informative)

| Section | Holds | Example (demonstrator) |
|---|---|---|
| `phenomenon` | what the card is about + status + external ref | wildfire, `externally-reported`, EONET id |
| `spatial`, `temporal` | extent + the timestamps of every observation used | chip center/extent; before/after dates |
| `evidence[]` | the payload: band statistics (`observed`), NDVI/NBR/deltas (`computed`), FM embedding descriptors and Δ-representation (`learned-representation`), event records (`contextual`), any task-model outputs (`inferred`) | `delta_nbr = -0.31, method=NBR difference, source=Sentinel-2 L2A, uncertainty={type: cloud-fraction, value: 0.02}` |
| `analogs[]` | nearest neighbors + similarity method | top-3 cosine neighbors in embedding space |
| `relationships[]` | typed links among evidence/cards | `after-of`, `control-for` |
| `reasoning_affordances` | operations the evidence supports | detect, discriminate, explain, abstain |
| `insufficiencies` | recorded gaps | "no baseline earlier than 2024" |
| `provenance` | pipeline id + build time (data-derived) | `demonstrator/build_cards.py@<commit>` |

## Scalable construction (§9 mapping)

| Card content | Construction mechanism |
|---|---|
| identity, spatial/temporal extent, band values | direct metadata extraction + windowed reads |
| indices, deltas, statistics | deterministic scientific computation |
| event context | catalog + spatial + temporal joins, event alignment |
| FM descriptors, Δ-representation | Science FM inference |
| analogs | vector similarity search |
| scientific knowledge | knowledge-base/literature retrieval (always `class: contextual`) |
| free-text syntheses | LLM-assisted, only over the above, with hallucination audit |

Per-card marginal cost is measured in the demonstrator README; every
mechanism above is automation-only — the schema requires no manual expert
annotation anywhere.
