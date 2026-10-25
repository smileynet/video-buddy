"""THROWAWAY: oracle fixed boxes, stable OCR strings, equal upper output budget."""

import io
import json
from pathlib import Path
import re
import subprocess
import time

import cv2
import numpy as np
from PIL import Image

from video_buddy.frames.capture import extract_frames, select_frames

ROOT = Path(__file__).resolve().parent
BUDGET = 4
MIN_SUPPORT = 6


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


results = []
for case in json.loads((ROOT / "cases.json").read_text(encoding="utf-8")):
    folder = Path(".scratch") / case["folder"]
    capture = json.loads((folder / "capture.json").read_text())
    files = [folder / f["filename"] for f in capture["frames"]]
    times = {f["filename"]: f["pts_s"] for f in capture["frames"]}
    start = time.perf_counter()
    rows = []
    for path in files:
        with Image.open(path) as image:
            crop = image.crop(case["box"])
            gray = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2GRAY)
            sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
            buffer = io.BytesIO()
            crop.save(buffer, format="PNG")
        began = time.perf_counter()
        text = subprocess.run(
            ["tesseract", "stdin", "stdout", "--psm", "13"],
            input=buffer.getvalue(),
            capture_output=True,
            check=True,
        ).stdout.decode("utf-8")
        rows.append(
            dict(
                filename=path.name,
                pts_s=times[path.name],
                text=norm(text),
                sharpness=sharpness,
                ocr_s=time.perf_counter() - began,
            )
        )
    crop_total = time.perf_counter() - start
    groups = {}
    for row in rows:
        if row["text"]:
            groups.setdefault(row["text"], []).append(row)
    # Frequency is not an annotation; repeated OCR errors can also earn support.
    stable = [g for g in groups.values() if len(g) >= MIN_SUPPORT]
    stable.sort(key=lambda g: len(g), reverse=True)
    sought = [max(g, key=lambda r: r["sharpness"]) for g in stable[:BUDGET]]
    sought.sort(key=lambda r: r["pts_s"])
    began = time.perf_counter()
    sparse = extract_frames(
        Path(capture["source"]),
        [(capture["start"], capture["end"])],
        folder / "baseline",
        fps=2,
    )
    sparse_decode = time.perf_counter() - began
    began = time.perf_counter()
    selected = select_frames(sparse, video_id=case["source"], max_frames=BUDGET)
    sparse_select = time.perf_counter() - began
    began = time.perf_counter()
    dense_selected = select_frames(files, video_id=case["source"], max_frames=BUDGET)
    dense_select = time.perf_counter() - began
    choices = {
        "sparse_existing": [r["timestamp_ms"] / 1000 for r in selected],
        "dense_existing": [r["timestamp_ms"] / 1000 for r in dense_selected],
        "time_grid": [
            capture["start"] + (i + 0.5) * (capture["end"] - capture["start"]) / BUDGET
            for i in range(BUDGET)
        ],
        "subject_seek": [r["pts_s"] for r in sought],
    }
    metrics = {}
    for name, pts in choices.items():
        hits = [
            [s["id"] for s in case["states"] if any(a <= t < b for a, b in s["spans"])]
            for t in pts
        ]
        covered = set(sum(hits, []))
        metrics[name] = dict(
            times=pts,
            covered=sorted(covered),
            recall=len(covered) / len(case["states"]),
            missed=[s["id"] for s in case["states"] if s["id"] not in covered],
            redundant=sum(bool(h) for h in hits) - len(covered),
            nonessential=sum(not h for h in hits),
        )
    results.append(
        dict(
            case=case,
            capture=capture,
            rows=rows,
            selected=sought,
            metrics=metrics,
            costs=dict(
                crop_ocr_score_s=crop_total,
                ocr_s=sum(r["ocr_s"] for r in rows),
                sparse_decode_write_s=sparse_decode,
                sparse_select_s=sparse_select,
                dense_select_s=dense_select,
            ),
        )
    )
    (ROOT / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(case["id"], json.dumps(metrics))
