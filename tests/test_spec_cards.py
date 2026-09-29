"""AC-D4/D5: validate opportunity cards against the Spec Card template."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CARDS = sorted((ROOT / "opportunities" / "cards").glob("*.md"))

FIELDS = [
    "Card ID / name", "Application need", "Required capability",
    "Geospatial evidence", "Information source", "Semantic relationship",
    "Alignment", "Supervision generation", "Scaling strategy",
    "Grounding-quality risks", "Negative-control plan",
    "VLM adaptation family", "Application evaluation", "Novelty assessment",
    "Feasibility notes", "Metapattern lineage",
]


def test_at_least_ten_cards():
    assert len(CARDS) >= 10, f"only {len(CARDS)} cards"


@pytest.mark.parametrize("card", CARDS, ids=lambda p: p.stem)
def test_card_has_all_template_fields(card):
    text = card.read_text()
    for f in FIELDS:
        assert f in text, f"{card.name}: missing field '{f}'"


@pytest.mark.parametrize("card", CARDS, ids=lambda p: p.stem)
def test_card_names_generating_combination(card):
    text = card.read_text()
    assert "**Generating combination:**" in text, card.name
    combo_line = [
        line for line in text.splitlines()
        if line.startswith("**Generating combination:**")
    ][0]
    # need x observation x information source x mechanism
    assert combo_line.count("×") >= 3, f"{card.name}: combination incomplete"


@pytest.mark.parametrize("card", CARDS, ids=lambda p: p.stem)
def test_card_cites_metapattern(card):
    assert "MP-" in card.read_text(), card.name


def test_scores_cover_all_cards():
    scores = json.loads(
        (ROOT / "prioritization" / "scores.json").read_text()
    )
    assert {s["card"] for s in scores} == {c.stem for c in CARDS}
