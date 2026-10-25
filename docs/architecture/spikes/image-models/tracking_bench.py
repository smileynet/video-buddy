"""Throwaway composition and temporal propagation on real captured diagram states."""

import argparse
import json
from pathlib import Path
import shutil
import time
import traceback

from hf_context import configure

import numpy as np
from PIL import Image
import torch
from huggingface_hub import HfApi, hf_hub_download

configure()

root = Path(__file__).resolve().parent
repo_root = root.parents[3]
parser = argparse.ArgumentParser()
parser.add_argument("family")
family = parser.parse_args().family
report = {"family": family, "status": "running", "observations": []}
started = time.perf_counter()
torch.cuda.reset_peak_memory_stats()


def ckpt(name, file):
    sha = HfApi().model_info(name).sha
    report["checkpoint"] = {"repo": name, "revision": sha, "file": file}
    return hf_hub_download(name, file, revision=sha)


def extent(mask):
    yy, xx = np.where(mask)
    return (
        [int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())]
        if len(xx)
        else None
    )


try:
    if family == "groundedsam2":
        from sam2.build_sam import build_sam2
        from sam2.sam2_image_predictor import SAM2ImagePredictor

        path = ckpt("facebook/sam2.1-hiera-tiny", "sam2.1_hiera_tiny.pt")
        predictor = SAM2ImagePredictor(
            build_sam2(
                "configs/sam2.1/sam2.1_hiera_t.yaml", path, apply_postprocessing=False
            )
        )
        detections = json.loads((root / "groundingdino.json").read_text())[
            "observations"
        ]
        for row in [detections[0], detections[2]]:
            image = np.array(
                Image.open(root / f"fixtures/{row['fixture']}.jpg").convert("RGB")
            )
            with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
                predictor.set_image(image)
                for label, box in zip(row["labels"], row["boxes"]):
                    start = time.perf_counter()
                    masks, scores, _ = predictor.predict(
                        box=np.array(box), multimask_output=False
                    )
                    mask = masks[0]
                    torch.cuda.synchronize()
                    Image.fromarray(mask.astype("uint8") * 255).save(
                        root / f"groundedsam2-{label}-mask.png"
                    )
                    obs = {
                        "fixture": row["fixture"],
                        "label": label,
                        "input_box": box,
                        "mask_box": extent(mask),
                        "area": float(mask.mean()),
                        "score": float(scores[0]),
                        "seconds": time.perf_counter() - start,
                    }
                    if label == "dog":
                        obs.update(
                            includes_dog_seed=bool(mask[350, 800]),
                            includes_cat_seed=bool(mask[650, 300]),
                        )
                    report["observations"].append(obs)
        report["limit"] = (
            "Uses frozen outputs of prior Grounding DINO run; timings cover segmentation stage only, no annotated mask accuracy"
        )
    else:
        if family == "sam2_tracking":
            from sam2.build_sam import build_sam2_video_predictor

            path = ckpt("facebook/sam2.1-hiera-tiny", "sam2.1_hiera_tiny.pt")
            predictor = build_sam2_video_predictor(
                "configs/sam2.1/sam2.1_hiera_t.yaml", path, apply_postprocessing=False
            )
        else:
            from efficient_track_anything.build_efficienttam import (
                build_efficienttam_video_predictor,
            )

            path = ckpt(
                "yunyangx/efficient-track-anything", "efficienttam_ti_512x512.pt"
            )
            predictor = build_efficienttam_video_predictor(
                "configs/efficienttam/efficienttam_ti_512x512.yaml",
                path,
                apply_postprocessing=False,
                hydra_overrides_extra=["++model.compile_image_encoder=false"],
            )
        frames = repo_root / ".scratch/image-model-spike/track-frames"
        frames.mkdir(parents=True, exist_ok=True)
        times = [106, 112, 114, 116]
        for i, t in enumerate(times):
            shutil.copy2(
                root.parent / "s2-visual-comparison" / f"frame_{t * 1000:08d}.jpg",
                frames / f"{i:05d}.jpg",
            )
        start = time.perf_counter()
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
            state = predictor.init_state(
                video_path=str(frames), offload_video_to_cpu=True
            )
            predictor.add_new_points_or_box(
                inference_state=state,
                frame_idx=0,
                obj_id=1,
                box=np.array([710, 450, 1210, 945], dtype=np.float32),
            )
            for index, ids, logits in predictor.propagate_in_video(state):
                mask = (logits[0, 0] > 0).cpu().numpy()
                Image.fromarray(mask.astype("uint8") * 255).save(
                    root / f"{family}-{index}-mask.png"
                )
                report["observations"].append(
                    {
                        "frame": int(index),
                        "source_seconds": times[index],
                        "ids": list(ids),
                        "area": float(mask.mean()),
                        "mask_box": extent(mask),
                    }
                )
        torch.cuda.synchronize()
        report["inference_seconds"] = time.perf_counter() - start
        report["limit"] = (
            "Four temporally sparse real diagram frames, not continuous native video; one manually seeded panel, no mask ground truth or identity-switch rate"
        )
    report["status"] = "ran"
except Exception as e:
    report.update(
        status="runtime_or_setup_failure",
        error_type=type(e).__name__,
        error=str(e)[:1500],
        traceback=traceback.format_exc()[-2500:],
    )
report["total_seconds"] = time.perf_counter() - started
report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated()
(root / f"{family}.json").write_text(json.dumps(report, indent=2, default=str) + "\n")
print(
    json.dumps(
        {k: v for k, v in report.items() if k not in ["observations", "traceback"]},
        indent=2,
    )
)
