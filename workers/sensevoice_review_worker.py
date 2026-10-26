"""THROWAWAY ticket 15 CLI: blind waveform review, never human verification."""

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import threading
import time
import wave

import numpy as np
import psutil
import sherpa_onnx


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--tokens", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    protocol = json.loads(args.protocol.read_text())
    process = psutil.Process()
    samples = []
    stop = threading.Event()

    def monitor():
        while not stop.is_set():
            samples.append(process.memory_info().rss)
            stop.wait(0.02)

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    start = time.perf_counter()
    recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
        model=str(args.model), tokens=str(args.tokens), **protocol["settings"]
    )
    load_seconds = time.perf_counter() - start
    results = []
    try:
        for clip in protocol["clips"]:
            path = Path(clip["path"])
            assert sha(path) == clip["sha256"]
            with wave.open(str(path), "rb") as reader:
                assert (
                    reader.getnchannels() == 1
                    and reader.getsampwidth() == 2
                    and reader.getframerate() == 16000
                )
                pcm = reader.readframes(reader.getnframes())
            audio = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768
            start = time.perf_counter()
            stream = recognizer.create_stream()
            # Only numeric waveform enters the recognizer. No transcript or target hints.
            stream.accept_waveform(16000, audio)
            recognizer.decode_stream(stream)
            elapsed = time.perf_counter() - start
            result = stream.result
            row = {
                "clip": clip["id"],
                "audio_sha256": clip["sha256"],
                "duration": len(audio) / 16000,
                "text": result.text,
                "tokens": list(result.tokens),
                "timestamps": list(result.timestamps),
                "native_result": str(result),
                "seconds": elapsed,
                "reference_type": "model_reviewed_provisional",
                "human_verified": False,
            }
            results.append(row)
            print(
                json.dumps(
                    {
                        "clip": clip["id"],
                        "seconds": elapsed,
                        "tokens": len(row["tokens"]),
                    }
                ),
                flush=True,
            )
    finally:
        stop.set()
        thread.join()
    output = {
        "reviewer": "SenseVoiceSmall int8 2024-07-17",
        "runtime": importlib.metadata.version("sherpa-onnx"),
        "protocol_sha256": sha(args.protocol),
        "model_sha256": sha(args.model),
        "tokens_sha256": sha(args.tokens),
        "settings": protocol["settings"],
        "input_modality": "waveform only",
        "load_seconds": load_seconds,
        "sampled_peak_root_rss": max(samples),
        "sampling_seconds": 0.02,
        "timing_kind": "model token time points, not verified word intervals",
        "reference_type": "model_reviewed_provisional",
        "human_verified": False,
        "results": results,
    }
    args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
