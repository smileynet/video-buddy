from __future__ import annotations

from datetime import datetime, timezone
import re
import sys
from urllib.parse import parse_qs, urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .yt_dlp_opts import apply_youtube_auth

try:
    import yt_dlp
except ImportError:  # pragma: no cover - dependency should exist in normal installs
    yt_dlp = None

HTTP_TIMEOUT = 30
_CAPTIONS_RETRY = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset({"GET"}),
    respect_retry_after_header=True,
)
_captions_session = requests.Session()
_captions_session.mount("https://", HTTPAdapter(max_retries=_CAPTIONS_RETRY))

VIDEO_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{11}$")
REPO_URL_PATTERNS = [
    re.compile(
        r"https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"
        r"(?:/(?:tree|blob)/[A-Za-z0-9_.-/]+)?"
    ),
    re.compile(
        r"https?://gitlab\.com/([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+)"
        r"(?:/(?:-/tree|-/blob)/[A-Za-z0-9_.-/]+)?"
    ),
    re.compile(
        r"https?://bitbucket\.org/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"
        r"(?:/src/[A-Za-z0-9_.-/]+)?"
    ),
]


def extract_video_id(url: str) -> str:
    if not url:
        raise ValueError("URL cannot be empty")

    parsed = urlparse(url)
    video_id = None

    if parsed.netloc in ("youtu.be", "www.youtu.be"):
        path_id = parsed.path.lstrip("/")
        if path_id:
            video_id = path_id.split("/")[0].split("?")[0]
    elif parsed.netloc in ("youtube.com", "www.youtube.com", "m.youtube.com"):
        if parsed.path == "/watch":
            params = parse_qs(parsed.query)
            if "v" in params:
                video_id = params["v"][0]
        elif parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/")[2].split("?")[0]
        elif parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/")[2].split("?")[0]

    if video_id and VIDEO_ID_PATTERN.match(video_id):
        return video_id

    raise ValueError(f"Invalid YouTube URL: {url}")


def parse_vtt(vtt_content: str | None) -> list[dict]:
    if not vtt_content:
        return []

    captions = []
    lines = vtt_content.strip().split("\n")
    timestamp_pattern = re.compile(
        r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})\.(\d{3})"
    )

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        match = timestamp_pattern.match(line)
        if not match:
            i += 1
            continue

        start = (
            int(match.group(1)) * 3600
            + int(match.group(2)) * 60
            + int(match.group(3))
            + int(match.group(4)) / 1000
        )
        end = (
            int(match.group(5)) * 3600
            + int(match.group(6)) * 60
            + int(match.group(7))
            + int(match.group(8)) / 1000
        )
        text_lines = []
        i += 1
        while i < len(lines):
            text_line = lines[i].strip()
            if not text_line or timestamp_pattern.match(text_line):
                break
            if not text_line.isdigit() and "-->" not in text_line:
                text_lines.append(text_line)
            i += 1

        if text_lines:
            text = re.sub(r"<[^>]+>", "", "\n".join(text_lines)).strip()
            if text:
                captions.append(
                    {
                        "start": start,
                        "duration": round(end - start, 3),
                        "text": text,
                    }
                )

    return captions


def fetch_metadata(url: str, cookies_from_browser: str | None = None) -> dict:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "skip_download": True,
        "ignore_no_formats_error": True,
    }
    apply_youtube_auth(ydl_opts, cookies_from_browser)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "video_id": info.get("id"),
        "title": info.get("title"),
        "channel": info.get("channel") or info.get("uploader"),
        "channel_id": info.get("channel_id"),
        "description": info.get("description"),
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),
        "upload_date": info.get("upload_date"),
        "view_count": info.get("view_count"),
    }


def fetch_captions(
    url: str, cookies_from_browser: str | None = None
) -> tuple[list[dict], bool]:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en", "en-US", "en-GB"],
        "ignore_no_formats_error": True,
    }
    apply_youtube_auth(ydl_opts, cookies_from_browser)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    subtitles = info.get("subtitles") or {}
    auto_captions = info.get("automatic_captions") or {}
    caption_url = None

    for lang in ["en", "en-US", "en-GB"]:
        if lang in subtitles:
            for fmt in subtitles[lang]:
                if fmt.get("ext") == "vtt":
                    caption_url = fmt.get("url")
                    break
            if caption_url:
                break

    if not caption_url:
        for lang in ["en", "en-US", "en-GB", "en-orig"]:
            if lang in auto_captions:
                for fmt in auto_captions[lang]:
                    if fmt.get("ext") == "vtt":
                        caption_url = fmt.get("url")
                        break
                if caption_url:
                    break

    if not caption_url:
        return [], False

    try:
        response = _captions_session.get(caption_url, timeout=HTTP_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Warning: Failed to fetch captions: {exc}", file=sys.stderr)
        return [], False

    return parse_vtt(response.text), True


def extract_source_repos(
    description: str | None, captions: list[dict] | None
) -> list[dict]:
    if not description and not captions:
        return []

    texts = []
    if description:
        texts.append(description)
    if captions:
        texts.append(" ".join(cap.get("text", "") for cap in captions))
    combined = "\n".join(texts)
    lower = combined.lower()
    code_keywords = [
        "source code",
        "example project",
        "repository",
        "repo",
        "github",
        "clone",
        "follow along",
        "code from",
        "available on",
        "project on",
    ]
    likely_code = any(keyword in lower for keyword in code_keywords)

    seen: dict[str, dict] = {}
    for pattern in REPO_URL_PATTERNS:
        for match in pattern.finditer(combined):
            full_url = match.group(0).rstrip(")")
            owner_repo = match.group(1)
            if owner_repo in seen:
                continue

            provider = "unknown"
            if "github.com" in full_url:
                provider = "github"
            elif "gitlab.com" in full_url:
                provider = "gitlab"
            elif "bitbucket.org" in full_url:
                provider = "bitbucket"

            base_url = full_url.split("/tree/")[0].split("/blob/")[0].split("/src/")[0]
            seen[owner_repo] = {
                "url": base_url,
                "provider": provider,
                "owner_repo": owner_repo,
                "likely_code": likely_code,
            }

    return list(seen.values())


def fetch_video(url: str, cookies_from_browser: str | None = None) -> dict:
    extract_video_id(url)
    metadata = fetch_metadata(url, cookies_from_browser=cookies_from_browser)
    captions, has_captions = fetch_captions(
        url, cookies_from_browser=cookies_from_browser
    )
    source_repos = extract_source_repos(
        metadata.get("description"),
        captions if has_captions else None,
    )
    return {
        **metadata,
        "has_captions": has_captions,
        "captions": captions,
        "source_repos": source_repos,
        "cookies_from_browser": cookies_from_browser or "",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }
