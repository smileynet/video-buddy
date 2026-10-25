"""Pinned GUI specialist with its actual grounding-token decoder, no UI actions."""

import json
from pathlib import Path
import time
import traceback

from PIL import Image
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor, BitsAndBytesConfig

root = Path(__file__).resolve().parent
repo = "allenai/MolmoPoint-GUI-8B"
revision = "0337d39b721d0ce6fa9b315b158ac11c63e0dedc"
queries = [
    [
        "browser-search",
        "Point to the Google page search box containing today's price of microsoft, below the browser address bar.",
        [390, 205, 1776, 300],
    ],
    [
        "windows-search",
        "Point to the white Windows taskbar Search field with the magnifying glass at the bottom of the screen.",
        [1138, 2081, 1574, 2141],
    ],
    [
        "follow",
        "Point to the blue + Follow button on the Google stock result.",
        [1582, 802, 1736, 861],
    ],
    [
        "overview",
        "Point to the outlined Overview pill above the stock chart.",
        [1022, 536, 1223, 619],
    ],
]
report = {
    "repo": repo,
    "revision": revision,
    "status": "running",
    "config": {
        "language": "NF4",
        "vision": "bfloat16",
        "max_crops": 2,
        "max_new_tokens": 128,
    },
    "observations": [],
    "limits": "Four scoped queries on one previously inspected public UI screenshot; coarse target boxes, not independent held-out GUI qualification. Model returns points, no click is executed.",
}
start = time.perf_counter()
try:
    torch.cuda.reset_peak_memory_stats()
    quant = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        llm_int8_skip_modules=["vision_backbone"],
    )
    model = AutoModelForImageTextToText.from_pretrained(
        repo,
        revision=revision,
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
        quantization_config=quant,
        device_map={"": 0},
        low_cpu_mem_usage=True,
    ).eval()
    processor = AutoProcessor.from_pretrained(
        repo, revision=revision, trust_remote_code=True, padding_side="left"
    )
    processor.image_processor.max_crops = 2
    report["load_seconds"] = time.perf_counter() - start
    image = Image.open(root.parent / "image-models/fixtures/ui.jpg").convert("RGB")
    for label, prompt, box in queries:
        began = time.perf_counter()
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image", "image": image},
                ],
            }
        ]
        inputs = processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True,
            padding=True,
            return_pointing_metadata=True,
        )
        metadata = inputs.pop("metadata")
        inputs = {k: v.to("cuda") for k, v in inputs.items()}
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
            generated = model.generate(
                **inputs,
                logits_processor=model.build_logit_processor_from_inputs(inputs),
                max_new_tokens=128,
                do_sample=False,
            )
        tokens = generated[:, inputs["input_ids"].shape[1] :]
        text = processor.post_process_image_text_to_text(
            tokens, skip_special_tokens=False, clean_up_tokenization_spaces=False
        )[0]
        points = model.extract_image_points(
            text,
            metadata["token_pooling"],
            metadata["subpatch_mapping"],
            metadata["image_sizes"],
        )
        points = [[float(v) for v in point] for point in points]
        torch.cuda.synchronize()
        report["observations"].append(
            {
                "target": label,
                "prompt": prompt,
                "reference_box": box,
                "raw": text,
                "points": points,
                "point_inside_target": any(
                    box[0] <= p[2] <= box[2] and box[1] <= p[3] <= box[3]
                    for p in points
                ),
                "generated_tokens": tokens.shape[1],
                "seconds": time.perf_counter() - began,
            }
        )
    report["status"] = "ran"
except Exception as exc:
    report.update(
        status="runtime_or_setup_failure",
        error=str(exc)[:1800],
        traceback=traceback.format_exc()[-3000:],
    )
report["total_seconds"] = time.perf_counter() - start
report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated()
(root / "molmopoint-gui.json").write_text(json.dumps(report, indent=2) + "\n")
print(
    json.dumps(
        {k: v for k, v in report.items() if k not in ["observations", "traceback"]},
        indent=2,
    )
)
