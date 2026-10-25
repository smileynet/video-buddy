"""Throwaway viewport OCR; phase separation prevents reading validation early."""

import argparse
import csv
import gzip
import io
import json
from pathlib import Path
import subprocess
import time

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("phase", choices=["development", "validation"])
args = parser.parse_args()
protocol = json.loads((ROOT / "protocol.json").read_text())
for case in protocol["cases"]:
    if case["phase"] != args.phase:
        continue
    folder = Path(".scratch") / case["folder"]
    cap = json.loads((folder / "capture.json").read_text())
    rows = []
    for frame in cap["frames"]:
        crop = Image.open(folder / frame["filename"]).crop(case["viewport"])
        gray = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2GRAY)
        sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        buf = io.BytesIO()
        crop.save(buf, format="PNG")
        start = time.perf_counter()
        tsv = subprocess.run(
            ["tesseract", "stdin", "stdout", "--psm", "6", "tsv"],
            input=buf.getvalue(),
            capture_output=True,
            check=True,
        ).stdout.decode("utf-8")
        elapsed = time.perf_counter() - start
        grouped = {}
        for word in csv.DictReader(
            io.StringIO(tsv), delimiter="\t", quoting=csv.QUOTE_NONE
        ):
            if word["text"].strip():
                key = tuple(word[k] for k in ["block_num", "par_num", "line_num"])
                grouped.setdefault(key, []).append(
                    dict(
                        text=word["text"],
                        x=int(word["left"]),
                        y=int(word["top"]),
                        confidence=float(word["conf"]),
                    )
                )
        lines = [
            dict(
                text=" ".join(w["text"] for w in g),
                x=min(w["x"] for w in g),
                y=min(w["y"] for w in g),
                confidence=sum(w["confidence"] for w in g) / len(g),
            )
            for g in grouped.values()
        ]
        lines.sort(key=lambda r: r["y"])
        rows.append(
            dict(
                **frame,
                lines=lines,
                text="\n".join(r["text"] for r in lines),
                raw_tsv=tsv,
                sharpness=sharpness,
                ocr_s=elapsed,
            )
        )
    with gzip.open(ROOT / f"{case['id']}-ocr.json.gz", "wt", encoding="utf-8") as f:
        json.dump(rows, f)
    print(case["id"], len(rows), round(sum(r["ocr_s"] for r in rows), 3), flush=True)
