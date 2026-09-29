"""AC-D1: validate data/corpus/papers.json against methods/schema.md."""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOMAINS = {
    "earth-observation-general",
    "agriculture",
    "disasters",
    "urban",
    "mapping",
    "infrastructure",
    "defense-intelligence",
    "science-adjacent",  # v2 extension, methods/schema-v2.md
}
REQUIRED = {"id", "source", "title", "year", "month", "venue", "domains", "url"}


@pytest.fixture(scope="module")
def papers():
    return json.loads((ROOT / "data" / "corpus" / "papers.json").read_text())


def test_corpus_size(papers):
    assert len(papers) >= 40


def test_required_fields_present_and_nonempty(papers):
    for p in papers:
        missing = REQUIRED - set(p)
        assert not missing, f"{p.get('id')}: missing {missing}"
        for f in REQUIRED:
            assert p[f] not in ("", None, []), f"{p['id']}: empty {f}"


def test_ids_unique_and_wellformed(papers):
    ids = [p["id"] for p in papers]
    assert len(ids) == len(set(ids))
    for i in ids:
        assert re.fullmatch(r"\d{4}\.\d{4,5}", i) or i.startswith("doi:"), i


def test_year_in_window(papers):
    for p in papers:
        assert 2021 <= p["year"] <= 2026, f"{p['id']}: year {p['year']}"


def test_domains_in_vocabulary(papers):
    for p in papers:
        assert p["domains"], f"{p['id']}: no domain tag"
        bad = set(p["domains"]) - DOMAINS
        assert not bad, f"{p['id']}: unknown domains {bad}"


def test_source_wellformed(papers):
    for p in papers:
        assert p["source"] == "arxiv" or p["source"].startswith("other:")


def test_all_domains_represented_or_justified(papers):
    covered = {d for p in papers for d in p["domains"]}
    missing = DOMAINS - covered
    if missing:
        log = (ROOT / "data" / "corpus" / "collection-log.md").read_text()
        for d in missing:
            assert d in log, f"domain {d} absent and not justified in log"


def test_abstracts_cover_corpus(papers):
    abstracts = json.loads(
        (ROOT / "data" / "corpus" / "abstracts.json").read_text()
    )
    for p in papers:
        assert abstracts.get(p["id"]), f"{p['id']}: no abstract stored"
