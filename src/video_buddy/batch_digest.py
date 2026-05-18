from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time
from typing import Any

from .fetch.article import detect_doi, detect_source_type
from .fetch.youtube import extract_video_id, fetch_video


def load_urls(input_path: str) -> list[str]:
    content = (
        sys.stdin.read()
        if input_path == "-"
        else Path(input_path).read_text(encoding="utf-8")
    )
    content = content.strip()
    if not content:
        return []
    if content.startswith("[") or content.startswith("{"):
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                data = [data]
            urls = []
            for item in data:
                if isinstance(item, str):
                    urls.append(item)
                elif isinstance(item, dict) and "url" in item:
                    urls.append(str(item["url"]))
            return list(dict.fromkeys(urls))
        except json.JSONDecodeError:
            pass
    return list(
        dict.fromkeys(line.strip() for line in content.splitlines() if line.strip())
    )


def classify_url(url: str) -> str:
    try:
        extract_video_id(url)
        return "video"
    except ValueError:
        pass
    doi = detect_doi(url)
    return detect_source_type(url, None, doi)


def fetch_digest_urls(
    urls: list[str],
    *,
    workspace,
    cookies_from_browser: str | None = None,
    delay: float = 0.0,
) -> tuple[dict, Path]:
    video_urls: list[tuple[str, str]] = []
    for url in urls:
        if classify_url(url) != "video":
            continue
        video_urls.append((url, extract_video_id(url)))
    deduped: list[tuple[str, str]] = []
    seen: set[str] = set()
    for url, vid in video_urls:
        if vid in seen:
            continue
        seen.add(vid)
        deduped.append((url, vid))

    items: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for index, (url, vid) in enumerate(deduped):
        if index > 0 and delay > 0:
            time.sleep(delay)
        cache_file = workspace.video_json(vid)
        if cache_file.exists():
            data = json.loads(cache_file.read_text(encoding="utf-8"))
        else:
            try:
                data = fetch_video(url, cookies_from_browser=cookies_from_browser)
                cache_file.write_text(
                    json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
                )
            except Exception as exc:
                errors.append(
                    {"url": url, "video_id": vid, "stage": "fetch", "error": str(exc)}
                )
                continue
        items.append(
            {
                "url": url,
                "video_id": data.get("video_id", vid),
                "title": data.get("title", ""),
                "channel": data.get("channel", ""),
                "duration": data.get("duration"),
                "view_count": data.get("view_count"),
                "upload_date": data.get("upload_date", ""),
                "description_snippet": snippet(data.get("description")),
                "has_captions": data.get("has_captions", False),
                "already_in_notes": bool(list(workspace.notes.glob(f"**/*{vid}*.md"))),
                "paths": {
                    "video_json": str(workspace.video_json(vid)),
                    "transcript_json": str(workspace.transcript_json(vid)),
                    "summary_md": str(workspace.summary(vid)),
                },
            }
        )
    manifest = {
        "schema_version": "1.0",
        "kind": "digest_manifest",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input": {"submitted": len(video_urls), "deduped": len(deduped)},
        "counts": {
            "total": len(items) + len(errors),
            "succeeded": len(items),
            "failed": len(errors),
            "no_captions": sum(1 for item in items if not item.get("has_captions")),
            "already_in_notes": sum(
                1 for item in items if item.get("already_in_notes")
            ),
        },
        "items": items,
        "errors": errors,
    }
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    manifest_path = workspace.manifest(f"digest-manifest-{stamp}.json")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return manifest, manifest_path


def transcribe_manifest(
    manifest_path: Path, *, workspace, transcribe_fn
) -> tuple[dict, Path]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    updated = 0
    for item in manifest.get("items", []):
        if item.get("has_captions"):
            continue
        video_id = str(item.get("video_id") or "")
        if not video_id:
            continue
        captions = transcribe_fn(workspace.video_json(video_id))
        workspace.transcript_json(video_id).write_text(
            json.dumps(captions, indent=2, sort_keys=True), encoding="utf-8"
        )
        updated += 1
    manifest.setdefault("counts", {})["transcribed"] = updated
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return manifest, manifest_path


def compile_digest(manifest_path: Path, *, workspace, day: str) -> tuple[dict, Path]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_channel: dict[str, list[dict[str, Any]]] = {}
    missing: list[str] = []
    for item in manifest.get("items", []):
        video_id = str(item.get("video_id") or "")
        summary_path = workspace.summary(video_id)
        if not summary_path.exists():
            missing.append(video_id)
            continue
        by_channel.setdefault(str(item.get("channel") or "Unknown"), []).append(
            {
                "title": str(item.get("title") or video_id),
                "video_id": video_id,
                "summary": summary_path.read_text(encoding="utf-8").strip(),
            }
        )
    parts = [f"# Digest {day}", ""]
    for channel in sorted(by_channel):
        parts.append(f"## {channel}")
        parts.append("")
        for item in by_channel[channel]:
            parts.append(f"### {item['title']}")
            parts.append("")
            parts.append(item["summary"])
            parts.append("")
    if missing:
        parts.append("## Missing summaries")
        parts.append("")
        parts.extend(f"- {video_id}" for video_id in missing)
        parts.append("")
    digest_path = workspace.digest(day)
    digest_path.parent.mkdir(parents=True, exist_ok=True)
    digest_path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    result = {
        "missing_summaries": missing,
        "groups": sorted(by_channel),
        "digest_path": str(digest_path),
    }
    return result, digest_path


def snippet(text: str | None, max_len: int = 200) -> str:
    if not text:
        return ""
    normalized = " ".join(str(text).split())
    if len(normalized) <= max_len:
        return normalized
    truncated = normalized[:max_len].rsplit(" ", 1)[0]
    return truncated + "..."
