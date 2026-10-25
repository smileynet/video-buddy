"""Separate visual-box arm after text prompts miss tutorial UI."""

import json
from pathlib import Path
import time
import traceback

import numpy as np
import torch
from ultralytics import YOLOE

root = Path(__file__).resolve().parent
report = {
    "model": "yoloe-26s-seg.pt",
    "mode": "visual_box",
    "imgsz": 640,
    "conf": 0.25,
    "observations": [],
}
for fixture, seed in [
    ("image-models/fixtures/ui.jpg", [390, 205, 1776, 300]),
    ("real-video-ocr/frames/python-90.jpg", [675, 220, 1650, 820]),
]:
    observation = {
        "fixture": fixture,
        "seed_box": seed,
        "limit": "Manual region seed supplied; generic object0 label is not semantic identification",
    }
    try:
        model = YOLOE(".scratch/models/yoloe-26s-seg.pt")
        start = time.perf_counter()
        result = model.predict(
            str(root.parent / fixture),
            visual_prompts={"bboxes": np.array([seed]), "cls": np.array([0])},
            imgsz=640,
            conf=0.25,
            device=0,
            verbose=False,
        )[0]
        torch.cuda.synchronize()
        observation.update(
            status="ran",
            seconds=time.perf_counter() - start,
            boxes=result.boxes.xyxy.cpu().tolist(),
            scores=result.boxes.conf.cpu().tolist(),
            labels=[result.names[int(i)] for i in result.boxes.cls.cpu().tolist()],
        )
        result.save(
            filename=str(root / ("yoloe-visual-" + Path(fixture).stem + ".jpg"))
        )
    except Exception as exc:
        observation.update(
            status="runtime_or_setup_failure",
            error=str(exc)[:1600],
            traceback=traceback.format_exc()[-2000:],
        )
    report["observations"].append(observation)
(root / "yoloe-visual.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
