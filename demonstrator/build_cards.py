"""Assemble Structured Science Evidence Cards (O8) from deterministic +
FM + contextual evidence, validating each against schema/science_card.schema.json.

Writes demonstrator/out/cards/<site>.json.
Usage: python3 demonstrator/build_cards.py
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

S2_SOURCE = "Sentinel-2 L2A COG (Earth Search STAC, earth-search.aws.element84.com)"
PRITHVI = "Prithvi-EO-1.0-100M (ibm-nasa-geospatial, Apache-2.0)"

# thresholds used for affordances/insufficiencies (documented in README)
DNBR_CHANGE = -0.10       # burn-scar-scale NBR drop
REPR_CHANGE = None        # set adaptively: median of control distances * 3


def ev(key, value, cls, source, method, provenance, uncertainty=None,
       note=None, units=None):
    e = {"key": key, "value": value, "units": units, "class": cls,
         "source": source, "method": method, "provenance": provenance,
         "uncertainty": uncertainty}
    if uncertainty is None:
        e["uncertainty_note"] = note or "no formal uncertainty model for this quantity in this demonstrator"
    return e


def main() -> None:
    sites = {s["site_id"]: s for s in
             json.loads((HERE / "out" / "sites.json").read_text())}
    det = json.loads((HERE / "out" / "evidence.json").read_text())
    fm = json.loads((HERE / "out" / "fm_evidence.json").read_text())
    schema = json.loads(
        (ROOT / "schema" / "science_card.schema.json").read_text()
    )

    # adaptive representation-change threshold from controls
    ctl_d = sorted(fm[s]["repr_change_cosine_dist"] for s in det
                   if det[s]["kind"] == "control")
    repr_thresh = 3 * ctl_d[len(ctl_d) // 2] if ctl_d else 0.05

    outdir = HERE / "out" / "cards"
    outdir.mkdir(parents=True, exist_ok=True)
    built = 0
    for sid, d in det.items():
        s = sites[sid]
        f = fm[sid]
        sc = d["scenes"]
        is_event = d["kind"] == "event"

        evidence = [
            ev("band_means_before", d["before"]["band_means"], "observed",
               S2_SOURCE, "windowed COG read, 6 HLS-equivalent bands, mean over 224x224 chip",
               sc["before"]["scene"],
               {"type": "window-cloud-fraction", "value": sc["before"]["window_cloud_fraction"]},
               units="reflectance"),
            ev("band_means_after", d["after"]["band_means"], "observed",
               S2_SOURCE, "windowed COG read, 6 HLS-equivalent bands, mean over 224x224 chip",
               sc["after"]["scene"],
               {"type": "window-cloud-fraction", "value": sc["after"]["window_cloud_fraction"]},
               units="reflectance"),
            ev("ndvi_mean_before", d["before"]["ndvi_mean"], "computed",
               S2_SOURCE, "NDVI=(NIR-Red)/(NIR+Red), chip mean",
               "demonstrator/evidence.py"),
            ev("ndvi_mean_after", d["after"]["ndvi_mean"], "computed",
               S2_SOURCE, "NDVI=(NIR-Red)/(NIR+Red), chip mean",
               "demonstrator/evidence.py"),
            ev("nbr_mean_before", d["before"]["nbr_mean"], "computed",
               S2_SOURCE, "NBR=(NIR-SWIR2)/(NIR+SWIR2), chip mean",
               "demonstrator/evidence.py"),
            ev("nbr_mean_after", d["after"]["nbr_mean"], "computed",
               S2_SOURCE, "NBR=(NIR-SWIR2)/(NIR+SWIR2), chip mean",
               "demonstrator/evidence.py"),
            ev("delta_ndvi", d["delta_ndvi"], "computed", S2_SOURCE,
               "after minus before chip-mean NDVI", "demonstrator/evidence.py"),
            ev("delta_nbr", d["delta_nbr"], "computed", S2_SOURCE,
               "after minus before chip-mean NBR", "demonstrator/evidence.py"),
            ev("repr_change_cosine_dist", f["repr_change_cosine_dist"],
               "learned-representation", PRITHVI,
               "1 - cosine(mean patch embedding before, after)",
               "demonstrator/prithvi_embed.py",
               note="no calibrated uncertainty for FM embedding distances; "
                    "interpretation is relative to the control distribution"),
        ]
        if is_event:
            evidence.append(
                ev("reported_event", {"title": s["event_title"],
                                      "date": s["event_date"],
                                      "category": "wildfires"},
                   "contextual", "NASA EONET", "spatio-temporal catalog join",
                   s["event_url"])
            )
        else:
            evidence.append(
                ev("event_catalog_check", "no EONET event reported at this location/date",
                   "contextual", "NASA EONET",
                   "spatio-temporal catalog join (negative result)",
                   "https://eonet.gsfc.nasa.gov/api/v3/events")
            )

        insuff = []
        for phase in ("before", "after"):
            cf = sc[phase]["window_cloud_fraction"]
            if cf > 0.10:
                insuff.append(
                    f"{phase} chip has {cf:.0%} cloud/shadow fraction — "
                    "index means partly contaminated"
                )
        gap_days = (
            sc["after"]["datetime"], sc["before"]["datetime"]
        )
        big_dnbr = d["delta_nbr"] < DNBR_CHANGE
        big_repr = f["repr_change_cosine_dist"] > repr_thresh

        afford = ["describe", "compare", "detect"]
        if is_event and (big_dnbr or big_repr):
            afford += ["explain", "discriminate", "integrate"]
        if not is_event and (big_dnbr or big_repr):
            afford += ["hypothesize", "test-hypotheses", "recommend-analysis"]
        if insuff:
            afford.append("abstain")
        afford.append("retrieve-analogs")

        card = {
            "card_id": f"sc_{sid}",
            "card_type": "before-after",
            "phenomenon": {
                "description": (s["event_title"] or
                                "control site, no reported event"),
                "status": "externally-reported" if is_event else "none-expected",
                "external_reference": s["event_url"],
            },
            "spatial": {"lat": s["lat"], "lon": s["lon"],
                        "extent_m": 2240.0, "crs": "EPSG:4326"},
            "temporal": {
                "timestamps": [sc["before"]["datetime"], sc["after"]["datetime"]],
                "reference_event_time": s["event_date"] if is_event else None,
            },
            "evidence": evidence,
            "analogs": f["analogs"],
            "relationships": (
                [{"type": "control-for", "subject": f"sc_{sid}",
                  "object": f"sc_{s['control_for']}"}]
                if not is_event else []
            ),
            "reasoning_affordances": sorted(set(afford)),
            "provenance": {
                "pipeline": "demonstrator/build_cards.py",
                "built_at_data_time": max(gap_days),
                "notes": f"repr-change control-derived threshold: {repr_thresh:.4f}",
            },
            "insufficiencies": insuff,
        }
        jsonschema.validate(card, schema)
        (outdir / f"{sid}.json").write_text(json.dumps(card, indent=1), "utf-8")
        built += 1
    print(f"built and validated {built} cards (repr threshold {repr_thresh:.4f})")


if __name__ == "__main__":
    main()
