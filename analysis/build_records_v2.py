"""Apply the v2 characterization axes (methods/schema-v2.md) to every corpus
record and write data/characterization/records-v2.json.

The AXES mapping below is the characterization data (curated against the
stored verified abstracts, QC'd per methods/qc-protocol.md); this script
applies it deterministically and refuses to run if coverage is not 1:1 with
records.json.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# id: (evidence_to_lm, fm_role, reasoning_ops)
AXES = {
 "2106.10548": (["observed"], ["none"], ["describe"]),
 "2302.09208": (["observed"], ["none"], ["describe", "integrate"]),
 "2306.11029": (["observed"], ["embedding-generator"], ["describe"]),
 "2306.11300": (["observed"], ["embedding-generator"], ["describe"]),
 "2307.09758": (["observed"], ["none"], ["describe", "compare"]),
 "2307.15266": (["observed"], ["direct-multimodal-encoder"], ["describe"]),
 "2310.18340": (["observed"], ["embedding-generator"], ["describe"]),
 "2311.15826": (["observed"], ["direct-multimodal-encoder"], ["describe", "detect"]),
 "2311.16782": (["observed"], ["none"], ["describe"]),
 "2312.12222": (["observed", "ai-inferred"], ["none"], ["describe", "integrate"]),
 "2312.12856": (["observed"], ["embedding-generator"], ["describe"]),
 "2401.17600": (["observed"], ["none"], ["describe", "detect"]),
 "2402.02544": (["observed"], ["direct-multimodal-encoder"], ["describe", "integrate"]),
 "2402.11325": (["observed"], ["none"], ["describe"]),
 "2404.04326": (["observed"], ["none"], ["hypothesize"]),
 "2404.12606": (["observed", "ai-inferred"], ["downstream-task-backbone"], ["detect"]),
 "2406.04449": (["observed", "external-contextual"], ["direct-multimodal-encoder"], ["describe", "detect", "compare"]),
 "2406.09838": (["derived-deterministic"], ["none"], ["describe", "detect"]),
 "2406.11217": (["observed", "derived-deterministic"], ["none"], ["integrate", "explain"]),
 "2406.13181": (["observed", "external-contextual"], ["direct-multimodal-encoder"], ["describe", "integrate"]),
 "2406.18572": (["observed", "external-contextual"], ["none"], ["integrate"]),
 "2407.19719": (["observed"], ["embedding-generator"], ["compare"]),
 "2408.06292": (["derived-deterministic"], ["none"], ["hypothesize", "test-hypotheses", "explain"]),
 "2408.14744": (["observed"], ["none"], ["describe"]),
 "2409.00255": (["observed"], ["none"], ["describe", "integrate"]),
 "2410.01407": (["observed"], ["embedding-generator"], ["describe"]),
 "2410.02429": (["observed", "external-contextual"], ["none"], ["integrate", "detect", "explain"]),
 "2410.05080": (["observed"], ["none"], ["recommend-analysis"]),
 "2410.06234": (["observed"], ["direct-multimodal-encoder"], ["describe", "detect", "compare"]),
 "2410.08405": (["observed", "external-contextual"], ["direct-multimodal-encoder"], ["describe", "explain", "recommend-analysis"]),
 "2411.01511": (["observed", "ai-inferred"], ["none"], ["integrate", "recommend-analysis"]),
 "2411.03491": (["observed"], ["feature-extractor"], ["detect"]),
 "2411.19325": (["observed"], ["none"], ["describe", "detect"]),
 "2412.00465": (["observed", "external-contextual"], ["none"], ["describe", "integrate"]),
 "2501.13925": (["observed"], ["direct-multimodal-encoder"], ["describe", "detect"]),
 "2501.14905": (["observed", "external-contextual"], ["none"], ["describe", "detect"]),
 "2502.08168": (["observed"], ["none"], ["describe", "detect"]),
 "2502.09598": (["observed"], ["none"], ["describe"]),
 "2504.02866": (["observed", "external-contextual"], ["none"], ["describe", "integrate"]),
 "2504.06785": (["observed", "external-contextual"], ["none"], ["integrate"]),
 "2504.10568": (["observed", "external-contextual"], ["none"], ["describe", "explain", "recommend-analysis"]),
 "2504.19742": (["observed", "external-contextual"], ["embedding-generator"], ["integrate"]),
 "2505.03334": (["observed"], ["none"], ["detect"]),
 "2505.19358": (["observed"], ["embedding-generator"], ["describe"]),
 "2505.21089": (["observed"], ["none"], ["describe", "detect", "integrate"]),
 "2505.24223": (["observed"], ["none"], ["describe"]),
 "2506.00530": (["observed"], ["none"], ["integrate"]),
 "2506.12937": (["external-contextual"], ["none"], ["hypothesize", "test-hypotheses"]),
 "2506.20100": (["observed", "external-contextual"], ["none"], ["explain", "recommend-analysis", "integrate"]),
 "2507.15255": (["observed", "derived-deterministic"], ["none"], ["describe", "explain"]),
 "2507.16716": (["observed"], ["none"], ["describe"]),
 "2508.01380": (["observed", "external-contextual"], ["none"], ["unknown"]),
 "2509.01907": (["observed"], ["none"], ["detect", "compare"]),
 "2509.18123": (["observed", "derived-deterministic"], ["none"], ["detect", "describe", "explain"]),
 "2509.20628": (["observed", "ai-inferred"], ["none"], ["detect", "integrate"]),
 "2509.21609": (["observed", "external-contextual"], ["none"], ["describe"]),
 "2509.24378": (["observed", "learned-representation", "derived-deterministic"], ["feature-extractor"], ["detect", "explain"]),
 "2510.04281": (["observed", "derived-deterministic", "external-contextual"], ["direct-multimodal-encoder"], ["integrate", "explain"]),
 "2510.06931": (["observed"], ["none"], ["discriminate", "describe", "explain"]),
 "2512.03623": (["derived-deterministic"], ["none"], ["describe", "integrate"]),
 "2512.15977": (["observed"], ["none"], ["describe"]),
 "2601.01416": (["observed", "ai-inferred"], ["none"], ["detect", "integrate"]),
 "2601.18493": (["observed", "external-contextual"], ["none"], ["detect", "integrate"]),
 "2601.19099": (["observed"], ["none"], ["integrate"]),
 "2602.12843": (["observed", "ai-inferred"], ["direct-multimodal-encoder"], ["describe", "integrate"]),
 "2602.20066": (["observed", "external-contextual"], ["none"], ["integrate"]),
 "2603.11804": (["observed", "external-contextual"], ["direct-multimodal-encoder"], ["describe"]),
 "2603.13956": (["observed", "ai-inferred", "external-contextual"], ["downstream-task-backbone"], ["describe", "integrate", "explain"]),
 "2603.17108": (["observed"], ["none"], ["detect"]),
 "2604.16451": (["derived-deterministic"], ["none"], ["describe", "integrate", "explain"]),
 "2605.10772": (["observed"], ["none"], ["describe", "discriminate"]),
 "2606.13148": (["observed", "derived-deterministic", "external-contextual"], ["none"], ["integrate", "recommend-analysis"]),
 "2606.17246": (["observed", "ai-inferred", "external-contextual"], ["none"], ["integrate", "detect", "recommend-analysis"]),
 "2607.01584": (["external-contextual", "learned-representation"], ["none"], ["hypothesize", "recommend-analysis"]),
 "2608.00119": (["external-contextual", "derived-deterministic", "observed", "ai-inferred"], ["downstream-task-backbone"], ["integrate", "detect"]),
 "2608.21529": (["observed", "learned-representation"], ["embedding-generator", "similarity-retrieval"], ["describe", "retrieve-analogs"]),
}


def main() -> None:
    papers = json.loads((ROOT / "data" / "corpus" / "papers.json").read_text())
    ids = {p["id"] for p in papers}
    missing = ids - set(AXES)
    extra = set(AXES) - ids
    if missing or extra:
        raise SystemExit(f"coverage mismatch: missing={sorted(missing)} extra={sorted(extra)}")
    out = [
        {"id": i, "evidence_to_lm": e, "fm_role": f, "reasoning_ops": r}
        for i, (e, f, r) in sorted(AXES.items())
    ]
    path = ROOT / "data" / "characterization" / "records-v2.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"{len(out)} v2-axis records -> {path}")


if __name__ == "__main__":
    main()
