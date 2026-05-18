from __future__ import annotations

from pathlib import Path

from video_buddy.models import (
    inspect_cache,
    install_selectors,
    parse_selector_args,
    remove_selectors,
    whisper_gpu_available,
)


def test_parse_selector_args_splits_commas() -> None:
    assert parse_selector_args(["recommended-cpu,easyocr-en", "base"]) == [
        "recommended-cpu",
        "easyocr-en",
        "base",
    ]


def test_install_selectors_expands_default_cpu_bundle(
    tmp_path: Path, monkeypatch
) -> None:
    installed: list[tuple[str, Path]] = []

    monkeypatch.setattr(
        "video_buddy.models._download_whisper_model",
        lambda model, path: installed.append((model, path)),
    )
    monkeypatch.setattr(
        "video_buddy.models._prefetch_easyocr_english",
        lambda path: (_ for _ in ()).throw(
            AssertionError("unexpected easyocr install")
        ),
    )

    report = install_selectors(None, model_cache=tmp_path, gpu_path=False)

    assert report.whisper_models == ("base", "small")
    assert report.easyocr_en is False
    assert installed == [
        ("base", tmp_path / "whisper" / "base"),
        ("small", tmp_path / "whisper" / "small"),
    ]


def test_install_selectors_default_gpu_bundle_includes_easyocr(
    tmp_path: Path, monkeypatch
) -> None:
    installed: list[tuple[str, Path]] = []
    easyocr_dirs: list[Path] = []

    monkeypatch.setattr(
        "video_buddy.models._download_whisper_model",
        lambda model, path: installed.append((model, path)),
    )
    monkeypatch.setattr(
        "video_buddy.models._prefetch_easyocr_english",
        lambda path: easyocr_dirs.append(path),
    )

    report = install_selectors(None, model_cache=tmp_path, gpu_path=True)

    assert report.whisper_models == ("base", "small", "large-v3-turbo")
    assert report.easyocr_en is True
    assert easyocr_dirs == [tmp_path / "easyocr"]


def test_install_selectors_tracks_easyocr_and_tesseract(
    tmp_path: Path, monkeypatch
) -> None:
    installed_easyocr: list[Path] = []

    monkeypatch.setattr("video_buddy.models._download_whisper_model", lambda *_: None)
    monkeypatch.setattr(
        "video_buddy.models._prefetch_easyocr_english",
        lambda path: installed_easyocr.append(path),
    )

    report = install_selectors(
        ["easyocr-en", "cpu-only"],
        model_cache=tmp_path,
        gpu_path=False,
    )

    assert report.whisper_models == ("base", "small")
    assert report.easyocr_en is True
    assert report.tesseract_required is True
    assert installed_easyocr == [tmp_path / "easyocr"]


def test_remove_selectors_deletes_cached_paths(tmp_path: Path) -> None:
    (tmp_path / "whisper" / "base").mkdir(parents=True)
    (tmp_path / "easyocr").mkdir(parents=True)

    report = remove_selectors(
        ["base", "easyocr-en"], model_cache=tmp_path, gpu_path=False
    )

    assert report.whisper_models == ("base",)
    assert report.easyocr_en is True
    assert not (tmp_path / "whisper" / "base").exists()
    assert not (tmp_path / "easyocr").exists()


def test_inspect_cache_reports_present_entries(tmp_path: Path) -> None:
    (tmp_path / "whisper" / "small").mkdir(parents=True)
    (tmp_path / "whisper" / "base").mkdir(parents=True)
    (tmp_path / "easyocr" / "marker").mkdir(parents=True)

    report = inspect_cache(tmp_path)

    assert report.whisper_models == ("base", "small")
    assert report.easyocr_en_cached is True


def test_whisper_gpu_available_without_torch(monkeypatch) -> None:
    monkeypatch.setattr(
        "video_buddy.models.importlib.util.find_spec", lambda name: None
    )
    assert whisper_gpu_available() is False
