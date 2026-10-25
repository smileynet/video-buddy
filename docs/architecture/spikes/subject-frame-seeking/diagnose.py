"""Post-hoc diagnostic: bypass only the global inclusion veto, retaining hashes."""

import json
from pathlib import Path

from video_buddy.frames import capture

root = Path(__file__).resolve().parent
report = json.loads((root / "results.json").read_text(encoding="utf-8"))
original = capture.score_frame


def permit(path):
    return {**original(path), "should_include": True}


capture.score_frame = permit
results = []
for row in report["cases"]:
    case = row["case"]
    folder = Path(".scratch") / case["folder"]
    result = {"case": case["id"]}
    for mode, files in [
        ("sparse", sorted((folder / "baseline").glob("frame_*.jpg"))),
        ("dense", sorted(folder.glob("frame_*.jpg"))),
    ]:
        selected = capture.select_frames(files, video_id=case["source"], max_frames=4)
        times = [r["timestamp_ms"] / 1000 for r in selected]
        covered = [
            s["id"]
            for s in case["states"]
            if any(a <= t < b for a, b in s["spans"] for t in times)
        ]
        result[mode] = dict(times=times, covered=covered)
    results.append(result)
(root / "posthoc-veto-ablation.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results))
