import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "skill-evals.jsonl"


def test_behavior_evals_are_parseable_and_cover_core_pressures():
    records = [json.loads(line) for line in EVALS.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(records) >= 8
    for record in records:
        assert {"id", "prompt", "expected_behavior", "forbidden_behavior", "pass_criteria"} <= set(record)
    ids = {record["id"] for record in records}
    required = {
        "missing-sample-size",
        "decorative-ai-slop",
        "metadata-only-600dpi",
        "generative-evidence",
        "portrait-landscape-invariance",
        "journal-rule-conflict",
    }
    assert required <= ids
