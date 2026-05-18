#!/usr/bin/env python3
"""Batch EasyOCR worker for a directory of frame images."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(frames_dir: str) -> None:
    import os

    os.environ["EASYOCR_LOG_LEVEL"] = "ERROR"
    from easyocr import Reader

    reader = Reader(["en"], gpu=True, cudnn_benchmark=True, verbose=False)
    images = sorted(Path(frames_dir).glob("*.jpg")) or sorted(
        Path(frames_dir).glob("*.png")
    )
    if not images:
        (Path(frames_dir) / "results.json").write_text(json.dumps({}), encoding="utf-8")
        return
    results: dict[str, dict[str, str | float]] = {}
    for img_path in images:
        detections = reader.readtext(str(img_path))
        valid = [d for d in detections if d[2] > 0.3]
        text = " ".join(d[1] for d in valid)
        confidence = sum(d[2] for d in valid) / len(valid) if valid else 0.0
        results[img_path.name] = {
            "text": text.strip(),
            "confidence": round(float(confidence), 3),
        }
    (Path(frames_dir) / "results.json").write_text(
        json.dumps(results, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <frames_dir>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
