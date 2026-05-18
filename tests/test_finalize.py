from __future__ import annotations

import json
from pathlib import Path

from video_buddy.cli import main
from video_buddy.render.finalize import finalize_note, upload_month


def test_upload_month_for_video_payload() -> None:
    assert upload_month({"upload_date": "20260517"}) == "2026-05"
    assert upload_month({"upload_date": "bad"}) is None


def test_finalize_note_copies_to_destination(tmp_path: Path) -> None:
    draft = tmp_path / "note_abc123def45.md"
    draft.write_text("# Draft", encoding="utf-8")

    destination = finalize_note(
        {"video_id": "abc123def45", "title": "Hello World"},
        draft,
        notes_root=tmp_path / "notes",
        month="2026-05",
    )

    assert destination == tmp_path / "notes" / "2026-05" / "hello-world.md"
    assert destination.read_text(encoding="utf-8") == "# Draft"


def test_finalize_command_moves_rendered_note(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    intermediate = workspace / "intermediates"
    intermediate.mkdir(parents=True)
    (intermediate / "video_abc123def45.json").write_text(
        json.dumps(
            {
                "video_id": "abc123def45",
                "title": "Test Video",
                "upload_date": "20260517",
            }
        ),
        encoding="utf-8",
    )
    (intermediate / "note_abc123def45.md").write_text("# Draft", encoding="utf-8")
    exit_code = main(["finalize", "abc123def45", "--workspace", str(workspace)])

    assert exit_code == 0
    assert (workspace / "notes" / "test-video.md").is_file()
