"""Experimental false-only API adapter; no upstream or production changes."""

import argparse
import json
from pathlib import Path
import time
import traceback

import numpy as np
from PIL import Image, ImageDraw
import torch
from huggingface_hub import hf_hub_download
from sam3.model_builder import build_sam3_predictor

parser = argparse.ArgumentParser()
parser.add_argument("--box-only", action="store_true")
box_only = parser.parse_args().box_only
root = Path(__file__).resolve().parent
repo = root.parents[3]
report = {
    "status": "running",
    "source_revision": "f1647e8d0c1d280991f4d1b7d974c2704537fe66",
    "checkpoint_revision": "daa63191845a41281374e725f4c9e51c7a824460",
    "adapter": "Drop unsupported offload_state_to_cpu only when false; reject true",
    "sessions": [],
}
began = time.perf_counter()


def serial(value):
    return value.tolist() if hasattr(value, "tolist") else value


def summarize(payload, prefix):
    result = {"keys": list(payload)}
    for key in ["out_obj_ids", "out_probs", "out_boxes_xywh", "out_boxes_xyxy"]:
        if key in payload:
            result[key] = serial(payload[key])
    if "out_binary_masks" in payload:
        masks = payload["out_binary_masks"]
        if hasattr(masks, "cpu"):
            masks = masks.cpu().numpy()
        masks = np.asarray(masks)
        result["mask_shape"] = list(masks.shape)
        result["mask_areas"] = []
        for i, mask in enumerate(masks):
            mask = mask.squeeze().astype(bool)
            result["mask_areas"].append(float(mask.mean()))
            Image.fromarray(mask.astype("uint8") * 255).save(
                root / f"{prefix}-object{i}.png"
            )
    return result


try:
    torch.cuda.reset_peak_memory_stats()
    checkpoint = hf_hub_download(
        "facebook/sam3.1", "sam3.1_multiplex.pt", revision=report["checkpoint_revision"]
    )
    predictor = build_sam3_predictor(
        checkpoint_path=checkpoint,
        version="sam3.1",
        compile=False,
        warm_up=False,
        use_fa3=False,
        async_loading_frames=False,
        max_num_objects=16,
        multiplex_count=16,
    )
    original = predictor.model.init_state

    def compatible_init(*args, offload_state_to_cpu=False, **kwargs):
        if offload_state_to_cpu:
            raise NotImplementedError(
                "Experimental adapter does not implement CPU state offload"
            )
        return original(*args, **kwargs)

    predictor.model.init_state = compatible_init
    try:
        compatible_init(offload_state_to_cpu=True)
    except NotImplementedError:
        report["true_offload_rejected"] = True
    synthetic = repo / ".scratch/image-model-spike/sam31-controlled"
    synthetic.mkdir(parents=True, exist_ok=True)
    source = Image.open(root.parent / "image-models/fixtures/objects.jpg").convert(
        "RGB"
    )
    for i in range(4):
        frame = Image.new("RGB", source.size)
        frame.paste(source, (i * 10, 0))
        if i == 2:
            ImageDraw.Draw(frame).rectangle((620, 150, 850, 420), fill="gray")
        frame.save(synthetic / f"{i:05d}.jpg")
    report["load_seconds"] = time.perf_counter() - began
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
        for label, path, prompt in (
            [
                (
                    "real-diagram-box",
                    repo / ".scratch/image-model-spike/track-frames",
                    None,
                )
            ]
            if box_only
            else [
                ("controlled-dog", synthetic, "dog"),
                ("controlled-negative", synthetic, "elephant"),
                (
                    "real-diagram",
                    repo / ".scratch/image-model-spike/track-frames",
                    "diagram",
                ),
            ]
        ):
            row = {
                "case": label,
                "prompt": prompt,
                "frames": [],
                "fixture_kind": "controlled translation/occlusion of one photo"
                if label.startswith("controlled")
                else "four sparse real captured diagram states",
            }
            sid = None
            start = time.perf_counter()
            try:
                sid = predictor.handle_request(
                    {"type": "start_session", "resource_path": str(path)}
                )["session_id"]
                request = {
                    "type": "add_prompt",
                    "session_id": sid,
                    "frame_index": 0,
                    "text": prompt,
                }
                if box_only:
                    request.update(
                        bounding_boxes=[
                            [710 / 1920, 450 / 1080, 500 / 1920, 495 / 1080]
                        ],
                        bounding_box_labels=[1],
                    )
                    row["seed_box_xyxy_pixels"] = [710, 450, 1210, 945]
                response = predictor.handle_request(request)
                row["initial"] = summarize(
                    response.get("outputs", {}), label + "-initial"
                )
                for item in predictor.handle_stream_request(
                    {"type": "propagate_in_video", "session_id": sid}
                ):
                    index = item.get("frame_index")
                    row["frames"].append(
                        {
                            "index": index,
                            **summarize(
                                item.get("outputs", {}), f"{label}-frame{index}"
                            ),
                        }
                    )
                row["status"] = "ran"
            except Exception as exc:
                row.update(
                    status="runtime_failure",
                    error=str(exc)[:1800],
                    traceback=traceback.format_exc()[-2500:],
                )
            finally:
                if sid:
                    predictor.handle_request(
                        {"type": "close_session", "session_id": sid}
                    )
            row["seconds"] = time.perf_counter() - start
            report["sessions"].append(row)
    report["status"] = "recorded"
except Exception as exc:
    report.update(
        status="runtime_or_setup_failure",
        error=str(exc)[:1800],
        traceback=traceback.format_exc()[-3000:],
    )
report["total_seconds"] = time.perf_counter() - began
report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated()
(root / ("sam31-box-followup.json" if box_only else "sam31-followup.json")).write_text(
    json.dumps(report, indent=2) + "\n"
)
print(
    json.dumps(
        {k: v for k, v in report.items() if k not in ["sessions", "traceback"]},
        indent=2,
    )
)
