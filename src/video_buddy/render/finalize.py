from __future__ import annotations

import shutil
from pathlib import Path

from .note import draft_note_slug


def finalize_note(
    source_payload: dict,
    draft_note_path: Path,
    *,
    notes_root: Path,
    month: str | None = None,
) -> Path:
    if not draft_note_path.exists():
        raise RuntimeError(f"Draft note not found: {draft_note_path}")

    slug = draft_note_slug(source_payload)
    destination_dir = notes_root / month if month else notes_root
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{slug}.md"
    shutil.copyfile(draft_note_path, destination)
    return destination


def upload_month(payload: dict) -> str | None:
    raw = str(payload.get("upload_date") or "")
    if len(raw) != 8 or not raw.isdigit():
        return None
    return f"{raw[:4]}-{raw[4:6]}"
