from __future__ import annotations

import json
from pathlib import Path

from video_buddy.batch_digest import (
    compile_digest,
    fetch_digest_urls,
    load_urls,
    transcribe_manifest,
)
from video_buddy.workspace import Workspace


def test_load_urls_plain_and_json(tmp_path: Path) -> None:
    text_file = tmp_path / "urls.txt"
    text_file.write_text("a\na\nb\n", encoding="utf-8")
    assert load_urls(str(text_file)) == ["a", "b"]

    json_file = tmp_path / "urls.json"
    json_file.write_text(json.dumps([{"url": "a"}, "b", "a"]), encoding="utf-8")
    assert load_urls(str(json_file)) == ["a", "b"]


def test_fetch_digest_urls_writes_manifest(tmp_path: Path, monkeypatch) -> None:
    workspace = Workspace.resolve(
        root=tmp_path / "ws", cwd=tmp_path, xdg_cache_home=tmp_path / "cache"
    )
    workspace.ensure_layout()
    monkeypatch.setattr(
        "video_buddy.batch_digest.fetch_video",
        lambda url, cookies_from_browser=None: {
            "video_id": "abc123def45",
            "title": "Video",
            "channel": "Chan",
            "duration": 10,
            "view_count": 2,
            "upload_date": "20260517",
            "description": "desc",
            "has_captions": False,
        },
    )

    manifest, manifest_path = fetch_digest_urls(
        ["https://www.youtube.com/watch?v=abc123def45"], workspace=workspace
    )

    assert manifest_path.is_file()
    assert manifest["counts"]["succeeded"] == 1


def test_transcribe_manifest_updates_counts(tmp_path: Path) -> None:
    workspace = Workspace.resolve(
        root=tmp_path / "ws", cwd=tmp_path, xdg_cache_home=tmp_path / "cache"
    )
    workspace.ensure_layout()
    manifest_path = workspace.manifest("digest.json")
    manifest_path.write_text(
        json.dumps(
            {
                "items": [{"video_id": "abc123def45", "has_captions": False}],
                "counts": {},
            }
        ),
        encoding="utf-8",
    )
    (workspace.video_json("abc123def45")).write_text(
        json.dumps({"video_id": "abc123def45"}), encoding="utf-8"
    )

    manifest, _ = transcribe_manifest(
        manifest_path,
        workspace=workspace,
        transcribe_fn=lambda path: [{"text": "hi", "start": 0, "duration": 1}],
    )

    assert manifest["counts"]["transcribed"] == 1
    assert workspace.transcript_json("abc123def45").is_file()


def test_compile_digest_groups_summaries(tmp_path: Path) -> None:
    workspace = Workspace.resolve(
        root=tmp_path / "ws", cwd=tmp_path, xdg_cache_home=tmp_path / "cache"
    )
    workspace.ensure_layout()
    manifest_path = workspace.manifest("digest.json")
    manifest_path.write_text(
        json.dumps(
            {
                "items": [
                    {"video_id": "abc123def45", "title": "Video", "channel": "Chan"}
                ]
            }
        ),
        encoding="utf-8",
    )
    workspace.summary("abc123def45").write_text("Summary body", encoding="utf-8")

    result, digest_path = compile_digest(
        manifest_path, workspace=workspace, day="2026-05-17"
    )

    assert digest_path.is_file()
    assert "Chan" in digest_path.read_text(encoding="utf-8")
    assert result["missing_summaries"] == []
