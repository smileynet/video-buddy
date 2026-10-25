"""Same pointing queries on the earlier Qwen candidate; no precision parity claim."""

import json
from pathlib import Path
import time
import traceback

import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

root = Path(__file__).resolve().parent
repo = "Qwen/Qwen3-VL-2B-Instruct"
revision = "89644892e4d85e24eaac8bacfd4f463576704203"
report = {
    "repo": repo,
    "revision": revision,
    "config": {"dtype": "bfloat16", "max_pixels": 262144, "max_new_tokens": 128},
    "status": "running",
    "observations": [],
}
start = time.perf_counter()
try:
    torch.cuda.reset_peak_memory_stats()
    model = (
        AutoModelForImageTextToText.from_pretrained(
            repo,
            revision=revision,
            torch_dtype=torch.bfloat16,
            attn_implementation="sdpa",
        )
        .to("cuda")
        .eval()
    )
    processor = AutoProcessor.from_pretrained(
        repo, revision=revision, min_pixels=128 * 128, max_pixels=512 * 512
    )
    report["load_seconds"] = time.perf_counter() - start
    for query in json.loads((root / "molmo2-nf4.json").read_text())["observations"]:
        path = root.parent / query["fixture"]
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": str(path)},
                    {"type": "text", "text": query["prompt"]},
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
        began = time.perf_counter()
        with torch.inference_mode():
            ids = model.generate(**inputs, max_new_tokens=128, do_sample=False)
        torch.cuda.synchronize()
        output = processor.batch_decode(
            ids[:, inputs["input_ids"].shape[1] :], skip_special_tokens=True
        )[0]
        report["observations"].append(
            {
                "fixture": query["fixture"],
                "prompt": query["prompt"],
                "output": output,
                "generated_tokens": int(ids.shape[1] - inputs["input_ids"].shape[1]),
                "seconds": time.perf_counter() - began,
            }
        )
    report["status"] = "ran"
except Exception as exc:
    report.update(
        status="runtime_or_setup_failure",
        error_type=type(exc).__name__,
        error=str(exc)[:1600],
        traceback=traceback.format_exc()[-2500:],
    )
report["total_seconds"] = time.perf_counter() - start
report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated()
(root / "qwen-pointing.json").write_text(json.dumps(report, indent=2) + "\n")
print(
    json.dumps(
        {k: v for k, v in report.items() if k not in ["observations", "traceback"]},
        indent=2,
    )
)
