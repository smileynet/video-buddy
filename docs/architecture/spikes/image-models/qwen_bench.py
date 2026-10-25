"""Bounded local visual-reasoning challenger from the prior tool shortlist."""

import json
from pathlib import Path
import time
import traceback
from hf_context import configure

import torch
from huggingface_hub import HfApi
from transformers import AutoProcessor, AutoModelForImageTextToText

configure()

root = Path(__file__).resolve().parent
report = {"family": "qwen3vl", "status": "running", "observations": []}
began = time.perf_counter()
torch.cuda.reset_peak_memory_stats()
try:
    name = "Qwen/Qwen3-VL-2B-Instruct"
    sha = HfApi().model_info(name).sha
    model = (
        AutoModelForImageTextToText.from_pretrained(
            name, revision=sha, torch_dtype=torch.bfloat16, attn_implementation="sdpa"
        )
        .to("cuda")
        .eval()
    )
    processor = AutoProcessor.from_pretrained(
        name, revision=sha, min_pixels=128 * 128, max_pixels=512 * 512
    )
    report["checkpoint"] = {"repo": name, "revision": sha, "max_pixels": 512 * 512}
    tasks = [
        (
            "objects.jpg",
            "List the visible animals and report whether an elephant is visible. Be literal.",
        ),
        (
            "real-settings.png",
            "Transcribe the visible text exactly. Output only the text; do not correct or invent characters.",
        ),
        (
            "ui.jpg",
            "Identify the search field, Follow button and Overview tab. Describe them concisely; do not claim any action was performed.",
        ),
    ]
    for fixture, prompt in tasks:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": str(root / "fixtures" / fixture)},
                    {"type": "text", "text": prompt},
                ],
            }
        ]
        inputs = processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        ).to("cuda")
        start = time.perf_counter()
        with torch.inference_mode():
            ids = model.generate(**inputs, max_new_tokens=180, do_sample=False)
        text = processor.batch_decode(
            ids[:, inputs["input_ids"].shape[1] :], skip_special_tokens=True
        )[0]
        torch.cuda.synchronize()
        report["observations"].append(
            {
                "fixture": fixture,
                "prompt": prompt,
                "response": text,
                "seconds": time.perf_counter() - start,
            }
        )
    report["status"] = "ran"
except Exception as e:
    report.update(
        status="runtime_or_setup_failure",
        error_type=type(e).__name__,
        error=str(e)[:1600],
        traceback=traceback.format_exc()[-2500:],
    )
report["total_seconds"] = time.perf_counter() - began
report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated()
(root / "qwen3vl.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k != "traceback"}, indent=2))
