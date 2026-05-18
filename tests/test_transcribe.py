from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from video_buddy.cli import main
from video_buddy.transcribe.pipeline import (
    default_compute_type,
    default_model_name,
    download_audio,
    transcribe_audio,
    transcribe_video_json,
)


def test_default_compute_type() -> None:
    assert default_compute_type("cpu") == "int8"
    assert default_compute_type("cuda") == "float16"


def test_default_model_name_cpu() -> None:
    assert default_model_name("cpu") == "base"


def test_default_model_name_gpu() -> None:
    assert default_model_name("cuda") == "large-v3-turbo"


@patch("video_buddy.transcribe.pipeline.apply_youtube_auth")
def test_download_audio_returns_downloaded_path(
    mock_apply_auth: Mock,
    tmp_path: Path,
) -> None:
    mock_ydl = MagicMock()
    mock_ydl.__enter__.return_value.extract_info.return_value = {
        "requested_downloads": [{"filepath": str(tmp_path / "audio.webm")}]
    }

    with patch.dict(
        "sys.modules",
        {"yt_dlp": Mock(YoutubeDL=Mock(return_value=mock_ydl))},
    ):
        path = download_audio("https://youtube.com/watch?v=dQw4w9WgXcQ", tmp_path)

    assert path == tmp_path / "audio.webm"
    mock_apply_auth.assert_called_once()


def test_transcribe_audio_retries_without_vad() -> None:
    empty_segment = Mock(text="   ", start=0.0, end=1.0)
    real_segment = Mock(text=" hello ", start=1.0, end=3.0)
    model = Mock()
    model.transcribe.side_effect = [([empty_segment], None), ([real_segment], None)]

    captions = transcribe_audio(Path("audio.mp3"), model)

    assert captions == [{"start": 1.0, "duration": 2.0, "text": "hello"}]
    assert model.transcribe.call_args_list[1].kwargs["vad_filter"] is False


@patch("video_buddy.transcribe.pipeline.load_model")
@patch("video_buddy.transcribe.pipeline.download_audio")
@patch("video_buddy.transcribe.pipeline.transcribe_audio")
@patch("video_buddy.transcribe.pipeline.detect_device", return_value="cpu")
def test_transcribe_video_json_downloads_when_captions_missing(
    mock_detect: Mock,
    mock_transcribe_audio: Mock,
    mock_download_audio: Mock,
    mock_load_model: Mock,
    tmp_path: Path,
) -> None:
    video_json = tmp_path / "video_abc123def45.json"
    video_json.write_text(
        json.dumps({"video_id": "abc123def45", "has_captions": False, "captions": []}),
        encoding="utf-8",
    )
    mock_download_audio.return_value = tmp_path / "audio.webm"
    mock_load_model.return_value = object()
    mock_transcribe_audio.return_value = [{"start": 0.0, "duration": 1.0, "text": "hi"}]
    model_cache = tmp_path / "cache"

    captions = transcribe_video_json(video_json, model_cache=model_cache)

    assert captions == [{"start": 0.0, "duration": 1.0, "text": "hi"}]
    mock_load_model.assert_called_once_with(
        "base",
        "cpu",
        "int8",
        model_cache=model_cache,
    )
    mock_download_audio.assert_called_once()
    mock_detect.assert_called_once()


def test_transcribe_video_json_reuses_existing_captions(tmp_path: Path) -> None:
    video_json = tmp_path / "video_abc123def45.json"
    video_json.write_text(
        json.dumps(
            {
                "video_id": "abc123def45",
                "has_captions": True,
                "captions": [{"start": 1, "duration": 2, "text": " hello "}],
            }
        ),
        encoding="utf-8",
    )

    captions = transcribe_video_json(video_json)

    assert captions == [{"start": 1.0, "duration": 2.0, "text": "hello"}]


def test_transcribe_command_writes_transcript_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace = tmp_path / "workspace"
    intermediate = workspace / "intermediates"
    intermediate.mkdir(parents=True)
    (intermediate / "video_abc123def45.json").write_text(
        json.dumps({"video_id": "abc123def45", "has_captions": False, "captions": []}),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "video_buddy.cli.transcribe_video_json",
        lambda path,
        model_name=None,
        device="auto",
        compute_type="auto",
        model_cache=None: [{"start": 0.0, "duration": 1.0, "text": "hi"}],
    )

    exit_code = main(["transcribe", "abc123def45", "--workspace", str(workspace)])

    assert exit_code == 0
    assert (intermediate / "transcript_abc123def45.json").is_file()
