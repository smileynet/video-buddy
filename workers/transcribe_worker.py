#!/usr/bin/env python3
"""Remote faster-whisper worker for a single audio file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

COMPUTE_TYPES = ["auto", "float16", "float32", "int8", "int8_float16"]


def detect_device() -> str:
    try:
        import ctranslate2

        if ctranslate2.get_supported_compute_types("cuda"):
            return "cuda"
    except Exception:
        pass
    return "cpu"


def default_compute_type(device: str) -> str:
    return "float16" if device == "cuda" else "int8"


def resolve_execution(device: str, compute_type: str) -> tuple[str, str]:
    import ctranslate2

    resolved_device = device if device != "auto" else detect_device()
    supported = list(ctranslate2.get_supported_compute_types(resolved_device) or [])
    if resolved_device == "cuda" and not supported:
        raise RuntimeError("CUDA requested but unavailable on remote host")
    resolved_compute_type = (
        compute_type
        if compute_type != "auto"
        else default_compute_type(resolved_device)
    )
    if resolved_compute_type not in supported:
        raise RuntimeError(
            f"Unsupported compute type {resolved_compute_type!r} for {resolved_device}. Supported: {supported}"
        )
    return resolved_device, resolved_compute_type


def _segments_to_captions(segments) -> list[dict]:
    captions = []
    for segment in segments:
        text = segment.text.strip()
        if not text:
            continue
        captions.append(
            {
                "start": segment.start,
                "duration": round(segment.end - segment.start, 3),
                "text": text,
            }
        )
    return captions


def transcribe_audio(
    audio_path: Path, *, model_name: str, device: str, compute_type: str
) -> list[dict]:
    from faster_whisper import WhisperModel

    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments, _ = model.transcribe(str(audio_path), vad_filter=True)
    captions = _segments_to_captions(segments)
    if captions:
        return captions
    segments, _ = model.transcribe(str(audio_path), vad_filter=False)
    return _segments_to_captions(segments)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run faster-whisper on a remote audio file"
    )
    parser.add_argument("audio_path")
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="base")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    parser.add_argument("--compute-type", default="auto", choices=COMPUTE_TYPES)
    args = parser.parse_args(argv)
    audio_path = Path(args.audio_path)
    if not audio_path.exists():
        print(f"Error: audio file not found: {audio_path}", file=sys.stderr)
        return 1
    try:
        device, compute_type = resolve_execution(args.device, args.compute_type)
        captions = transcribe_audio(
            audio_path, model_name=args.model, device=device, compute_type=compute_type
        )
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(captions, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
