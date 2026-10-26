"""THROWAWAY: same-machine/model-settings speech probe; no production integration."""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import threading
import time

from faster_whisper import WhisperModel
from huggingface_hub import snapshot_download
import psutil

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("option")
    args = parser.parse_args()
    protocol = json.loads((HERE / "protocol.json").read_text())
    refs = json.loads((HERE / "references.json").read_text())
    config = next(o for o in protocol["options"] if o["id"] == args.option)
    for fixture in refs["fixtures"]:
        assert sha(Path(fixture["path"])) == fixture["sha256"]
    model_path = Path(
        snapshot_download(
            config["repo"], revision=config["revision"], local_files_only=True
        )
    )
    config["model_files"] = {
        p.name: sha(p) for p in model_path.iterdir() if p.is_file()
    }
    stop = threading.Event()
    peaks = []
    root = psutil.Process()

    def monitor():
        while not stop.is_set():
            total = 0
            for process in [root, *root.children(recursive=True)]:
                try:
                    total += process.memory_info().rss
                except psutil.Error:
                    pass
            peaks.append(total)
            stop.wait(0.02)

    worker = threading.Thread(target=monitor, daemon=True)
    worker.start()
    start = time.perf_counter()
    model = WhisperModel(
        str(model_path),
        device=config["device"],
        compute_type=config["compute_type"],
        cpu_threads=8,
        num_workers=1,
    )
    load_seconds = time.perf_counter() - start
    outputs = []
    try:
        for fixture in refs["fixtures"]:
            start = time.perf_counter()
            settings = {
                k: v
                for k, v in protocol["settings"].items()
                if k not in ["cpu_threads", "num_workers"]
            }
            segments, info = model.transcribe(fixture["path"], **settings)
            segments = [s._asdict() for s in segments]
            for segment in segments:
                if segment["words"] is not None:
                    segment["words"] = [w._asdict() for w in segment["words"]]
            outputs.append(
                {
                    "fixture": fixture["id"],
                    "seconds": time.perf_counter() - start,
                    "duration": info.duration,
                    "duration_after_vad": info.duration_after_vad,
                    "segments": segments,
                }
            )
            print(
                json.dumps(
                    {
                        "option": args.option,
                        "fixture": fixture["id"],
                        "seconds": outputs[-1]["seconds"],
                    }
                ),
                flush=True,
            )
    finally:
        stop.set()
        worker.join()
    output = {
        "option": config,
        "settings": protocol["settings"],
        "protocol_sha256": sha(HERE / "protocol.json"),
        "references_sha256": sha(HERE / "references.json"),
        "host": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "logical_cpu": psutil.cpu_count(),
        },
        "load_seconds": load_seconds,
        "peak_sampled_root_children_rss": max(peaks),
        "rss_samples": len(peaks),
        "sampling_seconds": 0.02,
        "outputs": outputs,
    }
    (HERE / f"raw-{args.option}.json").write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
