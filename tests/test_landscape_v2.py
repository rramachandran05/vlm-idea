"""AC-O1: validate records-v2.json (v2 axes) against methods/schema-v2.md."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

EVIDENCE = {
    "observed", "derived-deterministic", "ai-inferred",
    "learned-representation", "external-contextual", "unknown",
}
FM_ROLE = {
    "direct-multimodal-encoder", "feature-extractor", "embedding-generator",
    "similarity-retrieval", "anomaly-detector",
    "temporal-change-representation", "downstream-task-backbone",
    "semantic-inference", "none", "unknown",
}
REASONING = {
    "describe", "compare", "detect", "integrate", "explain", "discriminate",
    "retrieve-analogs", "hypothesize", "test-hypotheses",
    "recommend-analysis", "unknown",
}


@pytest.fixture(scope="module")
def v2():
    return json.loads(
        (ROOT / "data" / "characterization" / "records-v2.json").read_text()
    )


@pytest.fixture(scope="module")
def corpus_ids():
    papers = json.loads((ROOT / "data" / "corpus" / "papers.json").read_text())
    return {p["id"] for p in papers}


def test_one_to_one_with_corpus(v2, corpus_ids):
    assert {r["id"] for r in v2} == corpus_ids


def test_corpus_extended_beyond_geodata(corpus_ids):
    papers = json.loads((ROOT / "data" / "corpus" / "papers.json").read_text())
    adjacent = [p for p in papers if "science-adjacent" in p["domains"]]
    assert len(adjacent) >= 10, "AC-O1 requires >=10 beyond-geodata works"


def test_axes_within_vocabulary(v2):
    for r in v2:
        assert r["evidence_to_lm"] and set(r["evidence_to_lm"]) <= EVIDENCE, r["id"]
        assert r["fm_role"] and set(r["fm_role"]) <= FM_ROLE, r["id"]
        assert r["reasoning_ops"] and set(r["reasoning_ops"]) <= REASONING, r["id"]


def test_fm_none_is_exclusive(v2):
    for r in v2:
        if "none" in r["fm_role"]:
            assert r["fm_role"] == ["none"], r["id"]


def test_new_reasoning_ops_are_represented(v2):
    ops = {o for r in v2 for o in r["reasoning_ops"]}
    for required in ("hypothesize", "explain", "integrate", "compare",
                     "discriminate", "recommend-analysis"):
        assert required in ops, f"no record exercises '{required}'"
