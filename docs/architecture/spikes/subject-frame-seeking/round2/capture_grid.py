"""Audit actual core seeks against the common decode for every grid request."""

from bisect import bisect_left
import json
from pathlib import Path
import time

import numpy as np
from PIL import Image

from video_buddy.frames.capture import _extract_single_frame

root = Path(__file__).resolve().parent
config = json.loads((root / "protocol.json").read_text())
work = Path(".scratch/seek-round2")
report = {}
for kind in config["clips"]:
    cap = json.loads((work / kind / "decoded/capture.json").read_text())
    times = [r["pts_s"] for r in cap["frames"]]
    folder = work / kind / "grids"
    folder.mkdir(exist_ok=True)
    cache = {}
    cells = {}
    for budget in config["budgets"]:
        for phase in config["grid_offsets"]:
            elapsed = 0
            errors = []
            for i in range(budget):
                request = (i + phase) * 6 / budget
                index = min(bisect_left(times, request), len(times) - 1)
                key = f"{request:.6f}"
                if key not in cache:
                    path = folder / f"seek_{key}.jpg"
                    start = time.perf_counter()
                    _extract_single_frame(root / f"{kind}.mp4", request, path)
                    seconds = time.perf_counter() - start
                    expected = (
                        work / kind / "decoded" / cap["frames"][index]["filename"]
                    )
                    error = float(
                        np.abs(
                            np.array(Image.open(path), dtype=float)
                            - np.array(Image.open(expected), dtype=float)
                        ).mean()
                    )
                    cache[key] = dict(
                        seconds=seconds,
                        mean_absolute_pixel_error=error,
                        expected_index=index,
                    )
                elapsed += cache[key]["seconds"]
                errors.append(cache[key]["mean_absolute_pixel_error"])
            cells[f"{budget}/{phase}"] = dict(
                sum_unique_seek_cost_s=elapsed,
                max_mean_absolute_pixel_error=max(errors),
            )
    report[kind] = dict(unique_requests=cache, configurations=cells)
    (root / "grid-capture-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        kind,
        "unique seeks",
        len(cache),
        "max error",
        max(v["mean_absolute_pixel_error"] for v in cache.values()),
        flush=True,
    )
