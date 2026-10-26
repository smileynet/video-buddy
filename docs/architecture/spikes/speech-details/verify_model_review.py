"""Verify machine-reference provenance and scores without certifying speech truth."""

import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(text):
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())


def distance(a, b):
    grid = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        grid[i][0] = i
    for j in range(len(b) + 1):
        grid[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            grid[i][j] = min(
                grid[i - 1][j] + 1,
                grid[i][j - 1] + 1,
                grid[i - 1][j - 1] + (a[i - 1] != b[j - 1]),
            )
    return grid[-1][-1]


protocol = json.loads((HERE / "model-review-protocol.json").read_text())
raw = json.loads((HERE / "model-review-raw.json").read_text())
refs = json.loads((HERE / "model-reviewed-references.json").read_text())
comparison = json.loads((HERE / "model-review-comparison.json").read_text())
eligible = json.loads((HERE / "audio-review-eligibility.json").read_text())
assert (
    refs["human_verified"]
    is raw["human_verified"]
    is comparison["human_verified"]
    is False
)
assert raw["protocol_sha256"] == sha(HERE / "model-review-protocol.json")
assert refs["raw_sha256"] == sha(HERE / "model-review-raw.json")
assert raw["model_sha256"] == eligible["files"]["model.int8.onnx"]["sha256"]
assert raw["tokens_sha256"] == eligible["files"]["tokens.txt"]["sha256"]
assert not subprocess.check_output(
    [
        "git",
        "diff",
        "a18749f",
        "--",
        str(HERE / "model-reviewed-references.json"),
        str(HERE / "model-review-raw.json"),
    ]
)
reference = {r["id"]: r for r in refs["fixtures"]}
for clip, result in zip(protocol["clips"], raw["results"]):
    assert sha(Path(clip["path"])) == clip["sha256"] == result["audio_sha256"]
    assert len(result["tokens"]) == len(result["timestamps"])
    assert all(0 <= t <= result["duration"] for t in result["timestamps"])
    assert all(a <= b for a, b in zip(result["timestamps"], result["timestamps"][1:]))
checks = 0
for candidate in comparison["candidates"]:
    candidate_raw = json.loads(
        (HERE / f"raw-{candidate['option']}-model-reviewed.json").read_text()
    )
    assert candidate_raw["references_sha256"] == sha(
        HERE / "model-reviewed-references.json"
    )
    assert (
        candidate_raw["settings"]
        == json.loads((HERE / "protocol.json").read_text())["settings"]
    )
    total = 0
    for row in candidate["records"]:
        a, b = tokens(reference[row["clip"]]["text"]), tokens(row["text"])
        assert distance(a, b) == row["word_edit_distance"]
        assert distance("".join(a), "".join(b)) == row["character_edit_distance"]
        total += len(a)
        checks += 2
    assert total == candidate["reference_words"] == 180
assert all(row["wer"] is None for row in comparison["captions"])
(HERE / "model-review-verification.json").write_text(
    json.dumps(
        {
            "passed": True,
            "independent_edit_distance_checks": checks,
            "audio_hashes": 3,
            "reference_freeze": "a18749f",
            "original_model_reference_unchanged": True,
            "human_verified": False,
            "claim": "provenance and arithmetic verified, not spoken correctness",
        },
        indent=2,
    )
    + "\n"
)
print(
    f"PASS:{checks} score checks,3 audio hashes,reviewer identity,locked refs; human verification remains false"
)
