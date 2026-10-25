"""Throwaway model observations; families run in separate processes to free VRAM."""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys
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
models = repo_root / ".scratch/models"
cache = repo_root / ".scratch/checkpoints"
cache.mkdir(parents=True, exist_ok=True)
args = argparse.ArgumentParser()
args.add_argument("family")
family = args.parse_args().family
report = {"family": family, "status": "running", "revisions": {}, "observations": []}
began = time.perf_counter()
torch.cuda.reset_peak_memory_stats()
torch.manual_seed(0)


def revision(repo):
    sha = HfApi().model_info(repo).sha
    report["revisions"][repo] = sha
    return sha


def checkpoint(repo, file):
    return hf_hub_download(repo, file, revision=revision(repo))


def save_mask(mask, score=None):
    mask = np.asarray(mask, dtype=bool)
    Image.fromarray(mask.astype("uint8") * 255).save(root / f"{family}-mask.png")
    yy, xx = np.where(mask)
    report["observations"].append(
        {
            "fixture": "objects.jpg",
            "prompt": {"positive": [800, 350], "negative": [300, 650]},
            "mask_area_ratio": float(mask.mean()),
            "includes_positive_seed": bool(mask[350, 800]),
            "includes_negative_seed": bool(mask[650, 300]),
            "predicted_score": float(score) if score is not None else None,
            "mask_box": [int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())]
            if len(xx)
            else None,
            "ground_truth_mask": "not annotated; these are seed/extent sanity checks, not segmentation accuracy",
        }
    )


def candidates(masks, scores):
    report["candidate_seed_checks"] = [
        {
            "index": i,
            "score": float(s),
            "positive": bool(m[350, 800]),
            "negative": bool(m[650, 300]),
            "area": float(m.mean()),
        }
        for i, (m, s) in enumerate(zip(masks, scores))
    ]


