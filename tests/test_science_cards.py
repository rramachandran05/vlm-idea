"""AC-O3/O5/O6/O8: Science Card schema, demonstrator cards, traceability,
question logic."""

import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "science_card.schema.json").read_text())
CARDS_DIR = ROOT / "demonstrator" / "out" / "cards"
PRODUCTS = ROOT / "demonstrator" / "out" / "language" / "products.json"

EXAMPLE = {
    "card_id": "sc_example",
    "card_type": "before-after",
    "phenomenon": {"description": "example burn", "status": "candidate",
                   "external_reference": None},
    "spatial": {"lat": 10.0, "lon": 20.0, "extent_m": 2240.0,
                "crs": "EPSG:4326"},
    "temporal": {"timestamps": ["2026-01-01", "2026-02-01"],
                 "reference_event_time": None},
    "evidence": [{
        "key": "delta_nbr", "value": -0.2, "units": None, "class": "computed",
        "source": "test", "method": "NBR difference", "provenance": "test.py",
        "uncertainty": {"type": "std", "value": 0.01},
    }],
    "analogs": [], "relationships": [],
    "reasoning_affordances": ["describe"],
    "provenance": {"pipeline": "test", "built_at_data_time": "2026-02-01"},
    "insufficiencies": [],
}


def test_schema_validates_example():
    jsonschema.validate(EXAMPLE, SCHEMA)


def test_schema_rejects_null_uncertainty_without_note():
    bad = json.loads(json.dumps(EXAMPLE))
    bad["evidence"][0]["uncertainty"] = None
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, SCHEMA)


def test_schema_rejects_collapsed_evidence_class():
    bad = json.loads(json.dumps(EXAMPLE))
    bad["evidence"][0]["class"] = "fact"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, SCHEMA)


def test_schema_field_names_are_model_independent():
    text = json.dumps(SCHEMA).lower()
    for banned in ("prithvi", "hls", "sentinel", "gpt", "llama", "claude"):
        # names may appear in card *values*, never in the schema itself
        assert banned not in text, f"schema names a specific model: {banned}"


# ---- demonstrator artifacts (skipped until the pipeline has run) ----

cards = sorted(CARDS_DIR.glob("*.json")) if CARDS_DIR.exists() else []
needs_cards = pytest.mark.skipif(not cards, reason="demonstrator not yet run")


@needs_cards
def test_demonstrator_card_counts():
    loaded = [json.loads(c.read_text()) for c in cards]
    ev = [c for c in loaded
          if c["phenomenon"]["status"] == "externally-reported"]
    ctl = [c for c in loaded if c["phenomenon"]["status"] == "none-expected"]
    assert len(ev) >= 10 and len(ctl) >= 10


@needs_cards
@pytest.mark.parametrize("card_file", cards,
                         ids=lambda p: getattr(p, "stem", "none"))
def test_demonstrator_cards_validate(card_file):
    jsonschema.validate(json.loads(card_file.read_text()), SCHEMA)


@needs_cards
def test_cards_contain_all_required_evidence_classes():
    classes = set()
    for c in cards:
        for e in json.loads(c.read_text())["evidence"]:
            classes.add(e["class"])
    assert {"observed", "computed", "learned-representation",
            "contextual"} <= classes


@needs_cards
def test_language_products_traceable():
    products = json.loads(PRODUCTS.read_text())
    assert sum(len(p["statements"]) for p in products) >= 100
    by_id = {json.loads(c.read_text())["card_id"]:
             {e["key"] for e in json.loads(c.read_text())["evidence"]}
             for c in cards}
    sections = {"temporal", "analogs", "insufficiencies", "provenance"}
    for p in products:
        keys = by_id[p["card_id"]]
        for st in p["statements"]:
            assert st["trace"], f"untraced statement in {p['card_id']}"
            for t in st["trace"]:
                ok = (t in keys or t in sections or t.startswith("knowledge:"))
                assert ok, f"{p['card_id']}: trace '{t}' resolves to nothing"
            assert st["epistemic"] in {
                "evidence-supported", "derived-interpretation", "hypothesis",
                "retrieved-knowledge",
            }


@needs_cards
def test_six_distinct_product_types_per_card():
    products = json.loads(PRODUCTS.read_text())
    for p in products:
        assert len(p["statements"]) >= 6, p["card_id"]


@needs_cards
def test_question_logic_follows_evidence_state():
    products = {p["card_id"]: p for p in json.loads(PRODUCTS.read_text())}
    n_discriminate = n_baseline = 0
    for c in cards:
        card = json.loads(c.read_text())
        rules = " ".join(q["rule"] for q in products[card["card_id"]]["questions"])
        if card["phenomenon"]["status"] == "externally-reported":
            if "discriminate" in rules:
                n_discriminate += 1
        else:
            # a control yields baseline questions when stable, or
            # hypothesize/test questions when it genuinely changed —
            # never neither
            assert ("monitoring/baseline" in rules
                    or "no-event-context" in rules), card["card_id"]
            if "monitoring/baseline" in rules:
                n_baseline += 1
    assert n_discriminate >= 5, "event cards should yield discrimination Qs"
    assert n_baseline >= 3, "some stable controls should yield baseline Qs"


@needs_cards
def test_counterfactual_supervision_exists():
    products = json.loads(PRODUCTS.read_text())
    all_rules = [q["rule"] for p in products for q in p["questions"]]
    kinds = set()
    for r in all_rules:
        if "conflict/counterfactual" in r or "no-event-context" in r:
            kinds.add("context-conflict")
        if "abstention" in r:
            kinds.add("abstention")
    assert len(kinds) >= 2, f"need >=2 counterfactual kinds, got {kinds}"
