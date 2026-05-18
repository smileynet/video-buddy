from __future__ import annotations

import json
from pathlib import Path

import pytest

from video_buddy.cli import main


def test_init_creates_workspace_layout(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    target = tmp_path / "research"

    exit_code = main(["init", str(target), "--no-models"])

    assert exit_code == 0
    assert target.is_dir()
    assert (target / "intermediates").is_dir()
    assert (target / "intermediates" / "agent-prompts").is_dir()
    assert (target / "notes").is_dir()
    assert (target / "notes" / "media").is_dir()
    assert (target / "notes" / "concepts").is_dir()
    assert (target / "notes" / "digests").is_dir()
    assert (target / ".video-buddy.toml").is_file()
    assert (target / ".gitignore").is_file()
    assert capsys.readouterr().out.strip() == str(target.resolve())


def test_init_refuses_non_empty_directory_without_force(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    target = tmp_path / "research"
    target.mkdir()
    (target / "existing.txt").write_text("keep", encoding="utf-8")

    exit_code = main(["init", str(target), "--no-models"])

    assert exit_code == 1
    assert "Refusing to initialize non-empty directory" in capsys.readouterr().err


def test_init_allows_non_empty_directory_with_force(tmp_path: Path) -> None:
    target = tmp_path / "research"
    target.mkdir()
    (target / "existing.txt").write_text("keep", encoding="utf-8")

    exit_code = main(["init", str(target), "--force", "--no-models"])

    assert exit_code == 0
    assert (target / "existing.txt").read_text(encoding="utf-8") == "keep"


def test_init_accepts_workspace_flag(tmp_path: Path) -> None:
    target = tmp_path / "workspace-flag"

    exit_code = main(["init", "--workspace", str(target), "--no-models"])

    assert exit_code == 0
    assert (target / ".video-buddy.toml").is_file()


def test_init_rejects_conflicting_workspace_inputs(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main(
        [
            "init",
            str(tmp_path / "one"),
            "--workspace",
            str(tmp_path / "two"),
            "--no-models",
        ]
    )

    assert exit_code == 1
    assert "Pass either init <dir> or --workspace <dir>" in capsys.readouterr().err


def test_init_no_models_skips_model_install(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "skip-models"

    def _fail(*args: object, **kwargs: object) -> None:
        raise AssertionError("install_selectors should not be called")

    monkeypatch.setattr("video_buddy.cli.install_selectors", _fail)

    exit_code = main(["init", str(target), "--no-models"])

    assert exit_code == 0


def test_fetch_writes_video_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace = tmp_path / "fetch-workspace"
    payload = {
        "video_id": "dQw4w9WgXcQ",
        "title": "Test Video",
        "channel": "Test Channel",
        "has_captions": False,
        "captions": [],
        "source_repos": [],
        "fetched_at": "2026-05-17T00:00:00+00:00",
    }

    monkeypatch.setattr(
        "video_buddy.cli.fetch_video",
        lambda url, cookies_from_browser=None: payload,
    )

    exit_code = main(
        [
            "fetch",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "--workspace",
            str(workspace),
        ]
    )

    assert exit_code == 0
    assert (workspace / "intermediates" / "video_dQw4w9WgXcQ.json").is_file()


def test_fetch_writes_article_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace = tmp_path / "fetch-article-workspace"
    payload = {
        "source_id": "web-abc123def456",
        "source_type": "article",
        "url": "https://example.com/article",
        "content": "body",
        "word_count": 1,
        "fetched_at": "2026-05-17T00:00:00+00:00",
    }

    monkeypatch.setattr("video_buddy.cli.fetch_article", lambda url: payload)

    exit_code = main(
        [
            "fetch",
            "https://example.com/article",
            "--workspace",
            str(workspace),
        ]
    )

    assert exit_code == 0
    assert (workspace / "intermediates" / "article_web-abc123def456.json").is_file()


def test_fetch_json_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    workspace = tmp_path / "fetch-json-workspace"
    payload = {
        "video_id": "dQw4w9WgXcQ",
        "title": "Test Video",
        "channel": "Test Channel",
        "has_captions": False,
        "captions": [],
        "source_repos": [],
        "fetched_at": "2026-05-17T00:00:00+00:00",
    }
    monkeypatch.setattr(
        "video_buddy.cli.fetch_video", lambda url, cookies_from_browser=None: payload
    )

    exit_code = main(
        [
            "--json",
            "fetch",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "--workspace",
            str(workspace),
        ]
    )

    result = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert result["verb"] == "fetch"
    assert result["schema_version"] == "1.0"


def test_render_uses_template_from_config(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / ".video-buddy.toml").write_text(
        '[notes]\ntemplate = "obsidian"\n', encoding="utf-8"
    )
    intermediate = workspace / "intermediates"
    intermediate.mkdir()
    (intermediate / "video_abc123def45.json").write_text(
        json.dumps(
            {
                "video_id": "abc123def45",
                "title": "Test Video",
                "description": "desc",
                "channel": "Chan",
                "captions": [],
            }
        ),
        encoding="utf-8",
    )

    exit_code = main(["render", "abc123def45", "--workspace", str(workspace)])

    assert exit_code == 0
    text = (intermediate / "note_abc123def45.md").read_text(encoding="utf-8")
    assert "Obsidian wiki-link bullet list" in text
