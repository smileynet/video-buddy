"""Bounded Molmo2 NF4 candidate, separate from full-precision qualification."""

import argparse
import json
from pathlib import Path
import time
import traceback

from PIL import Image
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor, BitsAndBytesConfig

parser = argparse.ArgumentParser()
parser.add_argument("--max-new-tokens", type=int, default=64)
max_tokens = parser.parse_args().max_new_tokens
suffix = "" if max_tokens == 64 else "-" + str(max_tokens)
root = Path(__file__).resolve().parent
sources = root.parent
repo = "allenai/Molmo2-4B"
revision = "042abfa7a38879a376cec03d949eff0aefaa0600"
report = {
    "repo": repo,
    "revision": revision,
    "status": "running",
    "config": {
        "quantization": "NF4 language / bfloat16 vision",
        "compute_dtype": "bfloat16",
        "max_crops": 2,
        "max_new_tokens": max_tokens,
        "device": "cuda:0",
        "limit": "Quantized image-only smoke probe; not full-precision, GUI-specialist or temporal qualification",
    },
    "observations": [],
}
start = time.perf_counter()
try:
    torch.cuda.reset_peak_memory_stats()
    processor = AutoProcessor.from_pretrained(
        repo, revision=revision, trust_remote_code=True
    )
    processor.image_processor.max_crops = 2
    quantization = BitsAndBytesConfig(
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
        quantization_config=quantization,
        device_map={"": 0},
        low_cpu_mem_usage=True,
    ).eval()
    report["load_seconds"] = time.perf_counter() - start
    for path, prompt in [
        (sources / "image-models/fixtures/objects.jpg", "Point to the dog."),
        (sources / "image-models/fixtures/objects.jpg", "Point to the elephant."),
        (sources / "image-models/fixtures/ui.jpg", "Point to the search input field."),
        (
            sources / "image-models/fixtures/diagram.jpg",
            "Point to the text showing harmonic settings.",
        ),
    ]:
        image = Image.open(path).convert("RGB")
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt},
                ],
            }
        ]
        began = time.perf_counter()
        inputs = processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True,
        )
        inputs = {
            k: v.to(model.device) if hasattr(v, "to") else v for k, v in inputs.items()
        }
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
            generated = model.generate(
                **inputs, max_new_tokens=max_tokens, do_sample=False
            )
        torch.cuda.synchronize()
        output = processor.tokenizer.decode(
            generated[0, inputs["input_ids"].shape[1] :], skip_special_tokens=True
        )
        report["observations"].append(
            {
                "fixture": str(path.relative_to(sources)),
                "prompt": prompt,
                "output": output,
                "generated_tokens": int(
                    generated.shape[1] - inputs["input_ids"].shape[1]
                ),
                "seconds": time.perf_counter() - began,
            }
        )
    report["status"] = "ran"
except Exception as exc:
    report.update(
        status="runtime_or_setup_failure",
        error_type=type(exc).__name__,
        error=str(exc)[:1800],
        traceback=traceback.format_exc()[-3500:],
    )
report["total_seconds"] = time.perf_counter() - start
report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated()
(root / ("molmo2-nf4" + suffix + ".json")).write_text(
    json.dumps(report, indent=2) + "\n"
)
print(
    json.dumps(
        {k: v for k, v in report.items() if k not in ["observations", "traceback"]},
        indent=2,
    )
)
