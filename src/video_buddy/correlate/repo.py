from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

SEARCHABLE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".gd",
    ".cs",
    ".java",
    ".rs",
    ".go",
    ".rb",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".swift",
    ".kt",
    ".scala",
    ".lua",
    ".zig",
    ".ex",
    ".exs",
    ".hs",
    ".tscn",
}
FILENAME_PATTERN = re.compile(
    r"\b([A-Za-z0-9_.-]+\.(?:py|js|ts|gd|cs|java|rs|go|rb|cpp|c|h|hpp|swift|kt|scala|lua|zig|ex|exs|hs|tscn))\b"
)
IDENTIFIER_PATTERN = re.compile(
    r"\b(?:func|def|class|class_name|signal)\s+([A-Za-z_][A-Za-z0-9_]*)", re.IGNORECASE
)


def correlate_video(
    video_json_path: Path,
    frames_meta_path: Path,
    *,
    repo_clone_root: Path,
) -> dict:
    video_payload = json.loads(video_json_path.read_text(encoding="utf-8"))
    metadata = json.loads(frames_meta_path.read_text(encoding="utf-8"))
    source_repos = video_payload.get("source_repos") or []
    frames = metadata.get("frames") or []

    indexed_repos = []
    for repo in source_repos:
        url = str(repo.get("url") or "")
        if not url or "github.com" not in url:
            continue
        repo_dir, branch = clone_or_update_repo(url, repo_clone_root)
        indexed_repos.append((repo, repo_dir, branch, index_repo_files(repo_dir)))

    for frame in frames:
        if not isinstance(frame, dict):
            continue
        text = str(frame.get("ocr_text") or "").strip()
        if not text:
            continue
        filename_candidates = extract_filename_candidates(text)
        identifiers = extract_identifiers(text)
        matches = []
        for repo, repo_dir, branch, repo_files in indexed_repos:
            for candidate in filename_candidates:
                for repo_file in repo_files:
                    if repo_file["name"].lower() != candidate.lower():
                        continue
                    matches.append(
                        {
                            "file": repo_file["relative_path"],
                            "snippet": repo_file["snippet"],
                            "permalink": f"{repo['url']}/blob/{branch}/{repo_file['relative_path']}",
                            "confidence": 0.9,
                        }
                    )
            for identifier in identifiers:
                for repo_file in repo_files:
                    if identifier.lower() not in repo_file["content_lower"]:
                        continue
                    matches.append(
                        {
                            "file": repo_file["relative_path"],
                            "snippet": snippet_around_identifier(
                                repo_file["content"], identifier
                            ),
                            "permalink": f"{repo['url']}/blob/{branch}/{repo_file['relative_path']}",
                            "confidence": 0.82,
                        }
                    )
        if matches:
            frame["repo_matches"] = dedupe_matches(matches)[:3]

    frames_meta_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return metadata


def clone_or_update_repo(repo_url: str, repo_clone_root: Path) -> tuple[Path, str]:
    owner, repo = parse_github_repo(repo_url)
    repo_dir = repo_clone_root / owner / repo
    repo_dir.parent.mkdir(parents=True, exist_ok=True)
    if repo_dir.exists():
        run_git(["git", "fetch", "origin"], cwd=repo_dir)
        run_git(["git", "pull", "--ff-only"], cwd=repo_dir)
    else:
        run_git(["git", "clone", "--depth", "1", repo_url, str(repo_dir)])
    branch = run_git(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_dir).strip()
    return repo_dir, branch


def parse_github_repo(repo_url: str) -> tuple[str, str]:
    parsed = urlparse(repo_url)
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 2:
        raise ValueError(f"Invalid GitHub repository URL: {repo_url}")
    return parts[0], parts[1]


def run_git(command: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        command, cwd=cwd, check=True, capture_output=True, text=True
    )
    return result.stdout


def index_repo_files(repo_dir: Path) -> list[dict[str, str]]:
    files = []
    for path in repo_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SEARCHABLE_EXTENSIONS:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = path.relative_to(repo_dir).as_posix()
        files.append(
            {
                "name": path.name,
                "relative_path": rel,
                "snippet": snippet_from_content(content),
                "content": content,
                "content_lower": content.lower(),
            }
        )
    return files


def snippet_from_content(content: str, *, max_lines: int = 30) -> str:
    lines = content.strip().splitlines()
    return "\n".join(lines[:max_lines])


def extract_filename_candidates(text: str) -> list[str]:
    return sorted({match.group(1) for match in FILENAME_PATTERN.finditer(text)})


def extract_identifiers(text: str) -> list[str]:
    return sorted({match.group(1) for match in IDENTIFIER_PATTERN.finditer(text)})


def dedupe_matches(matches: list[dict]) -> list[dict]:
    seen = set()
    deduped = []
    for match in sorted(
        matches, key=lambda item: float(item.get("confidence", 0.0)), reverse=True
    ):
        key = (match.get("file"), match.get("permalink"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(match)
    return deduped


def snippet_around_identifier(
    content: str, identifier: str, *, window: int = 15
) -> str:
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if identifier.lower() in line.lower():
            start = max(0, index - window // 2)
            end = min(len(lines), index + window // 2)
            return "\n".join(lines[start:end])
    return snippet_from_content(content)
