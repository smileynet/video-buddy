#!/usr/bin/env python3
"""Remote CrisperWhisper worker for a single audio file.

Runs inside the CrisperWhisper isolated venv on a GPU machine.
Same CLI contract as transcribe_worker.py: positional audio_path, --output, flags.
Outputs v2 schema JSON with word-level timestamps.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


def detect_device() -> str:
    try:
        import ctranslate2

        if ctranslate2.get_cuda_device_count() > 0:
            return "cuda"
    except Exception:
        pass
    return "cpu"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run CrisperWhisper on a remote audio file"
    )
    parser.add_argument("audio_path")
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="turbo")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    parser.add_argument(
        "--compute-type", default="float16", choices=["float16", "float32", "int8"]
    )
    parser.add_argument(
        "--mode", default="verbatim", choices=["verbatim", "intended"]
    )
    args = parser.parse_args(argv)

    audio_path = Path(args.audio_path)
    if not audio_path.exists():
        print(f"Error: audio file not found: {audio_path}", file=sys.stderr)
        return 1

    # Convert non-wav formats to wav (CrisperWhisper's soundfile requires wav/flac)
    if audio_path.suffix.lower() not in (".wav", ".flac"):
        import subprocess

        wav_path = audio_path.with_suffix(".wav")
        try:
            subprocess.run(
                ["ffmpeg", "-i", str(audio_path), "-ar", "16000", "-ac", "1", str(wav_path), "-y"],
                check=True, capture_output=True,
            )
            audio_path = wav_path
        except (subprocess.SubprocessError, FileNotFoundError) as exc:
            print(f"Error: failed to convert audio to wav: {exc}", file=sys.stderr)
            return 1

    try:
        from crisperwhisper import CrisperWhisperModel

        device = args.device if args.device != "auto" else detect_device()
        start = time.time()
        model = CrisperWhisperModel(
            args.model, device=device, compute_type=args.compute_type
        )
        result = model.transcribe(
            str(audio_path), mode=args.mode, word_timestamps=True
        )
        processing_time = time.time() - start
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    output = _format_v2(result, args.model, args.mode, processing_time)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return 0


def _format_v2(result, model_name: str, mode: str, processing_time: float) -> dict:
    """Convert CrisperWhisper TranscriptionResult to v2 schema."""
    words = []
    if result.words:
        for w in result.words:
            words.append({"start": w.start, "end": w.end, "text": w.word})

    # Group words into segments (~5-10s each) for compatibility
    segments = []
    if words:
        seg_words: list[dict] = []
        seg_start = words[0]["start"]
        for w in words:
            seg_words.append(w)
            # Break segment at sentence-ending punctuation or after ~8s
            is_sentence_end = w["text"].rstrip().endswith((".", "?", "!"))
            duration = w["end"] - seg_start
            if (is_sentence_end and duration > 3.0) or duration > 10.0:
                segments.append({
                    "start": seg_start,
                    "duration": round(w["end"] - seg_start, 3),
                    "text": " ".join(sw["text"] for sw in seg_words).strip(),
                    "words": seg_words,
                })
                seg_words = []
                seg_start = words[words.index(w) + 1]["start"] if w != words[-1] else w["end"]
        if seg_words:
            segments.append({
                "start": seg_start,
                "duration": round(seg_words[-1]["end"] - seg_start, 3),
                "text": " ".join(sw["text"] for sw in seg_words).strip(),
                "words": seg_words,
            })

    return {
        "schema_version": "2.0",
        "metadata": {
            "engine": "crisperwhisper",
            "model": model_name,
            "mode": mode,
            "processing_time": round(processing_time, 2),
            "audio_duration": round(result.duration, 2),
        },
        "segments": segments,
    }


if __name__ == "__main__":
    sys.exit(main())
