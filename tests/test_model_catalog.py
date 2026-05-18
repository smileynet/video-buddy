from __future__ import annotations

import pytest

from video_buddy.model_catalog import default_bundle, resolve_model_selection


def test_default_bundle_prefers_gpu_when_path_available() -> None:
    assert default_bundle(gpu_path_available=True) == "recommended-gpu"
    assert default_bundle(gpu_path_available=False) == "recommended-cpu"


def test_default_selection_matches_cpu_bundle() -> None:
    selection = resolve_model_selection(None, gpu_path_available=False)

    assert selection.whisper_models == ("base", "small")
    assert selection.needs_easyocr_en is False
    assert selection.needs_tesseract is False


def test_default_selection_matches_gpu_bundle() -> None:
    selection = resolve_model_selection(None, gpu_path_available=True)

    assert selection.whisper_models == ("base", "small", "large-v3-turbo")
    assert selection.needs_easyocr_en is False
    assert selection.needs_tesseract is False


def test_bundle_and_raw_model_selectors_merge_without_duplicates() -> None:
    selection = resolve_model_selection(
        ["recommended-cpu", "small", "large-v3-turbo", "easyocr-en", "cpu-only"],
        gpu_path_available=False,
    )

    assert selection.whisper_models == ("base", "small", "large-v3-turbo")
    assert selection.needs_easyocr_en is True
    assert selection.needs_tesseract is True


def test_unknown_selector_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown model selector"):
        resolve_model_selection(["nope"], gpu_path_available=False)
