# HLS + Prithvi Demonstrator (O8)

End-to-end instantiation of the v2 pipeline:
**observations → deterministic science + Prithvi-EO representations →
Structured Science Card → grounded language products + evidence-driven
questions → ablation.**

## Data and model sources (all live-verified this run)

| Component | Source | Size / license |
|---|---|---|
| Observations | Sentinel-2 L2A COGs via Earth Search STAC (`earth-search.aws.element84.com/v1`) — the **HLS-equivalent testbed**: S30's source sensor, same six HLS bands (B02/B03/B04/B8A/B11/B12). True HLS requires an Earthdata login this session does not hold; the card schema keeps the sensor as a provenance value so HLS drops in unchanged. | open, no key |
| Event context | NASA EONET wildfire events (2024-06→2026-06 window) | open API |
| Science FM | Prithvi-EO-1.0-100M (`ibm-nasa-geospatial/Prithvi-EO-1.0-100M`: `Prithvi_EO_V1_100M.pt` 453 MB + `prithvi_mae.py` + `config.json`) | Apache-2.0 |
| Python deps added | torch 2.14.0, rasterio 1.5.1 (**affine pinned 2.4.0** — 3.x breaks rasterio 1.5.1 window math), einops, timm | PyPI |

## Run order

```bash
python3 demonstrator/sites.py --n 14      # EONET events + paired 0.7° offset controls
python3 demonstrator/fetch_chips.py       # STAC search + windowed COG reads, SCL cloud screen
python3 demonstrator/evidence.py          # band stats, NDVI/NBR, deltas
python3 demonstrator/prithvi_embed.py     # embeddings, Δ-representation, analogs (CPU)
python3 demonstrator/build_cards.py       # schema-validated Science Cards
python3 demonstrator/generate_language.py # traced statements + evidence-driven questions
python3 demonstrator/ablation.py          # tiered event-vs-control discrimination
```

Committed outputs: `out/sites.json`, `out/chips_meta.json`, `out/evidence.json`,
`out/fm_evidence.json`, `out/cards/*.json`, `out/language/products.json`,
`out/ablation.json`. Bulk arrays (`chips.npz`, `embeddings.npz`) and model
weights are git-ignored and regenerable.

## Design notes
- **Paired controls:** every event site has a control at +0.7° longitude with
  the same acquisition windows, so seasonal phenology is partially controlled
  and the ablation is a paired discrimination task.
- **Cloud screen:** scenes sorted by `eo:cloud_cover`, then a per-window SCL
  check (cloud/shadow/cirrus ≤25%, nodata ≤20%); residual contamination >10%
  is recorded on the card as an insufficiency and drives abstention
  supervision rather than being silently accepted.
- **Representation-change threshold** is derived from the control
  distribution (3× control median), recorded in each card's provenance —
  no hand-tuned magic number.
- **Single-frame Prithvi inference:** chips are fed as one-frame inputs; the
  encoder interpolates its (3-frame) positional embedding. Upgrade path:
  Prithvi-EO-2.0 via terratorch with true 3-frame time series.
- **Per-card marginal cost** (measured this run): ~12 windowed COG reads +
  one CPU forward pass + catalog join per site — no manual annotation
  anywhere in the pipeline, supporting the requirements §9 scale question.

## Grounding QC (Task 9)
Seeded sample of generated language manually reviewed against card evidence —
results recorded here after the run: see `out/language/qc-language.json`.
