from __future__ import annotations

import json
from pathlib import Path

from video_buddy.concepts import process_concepts_file, slugify


def test_slugify() -> None:
    assert slugify("Machine Learning") == "machine-learning"


def test_process_concepts_file_creates_and_updates_notes(tmp_path: Path) -> None:
    concepts_dir = tmp_path / "concepts"
    concepts_json = tmp_path / "concepts_abc.json"
    concepts_json.write_text(
        json.dumps(
            {
                "tags": ["ai"],
                "concepts": [
                    {
                        "name": "Agent Speed",
                        "definition": "Optimizing agent throughput.",
                        "relevance": "Core theme",
                        "related_concepts": ["Guardrails"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    summary = process_concepts_file(
        concepts_json,
        concepts_dir=concepts_dir,
        source_title="Test Note",
        source_slug="test-note",
    )

    note = concepts_dir / "agent-speed.md"
    assert summary.created == ("Agent Speed",)
    assert note.is_file()
    text = note.read_text(encoding="utf-8")
    assert "[Test Note](../test-note.md)" in text
    assert "[Guardrails](guardrails.md)" in text

    summary2 = process_concepts_file(
        concepts_json,
        concepts_dir=concepts_dir,
        source_title="Test Note",
        source_slug="test-note",
    )
    assert summary2.created == ()
    assert summary2.updated == ()
