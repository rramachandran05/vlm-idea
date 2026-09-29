"""Regenerate the prioritization score table (D6) from prioritization/scores.json.

Usage: python3 analysis/score_table.py            # print markdown table
       python3 analysis/score_table.py --check    # exit 1 if scoring.md table is stale
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIMS = [
    ("application_value", "App"),
    ("scientific_relevance", "Sci"),
    ("novelty", "Nov"),
    ("scalability", "Scale"),
    ("data_availability", "Avail"),
    ("grounding_quality", "Ground"),
    ("construction_feasibility", "Feas"),
]


def build_table() -> str:
    scores = json.loads((ROOT / "prioritization" / "scores.json").read_text())
    for s in scores:
        s["total"] = sum(s[d] for d, _ in DIMS)
    scores.sort(key=lambda s: (-s["total"], s["card"]))
    lines = [
        "| Rank | Card | " + " | ".join(h for _, h in DIMS) + " | Total |",
        "|---|---|" + "---|" * (len(DIMS) + 1),
    ]
    for i, s in enumerate(scores, 1):
        lines.append(
            f"| {i} | `{s['card']}` | "
            + " | ".join(str(s[d]) for d, _ in DIMS)
            + f" | **{s['total']}** |"
        )
    return "\n".join(lines)


def main() -> None:
    table = build_table()
    if "--check" in sys.argv:
        doc = (ROOT / "prioritization" / "scoring.md").read_text()
        if table not in doc:
            print("scoring.md table is stale — regenerate with score_table.py")
            raise SystemExit(1)
        print("scoring.md table matches scores.json")
        return
    print(table)


if __name__ == "__main__":
    main()
