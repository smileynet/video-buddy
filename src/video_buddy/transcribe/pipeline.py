from __future__ import annotations

import json
from pathlib import Path
import tempfile
from typing import Any

from ..fetch.yt_dlp_opts import apply_youtube_auth


def detect_device() -> str:
    try:
        import ctranslate2

        if ctranslate2.get_supported_compute_types("cuda"):
            return "cuda"
    except Exception:
        pass
    return "cpu"


def default_model_name(device: str) -> str:
    return "large-v3-turbo" if device == "cuda" else "base"


def default_compute_type(device: str) -> str:
    return "float16" if device == "cuda" else "int8"


def download_audio(
    url: str, output_dir: Path, cookies_from_browser: str | None = None
) -> Path:
    import yt_dlp

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "outtmpl": str(output_dir / "audio.%(ext)s"),
    }
    apply_youtube_auth(ydl_opts, cookies_from_browser)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
        return Path(info["requested_downloads"][0]["filepath"])
    except Exception as error:
        raise RuntimeError(f"Failed to download audio: {error}") from error


def load_model(
    model_name: str,
    device: str,
    compute_type: str,
    *,
    model_cache: Path | None = None,
):
    from faster_whisper import WhisperModel

    model_ref: str | Path = model_name
    if model_cache is not None:
        cached_path = model_cache / "whisper" / model_name
        if cached_path.exists():
            model_ref = cached_path

    return WhisperModel(str(model_ref), device=device, compute_type=compute_type)


def transcribe_audio(audio_path: Path, model: Any) -> list[dict]:
    segments, _ = model.transcribe(str(audio_path), vad_filter=True)
    captions = _segments_to_captions(segments)
    if captions:
        return captions
    segments, _ = model.transcribe(str(audio_path), vad_filter=False)
    return _segments_to_captions(segments)


def transcribe_video_json(
    video_json_path: Path,
    *,
    model_name: str | None = None,
    device: str = "auto",
    compute_type: str = "auto",
    model_cache: Path | None = None,
) -> list[dict]:
    payload = json.loads(video_json_path.read_text(encoding="utf-8"))
    if payload.get("has_captions") and payload.get("captions"):
        return _normalize_captions(payload["captions"])

    url = _video_url_from_payload(payload)
    resolved_device = detect_device() if device == "auto" else device
    resolved_compute_type = (
        default_compute_type(resolved_device)
        if compute_type == "auto"
        else compute_type
    )
    resolved_model = model_name or default_model_name(resolved_device)
    model = load_model(
        resolved_model,
        resolved_device,
        resolved_compute_type,
        model_cache=model_cache,
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        audio_path = download_audio(
            url,
            Path(tmp_dir),
            cookies_from_browser=payload.get("cookies_from_browser") or None,
        )
        return transcribe_audio(audio_path, model)


def _video_url_from_payload(payload: dict[str, Any]) -> str:
    video_id = str(payload.get("video_id") or "").strip()
    if not video_id:
        raise RuntimeError("video_json is missing video_id")
    return f"https://www.youtube.com/watch?v={video_id}"


def _segments_to_captions(segments: Any) -> list[dict]:
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


def _normalize_captions(raw_captions: object) -> list[dict]:
    if not isinstance(raw_captions, list):
        raise RuntimeError("Transcription output must be a JSON list")

    normalized = []
    for segment in raw_captions:
        if not isinstance(segment, dict):
            raise RuntimeError("Transcription segment must be a JSON object")
        text = str(segment.get("text", "")).strip()
        if not text:
            continue
        normalized.append(
            {
                "start": float(segment.get("start", 0.0)),
                "duration": round(float(segment.get("duration", 0.0)), 3),
                "text": text,
            }
        )
    return normalized


def read_transcript(path: Path) -> list[dict]:
    """Read transcript JSON, handling both v1 (list) and v2 (dict with segments)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("segments", [])
    raise RuntimeError(f"Unexpected transcript format in {path}")


def transcribe_video_json_whisperx(
    video_json_path: Path,
    *,
    model_name: str | None = None,
    device: str = "auto",
    compute_type: str = "auto",
    model_cache: Path | None = None,
) -> dict:
    """Transcribe with WhisperX, returning v2 schema with word-level timestamps."""
    payload = json.loads(video_json_path.read_text(encoding="utf-8"))
    if payload.get("has_captions") and payload.get("captions"):
        segments = _normalize_captions(payload["captions"])
        return {
            "schema_version": "2.0",
            "metadata": {"engine": "captions", "model": None},
            "segments": segments,
        }

    import gc
    import warnings

    try:
        import whisperx
    except ImportError:
        warnings.warn(
            "whisperx not installed, falling back to faster-whisper",
            stacklevel=2,
        )
        return {
            "schema_version": "2.0",
            "metadata": {"engine": "faster-whisper", "model": None},
            "segments": transcribe_video_json(
                video_json_path,
                model_name=model_name,
                device=device,
                compute_type=compute_type,
                model_cache=model_cache,
            ),
        }

    url = _video_url_from_payload(payload)
    resolved_device = detect_device() if device == "auto" else device
    resolved_compute_type = (
        default_compute_type(resolved_device)
        if compute_type == "auto"
        else compute_type
    )
    resolved_model = model_name or default_model_name(resolved_device)
    batch_size = 16 if resolved_device == "cuda" else 4

    with tempfile.TemporaryDirectory() as tmp_dir:
        audio_path = download_audio(
            url,
            Path(tmp_dir),
            cookies_from_browser=payload.get("cookies_from_browser") or None,
        )

        # Step 1: Transcribe
        model = whisperx.load_model(
            resolved_model,
            resolved_device,
            compute_type=resolved_compute_type,
        )
        audio = whisperx.load_audio(str(audio_path))
        result = model.transcribe(audio, batch_size=batch_size)
        del model
        gc.collect()
        _clear_cuda_cache()

        # Step 2: Align (word-level timestamps)
        language = result.get("language", "en")
        model_a, metadata = whisperx.load_align_model(
            language_code=language, device=resolved_device
        )
        result = whisperx.align(
            result["segments"],
            model_a,
            metadata,
            audio,
            resolved_device,
            return_char_alignments=False,
        )
        del model_a
        gc.collect()
        _clear_cuda_cache()

    return _whisperx_result_to_v2(result, resolved_model)


def _clear_cuda_cache() -> None:
    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except ImportError:
        pass


def _whisperx_result_to_v2(result: dict, model_name: str) -> dict:
    """Convert WhisperX result dict to our v2 transcript schema."""
    segments = []
    for seg in result.get("segments", []):
        start = float(seg.get("start", 0.0))
        end = float(seg.get("end", start))
        text = str(seg.get("text", "")).strip()
        if not text:
            continue

        words = []
        for w in seg.get("words", []):
            word_start = w.get("start")
            word_end = w.get("end")
            if word_start is None or word_end is None:
                continue
            words.append(
                {
                    "start": float(word_start),
                    "end": float(word_end),
                    "text": str(w.get("word", "")).strip(),
                }
            )

        segments.append(
            {
                "start": start,
                "duration": round(end - start, 3),
                "text": text,
                "words": words,
            }
        )

    return {
        "schema_version": "2.0",
        "metadata": {"engine": "whisperx", "model": model_name},
        "segments": segments,
    }
