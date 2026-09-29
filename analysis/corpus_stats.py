"""Corpus-level statistics (D2/D3). Every count quoted in patterns/ and
prioritization/ artifacts regenerates from here.

Usage: python3 analysis/corpus_stats.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    records = json.loads(
        (ROOT / "data" / "characterization" / "records.json").read_text()
    )
    papers = json.loads((ROOT / "data" / "corpus" / "papers.json").read_text())
    print(f"records: {len(records)}  corpus: {len(papers)}")

    def tally(field, listy=True):
        c = Counter()
        for r in records:
            vals = r[field] if listy else [r[field]]
            c.update(vals)
        return c

    for field, listy in [
        ("maturity", False), ("language_source", True),
        ("pair_generation", True), ("alignment", True),
        ("scalability", False), ("geodata_type", True),
    ]:
        print(f"\n{field}:")
        for v, n in tally(field, listy).most_common():
            print(f"  {v}: {n}")

    years = Counter(p["year"] for p in papers)
    print("\nyear:", dict(sorted(years.items())))

    neg = [r["id"] for r in records if r["negative_case"]]
    print(f"\nnegative cases ({len(neg)}):", neg)

    none_use = [r["id"] for r in records if r["use_enabled"] == "none identified"]
    print(f"\nuse_enabled == none identified ({len(none_use)}):")
    by_mat = Counter(
        r["maturity"] for r in records if r["use_enabled"] == "none identified"
    )
    print("  by maturity:", dict(by_mat))

    hi_mat = [
        r["id"] for r in records
        if r["maturity"] in (
            "decision-support-prototype", "operational-prototype", "deployed"
        )
    ]
    print(f"\ndecision-support prototype or beyond ({len(hi_mat)}):", hi_mat)

    unk = Counter()
    for r in records:
        for f in ("language_source", "pair_generation", "alignment",
                  "geodata_type"):
            if "unknown" in r[f]:
                unk[f] += 1
        if r["scalability"] == "unknown":
            unk["scalability"] += 1
    print("\nrecords with 'unknown' per axis:", dict(unk))


if __name__ == "__main__":
    main()
