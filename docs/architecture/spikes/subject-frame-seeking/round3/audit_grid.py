"""Core seek audit, retaining numerical/request rounding discrepancies."""

from bisect import bisect_left
import json
from pathlib import Path
import time

import numpy as np
from PIL import Image

from video_buddy.frames.capture import _extract_single_frame

ROOT = Path(__file__).resolve().parent
protocol = json.loads((ROOT / "protocol.json").read_text())
reference = json.loads((ROOT / "reference.json").read_text())
report = {}
for case in protocol["cases"]:
    kind = case["id"]
    folder = Path(".scratch") / case["folder"]
    cap = reference[kind]["capture"]
    frames = cap["frames"]
    pts = [f["pts_s"] for f in frames]
    out = folder / "grid-audit"
    out.mkdir(exist_ok=True)
    requests = {}
    for budget in protocol["budgets"]:
        for phase in protocol["offsets"]:
            for i in range(budget):
                request = (
                    cap["start"] + (i + phase) * (cap["end"] - cap["start"]) / budget
                )
                key = f"{request:.9f}"
                if key in requests:
                    continue
                path = out / f"seek_{key}.jpg"
                start = time.perf_counter()
                _extract_single_frame(Path(cap["source"]), request, path)
                seconds = time.perf_counter() - start
                expected = min(bisect_left(pts, request), len(pts) - 1)
                actual = np.array(Image.open(path), dtype=float)
                checks = []
                for index in range(
                    max(0, expected - 1), min(len(frames), expected + 2)
                ):
                    other = np.array(
                        Image.open(folder / frames[index]["filename"]), dtype=float
                    )
                    checks.append(
                        dict(index=index, error=float(np.abs(actual - other).mean()))
                    )
                requests[key] = dict(
                    request=request,
                    seconds=seconds,
                    expected_index=expected,
                    expected_error=next(
                        c["error"] for c in checks if c["index"] == expected
                    ),
                    neighboring_matches=checks,
                )
    report[kind] = requests
    (ROOT / "grid-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        kind,
        len(requests),
        "nonidentical expected",
        sum(r["expected_error"] != 0 for r in requests.values()),
        flush=True,
    )
