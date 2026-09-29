"""AC cross-cutting: committed artifacts regenerate from the structured data.

Live-API collection steps are excluded by design (their outputs vary by run
date); what must reproduce byte-for-byte is everything downstream of the
committed data files.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(script, *args):
    return subprocess.run(
        [sys.executable, str(ROOT / "analysis" / script), *args],
        capture_output=True, text=True, cwd=ROOT,
    )


def test_curation_reproduces_committed_corpus():
    before = (ROOT / "data" / "corpus" / "papers.json").read_bytes()
    r = run("curate_corpus.py")
    assert r.returncode == 0, r.stderr
    after = (ROOT / "data" / "corpus" / "papers.json").read_bytes()
    assert before == after, "papers.json changed on re-curation"


def test_score_table_in_doc_matches_scores_json():
    r = run("score_table.py", "--check")
    assert r.returncode == 0, r.stdout + r.stderr


def test_corpus_stats_runs_and_counts_match():
    r = run("corpus_stats.py")
    assert r.returncode == 0, r.stderr
    records = json.loads(
        (ROOT / "data" / "characterization" / "records.json").read_text()
    )
    assert f"records: {len(records)}" in r.stdout


def test_demo_pairs_meet_ac_thresholds():
    demos = sorted((ROOT / "data" / "demos").iterdir())
    selected = {
        "eonet-worldview-event-narration", "pager-shakemap-impact-briefs",
        "cmr-summary-product-grounding", "afd-hydro-outlook-pairs",
    }
    assert {d.name for d in demos if d.is_dir()} == selected
    for d in demos:
        pairs = json.loads((d / "pairs.json").read_text())
        assert len(pairs) >= 100, f"{d.name}: only {len(pairs)} pairs"
        qc = json.loads((d / "qc.json").read_text())
        assert qc["sample_size"] >= 20, d.name
        assert qc["image_resolve_rate"] == 1.0, (
            f"{d.name}: grounding QC not clean ({qc['image_resolve_rate']})"
        )
        readme = " ".join((d / "README.md").read_text().split())
        assert "QC" in readme and "manually reviewed" in readme, d.name


def test_demo_pairs_have_required_fields():
    for d in (ROOT / "data" / "demos").iterdir():
        if not d.is_dir():
            continue
        for p in json.loads((d / "pairs.json").read_text()):
            for f in ("pair_id", "geodata_ref", "language", "source_url"):
                assert p.get(f), f"{d.name}: pair missing {f}"
            assert len(p["language"]) > 40, f"{d.name}: thin language"
