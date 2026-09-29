"""AC-D2/D3: validate data/characterization/records.json against methods/schema.md."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

LANGUAGE_SOURCE = {
    "labels-as-language", "structured-observations", "expert-interpretation",
    "scientific-knowledge", "reports", "decision-workflow", "crowd-caption",
    "web-text", "llm-generated", "unknown",
}
PAIR_GENERATION = {
    "deterministic", "template", "combinatorial", "llm-synthesis",
    "weak-supervision", "knowledge-based", "manual", "unknown",
}
ALIGNMENT = {"spatial", "temporal", "entity", "event", "unknown"}
GEODATA = {
    "optical-satellite", "sar", "hyperspectral", "aerial", "street-level",
    "weather-climate-field", "dem-terrain", "map-vector", "multi-source",
    "non-geospatial", "in-situ-timeseries",  # v2 extension
    "unknown",
}
SCALABILITY = {"high", "medium", "low", "unknown"}
MATURITY = {
    "benchmark-research", "domain-research", "workflow-relevant",
    "decision-support-prototype", "operational-prototype", "deployed",
}
NOMINAL = {
    "vqa", "captioning", "retrieval", "classification", "grounding",
    "change-description", "instruction-following", "detection",
    "segmentation", "forecasting", "other",
}
REQUIRED = {
    "id", "geodata_type", "language_source", "semantic_relationship",
    "alignment", "pair_generation", "scalability", "scalability_note",
    "nominal_task", "capability", "use_enabled", "maturity",
    "novelty_data", "novelty_task", "novelty_science", "novelty_application",
    "negative_case", "negative_reason", "note",
}


@pytest.fixture(scope="module")
def records():
    return json.loads(
        (ROOT / "data" / "characterization" / "records.json").read_text()
    )


@pytest.fixture(scope="module")
def corpus_ids():
    papers = json.loads((ROOT / "data" / "corpus" / "papers.json").read_text())
    return {p["id"] for p in papers}


def test_one_to_one_with_corpus(records, corpus_ids):
    rec_ids = {r["id"] for r in records}
    assert rec_ids == corpus_ids


def test_all_fields_present(records):
    for r in records:
        missing = REQUIRED - set(r)
        assert not missing, f"{r['id']}: missing {missing}"


def test_enums_within_vocabulary(records):
    for r in records:
        assert set(r["geodata_type"]) <= GEODATA, r["id"]
        assert set(r["language_source"]) <= LANGUAGE_SOURCE, r["id"]
        assert set(r["alignment"]) <= ALIGNMENT, r["id"]
        assert set(r["pair_generation"]) <= PAIR_GENERATION, r["id"]
        assert r["scalability"] in SCALABILITY, r["id"]
        assert r["maturity"] in MATURITY, r["id"]
        assert set(r["nominal_task"]) <= NOMINAL, r["id"]


def test_no_blank_values(records):
    for r in records:
        for f in ("geodata_type", "language_source", "alignment",
                  "pair_generation", "nominal_task"):
            assert r[f], f"{r['id']}: empty {f} (use ['unknown'])"
        for f in ("semantic_relationship", "capability", "use_enabled",
                  "scalability_note"):
            assert r[f].strip(), f"{r['id']}: blank {f}"


def test_capability_not_a_task_restatement(records):
    for r in records:
        assert r["capability"].lower() not in {
            t.lower() for t in r["nominal_task"]
        }, r["id"]
        assert len(r["capability"]) > 20, f"{r['id']}: capability too thin"


def test_novelty_scores_in_range(records):
    for r in records:
        for dim in ("data", "task", "science", "application"):
            v = r[f"novelty_{dim}"]
            assert isinstance(v, int) and 0 <= v <= 3, f"{r['id']}: {dim}={v}"


def test_negative_cases_have_reasons(records):
    negatives = [r for r in records if r["negative_case"]]
    assert len(negatives) >= 5, "AC-D3 requires >=5 documented negative cases"
    for r in negatives:
        assert len(r["negative_reason"]) > 30, r["id"]
    for r in records:
        if not r["negative_case"]:
            assert r["negative_reason"] == "", r["id"]
