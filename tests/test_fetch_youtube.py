from __future__ import annotations

from unittest.mock import MagicMock, Mock, patch

import pytest

from video_buddy.fetch.youtube import (
    extract_source_repos,
    extract_video_id,
    fetch_captions,
    fetch_metadata,
    fetch_video,
    parse_vtt,
)


class TestExtractVideoId:
    def test_standard_watch_url(self) -> None:
        assert (
            extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            == "dQw4w9WgXcQ"
        )

    def test_short_url(self) -> None:
        assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_embed_url(self) -> None:
        assert (
            extract_video_id("https://www.youtube.com/embed/dQw4w9WgXcQ")
            == "dQw4w9WgXcQ"
        )

    def test_invalid_url_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid YouTube URL"):
            extract_video_id("https://example.com/video")


class TestParseVtt:
    def test_parses_captions(self) -> None:
        vtt = """WEBVTT\n\n00:00:01.000 --> 00:00:03.500\nHello world\n\n00:00:05.000 --> 00:00:07.000\nSecond line\n"""

        captions = parse_vtt(vtt)

        assert captions == [
            {"start": 1.0, "duration": 2.5, "text": "Hello world"},
            {"start": 5.0, "duration": 2.0, "text": "Second line"},
        ]

    def test_strips_tags_and_joins_multiline(self) -> None:
        vtt = """WEBVTT\n\n00:00:01.000 --> 00:00:03.000\n<c.color>First line</c>\nSecond line\n"""

        captions = parse_vtt(vtt)

        assert captions[0]["text"] == "First line\nSecond line"


class TestFetchMetadata:
    def test_fetch_metadata_extracts_fields(self) -> None:
        mock_ydl = Mock()
        mock_ydl.extract_info.return_value = {
            "id": "dQw4w9WgXcQ",
            "title": "Test Video",
            "channel": "Test Channel",
            "channel_id": "chan123",
            "description": "desc",
            "thumbnail": "thumb.jpg",
            "duration": 42,
            "upload_date": "20260517",
            "view_count": 99,
        }
        mock_cls = MagicMock()
        mock_cls.return_value.__enter__.return_value = mock_ydl

        with patch("video_buddy.fetch.youtube.yt_dlp", Mock(YoutubeDL=mock_cls)):
            result = fetch_metadata("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

        assert result["video_id"] == "dQw4w9WgXcQ"
        assert result["channel"] == "Test Channel"
        opts = mock_cls.call_args.args[0]
        assert opts["ignore_no_formats_error"] is True


class TestFetchCaptions:
    @patch("video_buddy.fetch.youtube._captions_session.get")
    def test_prefers_manual_captions(
        self,
        mock_get: Mock,
    ) -> None:
        mock_ydl = Mock()
        mock_ydl.extract_info.return_value = {
            "subtitles": {"en": [{"ext": "vtt", "url": "https://caption/manual.vtt"}]},
            "automatic_captions": {
                "en": [{"ext": "vtt", "url": "https://caption/auto.vtt"}]
            },
        }
        mock_cls = MagicMock()
        mock_cls.return_value.__enter__.return_value = mock_ydl
        mock_get.return_value = Mock(
            text="WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nHello\n",
            raise_for_status=Mock(),
        )

        with patch("video_buddy.fetch.youtube.yt_dlp", Mock(YoutubeDL=mock_cls)):
            captions, has_captions = fetch_captions(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )

        assert has_captions is True
        assert captions[0]["text"] == "Hello"
        assert mock_get.call_args.args[0] == "https://caption/manual.vtt"

    @patch("video_buddy.fetch.youtube._captions_session.get")
    def test_returns_empty_when_no_caption_tracks(
        self,
        mock_get: Mock,
    ) -> None:
        mock_ydl = Mock()
        mock_ydl.extract_info.return_value = {"subtitles": {}, "automatic_captions": {}}
        mock_cls = MagicMock()
        mock_cls.return_value.__enter__.return_value = mock_ydl

        with patch("video_buddy.fetch.youtube.yt_dlp", Mock(YoutubeDL=mock_cls)):
            captions, has_captions = fetch_captions(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )

        assert captions == []
        assert has_captions is False
        mock_get.assert_not_called()


class TestExtractSourceRepos:
    def test_extracts_deduped_repo_roots(self) -> None:
        description = (
            "Source code: https://github.com/example/project/tree/main/src and "
            "mirror https://github.com/example/project/blob/main/app.py"
        )

        repos = extract_source_repos(description, None)

        assert repos == [
            {
                "url": "https://github.com/example/project",
                "provider": "github",
                "owner_repo": "example/project",
                "likely_code": True,
            }
        ]


class TestFetchVideo:
    @patch("video_buddy.fetch.youtube.fetch_captions")
    @patch("video_buddy.fetch.youtube.fetch_metadata")
    def test_fetch_video_combines_all_outputs(
        self,
        mock_fetch_metadata: Mock,
        mock_fetch_captions: Mock,
    ) -> None:
        mock_fetch_metadata.return_value = {
            "video_id": "dQw4w9WgXcQ",
            "title": "Test Video",
            "channel": "Test Channel",
            "channel_id": "chan123",
            "description": "Source code: https://github.com/example/project",
            "thumbnail": "thumb.jpg",
            "duration": 42,
            "upload_date": "20260517",
            "view_count": 99,
        }
        mock_fetch_captions.return_value = ([{"text": "caption text"}], True)

        result = fetch_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

        assert result["has_captions"] is True
        assert result["captions"] == [{"text": "caption text"}]
        assert result["source_repos"][0]["owner_repo"] == "example/project"
        assert result["cookies_from_browser"] == ""
        assert result["fetched_at"].endswith("+00:00")

    @patch("video_buddy.fetch.youtube.fetch_captions")
    @patch("video_buddy.fetch.youtube.fetch_metadata")
    def test_fetch_video_preserves_cookies_setting(
        self,
        mock_fetch_metadata: Mock,
        mock_fetch_captions: Mock,
    ) -> None:
        mock_fetch_metadata.return_value = {
            "video_id": "dQw4w9WgXcQ",
            "title": "Test Video",
            "channel": "Test Channel",
            "channel_id": "chan123",
            "description": "",
            "thumbnail": "thumb.jpg",
            "duration": 42,
            "upload_date": "20260517",
            "view_count": 99,
        }
        mock_fetch_captions.return_value = ([], False)

        result = fetch_video(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            cookies_from_browser="firefox",
        )

        assert result["cookies_from_browser"] == "firefox"
