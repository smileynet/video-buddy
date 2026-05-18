from __future__ import annotations

import importlib.util
import shutil
from dataclasses import dataclass
from pathlib import Path

from .model_catalog import default_bundle, resolve_model_selection


@dataclass(frozen=True, slots=True)
class InstallReport:
    whisper_models: tuple[str, ...]
    easyocr_en: bool
    tesseract_required: bool


@dataclass(frozen=True, slots=True)
class CacheReport:
    whisper_models: tuple[str, ...]
    easyocr_en_cached: bool


def gpu_path_available() -> bool:
    if importlib.util.find_spec("easyocr") is None:
        return False
    return whisper_gpu_available()


def whisper_gpu_available() -> bool:
    if importlib.util.find_spec("torch") is None:
        return False
    import torch

    return bool(torch.cuda.is_available())


def install_selectors(
    selectors: list[str] | tuple[str, ...] | None,
    *,
    model_cache: Path,
    gpu_path: bool | None = None,
) -> InstallReport:
    resolved_gpu_path = gpu_path if gpu_path is not None else gpu_path_available()
    selection = resolve_model_selection(
        _default_selectors(selectors, gpu_path_available=resolved_gpu_path),
        gpu_path_available=resolved_gpu_path,
    )
    whisper_root = model_cache / "whisper"
    easyocr_root = model_cache / "easyocr"
    whisper_root.mkdir(parents=True, exist_ok=True)
    model_cache.mkdir(parents=True, exist_ok=True)

    for model_name in selection.whisper_models:
        _download_whisper_model(model_name, whisper_root / model_name)

    if selection.needs_easyocr_en:
        _prefetch_easyocr_english(easyocr_root)

    return InstallReport(
        whisper_models=selection.whisper_models,
        easyocr_en=selection.needs_easyocr_en,
        tesseract_required=selection.needs_tesseract,
    )


def remove_selectors(
    selectors: list[str] | tuple[str, ...],
    *,
    model_cache: Path,
    gpu_path: bool | None = None,
) -> InstallReport:
    resolved_gpu_path = gpu_path if gpu_path is not None else gpu_path_available()
    selection = resolve_model_selection(
        selectors,
        gpu_path_available=resolved_gpu_path,
    )
    whisper_root = model_cache / "whisper"
    easyocr_root = model_cache / "easyocr"

    for model_name in selection.whisper_models:
        shutil.rmtree(whisper_root / model_name, ignore_errors=True)

    if selection.needs_easyocr_en:
        shutil.rmtree(easyocr_root, ignore_errors=True)

    return InstallReport(
        whisper_models=selection.whisper_models,
        easyocr_en=selection.needs_easyocr_en,
        tesseract_required=selection.needs_tesseract,
    )


def inspect_cache(model_cache: Path) -> CacheReport:
    whisper_root = model_cache / "whisper"
    whisper_models = (
        tuple(sorted(path.name for path in whisper_root.iterdir() if path.is_dir()))
        if whisper_root.exists()
        else ()
    )
    easyocr_root = model_cache / "easyocr"
    easyocr_en_cached = easyocr_root.exists() and any(easyocr_root.iterdir())
    return CacheReport(
        whisper_models=whisper_models,
        easyocr_en_cached=easyocr_en_cached,
    )


def parse_selector_args(values: list[str] | None) -> list[str] | None:
    if not values:
        return None
    selectors: list[str] = []
    for value in values:
        selectors.extend(token.strip() for token in value.split(",") if token.strip())
    return selectors or None


def _default_selectors(
    selectors: list[str] | tuple[str, ...] | None,
    *,
    gpu_path_available: bool,
) -> list[str] | tuple[str, ...]:
    if selectors:
        return selectors
    chosen = [default_bundle(gpu_path_available=gpu_path_available)]
    if gpu_path_available:
        chosen.append("easyocr-en")
    return chosen


def _download_whisper_model(model_name: str, output_dir: Path) -> None:
    if importlib.util.find_spec("faster_whisper") is None:
        raise SystemExit(
            "Whisper support is unavailable in this environment. Reinstall the repo dependencies and retry."
        )

    from faster_whisper.utils import download_model

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    download_model(model_name, output_dir=str(output_dir))


def _prefetch_easyocr_english(model_dir: Path) -> None:
    if importlib.util.find_spec("easyocr") is None:
        raise SystemExit(
            "EasyOCR support is unavailable. Install the gpu-ocr extra and retry."
        )

    import easyocr

    model_dir.mkdir(parents=True, exist_ok=True)
    easyocr.Reader(
        ["en"],
        gpu=gpu_path_available(),
        model_storage_directory=str(model_dir),
        download_enabled=True,
        verbose=False,
    )
