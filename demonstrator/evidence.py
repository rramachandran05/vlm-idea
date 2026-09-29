"""Deterministic evidence per site (O8): band statistics, NDVI/NBR, deltas.

Reads demonstrator/out/chips.npz + chips_meta.json, writes evidence values
into demonstrator/out/evidence.json (merged later with FM evidence).

Bands order: blue, green, red, nir08(B8A), swir16(B11), swir22(B12).
Usage: python3 demonstrator/evidence.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

B_RED, B_NIR, B_SWIR2 = 2, 3, 5


def index_stats(chip: np.ndarray) -> dict:
    red, nir, swir2 = chip[B_RED], chip[B_NIR], chip[B_SWIR2]
    eps = 1e-6
    ndvi = (nir - red) / (nir + red + eps)
    nbr = (nir - swir2) / (nir + swir2 + eps)
    return {
        "ndvi_mean": float(ndvi.mean()),
        "nbr_mean": float(nbr.mean()),
        "band_means": [float(chip[i].mean()) for i in range(6)],
        "band_p90": [float(np.percentile(chip[i], 90)) for i in range(6)],
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    chips = np.load(here / "out" / "chips.npz")
    meta = {m["site_id"]: m for m in
            json.loads((here / "out" / "chips_meta.json").read_text())}

    out = {}
    for sid, m in meta.items():
        before = chips[f"{sid}_before"]
        after = chips[f"{sid}_after"]
        sb, sa = index_stats(before), index_stats(after)
        out[sid] = {
            "kind": m["kind"],
            "scenes": m["scenes"],
            "before": sb,
            "after": sa,
            "delta_ndvi": sa["ndvi_mean"] - sb["ndvi_mean"],
            "delta_nbr": sa["nbr_mean"] - sb["nbr_mean"],
            # raw band-stat delta proxy for the ablation's lowest tier:
            # mean absolute change across all band means
            "band_mean_abs_delta": float(
                np.mean(np.abs(np.array(sa["band_means"])
                               - np.array(sb["band_means"])))
            ),
        }
    (here / "out" / "evidence.json").write_text(
        json.dumps(out, indent=1), "utf-8"
    )
    print(f"deterministic evidence for {len(out)} sites")


if __name__ == "__main__":
    main()
