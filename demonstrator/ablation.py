"""Ablation (O9): can each evidence tier separate event sites from controls?

Tiers (per specs/science-evidence-cards/03-plan.md):
  T1 raw band-stat delta proxy  — mean |Δ band means| (no science computation)
  T2 deterministic indices      — burn-oriented -ΔNBR
  T3 FM representation change   — Prithvi cosine distance before->after
  T4 combined                   — mean of per-tier ranks (T2+T3)

Metric: rank-based AUC (probability a random event site scores above a random
control site), exact over all event x control pairs. Demonstration-grade n —
reported as such.

Reads demonstrator/out/evidence.json + fm_evidence.json;
writes demonstrator/out/ablation.json.
Usage: python3 demonstrator/ablation.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def auc(scores_pos, scores_neg):
    wins = ties = 0
    for p in scores_pos:
        for n in scores_neg:
            if p > n:
                wins += 1
            elif p == n:
                ties += 1
    total = len(scores_pos) * len(scores_neg)
    return (wins + 0.5 * ties) / total if total else float("nan")


def ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    r = [0.0] * len(values)
    for rank, i in enumerate(order):
        r[i] = rank
    return r


def main() -> None:
    det = json.loads((HERE / "out" / "evidence.json").read_text())
    fm = json.loads((HERE / "out" / "fm_evidence.json").read_text())
    sids = sorted(det)
    kinds = [det[s]["kind"] for s in sids]

    tiers = {
        "T1_raw_band_delta": [det[s]["band_mean_abs_delta"] for s in sids],
        "T2_deterministic_negative_dNBR": [-det[s]["delta_nbr"] for s in sids],
        "T3_fm_repr_change": [fm[s]["repr_change_cosine_dist"] for s in sids],
    }
    r2, r3 = ranks(tiers["T2_deterministic_negative_dNBR"]), ranks(
        tiers["T3_fm_repr_change"])
    tiers["T4_combined_T2_T3"] = [(a + b) / 2 for a, b in zip(r2, r3)]

    results, details = {}, {}
    for name, scores in tiers.items():
        pos = [v for v, k in zip(scores, kinds) if k == "event"]
        neg = [v for v, k in zip(scores, kinds) if k == "control"]
        results[name] = round(auc(pos, neg), 4)
        # misclassifications at the median-split threshold
        thresh = sorted(scores)[len(scores) // 2]
        details[name] = {
            "events_below_split": [
                s for s, v, k in zip(sids, scores, kinds)
                if k == "event" and v < thresh
            ],
            "controls_above_split": [
                s for s, v, k in zip(sids, scores, kinds)
                if k == "control" and v >= thresh
            ],
        }

    out = {
        "task": "event vs control discrimination (paired wildfire design)",
        "n_event": kinds.count("event"),
        "n_control": kinds.count("control"),
        "metric": "rank AUC over all event x control pairs",
        "auc": results,
        "median_split_misclassifications": details,
        "note": "demonstration-grade n; controls share dates/regions with "
                "their paired events (0.7 deg offset), so seasonal effects "
                "are partially controlled",
    }
    (HERE / "out" / "ablation.json").write_text(json.dumps(out, indent=1), "utf-8")
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
