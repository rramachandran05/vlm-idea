"""Evidence -> language generation (O5) and evidence-driven questions (O6).

Every emitted sentence is `{text, trace, epistemic}` where `trace` lists the
card evidence keys (or card sections) it uses and `epistemic` is one of
evidence-supported | derived-interpretation | hypothesis | retrieved-knowledge.
Question generation runs on rules over the card's evidence state, including
counterfactual/abstention constructions (O6, requirements §11–§12).

Reads demonstrator/out/cards/*.json; writes demonstrator/out/language/products.json.
Usage: python3 demonstrator/generate_language.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# retrieved domain knowledge used by attribution products (single, auditable
# place; each use is tagged retrieved-knowledge and traced here)
KNOWLEDGE = {
    "nbr_fire": "A substantial NBR decrease between dates is the standard "
                "spectral indicator of burn scarring (basis of the dNBR "
                "burn-severity convention).",
    "ndvi_causes": "NDVI decline alone is ambiguous among fire, drought "
                   "stress, harvest, and senescence; discriminating them "
                   "requires SWIR behavior and contextual records.",
}


def get(card, key):
    for e in card["evidence"]:
        if e["key"] == key:
            return e["value"]
    return None


def s(text, trace, epistemic):
    return {"text": text, "trace": trace, "epistemic": epistemic}


def products_for(card):
    cid = card["card_id"]
    t0, t1 = card["temporal"]["timestamps"][:2]
    dnbr = get(card, "delta_nbr")
    dndvi = get(card, "delta_ndvi")
    repr_d = get(card, "repr_change_cosine_dist")
    ev_ctx = get(card, "reported_event")
    thresh = float(card["provenance"]["notes"].split(":")[-1])
    big_dnbr, big_repr = dnbr < -0.10, repr_d > thresh
    out = []

    # 1 — factual observation description
    out.append(s(
        f"Between {t0} and {t1}, chip-mean NDVI moved from "
        f"{get(card,'ndvi_mean_before'):.3f} to {get(card,'ndvi_mean_after'):.3f} "
        f"and chip-mean NBR from {get(card,'nbr_mean_before'):.3f} to "
        f"{get(card,'nbr_mean_after'):.3f} at this 2.24 km site.",
        ["ndvi_mean_before", "ndvi_mean_after", "nbr_mean_before",
         "nbr_mean_after", "temporal"], "evidence-supported"))

    # 2 — temporal-change statement
    change_word = ("a pronounced decline" if dnbr < -0.10 else
                   "a moderate decline" if dnbr < -0.03 else
                   "no substantial change" if abs(dnbr) <= 0.03 else "an increase")
    out.append(s(
        f"The surface shows {change_word} in NBR (Δ={dnbr:+.3f}) and a "
        f"Prithvi representation change of {repr_d:.4f} "
        f"({'above' if big_repr else 'within'} the control-derived threshold "
        f"of {thresh:.4f}).",
        ["delta_nbr", "repr_change_cosine_dist", "provenance"],
        "derived-interpretation"))

    # 3 — comparison to nearest analog
    if card["analogs"]:
        a = card["analogs"][0]
        out.append(s(
            f"In Prithvi embedding space, the post-date scene most resembles "
            f"site {a['ref']} (cosine similarity {a['similarity']:.3f}), making "
            f"it the first analog to consult for comparative interpretation.",
            ["analogs"], "derived-interpretation"))

    # 4 — attribution / integration
    if ev_ctx and (big_dnbr or big_repr):
        out.append(s(
            f"The spectral change is consistent with the reported event "
            f"'{ev_ctx['title']}' ({ev_ctx['date']}): {KNOWLEDGE['nbr_fire']}",
            ["delta_nbr", "reported_event", "knowledge:nbr_fire"],
            "retrieved-knowledge"))
        out.append(s(
            "Taken together, the NBR drop, the representation shift, and the "
            "catalog record support fire-driven surface change over drought "
            "or harvest at this site.",
            ["delta_nbr", "repr_change_cosine_dist", "reported_event"],
            "derived-interpretation"))
    elif ev_ctx and not (big_dnbr or big_repr):
        out.append(s(
            f"Although '{ev_ctx['title']}' is cataloged for this area, neither "
            "the spectral indices nor the learned representation shows "
            "commensurate change; the burn may lie outside this chip, predate "
            "the before-scene, or be sub-resolution.",
            ["delta_nbr", "repr_change_cosine_dist", "reported_event"],
            "hypothesis"))
    elif not ev_ctx and (big_dnbr or big_repr):
        out.append(s(
            "A substantial change signal appears with no corresponding event "
            "in the consulted catalog; plausible processes include an "
            "uncataloged fire, harvest, or land clearing. "
            + KNOWLEDGE["ndvi_causes"],
            ["delta_nbr", "repr_change_cosine_dist", "event_catalog_check",
             "knowledge:ndvi_causes"], "hypothesis"))
    else:  # control, no substantial change: stable-baseline integration
        out.append(s(
            "Spectral indices and the learned representation agree that this "
            "site is stable over the interval, and no event is cataloged — "
            "consistent with its role as an undisturbed reference.",
            ["delta_nbr", "repr_change_cosine_dist", "event_catalog_check"],
            "derived-interpretation"))

    # 5 — uncertainty / abstention statement
    if card["insufficiencies"]:
        out.append(s(
            "Interpretation is limited: " + "; ".join(card["insufficiencies"])
            + ". Conclusions beyond the description above should be withheld "
            "until a cleaner acquisition is available.",
            ["insufficiencies"], "evidence-supported"))
    else:
        out.append(s(
            "Both acquisitions passed the cloud screen (window cloud fraction "
            "≤10%), so the index changes are unlikely to be acquisition "
            "artifacts.",
            ["band_means_before", "band_means_after"], "derived-interpretation"))

    # 6 — recommended follow-up
    follow = []
    if big_dnbr or big_repr:
        follow.append("acquire an intermediate-date scene to bracket the "
                      "change onset")
        follow.append("compute dNBR against a one-year-earlier baseline to "
                      "separate seasonal effects")
    if not ev_ctx and (big_dnbr or big_repr):
        follow.append("query active-fire detections for the interval to test "
                      "the uncataloged-fire hypothesis")
    if not follow:
        follow.append("no follow-up indicated; retain as a stable reference "
                      "site for analog retrieval")
    out.append(s("Recommended next analyses: " + "; ".join(follow) + ".",
                 ["delta_nbr", "repr_change_cosine_dist",
                  "reported_event" if ev_ctx else "event_catalog_check"],
                 "derived-interpretation"))
    return out


def questions_for(card):
    """Evidence-state-driven questions (O6): rules keyed to what the evidence
    shows, not generic image questions."""
    dnbr = get(card, "delta_nbr")
    repr_d = get(card, "repr_change_cosine_dist")
    ev_ctx = get(card, "reported_event")
    thresh = float(card["provenance"]["notes"].split(":")[-1])
    big = dnbr < -0.10 or repr_d > thresh
    qs = []
    if big and ev_ctx:
        qs += [
            {"q": "Does the evidence support fire rather than drought stress "
                  "or harvest as the cause of the observed decline?",
             "rule": "large-change AND event-context -> discriminate"},
            {"q": "When between the two acquisition dates did the surface "
                  "state transition most plausibly begin?",
             "rule": "large-change AND event-context -> detect-onset"},
        ]
    if big and not ev_ctx:
        qs += [
            {"q": "What process could explain a change of this magnitude with "
                  "no catalogued event at this location?",
             "rule": "large-change AND no-event-context -> hypothesize"},
            {"q": "What additional observation would best distinguish an "
                  "uncataloged fire from harvest or clearing here?",
             "rule": "large-change AND no-event-context -> test-hypotheses"},
        ]
    if not big and ev_ctx:
        qs.append(
            {"q": "Why does a cataloged wildfire show no commensurate spectral "
                  "or representation change in this chip?",
             "rule": "no-change AND event-context -> conflict/counterfactual"})
    if not big and not ev_ctx:
        qs.append(
            {"q": "Is this site suitable as a stable reference for analog "
                  "retrieval and baseline construction?",
             "rule": "stable-state -> monitoring/baseline"})
    if card["insufficiencies"]:
        qs.append(
            {"q": "Is the available evidence sufficient to attribute the "
                  "observed index changes, or should attribution be withheld?",
             "rule": "insufficiency-present -> abstention"})
    if card["analogs"]:
        qs.append(
            {"q": f"What does comparison with analog site "
                  f"{card['analogs'][0]['ref']} indicate about whether this "
                  "state is typical for the region?",
             "rule": "analogs-present -> retrieve-analogs/compare"})
    return qs


def main() -> None:
    cards_dir = HERE / "out" / "cards"
    all_products = []
    for f in sorted(cards_dir.glob("*.json")):
        card = json.loads(f.read_text())
        all_products.append({
            "card_id": card["card_id"],
            "kind": ("event" if card["phenomenon"]["status"] == "externally-reported"
                     else "control"),
            "statements": products_for(card),
            "questions": questions_for(card),
        })
    outdir = HERE / "out" / "language"
    outdir.mkdir(exist_ok=True)
    (outdir / "products.json").write_text(
        json.dumps(all_products, indent=1), "utf-8")
    n_s = sum(len(p["statements"]) for p in all_products)
    n_q = sum(len(p["questions"]) for p in all_products)
    print(f"{len(all_products)} cards -> {n_s} statements + {n_q} questions")


if __name__ == "__main__":
    main()
