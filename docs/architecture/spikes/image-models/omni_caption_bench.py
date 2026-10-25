"""Probe official OmniParser icon captions on four detected control crops."""

import json
from pathlib import Path
import time
import traceback
from hf_context import configure

import torch
from PIL import Image
from huggingface_hub import HfApi, hf_hub_download
from transformers import AutoProcessor, AutoModelForCausalLM

configure()

root = Path(__file__).resolve().parent
report = {"status": "running", "observations": []}
start = time.perf_counter()
try:
    repo = "microsoft/OmniParser-v2.0"
    sha = HfApi().model_info(repo).sha
    paths = [
        hf_hub_download(repo, "icon_caption/" + f, revision=sha)
        for f in ["config.json", "generation_config.json", "model.safetensors"]
    ]
    directory = Path(paths[0]).parent
    model = (
        AutoModelForCausalLM.from_pretrained(
            directory,
            torch_dtype=torch.float16,
            trust_remote_code=True,
            attn_implementation="eager",
        )
        .to("cuda")
        .eval()
    )
    p_repo = "microsoft/Florence-2-base"
    p_sha = HfApi().model_info(p_repo).sha
    processor = AutoProcessor.from_pretrained(
        p_repo, revision=p_sha, trust_remote_code=True
    )
    report["revisions"] = {repo: sha, p_repo: p_sha}
    image = Image.open(root / "fixtures/ui.jpg").convert("RGB")
    boxes = json.loads((root / "omniparser.json").read_text())["observations"][0][
        "boxes"
    ]
    for name, (x, y) in {
        "follow": (1660, 830),
        "search": (1000, 250),
        "overview": (1120, 575),
        "images": (1800, 370),
    }.items():
        choices = [b for b in boxes if b[0] <= x <= b[2] and b[1] <= y <= b[3]]
        if not choices:
            report["observations"].append(
                {
                    "target": name,
                    "result": "no detected box contains manually selected center",
                }
            )
            continue
        box = min(choices, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
        crop = image.crop(tuple(map(int, box))).resize((64, 64))
        crop.save(root / f"omni-{name}-crop.png")
        inputs = processor(
            images=crop, text="<CAPTION>", return_tensors="pt", do_resize=False
        ).to("cuda", torch.float16)
        begun = time.perf_counter()
        with torch.inference_mode():
            ids = model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=20,
                num_beams=1,
                do_sample=False,
            )
        torch.cuda.synchronize()
        report["observations"].append(
            {
                "target": name,
                "box": box,
                "caption": processor.batch_decode(ids, skip_special_tokens=True)[
                    0
                ].strip(),
                "seconds": time.perf_counter() - begun,
            }
        )
    report["status"] = "ran"
except Exception as e:
    report.update(
        status="runtime_or_setup_failure",
        error_type=type(e).__name__,
        error=str(e)[:1500],
        traceback=traceback.format_exc()[-2000:],
    )
report["total_seconds"] = time.perf_counter() - start
report["limit"] = (
    "Detector + official icon-caption component probe, manually selected target centers; not complete OmniParser OCR merging or GUI actions"
)
(root / "omniparser-captions.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k != "traceback"}, indent=2))
