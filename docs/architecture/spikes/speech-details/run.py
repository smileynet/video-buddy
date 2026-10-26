"""THROWAWAY: same-machine/model-settings speech probe; no production integration."""

import argparse
import subprocess
import sys
import hashlib
import json
from pathlib import Path
import platform
import threading
import time

from huggingface_hub import snapshot_download
import psutil

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("option")
    parser.add_argument("--natural", action="store_true")
    parser.add_argument("--tutorial", action="store_true")
    parser.add_argument("--model-reviewed", action="store_true")
    args = parser.parse_args()
    reference_file = (
        "model-reviewed-references.json"
        if args.model_reviewed
        else "references-tutorial.json"
        if args.tutorial
        else "references-natural.json"
        if args.natural
        else "references.json"
    )
    suffix = (
        "-model-reviewed"
        if args.model_reviewed
        else "-tutorial"
        if args.tutorial
        else "-natural"
        if args.natural
        else ""
    )
    protocol = json.loads((HERE / "protocol.json").read_text())
    refs = json.loads((HERE / reference_file).read_text())
    config = next(o for o in protocol["options"] if o["id"] == args.option)
    for fixture in refs["fixtures"]:
        assert sha(Path(fixture["path"])) == fixture["sha256"]
    model_path = Path(
        snapshot_download(
            config["repo"], revision=config["revision"], local_files_only=True
        )
    )
    config["model_files"] = {
        p.name: {"sha256": sha(p)} for p in model_path.iterdir() if p.is_file()
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
    load_seconds = 0
    outputs = []
    try:
        for fixture in refs["fixtures"]:
            start = time.perf_counter()
            output_path = (
                Path(".scratch/speech-details")
                / f"worker-{args.option}-{fixture['id']}.json"
            )
            command = [
                sys.executable,
                "workers/transcribe_worker.py",
                fixture["path"],
                "--output",
                str(output_path),
                "--model",
                str(model_path),
                "--device",
                config["device"],
                "--compute-type",
                config["compute_type"],
                "--spike-config",
                str(HERE / "protocol.json"),
            ]
            subprocess.run(command, check=True, capture_output=True)
            result = json.loads(output_path.read_text())
            load_seconds += result["load_seconds"]
            outputs.append(
                {
                    "fixture": fixture["id"],
                    "worker_wall_seconds": time.perf_counter() - start,
                    **result,
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
        "references_sha256": sha(HERE / reference_file),
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
    (HERE / f"raw-{args.option}{suffix}.json").write_text(
        json.dumps(output, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
