# Spec Card: earth-observatory-story-grounding

**Generating combination:** science-communication & analyst-briefing need × NASA-curated event imagery (H10/H8/H3) × science-writer narratives (H10/H8) × deterministic article-image pairing + LLM restructuring.

| # | Field | Value |
|---|---|---|
| 0 | Card ID / name | `earth-observatory-story-grounding` — NASA's narrative archives as explanation supervision |
| 1 | Application need | Science communicators, educators, and situational-awareness briefers need scientist-reviewed explanations of what an Earth image shows and why it matters; NASA has produced exactly this, daily, for 25+ years (Earth Observatory, Image & Video Library) |
| 2 | Required capability | Generate an accurate, causally framed Earth-science narrative for a given scene: what is visible, the process behind it, historical context, and significance |
| 3 | Geospatial evidence | Earth Observatory & NASA Image Library imagery with acquisition metadata (sensor, date, location); often multi-date comparisons |
| 4 | Information source | Science-writer narratives reviewed by NASA scientists (scientific-knowledge + reports); tens of thousands of articles; RSS/API verified this run (Salton Sea narrative sample) |
| 5 | Semantic relationship | Language explains the depicted phenomenon — process, cause, context — at expository depth beyond captioning |
| 6 | Alignment | Entity (article ↔ its images) + spatial/temporal from image metadata; event for Natural Hazards items |
| 7 | Supervision generation | Deterministic article-image pairing; LLM restructures long articles into grounded QA/explanations with hallucination audit vs article text (AP-5 control) |
| 8 | Scaling strategy | ~25 years × daily-cadence publications + 100K+ library items → 10^4–10^5 rich pairs; grows daily; zero marginal cost |
| 9 | Grounding-quality risks | Narratives include facts not evidenced in pixels (history, statistics) (AP-4) → tag statements as scene-evidenced vs context; image-article many-to-many needs careful keying |
| 10 | Negative-control plan | Blind baseline from title alone; factual-claim verification rate against source article; caption-metric-only evaluation prohibited (AP-2) |
| 11 | VLM adaptation family | Instruction tuning for long-form grounded generation; retrieval-augmented with the article archive |
| 12 | Application evaluation | Scientist-judged accuracy of generated narratives on held-out events; use in briefing drafting; target maturity: workflow-relevant (EO/communications drafting) |
| 13 | Novelty assessment | data 3 (narrative archives unexploited in corpus; GAIA scraped adjacent web sources but not these curated archives), task 2 (expository narrative vs caption), science 2, application 2 |
| 14 | Feasibility notes | NASA content is public-domain-friendly; article-image keying is the main engineering; strong NASA-internal story |
| 15 | Metapattern lineage | MP-3 (institutional expert text) + MP-5 (knowledge enrichment) |
