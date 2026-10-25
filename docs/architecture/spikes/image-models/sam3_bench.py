"""SAM 3 image concepts / SAM 3.1 propagation in the isolated Linux runtime."""

import argparse
import json
from pathlib import Path
import time
import traceback

from hf_context import configure

configure()
root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("version")
version = parser.parse_args().version
report = {"family": version, "status": "running", "observations": []}
began = time.perf_counter()
try:
    import platform
    from PIL import Image
    import torch
    from huggingface_hub import HfApi, hf_hub_download

    torch.cuda.reset_peak_memory_stats()
    repo = "facebook/" + version
    sha = HfApi().model_info(repo).sha
    file = "sam3.pt" if version == "sam3" else "sam3.1_multiplex.pt"
    path = hf_hub_download(repo, file, revision=sha)
    report["checkpoint"] = {"repo": repo, "revision": sha, "file": file}
    report["environment"] = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "torch": torch.__version__,
    }
    if version == "sam3":
        from sam3.model_builder import build_sam3_image_model
        from sam3.model.sam3_image_processor import Sam3Processor

        model = build_sam3_image_model(
            checkpoint_path=path, load_from_HF=False, compile=False
        )
        processor = Sam3Processor(model)
        report["load_seconds"] = time.perf_counter() - began
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
            for fixture, prompts in [
                ("objects", ["dog", "cat", "elephant"]),
                ("diagram", ["diagram", "text"]),
                ("ui", ["search input field", "button", "line chart"]),
            ]:
                image = Image.open(root / f"fixtures/{fixture}.jpg").convert("RGB")
                start = time.perf_counter()
                state = processor.set_image(image)
                torch.cuda.synchronize()
                encode_s = time.perf_counter() - start
                for prompt in prompts:
                    processor.reset_all_prompts(state)
                    start = time.perf_counter()
                    output = processor.set_text_prompt(state=state, prompt=prompt)
                    torch.cuda.synchronize()
                    obs = {
                        "fixture": fixture,
                        "prompt": prompt,
                        "encode_seconds": encode_s,
                        "prompt_seconds": time.perf_counter() - start,
                        "boxes": output["boxes"].cpu().tolist(),
                        "scores": output["scores"].cpu().tolist(),
                    }
                    report["observations"].append(obs)
                    if len(output["masks"]):
                        mask = output["masks"][0].squeeze().cpu().numpy()
                        Image.fromarray((mask > 0).astype("uint8") * 255).save(
                            root / f"sam3-{fixture}-{prompt.replace(' ', '-')}-mask.png"
                        )
    else:
        from sam3.model_builder import build_sam3_predictor

        predictor = build_sam3_predictor(
            checkpoint_path=path,
            version="sam3.1",
            compile=False,
            warm_up=False,
            use_fa3=False,
            async_loading_frames=False,
            max_num_objects=4,
            multiplex_count=16,
        )
        frames = root.parents[3] / ".scratch/image-model-spike/track-frames"
        start = time.perf_counter()
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
            session = predictor.handle_request(
                {"type": "start_session", "resource_path": str(frames)}
            )
            sid = session["session_id"]
            response = predictor.handle_request(
                {
                    "type": "add_prompt",
                    "session_id": sid,
                    "frame_index": 0,
                    "text": "diagram",
                }
            )
            report["initial_response_keys"] = list(response)
            for item in predictor.handle_stream_request(
                {"type": "propagate_in_video", "session_id": sid}
            ):
                index = item.get("frame_index")
                payload = item.get("outputs", item)
                obs = {"frame": index, "keys": list(payload)}
                for key in [
                    "out_obj_ids",
                    "out_probs",
                    "out_boxes_xywh",
                    "out_boxes_xyxy",
                ]:
                    if key in payload:
                        value = payload[key]
                        obs[key] = value.tolist() if hasattr(value, "tolist") else value
                report["observations"].append(obs)
            predictor.handle_request({"type": "close_session", "session_id": sid})
        torch.cuda.synchronize()
        report["inference_seconds"] = time.perf_counter() - start
        report["limit"] = (
            "Text-discovered diagram across four sparse captured frames; unlike the manual box seeds used for earlier trackers"
        )
    report["status"] = "ran"
except Exception as exc:
    report.update(
        status="runtime_or_setup_failure",
        error_type=type(exc).__name__,
        error=str(exc)[:2000],
        traceback=traceback.format_exc()[-3500:],
    )
report["total_seconds"] = time.perf_counter() - began
try:
    report["peak_cuda_allocated_bytes"] = torch.cuda.max_memory_allocated()
except Exception:
    pass
(root / f"{version}.json").write_text(json.dumps(report, indent=2, default=str) + "\n")
print(
    json.dumps(
        {k: v for k, v in report.items() if k not in ["observations", "traceback"]},
        indent=2,
    )
)
