"""Original event-time control, full-frame context ablation; no new policy."""

import gzip
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
result = {}
for case in protocol["cases"]:
    if case["phase"] != "validation":
        continue
    folder = Path(".scratch") / case["folder"]
    cap = json.loads((folder / "capture.json").read_text())
    first = np.array(Image.open(folder / cap["frames"][0]["filename"]))
    x, y, r, b = case["header"]
    header = cv2.cvtColor(first[y:b, x:r], cv2.COLOR_RGB2GRAY)
    sx, sy, sr, sb = case["roi"]
    rows = []
    for frame in cap["frames"]:
        im = Image.open(folder / frame["filename"])
        gray = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
        start = time.perf_counter()
        _, confidence, _, point = cv2.minMaxLoc(
            cv2.matchTemplate(gray, header, cv2.TM_CCOEFF_NORMED)
        )
        row = dict(
            **frame,
            confidence=confidence,
            template_s=time.perf_counter() - start,
            observations={},
        )
        if confidence >= 0.8:
            tx, ty = point
            box = [tx + sx - x, ty + sy - y, tx + sr - x, ty + sb - y]
            crop = im.crop(box)
            sharp = float(
                cv2.Laplacian(
                    cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2GRAY), cv2.CV_64F
                ).var()
            )
            buf = io.BytesIO()
            crop.save(buf, format="PNG")
            start = time.perf_counter()
            text = subprocess.run(
                ["tesseract", "stdin", "stdout", "--psm", "7"],
                input=buf.getvalue(),
                capture_output=True,
                check=True,
            ).stdout.decode()
            row["observations"]["tracked"] = dict(
                text=re.sub(r"\s+", " ", text).strip(),
                sharpness=sharp,
                ocr_s=time.perf_counter() - start,
                box=box,
            )
        rows.append(row)
    result[case["id"]] = rows
    print(case["id"], len(rows), flush=True)
with gzip.open(ROOT / "legacy-validation.json.gz", "wt") as f:
    json.dump(result, f)
