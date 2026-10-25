"""Throwaway OCR comparison; frozen labels and tuning-only configuration choice."""

import argparse
import csv
import io
import json
from pathlib import Path
import re
import subprocess
import time

import numpy as np
from PIL import Image


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def distance(a, b):
    row = list(range(len(b) + 1))
    for i, char in enumerate(a):
        nxt = [i + 1]
        for j, other in enumerate(b):
            nxt.append(min(nxt[-1] + 1, row[j + 1] + 1, row[j] + (char != other)))
        row = nxt
    return row[-1]


parser = argparse.ArgumentParser()
parser.add_argument("engine", choices=["tesseract", "easyocr", "paddle"])
parser.add_argument("phase", choices=["tune", "heldout"])
args = parser.parse_args()
root = Path(__file__).resolve().parent
cases = json.loads((root / "cases.json").read_text())
began = time.perf_counter()
model = None
if args.engine == "easyocr":
    import easyocr
    import torch

    torch.cuda.reset_peak_memory_stats()
    model = easyocr.Reader(["en"], gpu=True, verbose=False)
elif args.engine == "paddle":
    from paddleocr import PaddleOCR

    model = PaddleOCR(
        text_detection_model_name="PP-OCRv5_mobile_det",
        text_recognition_model_name="en_PP-OCRv5_mobile_rec",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        device="cpu",
        cpu_threads=4,
        enable_mkldnn=False,
    )
report = {
    "engine": args.engine,
    "phase": args.phase,
    "load_seconds": time.perf_counter() - began,
    "cases": [],
    "frames": [],
}


def recognize(im, psm=7, full=False):
    if args.engine == "tesseract":
        buffer = io.BytesIO()
        im.save(buffer, format="PNG")
        command = ["tesseract", "stdin", "stdout", "--psm", str(11 if full else psm)]
        if full:
            command.append("tsv")
        result = subprocess.run(
            command, input=buffer.getvalue(), capture_output=True, check=True
        ).stdout.decode("utf-8")
        if not full:
            return result, []
        boxes = []
        for row in csv.DictReader(io.StringIO(result), delimiter="\t"):
            if row["text"].strip():
                x, y, w, h = [int(row[k]) for k in ["left", "top", "width", "height"]]
                boxes.append(
                    {
                        "box": [x, y, x + w, y + h],
                        "text": row["text"],
                        "confidence": float(row["conf"]),
                    }
                )
        return " ".join(x["text"] for x in boxes), boxes
    if args.engine == "easyocr":
        raw = model.readtext(np.array(im))
        boxes = [
            {
                "box": [
                    float(min(p[0] for p in b)),
                    float(min(p[1] for p in b)),
                    float(max(p[0] for p in b)),
                    float(max(p[1] for p in b)),
                ],
                "text": t,
                "confidence": float(c),
            }
            for b, t, c in raw
        ]
    else:
        prediction = list(model.predict(np.array(im)))[0]
        raw = prediction.json["res"]
        boxes = [
            {
                "box": [
                    float(min(p[0] for p in b)),
                    float(min(p[1] for p in b)),
                    float(max(p[0] for p in b)),
                    float(max(p[1] for p in b)),
                ],
                "text": t,
                "confidence": float(c),
            }
            for b, t, c in zip(
                raw["rec_polys"], raw["rec_texts"], raw["rec_scores"], strict=True
            )
        ]
    return " ".join(x["text"] for x in boxes), boxes


def score(case, text, **extra):
    expected, text = norm(case["expected"]), norm(text)
    edits = distance(expected, text)
    return {
        "id": case["id"],
        "kind": case["kind"],
        "expected": expected,
        "text": text,
        "exact": expected == text,
        "edits": edits,
        "cer": edits / len(expected),
        "empty": not text,
        **extra,
    }


choices = [
    {"scale": scale, "psm": psm}
    for scale in [1, 2]
    for psm in ([7, 13] if args.engine == "tesseract" else [7])
]
selection = root / f"{args.engine}-selection.json"
if args.phase == "heldout":
    choices = [json.loads(selection.read_text())["selected"]]
for config in choices:
    for case in cases:
        if case["split"] != args.phase:
            continue
        start = time.perf_counter()
        im = Image.open(root / case["path"]).convert("RGB")
        if config["scale"] == 2:
            im = im.resize((im.width * 2, im.height * 2), Image.Resampling.LANCZOS)
        prep = time.perf_counter() - start
        start = time.perf_counter()
        text, raw = recognize(im, config["psm"])
        report["cases"].append(
            score(
                case,
                text,
                config=config,
                preprocessing_seconds=prep,
                ocr_seconds=time.perf_counter() - start,
                raw=raw,
            )
        )
if args.phase == "tune":
    ranked = []
    for config in choices:
        rows = [x for x in report["cases"] if x["config"] == config]
        ranked.append(
            {
                "config": config,
                "exact": sum(x["exact"] for x in rows),
                "edits": sum(x["edits"] for x in rows),
            }
        )
    ranked.sort(
        key=lambda x: (
            -x["exact"],
            x["edits"],
            x["config"]["scale"],
            x["config"]["psm"],
        )
    )
    selection.write_text(
        json.dumps({"selected": ranked[0]["config"], "tuning_rank": ranked}, indent=2)
        + "\n"
    )
else:
    for frame in sorted({x["frame"] for x in cases if x["split"] == "heldout"}):
        im = Image.open(root / frame).convert("RGB")
        start = time.perf_counter()
        text, raw = recognize(im, full=True)
        observation = {
            "frame": frame,
            "ocr_seconds": time.perf_counter() - start,
            "raw": raw,
            "regions": [],
        }
        for case in cases:
            if case["frame"] != frame or case["split"] != "heldout":
                continue
            x0, y0, x1, y1 = case["box"]
            selected = [
                x
                for x in raw
                if x0 <= (x["box"][0] + x["box"][2]) / 2 <= x1
                and y0 <= (x["box"][1] + x["box"][3]) / 2 <= y1
            ]
            selected.sort(key=lambda x: x["box"][0])
            observation["regions"].append(
                score(
                    case,
                    " ".join(x["text"] for x in selected),
                    detections=len(selected),
                )
            )
        report["frames"].append(observation)
report["total_seconds"] = time.perf_counter() - began
if args.engine == "easyocr":
    report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated()
(root / f"{args.engine}-{args.phase}.json").write_text(
    json.dumps(report, indent=2) + "\n"
)
print(
    json.dumps(
        {k: v for k, v in report.items() if k not in ["cases", "frames"]}, indent=2
    )
)
