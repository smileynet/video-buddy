"""THROWAWAY: run one frozen local narration candidate; no app integration."""

import argparse
import hashlib
import importlib.metadata as metadata
import inspect
import json
import os
from pathlib import Path
import random
import subprocess
import threading
import time
import traceback


def main():
    started = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["qwen", "chatterbox"], required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    protocol = json.loads(args.protocol.read_text(encoding="utf-8"))
    ref = args.protocol.parent / protocol["reference"]["file"]
    assert (
        hashlib.sha256(ref.read_bytes()).hexdigest() == protocol["reference"]["sha256"]
    )
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    result = {
        "model": args.model,
        "protocol_sha256": hashlib.sha256(args.protocol.read_bytes()).hexdigest(),
        "cases": [],
        "phases": {},
        "offline_hub_flags": True,
        "network_behavior_audited": False,
    }
    target = args.out / f"{args.model}-results.json"
    stop = threading.Event()
    phase = ["imports"]
    samples = []
    import psutil

    proc = psutil.Process()

    def sample():
        while not stop.is_set():
            row = {
                "elapsed_s": time.perf_counter() - started,
                "phase": phase[0],
                "rss_bytes": proc.memory_info().rss,
            }
            try:
                text = (
                    subprocess.check_output(
                        [
                            "nvidia-smi",
                            "--query-gpu=memory.used,utilization.gpu,power.draw",
                            "--format=csv,noheader,nounits",
                        ],
                        text=True,
                        timeout=5,
                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                    )
                    .strip()
                    .splitlines()[0]
                )
                values = [float(x.strip()) for x in text.split(",")]
                row.update(
                    device_used_mib=values[0],
                    device_util_pct=values[1],
                    device_power_w=values[2],
                )
            except Exception as exc:
                row["gpu_sample_error"] = type(exc).__name__
            samples.append(row)
            stop.wait(0.5)

    thread = threading.Thread(target=sample, daemon=True)
    thread.start()
    try:
        import numpy as np
        import soundfile as sf
        import torch

        torch.set_num_threads(8)
        torch.set_num_interop_threads(4)
        torch.cuda.synchronize()
        result["device"] = {
            "name": torch.cuda.get_device_name(0),
            "capability": torch.cuda.get_device_capability(0),
            "total_bytes": torch.cuda.get_device_properties(0).total_memory,
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "threads": torch.get_num_threads(),
        }
        result["packages"] = {
            d.metadata["Name"]: d.version for d in metadata.distributions()
        }
        result["phases"]["imports_cuda_init_s"] = time.perf_counter() - started
        phase[0] = "model_load"
        t = time.perf_counter()
        if args.model == "qwen":
            from qwen_tts import Qwen3TTSModel

            model = Qwen3TTSModel.from_pretrained(
                str(args.snapshot),
                device_map="cuda:0",
                dtype=torch.bfloat16,
                attn_implementation="sdpa",
            )
            result["generation_config"] = getattr(model.model, "generate_config", None)
            if result["generation_config"] is None:
                result["generation_config"] = model.model.generation_config.to_dict()
        else:
            from chatterbox.tts_turbo import ChatterboxTurboTTS

            model = ChatterboxTurboTTS.from_local(args.snapshot, device="cuda")
            if model.watermarker is None:
                raise RuntimeError(
                    "Official watermark implementation unavailable; no bypass applied"
                )
            result["generation_config"] = {
                "signature": str(inspect.signature(model.generate)),
                "watermarker": type(model.watermarker).__name__,
                "norm_loudness": True,
            }
        torch.cuda.synchronize()
        result["phases"]["model_load_s"] = time.perf_counter() - t
        phase[0] = "reference_conditioning"
        t = time.perf_counter()
        if args.model == "qwen":
            prompt = model.create_voice_clone_prompt(
                ref_audio=str(ref),
                ref_text=protocol["reference"]["transcript"],
                x_vector_only_mode=False,
            )
        else:
            model.prepare_conditionals(str(ref), exaggeration=0.0, norm_loudness=True)
        torch.cuda.synchronize()
        result["phases"]["reference_conditioning_s"] = time.perf_counter() - t
        for case in protocol["cases"]:
            phase[0] = case["id"]
            random.seed(case["seed"])
            np.random.seed(case["seed"])
            torch.manual_seed(case["seed"])
            torch.cuda.manual_seed_all(case["seed"])
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
            cpu = proc.cpu_times()
            t = time.perf_counter()
            with torch.inference_mode():
                if args.model == "qwen":
                    waves, sr = model.generate_voice_clone(
                        text=protocol["texts"][case["text"]],
                        language="English",
                        voice_clone_prompt=prompt,
                    )
                    audio = np.asarray(waves[0], dtype=np.float32)
                else:
                    wave = model.generate(protocol["texts"][case["text"]])
                    sr = model.sr
                    audio = wave.detach().cpu().numpy().reshape(-1).astype(np.float32)
            torch.cuda.synchronize()
            wall = time.perf_counter() - t
            row = dict(
                case,
                wall_s=wall,
                sample_rate=sr,
                samples=len(audio),
                duration_s=len(audio) / sr,
                rtf=wall / (len(audio) / sr),
                cuda_peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                cuda_peak_reserved_bytes=torch.cuda.max_memory_reserved(),
                peak_abs=float(np.max(np.abs(audio))),
                rms=float(np.sqrt(np.mean(audio**2))),
                nonfinite=int(np.count_nonzero(~np.isfinite(audio))),
                clipped_fraction=float(np.mean(np.abs(audio) >= 1)),
                cpu_s=(proc.cpu_times().user + proc.cpu_times().system)
                - (cpu.user + cpu.system),
            )
            path = args.out / f"{args.model}-{case['id']}.wav"
            sf.write(path, audio, sr, subtype="PCM_16")
            row["file"] = path.name
            row["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            result["cases"].append(row)
            target.write_text(json.dumps(result, indent=2, default=str) + "\n")
            print(
                json.dumps(
                    {
                        "model": args.model,
                        "case": case["id"],
                        "wall_s": round(wall, 3),
                        "audio_s": round(len(audio) / sr, 3),
                        "rtf": round(row["rtf"], 3),
                    }
                ),
                flush=True,
            )
        result["status"] = "complete"
    except Exception as exc:
        result.update(
            status="failed",
            failed_phase=phase[0],
            error=repr(exc),
            traceback=traceback.format_exc(),
        )
        print(result["traceback"], flush=True)
    finally:
        stop.set()
        thread.join(timeout=7)
        result["wall_total_s"] = time.perf_counter() - started
        result["resource_samples"] = samples
        result["measurement_limits"] = (
            "Sampled RSS/device totals include measurement overhead and other GPU users. CUDA allocator peaks omit non-Torch memory. Generation timing excludes saving files; reference and model load separate. No exclusive-device/isolated throughput claim."
        )
        target.write_text(json.dumps(result, indent=2, default=str) + "\n")
        print("result", target, "status", result["status"], flush=True)


if __name__ == "__main__":
    main()
