from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path


def easyocr_available() -> bool:
    if importlib.util.find_spec("easyocr") is None:
        return False
    if importlib.util.find_spec("torch") is None:
        return False
    import torch

    return bool(torch.cuda.is_available())


def tesseract_available(tesseract_cmd: str | None = None) -> bool:
    if importlib.util.find_spec("pytesseract") is None:
        return False
    return _tesseract_binary(tesseract_cmd) is not None


def apply_ocr_to_metadata(
    media_dir: Path,
    metadata: dict,
    *,
    ocr_mode: str = "auto",
    engine: str | None = None,
    model_dir: Path | None = None,
    tesseract_cmd: str | None = None,
) -> dict:
    if ocr_mode == "off":
        return metadata

    eligible = [
        frame
        for frame in metadata.get("frames", [])
        if isinstance(frame, dict)
        and frame.get("should_ocr")
        and isinstance(frame.get("filename"), str)
        and frame["filename"]
    ]
    if not eligible:
        return metadata

    results: dict[str, dict]
    engine_used: str
    if engine == "tesseract":
        if not tesseract_available(tesseract_cmd):
            raise RuntimeError(
                "Tesseract OCR requested but unavailable. Install the ocr-cpu extra and the system tesseract binary."
            )
        results = run_tesseract(media_dir, eligible, tesseract_cmd=tesseract_cmd)
        engine_used = "tesseract"
    elif engine == "easyocr":
        if not easyocr_available():
            raise RuntimeError(
                "EasyOCR requested but unavailable. Install the gpu-ocr extra on a CUDA-capable machine."
            )
        results = run_easyocr(media_dir, eligible, model_dir=model_dir)
        engine_used = "easyocr"
    else:
        if easyocr_available():
            try:
                results = run_easyocr(media_dir, eligible, model_dir=model_dir)
                engine_used = "easyocr"
            except Exception:
                if not tesseract_available(tesseract_cmd):
                    raise
                results = run_tesseract(
                    media_dir, eligible, tesseract_cmd=tesseract_cmd
                )
                engine_used = "tesseract"
        elif tesseract_available(tesseract_cmd):
            results = run_tesseract(media_dir, eligible, tesseract_cmd=tesseract_cmd)
            engine_used = "tesseract"
        else:
            raise RuntimeError(
                "No OCR engine available. Install the gpu-ocr extra, install the ocr-cpu extra with the system tesseract binary, or rerun with --ocr off."
            )

    _apply_results(metadata, results, engine=engine_used)

    if (
        engine is None
        and engine_used == "easyocr"
        and tesseract_available(tesseract_cmd)
    ):
        blank = [frame for frame in eligible if not _frame_text(frame)]
        if eligible and len(blank) / len(eligible) > 0.5:
            retry_results = run_tesseract(media_dir, blank, tesseract_cmd=tesseract_cmd)
            _apply_results(metadata, retry_results, engine="tesseract-fallback")

    return metadata


def run_easyocr(
    media_dir: Path,
    frames: list[dict],
    *,
    model_dir: Path | None = None,
) -> dict[str, dict]:
    from easyocr import Reader

    reader = Reader(
        ["en"],
        gpu=True,
        model_storage_directory=str(model_dir) if model_dir is not None else None,
        download_enabled=True,
        verbose=False,
    )
    results = {}
    for frame in frames:
        frame_path = media_dir / str(frame["filename"])
        detections = reader.readtext(str(frame_path))
        valid = [item for item in detections if item[2] > 0.3]
        text = " ".join(item[1] for item in valid)
        confidence = sum(item[2] for item in valid) / len(valid) if valid else 0.0
        results[str(frame["filename"])] = {
            "text": text.strip(),
            "confidence": round(float(confidence), 3),
        }
    return results


def run_tesseract(
    media_dir: Path,
    frames: list[dict],
    *,
    tesseract_cmd: str | None = None,
) -> dict[str, dict]:
    import pytesseract
    from PIL import Image

    binary = _tesseract_binary(tesseract_cmd)
    if binary is None:
        raise RuntimeError("Tesseract binary not found on PATH")
    pytesseract.pytesseract.tesseract_cmd = binary

    results = {}
    for frame in frames:
        frame_path = media_dir / str(frame["filename"])
        with Image.open(frame_path) as image:
            text = pytesseract.image_to_string(image, lang="eng")
            data = pytesseract.image_to_data(
                image,
                lang="eng",
                output_type=pytesseract.Output.DICT,
            )
        results[str(frame["filename"])] = {
            "text": text.strip(),
            "confidence": _average_confidence(data),
        }
    return results


def _average_confidence(data: dict) -> float:
    confidences = []
    for value in data.get("conf", []):
        try:
            confidence = float(value)
        except (TypeError, ValueError):
            continue
        if confidence >= 0:
            confidences.append(confidence)
    if not confidences:
        return 0.0
    return round(sum(confidences) / len(confidences) / 100, 3)


def _apply_results(metadata: dict, results: dict[str, dict], *, engine: str) -> None:
    for frame in metadata.get("frames", []):
        if not isinstance(frame, dict):
            continue
        filename = frame.get("filename")
        if not isinstance(filename, str):
            continue
        result = results.get(filename)
        if result is None:
            continue
        frame["ocr_text"] = str(result.get("text", "")).strip()
        frame["ocr_confidence"] = round(float(result.get("confidence", 0.0)), 3)
        frame["ocr_engine"] = engine


def _frame_text(frame: dict) -> str:
    text = frame.get("ocr_text")
    return text.strip() if isinstance(text, str) else ""


def _tesseract_binary(value: str | None = None) -> str | None:
    if value:
        candidate = Path(value).expanduser()
        if candidate.exists():
            return str(candidate)
        resolved = shutil.which(value)
        if resolved is not None:
            return resolved
    binary = shutil.which("tesseract")
    if binary is not None:
        return binary
    win_default = Path("C:/Program Files/Tesseract-OCR/tesseract.exe")
    if win_default.exists():
        return str(win_default)
    return None
