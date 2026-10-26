"""Validate retained reference recovery and scalar edit-distance totals."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent


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


checks = 0
restored = []
for rfile, sfile, bundle in [
    ("references.json", "scores.json", "fixtures.zip"),
    ("references-natural.json", "scores-natural.json", "natural-fixtures.zip"),
]:
    refs = {f["id"]: f for f in json.loads((HERE / rfile).read_text())["fixtures"]}
    with tempfile.TemporaryDirectory(prefix="vb-speech-restore-") as target:
        with zipfile.ZipFile(HERE / bundle) as archive:
            for ref in refs.values():
                name = Path(ref["path"]).name
                path = Path(target) / name
                path.write_bytes(archive.read(name))
                assert hashlib.sha256(path.read_bytes()).hexdigest() == ref["sha256"]
                restored.append(
                    {"fixture": ref["id"], "sha256": ref["sha256"], "restored": True}
                )
    for option in json.loads((HERE / sfile).read_text()):
        rawfile = (
            f"raw-{option['option']}{'-natural' if 'natural' in rfile else ''}.json"
        )
        raw = json.loads((HERE / rawfile).read_text())
        assert (
            raw["references_sha256"]
            == hashlib.sha256((HERE / rfile).read_bytes()).hexdigest()
        )
        assert (
            raw["protocol_sha256"]
            == hashlib.sha256((HERE / "protocol.json").read_bytes()).hexdigest()
        )
        for row in option["rows"]:
            ref = refs[row["fixture"]]
            if ref["text"] is None:
                continue
            a, b = tokens(ref["text"]), tokens(row["text"])
            assert distance(a, b) == row["word_counts"]["errors"]
            assert distance("".join(a), "".join(b)) == row["character_counts"]["errors"]
            checks += 2
tutorial_refs = json.loads((HERE / "references-tutorial.json").read_text())["fixtures"]
with tempfile.TemporaryDirectory(prefix="vb-speech-restore-") as target:
    with zipfile.ZipFile(HERE / "tutorial-fixture.zip") as archive:
        for ref in tutorial_refs:
            name = Path(ref["path"]).name
            path = Path(target) / name
            path.write_bytes(archive.read(name))
            assert hashlib.sha256(path.read_bytes()).hexdigest() == ref["sha256"]
            restored.append(
                {"fixture": ref["id"], "sha256": ref["sha256"], "restored": True}
            )
for option in ["base", "small", "turbo"]:
    raw = json.loads((HERE / f"raw-{option}-tutorial.json").read_text())
    assert (
        raw["references_sha256"]
        == hashlib.sha256((HERE / "references-tutorial.json").read_bytes()).hexdigest()
    )
assert not subprocess.check_output(
    [
        "git",
        "diff",
        "9a23e51",
        "--",
        str(HERE / "protocol.json"),
        str(HERE / "references.json"),
    ]
)
(HERE / "score-check.json").write_text(
    json.dumps(
        {
            "independent_scalar_edit_checks": checks,
            "passed": True,
            "original_protocol_references_unchanged_from": "9a23e51",
            "frozen": True,
        },
        indent=2,
    )
    + "\n"
)
(HERE / "restore-check.json").write_text(json.dumps(restored, indent=2) + "\n")
print(
    f"PASS: {checks} edit-distance checks, {len(restored)} restored inputs, raw/frozen reference hashes"
)

review_path = HERE / "review-manifest.json"
if review_path.exists():
    packet = json.loads(review_path.read_text())
    restored_review = []
    with tempfile.TemporaryDirectory(prefix="vb-speech-listening-") as target:
        for clip in packet["clips"]:
            with zipfile.ZipFile(HERE / f"review-inputs-{clip['id']}.zip") as archive:
                path = Path(target) / Path(clip["audio"]).name
                path.write_bytes(archive.read(path.name))
                assert hashlib.sha256(path.read_bytes()).hexdigest() == clip["sha256"]
                restored_review.append(clip["id"])
    html = (HERE / "reference-review.html").read_text()
    embedded = json.loads(
        html.split('<script id="reference-data" type="application/json">')[1].split(
            "</script>"
        )[0]
    )
    assert (
        embedded["manifest_sha256"]
        == hashlib.sha256(review_path.read_bytes()).hexdigest()
    )
    assert embedded["clips"] == packet["clips"]
    (HERE / "review-restore-check.json").write_text(
        json.dumps(
            {
                "restored": restored_review,
                "count": len(restored_review),
                "total_seconds": sum(c["duration"] for c in packet["clips"]),
                "manifest_sha256": embedded["manifest_sha256"],
                "embedded_manifest_matches": True,
                "human_review_completed": False,
                "new_model_inference": False,
            },
            indent=2,
        )
        + "\n"
    )
    print(
        "PASS:3 additional listening-pack restores and embedded manifest; human review remains unverified"
    )
