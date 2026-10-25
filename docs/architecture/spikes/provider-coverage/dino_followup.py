"""Matched bounded DINO feature probes, not a video tracking benchmark."""

import importlib
import json
from pathlib import Path
import sys
import time
import traceback

from PIL import Image, ImageDraw, ImageFont
import torch
from transformers import AutoImageProcessor, AutoModel

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root.parent / "image-models"))
configure = importlib.import_module("hf_context").configure

configure()
report = {"status": "running", "observations": []}
for name, revision in [
    ("facebook/dinov2-small", "ed25f3a31f01632728cabb09d1542f84ab7b0056"),
    (
        "facebook/dinov3-vits16-pretrain-lvd1689m",
        "114c1379950215c8b35dfcd4e90a5c251dde0d32",
    ),
]:
    start = time.perf_counter()
    row = {"repo": name, "revision": revision}
    try:
        if "dinov2" in name:
            revision = json.loads(
                (root.parent / "image-models/dinov2.json").read_text()
            )["revisions"][name]
            row["revision"] = revision
        processor = AutoImageProcessor.from_pretrained(name, revision=revision)
        model = AutoModel.from_pretrained(name, revision=revision).to("cuda").eval()
        patch = model.config.patch_size
        offset = 1 + getattr(model.config, "num_register_tokens", 0)
        original = Image.open(
            root.parent / "image-models/fixtures/text-dark-22-4.png"
        ).convert("RGB")
        changed = original.copy()
        draw = ImageDraw.Draw(changed)
        draw.rectangle((0, 0, 1100, 80), fill="#111827")
        draw.text(
            (15, 22),
            "port=8000",
            font=ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 22),
            fill="white",
        )
        inputs = processor(
            images=[original, changed],
            return_tensors="pt",
            do_center_crop=False,
            size={"height": 224, "width": 224},
        ).to("cuda")
        with torch.inference_mode():
            features = model(**inputs).last_hidden_state
        row["processed_pixel_l1"] = float(
            (inputs["pixel_values"][0] - inputs["pixel_values"][1]).abs().sum()
        )
        row["one_character_cls_cosine"] = float(
            torch.nn.functional.cosine_similarity(features[0:1, 0], features[1:2, 0])
        )
        natural = (
            Image.open(root.parent / "image-models/fixtures/objects.jpg")
            .convert("RGB")
            .resize((224, 224))
        )
        shifted = Image.new("RGB", (224, 224))
        shifted.paste(natural, (patch, 0))
        batch = processor(
            images=[natural, shifted],
            return_tensors="pt",
            do_resize=False,
            do_center_crop=False,
        ).to("cuda")
        with torch.inference_mode():
            tokens = model(**batch).last_hidden_state[:, offset:]
        grid = 224 // patch
        assert tokens.shape[1] == grid * grid
        tokens = torch.nn.functional.normalize(tokens, dim=-1)
        matches = []
        for x, y in [(4, 10), (11, 5), (12, 12), (5, 3), (8, 8)]:
            scores = tokens[0, y * grid + x] @ tokens[1].T
            index = int(scores.argmax())
            predicted = [index % grid, index // grid]
            matches.append(
                {
                    "source": [x, y],
                    "expected": [x + 1, y],
                    "predicted": predicted,
                    "exact": predicted == [x + 1, y],
                    "cosine": float(scores.max()),
                }
            )
        row.update(
            status="ran",
            patch_size=patch,
            register_offset=offset,
            shift_pixels=patch,
            matches=matches,
        )
        del model, inputs, batch, features, tokens
        torch.cuda.empty_cache()
    except Exception as exc:
        row.update(
            status="runtime_or_setup_failure",
            error=str(exc)[:1500],
            traceback=traceback.format_exc()[-2500:],
        )
    row["total_seconds"] = time.perf_counter() - start
    report["observations"].append(row)
report["status"] = "recorded"
report["limits"] = (
    "224px full-image resize; each model shifted one of its own patches (14 vs16px). Five selected natural-image patches and one controlled text revision, not held-out video association or a common score calibration."
)
(root / "dino-followup.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
