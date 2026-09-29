# Spec Card: cmr-summary-product-grounding

**Generating combination:** data-discovery need × DAAC product browse imagery (H3/H7) × CMR collection summaries (H1) × knowledge-based rendering + LLM restructuring.

| # | Field | Value |
|---|---|---|
| 0 | Card ID / name | `cmr-summary-product-grounding` — grounding NASA product knowledge in what products look like |
| 1 | Application need | Earthdata users and DAAC user-services staff need "which NASA product answers my question, and what am I looking at" guidance; today that knowledge lives in prose summaries divorced from imagery |
| 2 | Required capability | Given a rendered granule/browse image, explain what the product measures, its units/resolution/limitations, and which science questions it serves (and inversely: recommend products from a described need) |
| 3 | Geospatial evidence | Browse/rendered granule imagery for CMR collections (GIBS layers where available, DAAC browse elsewhere); global; open |
| 4 | Information source | CMR collection summaries — dense scientific prose per collection (~9K collections), plus variable metadata (scientific-knowledge); open API, content verified this run |
| 5 | Semantic relationship | Language explains what the depicted measurement is and means — scientific knowledge about the product, evidenced by its visual signature |
| 6 | Alignment | Entity (collection id ↔ its rendered granules) + spatial/temporal per granule |
| 7 | Supervision generation | Knowledge-based: render granules per collection, attach summary-derived captions; LLM restructures summaries into QA with hallucination audit vs source text (AP-5 control) |
| 8 | Scaling strategy | ~9K collections × many granules/layers → 10^5+ pairs; grows with the catalog; marginal cost is rendering compute |
| 9 | Grounding-quality risks | Summary text describes the product, not the specific scene (AP-4-adjacent) → split captions into product-level (always true) vs scene-level (from granule metadata) statements; renderings vary by colormap → include legend context |
| 10 | Negative-control plan | Product-identification accuracy from imagery alone vs random; blind-LM baseline answering from question text only |
| 11 | VLM adaptation family | Contrastive (product retrieval) + instruction tuning (explanation/recommendation); retrieval-augmented over CMR |
| 12 | Application evaluation | Product-recommendation precision vs Earthdata search logs/user-services judgments; target maturity: workflow-relevant (Earthdata search/support assistant) |
| 13 | Novelty assessment | data 3 (CMR summaries unexploited as supervision in corpus), task 2 (product epistemology, not scene description), science 2 (links measurement provenance to visual evidence), application 2 |
| 14 | Feasibility notes | Fully open; NASA-internal alignment (Earthdata) makes institutional adoption plausible; rendering pipeline is the main engineering cost |
| 15 | Metapattern lineage | MP-5 (knowledge bridged via the collection entity) + MP-1 join mechanics |
