# Science FM Contribution Taxonomy (O4)

Answers requirements §3's question — *what does a Science FM contribute that
cannot be obtained more transparently or reliably from metadata, physical
variables, or deterministic algorithms?* — from two evidence bases: the
76-record corpus (`records-v2.json`, counts from `analysis/corpus_stats.py`)
and the demonstrator ablation (`demonstrator/out/ablation.json`, n=13 event ×
13 control, rank AUC; demonstration-grade and stated as such).

## The corpus baseline
51/76 systems use **no science FM at all**; where FMs appear they are mostly
in-domain contrastive encoders (`direct-multimodal-encoder` 11,
`embedding-generator` 9). The roles the requirements care most about —
`similarity-retrieval` (1), `anomaly-detector` (0),
`temporal-change-representation` (0) — are essentially unexplored in the
literature we surveyed. Only 3/76 systems feed `learned-representation`
evidence to the language layer at all.

## Taxonomy: where the FM earns its place

| Role | FM contribution beyond deterministic science | Evidence |
|---|---|---|
| **Analog / similarity retrieval** | "This state resembles X" over arbitrary content — no index or metadata query expresses open-ended state similarity. This is the clearest deterministic-irreplaceable capability. | DamageScope [2608.21529](https://arxiv.org/abs/2608.21529); demonstrator analogs (every card carries cosine neighbors no index could produce) |
| **Confusable-case mining** | Finding *visually/spectrally similar sites with different causes* to build discrimination and abstention supervision (catalog C8) — deterministic thresholds select by value, not by resemblance. | AXIS encoder hints [2509.24378](https://arxiv.org/abs/2509.24378); corpus gap: discriminate trained in 2/76 |
| **Representation over content without algorithms** | Where no established algorithm exists for the semantic content (building function, scene resemblance, cross-view identity), embeddings are the only automated evidence. | pathology/pollen-scale retrieval patterns in medicine (e.g., MMRad-22K evidence units [2602.12843](https://arxiv.org/abs/2602.12843)); EO-Agents learned rankings [2607.01584](https://arxiv.org/abs/2607.01584) |
| **Encoder for adaptation** | As a fine-tuning backbone, in-domain FMs demonstrably lift task performance vs generic backbones (v1 evidence: zero-shot RemoteCLIP 4.9% → 47.7% fine-tuned on RoofNet [2505.19358](https://arxiv.org/abs/2505.19358)). | 11 corpus systems |

## Where deterministic science is preferable (≥3, evidence-cited)

1. **Burn-scar change detection at chip scale** — the demonstrator's own
   result: −ΔNBR separates event from control sites at AUC 0.63 vs 0.54 for
   Prithvi representation-change (raw band deltas: 0.44, worse than chance);
   combining did not beat ΔNBR alone (0.59). Where a physical index encodes
   the phenomenon, hand the LM the index. (Caveats recorded in
   `ablation.json`: single-frame CPU inference, mean-pooled embeddings,
   EONET point geometry may not center the burn in the chip — an FM-favorable
   configuration could reverse this; the *method* of asking is the
   contribution.)
2. **Quantities with established algorithms** — indices, anomalies,
   climatologies, biomarkers: RetiBridge's whole design premise is that
   quantified biomarkers, not embeddings, bridge to diagnosis
   [2510.04281](https://arxiv.org/abs/2510.04281); ClimateIQA builds from
   reanalysis quantities [2406.09838](https://arxiv.org/abs/2406.09838).
3. **Verifiable ground truth for supervision** — GeoDisaster derives answers
   from executable geospatial workflows precisely to avoid learned annotation
   [2606.17246](https://arxiv.org/abs/2606.17246); ScienceAgentBench uses
   program outputs [2410.05080](https://arxiv.org/abs/2410.05080).
4. **Anything requiring provenance and uncertainty statements** — FM
   embedding distances have no calibrated uncertainty (our cards must say so
   explicitly in `uncertainty_note`); deterministic quantities carry error
   models.

## Decision rule (the taxonomy compressed)

> Use deterministic science wherever an established algorithm names the
> quantity the language must state. Use the Science FM for what has no
> algorithm: resemblance, analogs, confusable-case mining, and as an
> adaptation backbone. Never present FM outputs as measurements — they are a
> separate evidence class with model provenance and control-derived
> thresholds (as the card schema enforces).
