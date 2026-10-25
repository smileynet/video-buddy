"""Throwaway current-provider probe against previously frozen public fixtures."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import time
import traceback

from PIL import Image
import torch
from ultralytics import YOLOE, __version__

parser = argparse.ArgumentParser()
parser.add_argument("--imgsz", type=int, default=640)
size = parser.parse_args().imgsz
suffix = "" if size == 640 else "-" + str(size)
root = Path(__file__).resolve().parent
sources = root.parent
fixtures = [
    (sources / "image-models/fixtures/objects.jpg", ["dog", "cat", "elephant"]),
    (sources / "image-models/fixtures/diagram.jpg", ["diagram", "text"]),
    (
        sources / "image-models/fixtures/ui.jpg",
        ["search input field", "button", "line chart"],
    ),
    (
        sources / "real-video-ocr/frames/python-90.jpg",
        ["code editor", "text", "button"],
    ),
]
report = {
    "model": "yoloe-26s-seg.pt",
    "ultralytics": __version__,
    "status": "running",
    "config": {"imgsz": size, "conf": 0.25, "device": 0, "text_prompts": True},
    "fixtures": [],
}
start = time.perf_counter()
try:
    torch.cuda.reset_peak_memory_stats()
    checkpoint = Path(".scratch/models/yoloe-26s-seg.pt")
    model = YOLOE(str(checkpoint))
    report["weights_sha256"] = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    report["load_seconds"] = time.perf_counter() - start
    os.chdir(checkpoint.parent.resolve())
    for path, prompts in fixtures:
        began = time.perf_counter()
        model.set_classes(prompts)
        torch.cuda.synchronize()
        prompt_seconds = time.perf_counter() - began
        began = time.perf_counter()
        result = model.predict(
            str(path), imgsz=size, conf=0.25, device=0, verbose=False
        )[0]
        torch.cuda.synchronize()
        observation = {
            "fixture": str(path.relative_to(sources)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "prompts": prompts,
            "prompt_seconds": prompt_seconds,
            "inference_seconds": time.perf_counter() - began,
            "boxes": result.boxes.xyxy.cpu().tolist(),
            "scores": result.boxes.conf.cpu().tolist(),
            "labels": [result.names[int(i)] for i in result.boxes.cls.cpu().tolist()],
        }
        report["fixtures"].append(observation)
        result.save(
            filename=str(root / ("yoloe" + suffix + "-" + path.stem + "-overlay.jpg"))
        )
        if result.masks is not None and len(result.masks.data):
            mask = result.masks.data[0].cpu().numpy()
            Image.fromarray((mask > 0).astype("uint8") * 255).save(
                root / ("yoloe" + suffix + "-" + path.stem + "-mask.png")
            )
    report["status"] = "ran"
    encoder = Path("mobileclip2_b.ts")
    report["text_encoder_sha256"] = hashlib.sha256(encoder.read_bytes()).hexdigest()
except Exception as exc:
    report.update(
        status="runtime_or_setup_failure",
        error_type=type(exc).__name__,
        error=str(exc)[:1600],
        traceback=traceback.format_exc()[-3000:],
    )
report["total_seconds"] = time.perf_counter() - start
report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated()
(root / ("yoloe" + suffix + ".json")).write_text(json.dumps(report, indent=2) + "\n")
print(
    json.dumps(
        {k: v for k, v in report.items() if k not in ["fixtures", "traceback"]},
        indent=2,
    )
)
