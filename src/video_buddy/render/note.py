from __future__ import annotations

from datetime import date
import re
from typing import Any

VIDEO_DEFAULT_TEMPLATE = """---
video_id: "{{video_id}}"
title: "{{title}}"
description: "{{description}}"
source: youtube
url: "https://www.youtube.com/watch?v={{video_id}}"
thumbnail: "{{thumbnail}}"
channel: "{{channel}}"
channel_id: "{{channel_id}}"
published: "{{upload_date}}"
created: "{{processed_date}}"
duration: {{duration}}
view_count: {{view_count}}
status: draft
tags: []
---

# {{title_raw}}

## Quick Summary

<!-- agent: fill Quick Summary (2-3 sentences from transcript) -->

## Key Concepts

<!-- agent: fill Key Concepts (flat markdown bullet list) -->

## Detailed Notes

<!-- agent: fill Detailed Notes (sectioned markdown notes) -->

## Visual Notes

{{visual_notes}}

## Source Code

{{source_code}}

## Timestamps

{{timestamps}}
## Full Transcript

<details>
<summary>Click to expand transcript</summary>

{{transcript}}

</details>
"""

VIDEO_OBSIDIAN_TEMPLATE = VIDEO_DEFAULT_TEMPLATE.replace(
    "flat markdown bullet list", "Obsidian wiki-link bullet list"
)

ARTICLE_DEFAULT_TEMPLATE = """---
source_id: "{{source_id}}"
title: "{{title}}"
authors:
{{authors_yaml}}description: "{{description}}"
source: {{source_type}}
url: "{{url}}"
doi: "{{doi}}"
venue: "{{venue}}"
published: "{{published}}"
created: "{{processed_date}}"
word_count: {{word_count}}
tags: []
---

# {{title_raw}}

## Quick Summary

<!-- agent: fill Quick Summary (2-3 sentences from article) -->

## Key Concepts

<!-- agent: fill Key Concepts (flat markdown bullet list) -->

## Detailed Notes

<!-- agent: fill Detailed Notes (sectioned markdown notes) -->

## Full Text

<details>
<summary>Click to expand full text</summary>

{{content}}

</details>
"""

ARTICLE_OBSIDIAN_TEMPLATE = ARTICLE_DEFAULT_TEMPLATE.replace(
    "flat markdown bullet list", "Obsidian wiki-link bullet list"
)


def draft_note_id(payload: dict[str, Any]) -> str:
    return str(payload.get("video_id") or payload.get("source_id") or "")


def draft_note_slug(payload: dict[str, Any]) -> str:
    title = str(
        payload.get("title")
        or payload.get("video_id")
        or payload.get("source_id")
        or "note"
    )
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "note"


def render_note(payload: dict[str, Any], *, template: str = "default") -> str:
    if "video_id" in payload:
        return _render_video(payload, template=template)
    return _render_article(payload, template=template)


def _render_video(payload: dict[str, Any], *, template: str) -> str:
    if template == "obsidian":
        body = VIDEO_OBSIDIAN_TEMPLATE
    elif template == "default":
        body = VIDEO_DEFAULT_TEMPLATE
    else:
        body = template
    replacements = {
        "video_id": str(payload.get("video_id") or ""),
        "title": _yaml_escape(str(payload.get("title") or "")),
        "title_raw": str(payload.get("title") or ""),
        "description": _yaml_escape(str(payload.get("description") or "")),
        "thumbnail": str(payload.get("thumbnail") or ""),
        "channel": _yaml_escape(str(payload.get("channel") or "")),
        "channel_id": _yaml_escape(str(payload.get("channel_id") or "")),
        "upload_date": str(payload.get("upload_date") or ""),
        "processed_date": date.today().isoformat(),
        "duration": str(payload.get("duration") or 0),
        "view_count": str(payload.get("view_count") or 0),
        "transcript": _build_transcript(payload.get("captions", [])),
        "timestamps": _build_timestamps(payload.get("captions", []))
        or "<!-- no timestamps available -->",
        "visual_notes": _build_visual_notes(payload.get("frames", []))
        or "<!-- no frames captured -->",
        "source_code": _build_source_code_section(
            payload.get("frames", []), payload.get("source_repos")
        )
        or "<!-- no source snippets correlated -->",
    }
    return _apply_replacements(body, replacements)


