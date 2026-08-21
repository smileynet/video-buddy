"""Tests for WhisperX integration."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from video_buddy.transcribe.pipeline import (
    read_transcript,
    _whisperx_result_to_v2,
    transcribe_video_json_whisperx,
)


class TestReadTranscript:
    """Tests for the v1/v2 compatibility shim."""

    def test_reads_v1_flat_list(self, tmp_path: Path) -> None:
        v1_data = [
            {"start": 0.0, "duration": 3.5, "text": "Hello world"},
            {"start": 3.5, "duration": 2.0, "text": "Second segment"},
        ]
        path = tmp_path / "transcript.json"
        path.write_text(json.dumps(v1_data))

        result = read_transcript(path)
        assert result == v1_data

    def test_reads_v2_dict_with_segments(self, tmp_path: Path) -> None:
        v2_data = {
            "schema_version": "2.0",
            "metadata": {"engine": "whisperx", "model": "large-v3-turbo"},
            "segments": [
                {"start": 0.0, "duration": 3.5, "text": "Hello world", "words": []},
                {"start": 3.5, "duration": 2.0, "text": "Second segment", "words": []},
            ],
        }
        path = tmp_path / "transcript.json"
        path.write_text(json.dumps(v2_data))

        result = read_transcript(path)
        assert len(result) == 2
        assert result[0]["text"] == "Hello world"
        assert result[1]["start"] == 3.5

    def test_v2_without_segments_key_returns_empty(self, tmp_path: Path) -> None:
        v2_data = {"schema_version": "2.0", "metadata": {}}
        path = tmp_path / "transcript.json"
        path.write_text(json.dumps(v2_data))

        result = read_transcript(path)
        assert result == []

    def test_raises_on_unexpected_format(self, tmp_path: Path) -> None:
        path = tmp_path / "transcript.json"
        path.write_text('"just a string"')

        with pytest.raises(RuntimeError, match="Unexpected transcript format"):
            read_transcript(path)


class TestWhisperxResultToV2:
    """Tests for WhisperX output conversion."""

    def test_converts_segments_with_words(self) -> None:
        whisperx_result = {
            "segments": [
                {
                    "start": 0.5,
                    "end": 3.8,
                    "text": "Hello and welcome",
                    "words": [
                        {"word": "Hello", "start": 0.5, "end": 0.9},
                        {"word": "and", "start": 1.0, "end": 1.2},
                        {"word": "welcome", "start": 1.3, "end": 1.8},
                    ],
                }
            ]
        }

        result = _whisperx_result_to_v2(whisperx_result, "large-v3-turbo")

        assert result["schema_version"] == "2.0"
        assert result["metadata"]["engine"] == "whisperx"
        assert result["metadata"]["model"] == "large-v3-turbo"
        assert len(result["segments"]) == 1

        seg = result["segments"][0]
        assert seg["start"] == 0.5
        assert seg["duration"] == 3.3
        assert seg["text"] == "Hello and welcome"
        assert len(seg["words"]) == 3
        assert seg["words"][0] == {"start": 0.5, "end": 0.9, "text": "Hello"}

    def test_skips_empty_text_segments(self) -> None:
        whisperx_result = {
            "segments": [
                {"start": 0.0, "end": 1.0, "text": "  ", "words": []},
                {"start": 1.0, "end": 2.0, "text": "Real content", "words": []},
            ]
        }

        result = _whisperx_result_to_v2(whisperx_result, "base")
        assert len(result["segments"]) == 1
        assert result["segments"][0]["text"] == "Real content"

    def test_skips_words_without_timestamps(self) -> None:
        whisperx_result = {
            "segments": [
                {
                    "start": 0.0,
                    "end": 2.0,
                    "text": "Hello world",
                    "words": [
                        {"word": "Hello", "start": 0.0, "end": 0.5},
                        {"word": "world", "start": None, "end": None},
                    ],
                }
            ]
        }

        result = _whisperx_result_to_v2(whisperx_result, "base")
        assert len(result["segments"][0]["words"]) == 1

    def test_handles_empty_segments(self) -> None:
        result = _whisperx_result_to_v2({"segments": []}, "base")
        assert result["segments"] == []


class TestTranscribeVideoJsonWhisperx:
    """Tests for the WhisperX adapter function."""

    def test_uses_captions_when_available(self, tmp_path: Path) -> None:
        video_json = tmp_path / "video.json"
        video_json.write_text(
            json.dumps(
                {
                    "video_id": "test123",
                    "has_captions": True,
                    "captions": [
                        {"start": 0.0, "duration": 2.0, "text": "Caption text"}
                    ],
                }
            )
        )

        result = transcribe_video_json_whisperx(video_json)

        assert result["schema_version"] == "2.0"
        assert result["metadata"]["engine"] == "captions"
        assert len(result["segments"]) == 1
        assert result["segments"][0]["text"] == "Caption text"

    def test_falls_back_when_whisperx_not_installed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        video_json = tmp_path / "video.json"
        video_json.write_text(
            json.dumps(
                {
                    "video_id": "test456",
                    "has_captions": False,
                    "captions": [],
                }
            )
        )

        # Mock the import to raise ImportError
        import builtins

        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "whisperx":
                raise ImportError("No module named 'whisperx'")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)

        # Mock transcribe_video_json to avoid needing real whisper
        mock_captions = [{"start": 0.0, "duration": 1.0, "text": "Fallback"}]
        monkeypatch.setattr(
            "video_buddy.transcribe.pipeline.transcribe_video_json",
            lambda *a, **kw: mock_captions,
        )

        import warnings

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = transcribe_video_json_whisperx(video_json)

        assert result["schema_version"] == "2.0"
        assert result["metadata"]["engine"] == "faster-whisper"
        assert result["segments"] == mock_captions
        assert any("falling back" in str(warning.message) for warning in w)


class TestConfigEngine:
    """Test that engine field is properly parsed from config."""

    def test_default_engine_is_faster_whisper(self) -> None:
        from video_buddy.config import WhisperConfig

        config = WhisperConfig()
        assert config.engine == "faster-whisper"

    def test_engine_field_accepted_in_config(self) -> None:
        from video_buddy.config import WhisperConfig

        config = WhisperConfig(engine="whisperx")
        assert config.engine == "whisperx"
