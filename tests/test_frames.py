from __future__ import annotations

import json
from pathlib import Path

import pytest

from video_buddy.cli import main
from video_buddy.frames.capture import (
    format_timestamp_human,
    parse_timestamp_ms,
    select_frames,
)
from video_buddy.frames.ocr import apply_ocr_to_metadata


def test_parse_and_format_timestamp() -> None:
    assert parse_timestamp_ms(Path("frame_00001234.jpg")) == 1234
    assert format_timestamp_human(1234) == "0:01"


def test_select_frames_returns_chronological_subset(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    frames = []
    for ts in (1000, 2000, 3000):
        path = tmp_path / f"frame_{ts:08d}.jpg"
        path.write_bytes(b"jpg")
        frames.append(path)

    scores = {
        frames[0].name: {
            "edge_density": 5.0,
            "face_area_ratio": 0.0,
            "brightness": 120.0,
            "hash": "0" * 16,
            "should_ocr": True,
            "should_include": True,
        },
        frames[1].name: {
            "edge_density": 4.0,
            "face_area_ratio": 0.0,
            "brightness": 120.0,
            "hash": "f" * 16,
            "should_ocr": True,
            "should_include": True,
        },
        frames[2].name: {
            "edge_density": 1.0,
            "face_area_ratio": 0.0,
            "brightness": 120.0,
            "hash": "a" * 16,
            "should_ocr": False,
            "should_include": False,
        },
    }

    monkeypatch.setattr(
        "video_buddy.frames.capture.score_frame", lambda path: scores[path.name]
    )
    monkeypatch.setattr(
        "video_buddy.frames.capture.hash_distance", lambda left, right: 99
    )

    selected = select_frames(frames, video_id="abc123def45", max_frames=2)

    assert [frame["timestamp_ms"] for frame in selected] == [1000, 2000]
    assert all(frame["video_id"] == "abc123def45" for frame in selected)


def test_apply_ocr_to_metadata_off_leaves_frames_untouched() -> None:
    metadata = {
        "frames": [
            {"filename": "frame_00001000.jpg", "should_ocr": True},
        ]
    }

    updated = apply_ocr_to_metadata(Path("."), metadata, ocr_mode="off")

    assert updated["frames"][0] == {
        "filename": "frame_00001000.jpg",
        "should_ocr": True,
    }


def test_apply_ocr_to_metadata_auto_prefers_tesseract_when_easyocr_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata = {
        "frames": [
            {"filename": "frame_00001000.jpg", "should_ocr": True},
        ]
    }
    monkeypatch.setattr("video_buddy.frames.ocr.easyocr_available", lambda: False)
    monkeypatch.setattr(
        "video_buddy.frames.ocr.tesseract_available",
        lambda tesseract_cmd=None: True,
    )
    monkeypatch.setattr(
        "video_buddy.frames.ocr.run_tesseract",
        lambda media_dir, frames, tesseract_cmd=None: {
            "frame_00001000.jpg": {"text": "hello", "confidence": 0.8}
        },
    )

    updated = apply_ocr_to_metadata(tmp_path, metadata, ocr_mode="auto")

    assert updated["frames"][0]["ocr_text"] == "hello"
    assert updated["frames"][0]["ocr_engine"] == "tesseract"


def test_frames_command_writes_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace = tmp_path / "workspace"
    intermediate = workspace / "intermediates"
    intermediate.mkdir(parents=True)
    (intermediate / "video_abc123def45.json").write_text(
        json.dumps({"video_id": "abc123def45", "cookies_from_browser": ""}),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "video_buddy.cli.capture_video_frames",
        lambda video_id,
        media_dir,
        max_frames,
        cookies_from_browser=None,
        ffmpeg_bin=None,
        scene_detection_max_duration_s=600: {
            "video_id": video_id,
            "total_extracted": 2,
            "total_selected": 1,
            "frames": [
                {
                    "video_id": video_id,
                    "filename": "frame_00001000.jpg",
                    "timestamp_ms": 1000,
                    "timestamp_human": "0:01",
                    "edge_density": 1.0,
                    "face_area_ratio": 0.0,
                    "brightness": 120.0,
                    "hash": "abc",
                    "should_ocr": True,
                    "should_include": True,
                }
            ],
        },
    )
    monkeypatch.setattr(
        "video_buddy.cli.apply_ocr_to_metadata",
        lambda media_dir,
        metadata,
        ocr_mode,
        engine=None,
        model_dir=None,
        tesseract_cmd=None: metadata,
    )

    exit_code = main(
        ["frames", "abc123def45", "--workspace", str(workspace), "--ocr", "off"]
    )

    assert exit_code == 0
    assert (intermediate / "frames_abc123def45" / "frames_meta.json").is_file()