def _render_article(payload: dict[str, Any], *, template: str) -> str:
    if template == "obsidian":
        body = ARTICLE_OBSIDIAN_TEMPLATE
    elif template == "default":
        body = ARTICLE_DEFAULT_TEMPLATE
    else:
        body = template
    authors = payload.get("authors") or []
    if authors:
        authors_yaml = "".join(
            f"  - {_yaml_escape(str(author))}\n" for author in authors
        )
    else:
        authors_yaml = "  -\n"
    replacements = {
        "source_id": str(payload.get("source_id") or ""),
        "title": _yaml_escape(str(payload.get("title") or "")),
        "title_raw": str(payload.get("title") or ""),
        "authors_yaml": authors_yaml,
        "description": _yaml_escape(str(payload.get("description") or "")),
        "source_type": str(payload.get("source_type") or "article"),
        "url": str(payload.get("url") or ""),
        "doi": str(payload.get("doi") or ""),
        "venue": _yaml_escape(str(payload.get("venue") or "")),
        "published": str(payload.get("published") or ""),
        "processed_date": date.today().isoformat(),
        "word_count": str(payload.get("word_count") or 0),
        "content": str(payload.get("content") or ""),
    }
    return _apply_replacements(body, replacements)


def _apply_replacements(template: str, replacements: dict[str, str]) -> str:
    result = template
    for key, value in replacements.items():
        result = result.replace("{{" + key + "}}", value)
    return result


def _yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _build_transcript(captions: list[dict]) -> str:
    if not captions:
        return ""
    real_captions = [cap for cap in captions if cap.get("duration", 0) > 0.02]
    deduped: list[dict] = []
    prev_text = None
    for cap in real_captions:
        text = str(cap.get("intended_text") or cap.get("text", "")).split("\n")[0]
        if text != prev_text:
            deduped.append({**cap, "text": text})
            prev_text = text
    paragraphs: list[list[str]] = [[]]
    last_break = 0.0
    for cap in deduped:
        start = cap.get("start", 0)
        if start - last_break >= 300 and paragraphs[0]:
            paragraphs.append([])
            last_break = start
        paragraphs[-1].append(cap["text"])
    return "\n\n".join(" ".join(paragraph) for paragraph in paragraphs if paragraph)


def _build_timestamps(captions: list[dict]) -> str:
    if not captions:
        return ""
    lines = []
    last_start = None
    for cap in captions:
        start = float(cap.get("start", 0.0))
        words = cap.get("words")
        if words and words[0].get("start") is not None:
            start = float(words[0]["start"])
        text = str(cap.get("text", "")).strip().replace("\n", " ")
        if not text:
            continue
        if last_start is not None and start - last_start < 60:
            continue
        lines.append(f"- {_format_timestamp(start)} - {text}")
        last_start = start
        if len(lines) == 12:
            break
    return "\n".join(lines)


def _format_timestamp(seconds: float) -> str:
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def _build_visual_notes(frames: list[dict]) -> str:
    sections = []
    for frame in frames or []:
        if not frame.get("should_include", True):
            continue
        filename = str(frame.get("filename") or "")
        if not filename:
            continue
        timestamp = str(frame.get("timestamp_human") or "")
        video_id = str(frame.get("video_id") or "")
        block = f"### [{timestamp}]\n\n![{filename}](media/{video_id}/{filename})"
        ocr_text = str(frame.get("ocr_text") or "").strip()
        confidence = frame.get("ocr_confidence", 0.0)
        if ocr_text and isinstance(confidence, (int, float)) and confidence >= 0.6:
            cleaned = []
            for line in ocr_text.split("\n"):
                line = " ".join(line.split())
                if len(line) > 2 and any(char.isalnum() for char in line):
                    cleaned.append(line)
            if cleaned:
                block += "\n\n> " + "\n> ".join(cleaned)
        sections.append(block)
    return "\n\n".join(sections)


def _build_source_code_section(
    frames: list[dict], source_repos: list[dict] | None
) -> str:
    if not source_repos:
        return ""
    parts = []
    repo_links = []
    for repo in source_repos:
        url = str(repo.get("url") or "")
        owner_repo = str(repo.get("owner_repo") or "")
        if url and owner_repo:
            repo_links.append(f"- [{owner_repo}]({url})")
    if repo_links:
        parts.append("### Referenced Repositories\n")
        parts.append("\n".join(repo_links))

    seen_files: set[str] = set()
    code_sections = []
    for frame in frames or []:
        for match in frame.get("repo_matches", []):
            file_path = str(match.get("file") or "")
            if not file_path or file_path in seen_files:
                continue
            seen_files.add(file_path)
            snippet = str(match.get("snippet") or "").strip()
            permalink = str(match.get("permalink") or "")
            if not snippet:
                continue
            header = f"### {file_path}"
            if permalink:
                header += f"\n[{file_path}]({permalink})"
            code_sections.append(f"{header}\n\n```\n{snippet}\n```")
    if code_sections:
        parts.append("### Matched Source Files\n")
        parts.append("\n\n".join(code_sections[:5]))
    return "\n\n".join(parts)
