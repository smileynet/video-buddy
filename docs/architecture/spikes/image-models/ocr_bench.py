"""Throwaway per-engine OCR observation. No production imports."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import time
import traceback

from hf_context import configure

configure()
root = Path(__file__).resolve().parent
args = argparse.ArgumentParser()
args.add_argument("engine")
engine = args.parse_args().engine
cases = json.loads((root / "ocr-cases.json").read_text())
started = time.perf_counter()
report = {"engine": engine, "cases": [], "status": "running"}


def normalize(s):
    return re.sub(r"\s+", " ", s).strip()


def distance(a, b):
    row = list(range(len(b) + 1))
    for i, char in enumerate(a):
        nxt = [i + 1]
        for j, other in enumerate(b):
            nxt.append(min(nxt[-1] + 1, row[j + 1] + 1, row[j] + (char != other)))
        row = nxt
    return row[-1]


try:
    if engine == "easyocr":
        import easyocr

        model = easyocr.Reader(["en"], gpu=True, verbose=False)
    elif engine == "paddle":
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
    report["load_seconds"] = time.perf_counter() - started
    for case in cases:
        path = root / case["path"]
        start = time.perf_counter()
        if engine == "tesseract":
            r = subprocess.run(
                ["tesseract", str(path), "stdout", "--psm", "7"],
                capture_output=True,
                text=True,
                check=True,
            )
            text, raw = r.stdout, r.stdout
        elif engine == "easyocr":
            detections = model.readtext(str(path))
            text = " ".join(x[1] for x in detections)
            raw = [
                {
                    "box": [[float(y) for y in p] for p in x[0]],
                    "text": x[1],
                    "confidence": float(x[2]),
                }
                for x in detections
            ]
        else:
            predictions = list(model.predict(str(path)))
            raw = [p.json for p in predictions]
            text = " ".join(str(t) for p in predictions for t in p.get("rec_texts", []))
        expected, actual = normalize(case["expected"]), normalize(text)
        report["cases"].append(
            {
                "id": case["id"],
                "kind": case["kind"],
                "expected": expected,
                "text": actual,
                "exact": expected == actual,
                "cer": distance(expected, actual) / len(expected),
                "seconds": time.perf_counter() - start,
                "raw": raw,
            }
        )
    report["status"] = "ran"
    for kind in ["controlled_synthetic", "source_crop"]:
        rows = [x for x in report["cases"] if x["kind"] == kind]
        report[kind] = {
            "n": len(rows),
            "exact": sum(x["exact"] for x in rows),
            "mean_cer": sum(x["cer"] for x in rows) / len(rows),
        }
except Exception as exc:
    report.update(
        status="runtime_or_setup_failure",
        error_type=type(exc).__name__,
        error=str(exc)[:1800],
        traceback=traceback.format_exc()[-3000:],
    )
report["total_seconds"] = time.perf_counter() - started
(root / f"{engine}-ocr.json").write_text(
    json.dumps(report, indent=2, default=str) + "\n"
)
print(
    json.dumps(
        {k: v for k, v in report.items() if k not in ["cases", "traceback"]}, indent=2
    )
)