try:
    image = Image.open(root / "fixtures/objects.jpg").convert("RGB")
    array = np.array(image)
    if family == "sam":
        import requests

        path = cache / "sam_vit_b_01ec64.pth"
        if not path.exists():
            url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
            with requests.get(url, stream=True, timeout=90) as response:
                response.raise_for_status()
                with path.open("wb") as out:
                    for chunk in response.iter_content(1024 * 1024):
                        out.write(chunk)
        from segment_anything import sam_model_registry, SamPredictor

        model = sam_model_registry["vit_b"](checkpoint=str(path)).to("cuda")
        predictor = SamPredictor(model)
        start = time.perf_counter()
        predictor.set_image(array)
        masks, scores, _ = predictor.predict(
            point_coords=np.array([[800, 350], [300, 650]]),
            point_labels=np.array([1, 0]),
        )
        torch.cuda.synchronize()
        report["inference_seconds"] = time.perf_counter() - start
        candidates(masks, scores)
        save_mask(masks[scores.argmax()], scores.max())
    elif family in ["sam2", "efficienttam"]:
        if family == "sam2":
            from sam2.build_sam import build_sam2
            from sam2.sam2_image_predictor import SAM2ImagePredictor

            path = checkpoint("facebook/sam2.1-hiera-tiny", "sam2.1_hiera_tiny.pt")
            model = build_sam2(
                "configs/sam2.1/sam2.1_hiera_t.yaml",
                path,
                device="cuda",
                apply_postprocessing=False,
            )
            predictor = SAM2ImagePredictor(model)
        else:
            from efficient_track_anything.build_efficienttam import build_efficienttam
            from efficient_track_anything.efficienttam_image_predictor import (
                EfficientTAMImagePredictor,
            )

            path = checkpoint(
                "yunyangx/efficient-track-anything", "efficienttam_ti_512x512.pt"
            )
            model = build_efficienttam(
                "configs/efficienttam/efficienttam_ti_512x512.yaml",
                path,
                device="cuda",
                apply_postprocessing=False,
                hydra_overrides_extra=["++model.compile_image_encoder=false"],
            )
            report["runtime_adjustment"] = (
                "Disable optional torch.compile: native Windows environment has no Triton backend"
            )
            predictor = EfficientTAMImagePredictor(model)
        start = time.perf_counter()
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
            predictor.set_image(array)
            masks, scores, _ = predictor.predict(
                point_coords=np.array([[800, 350], [300, 650]]),
                point_labels=np.array([1, 0]),
            )
        torch.cuda.synchronize()
        report["inference_seconds"] = time.perf_counter() - start
        candidates(masks, scores)
        save_mask(masks[scores.argmax()], scores.max())
    elif family == "efficientsam":
        sys.path.insert(0, str(models / "efficient-sam"))
        from efficient_sam.build_efficient_sam import build_efficient_sam_vitt

        previous = Path.cwd()
        os.chdir(models / "efficient-sam")
        model = build_efficient_sam_vitt().to("cuda")
        os.chdir(previous)
        tensor = (
            torch.from_numpy(array.copy())
            .permute(2, 0, 1)
            .float()
            .div(255)
            .unsqueeze(0)
            .to("cuda")
        )
        start = time.perf_counter()
        with torch.inference_mode():
            masks, scores = model(
                tensor,
                torch.tensor([[[[800, 350], [300, 650]]]], device="cuda"),
                torch.tensor([[[1, 0]]], device="cuda"),
            )
        torch.cuda.synchronize()
        report["inference_seconds"] = time.perf_counter() - start
        candidates(masks[0, 0].ge(0).cpu().numpy(), scores[0, 0].cpu().numpy())
        best = int(scores[0, 0].argmax())
        save_mask(masks[0, 0, best].ge(0).cpu().numpy(), scores[0, 0, best].item())
    elif family == "groundingdino":
        from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection

        name = "IDEA-Research/grounding-dino-tiny"
        sha = revision(name)
        processor = AutoProcessor.from_pretrained(name, revision=sha)
        model = (
            AutoModelForZeroShotObjectDetection.from_pretrained(name, revision=sha)
            .to("cuda")
            .eval()
        )
        for fixture, prompt in [
            ("objects", "dog . cat . elephant ."),
            ("ui", "search input field . button . line chart ."),
            ("diagram", "diagram . text ."),
        ]:
            im = Image.open(root / f"fixtures/{fixture}.jpg").convert("RGB")
            inputs = processor(images=im, text=prompt, return_tensors="pt").to("cuda")
            start = time.perf_counter()
            with torch.inference_mode():
                output = model(**inputs)
            detections = processor.post_process_grounded_object_detection(
                output,
                inputs.input_ids,
                threshold=0.30,
                text_threshold=0.25,
                target_sizes=[(im.height, im.width)],
            )[0]
            torch.cuda.synchronize()
            report["observations"].append(
                {
                    "fixture": fixture,
                    "prompt": prompt,
                    "seconds": time.perf_counter() - start,
                    "boxes": detections["boxes"].tolist(),
                    "scores": detections["scores"].tolist(),
                    "labels": detections.get("text_labels", detections.get("labels")),
                }
            )
    elif family == "florence":
        from transformers import AutoProcessor, AutoModelForCausalLM

        name = "microsoft/Florence-2-base-ft"
        sha = revision(name)
        processor = AutoProcessor.from_pretrained(
            name, revision=sha, trust_remote_code=True
        )
        model = (
            AutoModelForCausalLM.from_pretrained(
                name,
                revision=sha,
                trust_remote_code=True,
                torch_dtype=torch.float16,
                attn_implementation="eager",
            )
            .to("cuda")
            .eval()
        )
        for fixture, task in [
            ("objects", "<OD>"),
            ("ui", "<DENSE_REGION_CAPTION>"),
            ("real-settings", "<OCR_WITH_REGION>"),
        ]:
            im = Image.open(
                root
                / (
                    "fixtures/real-settings.png"
                    if fixture == "real-settings"
                    else f"fixtures/{fixture}.jpg"
                )
            ).convert("RGB")
            inputs = processor(text=task, images=im, return_tensors="pt").to(
                "cuda", torch.float16
            )
            start = time.perf_counter()
            with torch.inference_mode():
                ids = model.generate(
                    **inputs, max_new_tokens=512, num_beams=1, do_sample=False
                )
            text = processor.batch_decode(ids, skip_special_tokens=False)[0]
            parsed = processor.post_process_generation(
                text, task=task, image_size=im.size
            )
            torch.cuda.synchronize()
            report["observations"].append(
                {
                    "fixture": fixture,
                    "task": task,
                    "seconds": time.perf_counter() - start,
                    "raw": text,
                    "parsed": parsed,
                }
            )
    elif family == "dinov2":
        from transformers import AutoImageProcessor, AutoModel

        name = "facebook/dinov2-small"
        sha = revision(name)
        processor = AutoImageProcessor.from_pretrained(name, revision=sha)
        model = AutoModel.from_pretrained(name, revision=sha).to("cuda").eval()
        im = Image.open(root / "fixtures/text-dark-22-4.png").convert("RGB")
        changed = im.copy()
        from PIL import ImageDraw, ImageFont

        draw = ImageDraw.Draw(changed)
        draw.rectangle((0, 0, 1100, 80), fill="#111827")
        font = ImageFont.truetype(
            str(Path(os.environ["WINDIR"]) / "Fonts/consola.ttf"), 22
        )
        draw.text((15, 22), "port=8000", font=font, fill="white")
        inputs = processor(
            images=[im, changed, image],
            return_tensors="pt",
            do_center_crop=False,
            size={"height": 224, "width": 224},
        ).to("cuda")
        report["preprocessing"] = (
            "Disable default center crop, resize full images to 224x224 so left-aligned text is retained"
        )
        report["processed_changed_pixel_l1"] = (
            (inputs["pixel_values"][0] - inputs["pixel_values"][1]).abs().sum().item()
        )
        start = time.perf_counter()
        with torch.inference_mode():
            features = model(**inputs).last_hidden_state[:, 0]
        cos = torch.nn.functional.cosine_similarity(features[0:1], features[1:2]).item()
        torch.cuda.synchronize()
        report["observations"].append(
            {
                "job": "do not lose a one-character settings revision",
                "changed": "port=8001 -> port=8000",
                "cls_cosine": cos,
                "seconds": time.perf_counter() - start,
                "limit": "CLS similarity only, not dense matching/track accuracy",
            }
        )
        original = image.resize((224, 224))
        translated = Image.new("RGB", (224, 224))
        translated.paste(original, (14, 0))
        batch = processor(
            images=[original, translated],
            return_tensors="pt",
            do_center_crop=False,
            do_resize=False,
        ).to("cuda")
        with torch.inference_mode():
            patches = model(**batch).last_hidden_state[:, 1:]
        normalized = torch.nn.functional.normalize(patches, dim=-1)
        matches = []
        for x, y in [(4, 10), (11, 5), (12, 12), (5, 3), (8, 8)]:
            scores = normalized[0, y * 16 + x] @ normalized[1].T
            index = int(scores.argmax())
            pred = [index % 16, index // 16]
            matches.append(
                {
                    "source_patch": [x, y],
                    "expected_target_patch": [x + 1, y],
                    "predicted_target_patch": pred,
                    "exact": pred == [x + 1, y],
                    "similarity": float(scores.max()),
                }
            )
        report["observations"].append(
            {
                "job": "dense correspondence on controlled image translation",
                "shift_pixels": [14, 0],
                "patch_size": 14,
                "matches": matches,
                "limit": "five chosen patches on one synthetically translated natural image; not video drift/occlusion evaluation",
            }
        )
    elif family == "omniparser":
        path = checkpoint("microsoft/OmniParser-v2.0", "icon_detect_v3/model.pt")
        module_path = models / "omniparser/util/yolov9.py"
        spec = importlib.util.spec_from_file_location("omni_detector", module_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        detector = mod.YOLOv9Detector(model_path=path, device="cuda")
        start = time.perf_counter()
        prediction = detector.predict(
            source=str(root / "fixtures/ui.jpg"), imgsz=1280, conf=0.1
        )[0]
        torch.cuda.synchronize()
        report["observations"].append(
            {
                "fixture": "ui",
                "stage": "icon_detect_v3 detector only; captions/OCR not yet composed",
                "seconds": time.perf_counter() - start,
                "boxes": prediction.boxes.xyxy.cpu().tolist(),
                "scores": prediction.boxes.conf.cpu().tolist(),
            }
        )
    else:
        raise ValueError(family)
    report["status"] = "ran"
except Exception as exc:
    report.update(
        status="runtime_or_setup_failure",
        error_type=type(exc).__name__,
        error=str(exc)[:2000],
        traceback=traceback.format_exc()[-3500:],
    )
finally:
    report["total_seconds"] = time.perf_counter() - began
    report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated()
    (root / f"{family}.json").write_text(
        json.dumps(report, indent=2, default=str) + "\n"
    )
    print(
        json.dumps(
            {k: v for k, v in report.items() if k not in ["traceback", "observations"]},
            indent=2,
        )
    )
