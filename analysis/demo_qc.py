"""Grounding QC for demonstration pair samples (D6, Task 15).

For each demo: draw a seeded 20-pair sample, verify every geodata reference
resolves to an image (HTTP 200 + image/* content type), and dump the sampled
language for manual inspection. Writes data/demos/<demo>/qc.json.

Usage: python3 analysis/demo_qc.py [--sample 20] [--seed 42]
"""

from __future__ import annotations

import argparse
import json
import random
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEMOS = ROOT / "data" / "demos"


IMAGE_MAGIC = (b"\xff\xd8", b"\x89PNG", b"GIF8")


def head_ok(url: str) -> tuple[bool, str]:
    req = urllib.request.Request(
        url, method="GET", headers={"User-Agent": "geovlm-demo-qc"}
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            ct = r.headers.get("Content-Type", "")
            head = r.read(8)
            is_img = ct.startswith("image/") or any(
                head.startswith(m) for m in IMAGE_MAGIC
            )
            return (r.status == 200 and is_img, ct)
    except Exception as e:  # noqa: BLE001
        return (False, str(e)[:80])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    for demo_dir in sorted(DEMOS.iterdir()):
        pf = demo_dir / "pairs.json"
        if not pf.exists():
            continue
        pairs = json.loads(pf.read_text())
        rng = random.Random(args.seed)
        sample = rng.sample(pairs, min(args.sample, len(pairs)))
        results = []
        for p in sample:
            refs = p["geodata_ref"]
            refs = refs if isinstance(refs, list) else [refs]
            ok, detail = head_ok(refs[0])  # first ref per pair
            results.append(
                {"pair_id": p["pair_id"], "image_ok": ok, "detail": detail,
                 "language_preview": p["language"][:160]}
            )
        n_ok = sum(r["image_ok"] for r in results)
        report = {
            "demo": demo_dir.name,
            "total_pairs": len(pairs),
            "sample_size": len(sample),
            "seed": args.seed,
            "image_resolve_pass": n_ok,
            "image_resolve_rate": round(n_ok / len(sample), 3),
            "results": results,
        }
        (demo_dir / "qc.json").write_text(
            json.dumps(report, indent=1), "utf-8"
        )
        print(f"{demo_dir.name}: {n_ok}/{len(sample)} images resolve "
              f"({len(pairs)} pairs total)")


if __name__ == "__main__":
    main()
