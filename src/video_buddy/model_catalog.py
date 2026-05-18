from __future__ import annotations

from dataclasses import dataclass

DEFAULT_CPU_BUNDLE = "recommended-cpu"
DEFAULT_GPU_BUNDLE = "recommended-gpu"

RAW_MODELS = frozenset(
    {
        "base",
        "small",
        "medium",
        "large-v3",
        "large-v3-turbo",
        "distil-large-v3",
    }
)

BUNDLES: dict[str, tuple[str, ...]] = {
    "recommended-cpu": ("base", "small"),
    "recommended-gpu": ("base", "small", "large-v3-turbo"),
    "whisper-core": ("base", "small"),
    "whisper-all": ("base", "small", "large-v3-turbo"),
    "easyocr-en": (),
    "cpu-only": ("base", "small"),
}


@dataclass(frozen=True, slots=True)
class ModelSelection:
    whisper_models: tuple[str, ...]
    needs_easyocr_en: bool = False
    needs_tesseract: bool = False


def default_bundle(*, gpu_path_available: bool) -> str:
    return DEFAULT_GPU_BUNDLE if gpu_path_available else DEFAULT_CPU_BUNDLE


def resolve_model_selection(
    selectors: list[str] | tuple[str, ...] | None,
    *,
    gpu_path_available: bool,
) -> ModelSelection:
    ordered = selectors or [default_bundle(gpu_path_available=gpu_path_available)]
    models: list[str] = []
    needs_easyocr_en = False
    needs_tesseract = False

    for selector in ordered:
        token = selector.strip()
        if not token:
            continue
        if token == "easyocr-en":
            needs_easyocr_en = True
            continue
        if token == "cpu-only":
            needs_tesseract = True
            _extend_unique(models, BUNDLES[token])
            continue
        bundle = BUNDLES.get(token)
        if bundle is not None:
            _extend_unique(models, bundle)
            continue
        if token in RAW_MODELS:
            _extend_unique(models, (token,))
            continue
        raise ValueError(f"Unknown model selector: {token}")

    return ModelSelection(
        whisper_models=tuple(models),
        needs_easyocr_en=needs_easyocr_en,
        needs_tesseract=needs_tesseract,
    )


def _extend_unique(target: list[str], additions: tuple[str, ...]) -> None:
    seen = set(target)
    for item in additions:
        if item in seen:
            continue
        target.append(item)
        seen.add(item)
