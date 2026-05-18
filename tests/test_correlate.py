from __future__ import annotations

import json
from pathlib import Path

from video_buddy.cli import main
from video_buddy.correlate.repo import dedupe_matches, extract_filename_candidates


def test_extract_filename_candidates() -> None:
    text = "See player.gd and main.py plus player.gd again"
    assert extract_filename_candidates(text) == ["main.py", "player.gd"]


def test_dedupe_matches() -> None:
    matches = [
        {"file": "src/main.py", "permalink": "a"},
        {"file": "src/main.py", "permalink": "a"},
        {"file": "src/other.py", "permalink": "b"},
    ]
    assert dedupe_matches(matches) == [
        {"file": "src/main.py", "permalink": "a"},
        {"file": "src/other.py", "permalink": "b"},
    ]


def test_correlate_command_updates_frames_meta(tmp_path: Path, monkeypatch) -> None:
    workspace = tmp_path / "workspace"
    intermediate = workspace / "intermediates"
    frames_dir = intermediate / "frames_abc123def45"
    frames_dir.mkdir(parents=True)
    video_json = intermediate / "video_abc123def45.json"
    video_json.write_text(
        json.dumps(
            {
                "video_id": "abc123def45",
                "source_repos": [
                    {
                        "url": "https://github.com/example/project",
                        "owner_repo": "example/project",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    frames_meta = frames_dir / "frames_meta.json"
    frames_meta.write_text(
        json.dumps(
            {
                "video_id": "abc123def45",
                "frames": [
                    {
                        "filename": "frame_00001000.jpg",
                        "ocr_text": "main.py",
                        "should_ocr": True,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    def _fake_correlate(video_json_path, frames_meta_path, repo_clone_root):
        data = json.loads(frames_meta_path.read_text(encoding="utf-8"))
        data["frames"][0]["repo_matches"] = [
            {
                "file": "src/main.py",
                "snippet": "print('hi')",
                "permalink": "https://github.com/example/project/blob/main/src/main.py",
                "confidence": 0.9,
            }
        ]
        frames_meta_path.write_text(json.dumps(data), encoding="utf-8")
        return data

    monkeypatch.setattr("video_buddy.cli.correlate_video", _fake_correlate)

    exit_code = main(["correlate", "abc123def45", "--workspace", str(workspace)])

    assert exit_code == 0
    updated = json.loads(frames_meta.read_text(encoding="utf-8"))
    assert updated["frames"][0]["repo_matches"][0]["file"] == "src/main.py"
