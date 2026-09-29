# NASA Opportunity Catalog v2 (O7) — evidence compositions where the text does not yet exist

v1's catalog mined holdings where authoritative *text already existed*
(PAGER briefs, AFDs, CMR summaries). The v2 question (requirements §16) is
different: **where can NASA observations, algorithms, models, catalogs, and
knowledge be automatically assembled into a Science Card from which the text
is *generated*?** Every entry composes live-verified holdings (H-numbers from
`opportunities/holdings-inventory.md`, plus HLS/Prithvi as exercised in the
demonstrator) and names its full composition: *need × observation ×
deterministic measurement × FM representation × contextual data × knowledge ×
reasoning operation × language product.*

Priority rubric (0–3 each) groups the 12 factors of requirements §18:
**Value** = scientific + operational value; **Evidence** = evidence quality +
grounding strength + negative/control availability + temporal richness;
**Scale** = constructibility at scale + evaluation feasibility;
**FM-lift** = plausible Science FM contribution + reasoning novelty;
**Path** = interpretability + research→operations pathway.

| # | Opportunity | Composition | Value | Evidence | Scale | FM-lift | Path | Σ |
|---|---|---|---|---|---|---|---|---|
| C1 | **Land-surface disturbance explanation service** (demonstrated) | disturbance triage × HLS/S2 time series × ΔNBR/ΔNDVI × Prithvi Δ-representation + analogs × EONET/FIRMS events (H2) × dNBR doctrine × discriminate/explain × attribution briefs + follow-ups | 3 | 3 | 3 | 2 | 3 | **14** |
| C2 | **Representation-trajectory anomaly narrator** | "what is this landscape doing?" × HLS sequences × phenology/climatology anomalies × Prithvi trajectory + break detection × station/weather context (H4) × land-cover knowledge × detect/hypothesize × anomaly explanations + evidence-driven questions | 3 | 2 | 2 | 3 | 2 | **12** |
| C3 | **Cross-mission analog finder with narrative comparison** | "where has this happened before?" × any EO scene × derived indices × FM embedding search over archive (EC-3) × event catalogs × regional knowledge × retrieve-analogs/compare × analog-event descriptions | 2 | 2 | 2 | 3 | 2 | **11** |
| C4 | **Observation–forecast discrepancy briefs** | model evaluation × satellite observations × obs-minus-forecast fields (H4/H7 products) × FM state descriptors × forecast-cycle metadata × model documentation × integrate/explain × discrepancy explanations for forecasters | 3 | 2 | 2 | 2 | 2 | **11** |
| C5 | **Ground-truth conflict auditor** (GLOBE × satellite) | product validation × co-located GLOBE photos+classifications (H6) × satellite land-cover product values × FM cross-view similarity × observer metadata × class definitions × discriminate/abstain × agreement/conflict reports with abstention cases | 2 | 3 | 2 | 2 | 2 | **11** |
| C6 | **Event-impact evidence dossiers** | disaster response × pre/post imagery (H3) × change metrics × FM damage-analog retrieval × PAGER/ShakeMap or EONET records (H5/H2) × infrastructure layers × integrate/recommend-analysis × structured impact dossiers | 3 | 2 | 2 | 2 | 3 | **12** |
| C7 | **Dataset-pairing hypothesis engine over CMR** | research ideation × CMR collection footprints/variables (H1/H7) × co-coverage statistics × KG/co-usage embeddings × literature links × domain ontologies × hypothesize/test-hypotheses × structured research hypotheses (extends corpus [2607.01584](https://arxiv.org/abs/2607.01584) from metadata-only to card-grounded) | 2 | 2 | 3 | 2 | 2 | **11** |
| C8 | **Counterfactual curriculum builder** | model training QC × visually similar site pairs (fire/drought/harvest NDVI declines) × index signatures × FM-similar-embedding mining × conflicting context records × discrimination doctrine × discriminate/abstain × negative and abstention supervision at scale (requirements §12 as a *product*, not a byproduct) | 2 | 3 | 3 | 3 | 2 | **13** |

## Selection guidance
- **C1 is demonstrated** end-to-end in `demonstrator/` (cards → language →
  ablation); its production path is archive back-fill plus FIRMS/active-fire
  context joins.
- **C8 and C2 are the highest-value next builds:** C8 turns the corpus's
  scarcest supervision (discrimination/abstention — 2/76 records) into a
  systematic product using FM similarity to *mine confusable cases*, which is
  a use of embeddings deterministic science cannot replace; C2 is the purest
  test of whether Prithvi trajectories carry state information beyond
  climatology.
- All entries generate text that **does not currently exist** — the defining
  v2 criterion — and every holding referenced was live-verified (v1 inventory
  or this session's demonstrator).
