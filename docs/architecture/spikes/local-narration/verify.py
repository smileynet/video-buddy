"""Verify retained receipts and decoded audio without repeating inference."""

import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np

here = Path(__file__).resolve().parent
repo = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], cwd=here, text=True
).strip()
frozen = subprocess.check_output(
    ["git", "show", "e5004d9:docs/architecture/spikes/local-narration/protocol.json"],
    cwd=repo,
)
protocol = json.loads((here / "protocol.json").read_text(encoding="utf-8"))
assert protocol == json.loads(frozen)
assert (
    hashlib.sha256((here / "reference.wav").read_bytes()).hexdigest()
    == protocol["reference"]["sha256"]
)
manifest = json.loads((here / "artifact-manifest.json").read_text())
summary = json.loads((here / "summary.json").read_text())
text = json.loads((here / "text-check.json").read_text())
checked = []
for model in ["qwen", "chatterbox"]:
    raw = json.loads((here / f"{model}-results.json").read_text())
    assert raw["status"] == "complete" and len(raw["cases"]) == 4
    warm = raw["cases"][1:]
    assert summary[model]["warm_wall_range_s"] == [
        min(x["wall_s"] for x in warm),
        max(x["wall_s"] for x in warm),
    ]
    assert (
        abs(
            summary[model]["sampled_peak_rss_gib"]
            - max(x["rss_bytes"] for x in raw["resource_samples"]) / 2**30
        )
        < 1e-10
    )
    for case, expected in zip(raw["cases"], protocol["cases"]):
        assert all(case[k] == expected[k] for k in ["id", "text", "seed"])
        item = next(
            a
            for a in manifest["audio"]
            if Path(a["file"]).stem == Path(case["file"]).stem
        )
        file = here / item["file"]
        assert hashlib.sha256(file.read_bytes()).hexdigest() == item["sha256"]
        pcm = subprocess.check_output(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(file),
                "-f",
                "s16le",
                "-acodec",
                "pcm_s16le",
                "-",
            ]
        )
        assert hashlib.sha256(pcm).hexdigest() == item["pcm_sha256"]
        audio = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
        assert len(audio) == case["samples"]
        assert abs(case["rtf"] - case["wall_s"] / case["duration_s"]) < 1e-10
        assert abs(float(np.abs(audio).max()) - case["peak_abs"]) < 1 / 32768 + 1e-7
        check = next(r for r in text["records"] if r["file"] == case["file"])
        assert check["audio_sha256"] == case["sha256"]
        assert check["pcm_sha256"] == item["pcm_sha256"]
        checked.append(case["file"])
result = {
    "verified_audio_cases": checked,
    "frozen_protocol_equal": True,
    "pcm_and_audio_hashes_match": True,
    "summary_receipts_checked": True,
    "human_listening": False,
    "quality_winner": None,
}
(here / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
print(
    "PASS: frozen protocol/reference; eight FLAC/PCM receipts; case timing/shape; resource summary; ASR linkage. No human quality verdict."
)
