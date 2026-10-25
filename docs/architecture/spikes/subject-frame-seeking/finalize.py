"""Rescore retained outputs after timestamp-boundary QA; capture time controls."""

import hashlib
import io
import json
from pathlib import Path
import platform
import shutil
import subprocess
import time

from PIL import Image

from video_buddy.frames.capture import _extract_single_frame, score_frame

ROOT = Path(__file__).resolve().parent
rows = json.loads((ROOT / "initial-label-results.json").read_text(encoding="utf-8"))
cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
for row, case in zip(rows, cases, strict=True):
    row["case"] = case
    folder = Path(".scratch") / case["folder"]
    for name, metric in row["metrics"].items():
        hits = [
            [s["id"] for s in case["states"] if any(a <= t < b for a, b in s["spans"])]
            for t in metric["times"]
        ]
        covered = set(sum(hits, []))
        metric.update(
            covered=sorted(covered),
            recall=len(covered) / len(case["states"]),
            missed=[s["id"] for s in case["states"] if s["id"] not in covered],
            redundant=sum(bool(h) for h in hits) - len(covered),
            nonessential=sum(not h for h in hits),
        )
    controls = []
    began = time.perf_counter()
    for i, pts in enumerate(row["metrics"]["time_grid"]["times"]):
        path = folder / f"control_{i}.jpg"
        _extract_single_frame(Path(row["capture"]["source"]), pts, path)
        controls.append((pts, path))
    row["costs"]["time_grid_seek_write_s"] = time.perf_counter() - began
    row["exact_text"] = {}
    for method in ["subject_seek", "time_grid"]:
        outputs = []
        inputs = (
            [(r["pts_s"], folder / r["filename"]) for r in row["selected"]]
            if method == "subject_seek"
            else controls
        )
        for i, (pts, path) in enumerate(inputs):
            crop = Image.open(path).crop(case["box"])
            buf = io.BytesIO()
            crop.save(buf, format="PNG")
            text = (
                subprocess.run(
                    ["tesseract", "stdin", "stdout", "--psm", "13"],
                    input=buf.getvalue(),
                    capture_output=True,
                    check=True,
                )
                .stdout.decode()
                .strip()
            )
            outputs.append(dict(pts_s=pts, text=text))
            crop.save(ROOT / f"{case['id']}-{method}-{i}.png")
        row["exact_text"][method] = outputs
    row["source_sha256"] = hashlib.sha256(
        Path(row["capture"]["source"]).read_bytes()
    ).hexdigest()
    scores = [score_frame(folder / r["filename"]) for r in row["rows"]]
    row["edge_density_range"] = [
        min(s["edge_density"] for s in scores),
        max(s["edge_density"] for s in scores),
    ]
    for name in ["all-crops.jpg", "capture.json"]:
        shutil.copy2(folder / name, ROOT / f"{case['id']}-{name}")
    if case["phase"] == "tune":
        shutil.copy2(folder / "boundaries.jpg", ROOT / "annotation-boundary-qa.jpg")
report = dict(
    python=platform.python_version(),
    machine=platform.platform(),
    tesseract=subprocess.run(
        ["tesseract", "--version"], capture_output=True, text=True
    ).stdout.splitlines()[0],
    cases=rows,
)
(ROOT / "results.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
for row in rows:
    print(row["case"]["id"], row["metrics"], row["exact_text"])
