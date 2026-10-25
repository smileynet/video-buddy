"""Sparse predecoded-frame pointing; not continuous/native-video qualification."""

import argparse
import json
from pathlib import Path
import time
import traceback

import numpy as np
from PIL import Image
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor, BitsAndBytesConfig

parser = argparse.ArgumentParser()
parser.add_argument("--all-frames", action="store_true")
all_frames = parser.parse_args().all_frames
root = Path(__file__).resolve().parent
repo = "allenai/MolmoPoint-Vid-4B"
revision = "b331ed6c6352e6db967325493c6dae515541a919"
report = {
    "repo": repo,
    "revision": revision,
    "status": "running",
    "config": {
        "language": "NF4",
        "vision": "bfloat16",
        "max_new_tokens": 128,
        "sampling": "none; four supplied frames with explicit relative timestamps",
    },
    "observations": [],
    "limits": "Predecoded sparse-frame video-processor input, not native-video decoding, all-frame coverage or long-video drift. Controlled dog sequence is derived from one photo.",
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
    report["load_seconds"] = time.perf_counter() - start
    for label, folder, times, prompt in [
        ("controlled-dog", root / "sam31-controlled", [0, 1, 2, 3], "Track the dog."),
        (
            "controlled-negative",
            root / "sam31-controlled",
            [0, 1, 2, 3],
            "Point to the elephant.",
        ),
        (
            "real-diagram",
            root.parents[3] / ".scratch/image-model-spike/track-frames",
            [0, 6, 8, 10],
            "Track the circular diagram panel in the middle.",
        ),
    ]:
        if all_frames:
            prompt += " Return a point in every supplied frame at each timestamp, preserving object identity."
        row = {"case": label, "prompt": prompt, "relative_requested_times": times}
        began = time.perf_counter()
        try:
            paths = sorted(folder.glob("*.jpg"))
            frames = np.stack([np.array(Image.open(p).convert("RGB")) for p in paths])
            row["input_frames"] = [p.name for p in paths]
            messages = [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}, {"type": "video"}],
                }
            ]
            text = processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            inputs = processor(
                text=text,
                videos=[frames],
                video_metadata=[
                    {
                        "total_num_frames": times[-1] + 1,
                        "fps": 1.0,
                        "duration": float(times[-1] + 1),
                        "width": frames.shape[2],
                        "height": frames.shape[1],
                        "frames_indices": times,
                    }
                ],
                do_sample_frames=False,
                return_tensors="pt",
                return_pointing_metadata=True,
            )
            metadata = inputs.pop("metadata")
            row["processed_times"] = [float(t) for t in metadata["timestamps"]]
            inputs = {k: v.to("cuda") for k, v in inputs.items()}
            with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
                output = model.generate(
                    **inputs,
                    logits_processor=model.build_logit_processor_from_inputs(inputs),
                    max_new_tokens=128,
                    do_sample=False,
                )
            tokens = output[:, inputs["input_ids"].shape[1] :]
            text = processor.post_process_image_text_to_text(
                tokens, skip_special_tokens=False, clean_up_tokenization_spaces=False
            )[0]
            points = model.extract_video_points(
                text,
                metadata["token_pooling"],
                metadata["subpatch_mapping"],
                metadata["timestamps"],
                metadata["video_size"],
            )
            torch.cuda.synchronize()
            row.update(
                status="ran",
                raw=text,
                points=[[float(x) for x in point] for point in points],
                generated_tokens=int(tokens.shape[1]),
                token_budget_exhausted=tokens.shape[1] >= 128,
            )
        except Exception as exc:
            row.update(
                status="runtime_failure",
                error=str(exc)[:1800],
                traceback=traceback.format_exc()[-2000:],
            )
        row["seconds"] = time.perf_counter() - began
        report["observations"].append(row)
    report["status"] = "recorded"
except Exception as exc:
    report.update(
        status="runtime_or_setup_failure",
        error=str(exc)[:1800],
        traceback=traceback.format_exc()[-2500:],
    )
report["total_seconds"] = time.perf_counter() - start
report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated()
(
    root
    / ("molmopoint-video-all-frames.json" if all_frames else "molmopoint-video.json")
).write_text(json.dumps(report, indent=2) + "\n")
print(
    json.dumps(
        {k: v for k, v in report.items() if k not in ["observations", "traceback"]},
        indent=2,
    )
)
