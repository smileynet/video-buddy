"""Frozen selectors consume decoded images and the first seeded box only."""

import argparse
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
parser = argparse.ArgumentParser()
parser.add_argument("--psm", type=int, default=13)
args = parser.parse_args()
WORK = Path(".scratch/seek-round2")
config = json.loads((ROOT / "protocol.json").read_text())
results = {}
for kind in config["clips"]:
    folder = WORK / kind / "decoded"
    cap = json.loads((folder / "capture.json").read_text())
    x, y = (160, 150) if kind == "motion" else (120, 140)
    seed = np.array(Image.open(folder / cap["frames"][0]["filename"]))
    header = cv2.cvtColor(seed[y : y + 34, x : x + 580], cv2.COLOR_RGB2GRAY)
    rows = []
    for frame in cap["frames"]:
        image = Image.open(folder / frame["filename"])
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        began = time.perf_counter()
        match = cv2.matchTemplate(gray, header, cv2.TM_CCOEFF_NORMED)
        _, confidence, _, point = cv2.minMaxLoc(match)
        tracking_s = time.perf_counter() - began
        boxes = {"static": [x + 20, y + 55, x + 560, y + 107]}
        if confidence >= 0.8:
            tx, ty = point
            boxes["tracked"] = [tx + 20, ty + 55, tx + 560, ty + 107]
        row = dict(
            pts_s=frame["pts_s"],
            filename=frame["filename"],
            tracking_s=tracking_s,
            match_confidence=confidence,
            observations={},
        )
        cache = {}
        for mode, box in boxes.items():
            key = tuple(box)
            if key not in cache:
                crop = image.crop(box)
                cg = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2GRAY)
                sharpness = float(cv2.Laplacian(cg, cv2.CV_64F).var())
                buf = io.BytesIO()
                crop.save(buf, format="PNG")
                began = time.perf_counter()
                text = subprocess.run(
                    ["tesseract", "stdin", "stdout", "--psm", str(args.psm)],
                    input=buf.getvalue(),
                    capture_output=True,
                    check=True,
                ).stdout.decode("utf-8")
                cache[key] = dict(
                    box=box,
                    text=re.sub(r"\s+", " ", text).strip(),
                    sharpness=sharpness,
                    ocr_s=time.perf_counter() - began,
                )
            row["observations"][mode] = cache[key]
        rows.append(row)
    results[kind] = rows
    (ROOT / f"observations-psm{args.psm}.json").write_text(
        json.dumps(results, indent=2) + "\n"
    )
    print(
        kind,
        "frames",
        len(rows),
        "tracking_s",
        sum(r["tracking_s"] for r in rows),
        flush=True,
    )
