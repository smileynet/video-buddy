from __future__ import annotations

import json
from pathlib import Path

from video_buddy.cli import main
from video_buddy.render.note import draft_note_id, draft_note_slug, render_note


def test_render_note_for_video_includes_placeholders() -> None:
    note = render_note(
        {
            "video_id": "abc123def45",
            "title": "Test Video",
            "description": "desc",
            "channel": "Chan",
            "captions": [{"start": 0.0, "duration": 1.0, "text": "hello"}],
        }
    )

    assert 'video_id: "abc123def45"' in note
    assert "<!-- agent: fill Quick Summary" in note
    assert "hello" in note
    assert "- 0:00 - hello" in note


def test_render_note_for_article_includes_full_text() -> None:
    note = render_note(
        {
            "source_id": "web-abc123def456",
            "source_type": "article",
            "title": "Article Title",
            "content": "body text",
            "authors": ["Author One"],
        }
    )

    assert 'source_id: "web-abc123def456"' in note
    assert "Author One" in note
    assert "body text" in note


def test_draft_helpers() -> None:
    assert draft_note_id({"video_id": "abc123def45"}) == "abc123def45"
    assert draft_note_slug({"title": "Hello, World!"}) == "hello-world"


def test_render_command_writes_draft_note(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    intermediate = workspace / "intermediates"
    intermediate.mkdir(parents=True)
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
    (intermediate / "transcript_abc123def45.json").write_text(
        json.dumps([{"start": 0.0, "duration": 1.0, "text": "hello from transcript"}]),
        encoding="utf-8",
    )
    frames_dir = intermediate / "frames_abc123def45"
    frames_dir.mkdir()
    (frames_dir / "frames_meta.json").write_text(
        json.dumps(
            {
                "video_id": "abc123def45",
                "frames": [
                    {
                        "video_id": "abc123def45",
                        "filename": "frame_00001000.jpg",
                        "timestamp_human": "0:01",
                        "should_include": True,
                        "ocr_text": "visible text",
                        "ocr_confidence": 0.9,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    exit_code = main(["render", "abc123def45", "--workspace", str(workspace)])

    assert exit_code == 0
    note_path = intermediate / "note_abc123def45.md"
    assert note_path.is_file()
    text = note_path.read_text(encoding="utf-8")
    assert "Test Video" in text
    assert "hello from transcript" in text
    assert "visible text" in text
    assert (intermediate / "agent-prompts" / "abc123def45_summary.md").is_file()


def test_render_command_accepts_custom_template(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    intermediate = workspace / "intermediates"
    intermediate.mkdir(parents=True)
    (intermediate / "article_web-abc123def456.json").write_text(
        json.dumps(
            {
                "source_id": "web-abc123def456",
                "source_type": "article",
                "title": "Article Title",
                "content": "body",
                "authors": [],
            }
        ),
        encoding="utf-8",
    )
    template = tmp_path / "custom.md"
    template.write_text("# {{title_raw}}\n\n{{content}}\n", encoding="utf-8")

    exit_code = main(
        [
            "render",
            "web-abc123def456",
            "--workspace",
            str(workspace),
            "--template",
            str(template),
        ]
    )

    assert exit_code == 0
    assert "# Article Title" in (intermediate / "note_web-abc123def456.md").read_text(
        encoding="utf-8"
    )
