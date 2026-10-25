"""Frozen PSM7/template candidate on new images; never reads reference labels."""

import io
import json
from pathlib import Path
import re
import subprocess
import time

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
protocol = json.loads((ROOT / "protocol.json").read_text())
results = {}
for case in protocol["cases"]:
    folder = Path(".scratch") / case["folder"]
    cap = json.loads((folder / "capture.json").read_text())
    first = np.array(Image.open(folder / cap["frames"][0]["filename"]))
    x, y, right, bottom = case["header"]
    header = cv2.cvtColor(first[y:bottom, x:right], cv2.COLOR_RGB2GRAY)
    sx, sy, sr, sb = case["roi"]
    rows = []
    for frame in cap["frames"]:
        image = Image.open(folder / frame["filename"])
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        began = time.perf_counter()
        _, confidence, _, point = cv2.minMaxLoc(
            cv2.matchTemplate(gray, header, cv2.TM_CCOEFF_NORMED)
        )
        row = dict(
            **frame,
            match_confidence=confidence,
            tracking_s=time.perf_counter() - began,
            observations={},
        )
        if confidence >= 0.8:
            tx, ty = point
            box = [tx + sx - x, ty + sy - y, tx + sr - x, ty + sb - y]
            crop = image.crop(box)
            cg = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2GRAY)
            sharpness = float(cv2.Laplacian(cg, cv2.CV_64F).var())
            buffer = io.BytesIO()
            crop.save(buffer, format="PNG")
            began = time.perf_counter()
            text = subprocess.run(
                ["tesseract", "stdin", "stdout", "--psm", "7"],
                input=buffer.getvalue(),
                capture_output=True,
                check=True,
            ).stdout.decode("utf-8")
            row["observations"]["tracked"] = dict(
                box=box,
                text=re.sub(r"\s+", " ", text).strip(),
                sharpness=sharpness,
                ocr_s=time.perf_counter() - began,
            )
        rows.append(row)
    results[case["id"]] = rows
    (ROOT / "observations.json").write_text(json.dumps(results, indent=2) + "\n")
    print(
        case["id"],
        len(rows),
        "accepted",
        sum(bool(r["observations"]) for r in rows),
        flush=True,
    )
