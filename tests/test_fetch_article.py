from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from video_buddy.fetch.article import (
    detect_doi,
    detect_source_type,
    fetch_article,
    source_id_from_doi,
    source_id_from_path,
    source_id_from_url,
)


def test_detect_doi_strips_trailing_punctuation() -> None:
    assert (
        detect_doi("https://doi.org/10.1145/3582437.3587212).")
        == "10.1145/3582437.3587212"
    )


def test_source_id_helpers_are_stable(tmp_path: Path) -> None:
    path = tmp_path / "paper.pdf"
    path.write_bytes(b"pdf")

    assert (
        source_id_from_doi("10.1145/3582437.3587212") == "doi-10.1145-3582437.3587212"
    )
    assert source_id_from_path(path).startswith("file-")
    assert source_id_from_url("https://example.com/article").startswith("web-")


def test_detect_source_type_prefers_paper_for_doi_and_pdf(tmp_path: Path) -> None:
    pdf = tmp_path / "paper.pdf"

    assert detect_source_type("https://example.com", None, "10.1000/test") == "paper"
    assert detect_source_type(None, pdf, None) == "paper"
    assert (
        detect_source_type("https://example.com/file.pdf?download=1", None, None)
        == "paper"
    )
    assert detect_source_type("https://example.com/article", None, None) == "article"


@patch("video_buddy.fetch.article.extract_web")
def test_fetch_article_for_web_fills_missing_metadata(mock_extract_web: Mock) -> None:
    mock_extract_web.return_value = {
        "content": "hello world",
        "word_count": 2,
        "title": "Article title",
        "authors": ["Author One"],
        "description": "Summary",
        "published": "2026-05-17",
    }

    result = fetch_article(url="https://example.com/article")

    assert result["source_type"] == "article"
    assert result["title"] == "Article title"
    assert result["authors"] == ["Author One"]
    assert result["source_id"].startswith("web-")


@patch("video_buddy.fetch.article.fetch_semantic_scholar")
@patch("video_buddy.fetch.article.extract_pdf")
def test_fetch_article_for_local_pdf_uses_semantic_scholar_metadata(
    mock_extract_pdf: Mock,
    mock_fetch_s2: Mock,
    tmp_path: Path,
) -> None:
    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"pdf")
    mock_fetch_s2.return_value = {
        "title": "Paper Title",
        "authors": [{"name": "Ada"}, {"name": "Grace"}],
        "abstract": "Abstract text",
        "venue": "Conf",
        "publicationDate": "2026-05-17",
    }
    mock_extract_pdf.return_value = {"content": "paper body", "word_count": 2}

    result = fetch_article(path=pdf, doi="10.1000/test")

    assert result["source_type"] == "paper"
    assert result["title"] == "Paper Title"
    assert result["authors"] == ["Ada", "Grace"]
    assert result["content"] == "paper body"
    assert result["source_id"] == "doi-10.1000-test"


@patch("video_buddy.fetch.article.extract_pdf")
@patch("video_buddy.fetch.article.requests.get")
def test_fetch_article_downloads_remote_pdf(
    mock_get: Mock,
    mock_extract_pdf: Mock,
) -> None:
    mock_get.return_value = Mock(content=b"pdf", raise_for_status=Mock())
    mock_extract_pdf.return_value = {"content": "paper body", "word_count": 2}

    result = fetch_article(url="https://example.com/paper.pdf")

    assert result["source_type"] == "paper"
    assert result["content"] == "paper body"


def test_fetch_article_requires_url_or_path() -> None:
    with pytest.raises(ValueError, match="Either url or path is required"):
        fetch_article()
