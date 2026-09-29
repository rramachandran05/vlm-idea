# Evidence-Composition Metapatterns (O2)

v2 reframe of `metapatterns.md` (v1, kept as the pairing-era record): the unit
is no longer a geodata–text pair but an **evidence composition** — multiple
evidence classes combined into a capability unavailable from any single
source. Each pattern instantiates the revised 13-element chain: *application
need → scientific question → required reasoning capability → observations →
deterministic evidence → Science FM evidence → contextual evidence →
Structured Science Card → language-generation strategy →
grounding/verification → LLM/VLM adaptation → scientific evaluation →
operational capability.* Citations are corpus IDs (`data/corpus/papers.json`);
axis counts come from `analysis/corpus_stats.py` (34/76 records already
compose ≥2 evidence classes — the compositions below are the recurring shapes
among them, plus the demonstrator's own instantiations).

---

## EC-1 — Observation + temporal context → change interpretation
- **Question/capability:** what changed, when, and is it real? (`detect`, `compare`)
- **Composition:** current observation (`observed`) + prior state or sequence (`observed`, joined deterministically by location/patient/site identity).
- **Card role:** `before-after` / `temporal-sequence` card types; the join key and interval live in `temporal`.
- **Generation:** change statements bounded to what both acquisitions evidence; verification = recomputation of deltas.
- **Evaluation → capability:** change-detection agreement; monitoring workflows.
- **Evidence:** longitudinal radiology reporting [2307.09758](https://arxiv.org/abs/2307.09758), TEOChat temporal EO dialogue [2410.06234](https://arxiv.org/abs/2410.06234), RSCC disaster change pairs [2509.01907](https://arxiv.org/abs/2509.01907); demonstrator cards (ΔNDVI/ΔNBR).
- **Unavailable from single source:** a lone scene cannot state change at all.

## EC-2 — Observation + deterministic science → quantitative grounding
- **Question/capability:** what do the physics-based quantities say? (`describe`, `integrate`)
- **Composition:** raw measurements (`observed`) + established algorithms' outputs (`computed`): indices, anomalies, statistics, biomarkers.
- **Card role:** `computed` entries with method+provenance; the LM never re-derives arithmetic it can be handed.
- **Generation:** statements quote computed values; verification = re-running the algorithm.
- **Evidence:** RetiBridge biomarker→diagnosis pathway [2510.04281](https://arxiv.org/abs/2510.04281), MEETI beat-level ECG features [2507.15255](https://arxiv.org/abs/2507.15255), ClimateIQA reanalysis quantities [2406.09838](https://arxiv.org/abs/2406.09838), SPADE wetting events [2509.18123](https://arxiv.org/abs/2509.18123).
- **Unavailable from single source:** pixels alone make the LM guess quantities it can be given exactly (AP-2/AP-3 territory).

## EC-3 — Observation + FM representation → similarity, anomaly, analog discovery
- **Question/capability:** is this state unusual, and where has it occurred before? (`retrieve-analogs`, `detect`)
- **Composition:** observation (`observed`) + embedding descriptors, representation-change metrics, nearest neighbors (`learned-representation`).
- **Card role:** FM outputs are a *separate evidence class* with model provenance — never presented as measurements; thresholds derived from control distributions.
- **Generation:** similarity/anomaly statements tagged `derived-interpretation`; analog references resolvable to other cards.
- **Evidence:** DamageScope multi-vector retrieval [2608.21529](https://arxiv.org/abs/2608.21529), AXIS encoder-hint anomaly explanation [2509.24378](https://arxiv.org/abs/2509.24378), EO-Agents learned rankings [2607.01584](https://arxiv.org/abs/2607.01584); demonstrator Prithvi Δ-representation + analogs. Only 3/76 corpus records feed learned-representation evidence to the LM — the emptiest, most novel cell in the composition space.
- **Unavailable from single source:** deterministic indices cannot say "this state resembles site X"; that is precisely the FM's contribution (O4).

## EC-4 — Observation + event/context records → attribution support
- **Question/capability:** which reported process explains the observation? (`discriminate`, `integrate`)
- **Composition:** observation + change evidence + authoritative event catalogs, patient records, weather context (`contextual`).
- **Card role:** context entries carry the catalog join (spatial+temporal+event); *absence of a record is itself recorded* (`event_catalog_check`), enabling counterfactuals.
- **Generation:** attribution statements cite both the physical signal and the record; conflict cases generate hypothesis/abstention supervision instead (requirements §12).
- **Evidence:** patient-data-augmented CXR reporting [2406.13181](https://arxiv.org/abs/2406.13181), DisasterInsight OSM-function damage reasoning [2601.18493](https://arxiv.org/abs/2601.18493), war-infrastructure incident fusion [2608.00119](https://arxiv.org/abs/2608.00119), IoT-LLM knowledge-augmented sensing [2410.02429](https://arxiv.org/abs/2410.02429); demonstrator EONET joins.
- **Unavailable from single source:** spectra can show *that* something changed, never *which catalogued event* did it.

## EC-5 — Observation + retrieved scientific knowledge → contextualized interpretation
- **Question/capability:** what does established science say this means? (`explain`)
- **Composition:** evidence state + literature/KG/standards content (`contextual`, retrieved).
- **Card role:** knowledge enters as traced, quoted entries (`knowledge:*`), so generated explanations separate retrieved doctrine from case evidence.
- **Generation:** retrieval-grounded; every knowledge claim tagged `retrieved-knowledge` (AP-5 control).
- **Evidence:** EviAgent clinical priors [2603.13956](https://arxiv.org/abs/2603.13956), VLCE knowledge-graph enrichment [2509.21609](https://arxiv.org/abs/2509.21609), HypER literature-grounded reasoning [2506.12937](https://arxiv.org/abs/2506.12937), EcoWikiRS habitat text [2504.19742](https://arxiv.org/abs/2504.19742).
- **Unavailable from single source:** no observation carries its own interpretive doctrine.

## EC-6 — Evidence state → generated questions and hypotheses
- **Question/capability:** what is worth asking here? (`hypothesize`, `test-hypotheses`)
- **Composition:** the *conjunction* of evidence entries (large Δ + no catalog record; catalog record + no Δ; conflicting classes) determines which questions are scientifically interesting (requirements §11).
- **Card role:** `reasoning_affordances` declares what the state supports; question rules fire on thresholds/conflicts/absences.
- **Generation:** question templates keyed to evidence-state rules, never to imagery alone; hypothesis outputs tagged `hypothesis`.
- **Evidence:** data-driven hypothesis generation [2404.04326](https://arxiv.org/abs/2404.04326), The AI Scientist's idea→experiment loop [2408.06292](https://arxiv.org/abs/2408.06292), EO-Agents [2607.01584](https://arxiv.org/abs/2607.01584); demonstrator question generator (event vs stable vs conflict states yield different question families — test-verified).
- **Unavailable from single source:** generic image questions ("what is visible?") are exactly what this replaces; only 4/76 corpus records train `hypothesize` at all.

## EC-7 — Evidence composition + workflow rules → decision-support outputs
- **Question/capability:** what should be done next? (`recommend-analysis`)
- **Composition:** any of EC-1…EC-5 + operational procedures/standards as the outer frame (v1's MP-6, lifted to evidence level).
- **Card role:** affordances include `recommend-analysis`; recommendations trace to the evidence entries that trigger them.
- **Generation:** follow-up recommendations as conditional templates over evidence state; evaluation = does the recommended analysis discriminate the open hypotheses?
- **Evidence:** GeoDisaster workflow-grounded tasks [2606.17246](https://arxiv.org/abs/2606.17246), TerraBench tool-grounded reasoning [2606.13148](https://arxiv.org/abs/2606.13148), AgMMU management instructions [2504.10568](https://arxiv.org/abs/2504.10568), ScienceAgentBench program outputs [2410.05080](https://arxiv.org/abs/2410.05080).
- **Unavailable from single source:** a recommendation needs both an evidence state and a workflow to recommend within.

---

## Reading of the composition space
The corpus concentrates in EC-1/EC-2 fragments and rarely composes further:
`describe` dominates reasoning operations (46/76) while `discriminate` (2),
`test-hypotheses` (2), and `retrieve-analogs` (1) are nearly empty — yet those
are exactly the operations the compositions above unlock. Medicine is ahead of
Earth science here (MAIRA-2, MMRad-22K, RetiBridge already run EC-2+EC-4+EC-5
compositions with structured evidence); the demonstrator shows the same
compositions are automatable for EO at near-zero marginal cost.
