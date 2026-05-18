from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class WorkspaceOverrides:
    intermediates: Path | None = None
    notes: Path | None = None
    media: Path | None = None
    model_cache: Path | None = None
    repo_clone_root: Path | None = None
    templates: Path | None = None


@dataclass(frozen=True, slots=True)
class Workspace:
    root: Path
    intermediates: Path
    notes: Path
    media: Path
    model_cache: Path
    repo_clone_root: Path
    templates: Path | None = None

    @classmethod
    def resolve(
        cls,
        root: Path | None = None,
        overrides: WorkspaceOverrides | None = None,
        *,
        cwd: Path | None = None,
        xdg_cache_home: Path | None = None,
    ) -> "Workspace":
        cwd = (cwd or Path.cwd()).resolve()
        root_path = (root or cwd / "vb-workspace").resolve()
        cache_home = _resolve_xdg_cache_home(xdg_cache_home, cwd)
        overrides = overrides or WorkspaceOverrides()

        notes = _resolve_path(overrides.notes, root_path / "notes")
        media = _resolve_path(overrides.media, notes / "media")

        return cls(
            root=root_path,
            intermediates=_resolve_path(
                overrides.intermediates, root_path / "intermediates"
            ),
            notes=notes,
            media=media,
            model_cache=_resolve_path(
                overrides.model_cache, cache_home / "video-buddy" / "models"
            ),
            repo_clone_root=_resolve_path(
                overrides.repo_clone_root, cache_home / "video-buddy" / "repos"
            ),
            templates=_resolve_optional_path(overrides.templates),
        )

    def config_path(self) -> Path:
        return self.root / ".video-buddy.toml"

    def workspace_gitignore_path(self) -> Path:
        return self.root / ".gitignore"

    def video_json(self, video_id: str) -> Path:
        return self.intermediates / f"video_{video_id}.json"

    def article_json(self, source_id: str) -> Path:
        return self.intermediates / f"article_{source_id}.json"

    def draft_note(self, source_id: str) -> Path:
        return self.intermediates / f"note_{source_id}.md"

    def concepts_json(self, source_id: str) -> Path:
        return self.intermediates / f"concepts_{source_id}.json"

    def concept_result_json(self, source_id: str) -> Path:
        return self.intermediates / f"concept_result_{source_id}.json"

    def manifest(self, name: str) -> Path:
        return self.intermediates / name

    def summary(self, video_id: str) -> Path:
        return self.intermediates / "summaries" / f"video_{video_id}.md"

    def digest(self, day: str) -> Path:
        return self.notes / "digests" / f"digest-{day}.md"

    def transcript_json(self, video_id: str) -> Path:
        return self.intermediates / f"transcript_{video_id}.json"

    def frames_dir(self, video_id: str) -> Path:
        return self.intermediates / f"frames_{video_id}"

    def frames_meta(self, video_id: str) -> Path:
        return self.frames_dir(video_id) / "frames_meta.json"

    def note(self, slug: str, *, month: str | None = None) -> Path:
        if month:
            return self.notes / month / f"{slug}.md"
        return self.notes / f"{slug}.md"

    def media_for(self, video_id: str) -> Path:
        return self.media / video_id

    def agent_prompt(self, video_id: str, kind: str) -> Path:
        return self.intermediates / "agent-prompts" / f"{video_id}_{kind}.md"

    def ensure_layout(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.intermediates.mkdir(parents=True, exist_ok=True)
        self.notes.mkdir(parents=True, exist_ok=True)
        self.media.mkdir(parents=True, exist_ok=True)
        (self.notes / "concepts").mkdir(parents=True, exist_ok=True)
        (self.notes / "digests").mkdir(parents=True, exist_ok=True)
        (self.intermediates / "agent-prompts").mkdir(parents=True, exist_ok=True)
        (self.intermediates / "summaries").mkdir(parents=True, exist_ok=True)


def annotated_config(workspace: Workspace) -> str:
    return "\n".join(
        [
            "# video-buddy workspace configuration",
            "# Every path shown below is the resolved default for this workspace.",
            "",
            "[workspace]",
            f'# root = "{workspace.root}"',
            f'# intermediates = "{workspace.intermediates}"',
            f'# notes = "{workspace.notes}"',
            f'# media = "{workspace.media}"',
            f'# model_cache = "{workspace.model_cache}"',
            f'# repo_clone_root = "{workspace.repo_clone_root}"',
            "",
            "[notes]",
            '# group_by = "flat"',
            '# template = "default"',
            "",
            "[whisper]",
            '# model = "auto"',
            '# device = "auto"',
            '# compute_type = "auto"',
            "",
            "[frames]",
            "# max_per_video = 15",
            "# scene_detection_max_duration_s = 600",
            '# ocr = "auto"',
            "[agent]",
            '# harness = "claude-code"',
            "",
            "[youtube]",
            '# cookies_from_browser = ""',
            "# caption_retry_max = 3",
            "",
            "[tools]",
            '# ffmpeg = "ffmpeg"',
            '# node = "node"',
            '# git = "git"',
            '# tesseract = "tesseract"',
            "",
            "# [[compute]]",
            '# name = "homelab"',
            '# type = "ssh"',
            "# priority = 10",
            '# host = "user@gpu-box.lan"',
            '# worker_root = "~/video-buddy-worker"',
            '# capabilities = ["whisper", "easyocr", "gpu"]',
            '# ssh_opts = ["-o", "ConnectTimeout=8", "-o", "BatchMode=yes"]',
            "",
        ]
    )


def workspace_gitignore() -> str:
    return "\n".join(
        [
            "# Intermediate artifacts regenerated by video-buddy",
            "intermediates/",
            "",
            "# Local env files if the user creates them",
            ".env",
            ".env.*",
            "!.env.example",
            "",
        ]
    )


def _resolve_xdg_cache_home(xdg_cache_home: Path | None, cwd: Path) -> Path:
    if xdg_cache_home is not None:
        return xdg_cache_home.resolve()
    configured = os.environ.get("XDG_CACHE_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path.home().joinpath(".cache").resolve()


def _resolve_path(path: Path | None, default: Path) -> Path:
    return _resolve_optional_path(path) or default.resolve()


def _resolve_optional_path(path: Path | None) -> Path | None:
    if path is None:
        return None
    return path.expanduser().resolve()
