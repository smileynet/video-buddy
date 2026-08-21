from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .workspace import Workspace, WorkspaceOverrides

_VALID_SECTION_KEYS: dict[str, set[str]] = {
    "workspace": {
        "root",
        "intermediates",
        "notes",
        "media",
        "model_cache",
        "repo_clone_root",
        "templates",
    },
    "notes": {"group_by", "template"},
    "whisper": {"model", "device", "compute_type", "engine"},
    "frames": {"max_per_video", "scene_detection_max_duration_s", "ocr"},
    "agent": {"harness"},
    "youtube": {"cookies_from_browser", "caption_retry_max"},
    "tools": {"ffmpeg", "node", "git", "tesseract"},
    "compute": set(),
}


@dataclass(frozen=True, slots=True)
class NotesConfig:
    group_by: str = "flat"
    template: str = "default"


@dataclass(frozen=True, slots=True)
class WhisperConfig:
    model: str = "auto"
    device: str = "auto"
    compute_type: str = "auto"
    engine: str = "faster-whisper"


@dataclass(frozen=True, slots=True)
class FramesConfig:
    max_per_video: int = 15
    scene_detection_max_duration_s: int = 600
    ocr: str = "auto"


@dataclass(frozen=True, slots=True)
class YoutubeConfig:
    cookies_from_browser: str = ""
    caption_retry_max: int = 3


@dataclass(frozen=True, slots=True)
class ToolsConfig:
    ffmpeg: str = "ffmpeg"
    node: str = "node"
    git: str = "git"
    tesseract: str = "tesseract"


@dataclass(frozen=True, slots=True)
class AppConfig:
    notes: NotesConfig = NotesConfig()
    whisper: WhisperConfig = WhisperConfig()
    frames: FramesConfig = FramesConfig()
    youtube: YoutubeConfig = YoutubeConfig()
    tools: ToolsConfig = ToolsConfig()


@dataclass(frozen=True, slots=True)
class LoadedConfig:
    workspace_root: Path | None
    overrides: WorkspaceOverrides
    app: AppConfig
    compute: tuple[dict[str, Any], ...]
    sources: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class CliWorkspaceArgs:
    workspace: Path | None = None
    config: Path | None = None
    notes_dir: Path | None = None
    intermediates: Path | None = None
    media_dir: Path | None = None
    model_cache: Path | None = None
    repo_clone_root: Path | None = None
    templates: Path | None = None


@dataclass(frozen=True, slots=True)
class ResolvedContext:
    workspace: Workspace
    config: AppConfig
    compute: tuple[dict[str, Any], ...]
    config_sources: tuple[Path, ...]


def resolve_context_from_sources(
    cli: CliWorkspaceArgs,
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    xdg_cache_home: Path | None = None,
) -> ResolvedContext:
    cwd = (cwd or Path.cwd()).resolve()
    env = os.environ if env is None else env
    explicit_root = _pick_root(cli.workspace, env.get("VIDEO_BUDDY_WORKSPACE"), cwd)
    loaded = load_config_stack(
        _config_candidates(
            cli.config,
            explicit_root=explicit_root,
            cwd=cwd,
            xdg_config_home=env.get("XDG_CONFIG_HOME"),
        )
    )

    overrides = merge_workspace_overrides(
        loaded.overrides,
        WorkspaceOverrides(
            intermediates=cli.intermediates,
            notes=cli.notes_dir,
            media=cli.media_dir,
            model_cache=cli.model_cache,
            repo_clone_root=cli.repo_clone_root,
            templates=cli.templates,
        ),
    )
    cache_home = (
        Path(env["XDG_CACHE_HOME"]).expanduser().resolve()
        if xdg_cache_home is None and env.get("XDG_CACHE_HOME")
        else xdg_cache_home
    )
    workspace = Workspace.resolve(
        root=explicit_root or loaded.workspace_root,
        overrides=overrides,
        cwd=cwd,
        xdg_cache_home=cache_home,
    )
    return ResolvedContext(
        workspace=workspace,
        config=loaded.app,
        compute=loaded.compute,
        config_sources=loaded.sources,
    )


def resolve_workspace_from_sources(
    cli: CliWorkspaceArgs,
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    xdg_cache_home: Path | None = None,
) -> Workspace:
    return resolve_context_from_sources(
        cli, cwd=cwd, env=env, xdg_cache_home=xdg_cache_home
    ).workspace


def load_config_stack(paths: tuple[Path, ...]) -> LoadedConfig:
    workspace_root: Path | None = None
    overrides = WorkspaceOverrides()
    merged_sections: dict[str, dict[str, Any]] = {
        section: {} for section in _VALID_SECTION_KEYS if section != "compute"
    }
    merged_compute: list[dict[str, Any]] = []
    sources: list[Path] = []
    for path in paths:
        resolved = path.expanduser().resolve()
        if not resolved.exists():
            continue
        try:
            data = tomllib.loads(resolved.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            raise SystemExit(f"Invalid TOML in {resolved}: {exc}") from exc
        _validate_config(resolved, data)
        parsed = _parse_workspace_config(resolved, data)
        workspace_root = parsed[0] or workspace_root
        overrides = merge_workspace_overrides(overrides, parsed[1])
        for section in merged_sections:
            section_data = data.get(section)
            if isinstance(section_data, dict):
                merged_sections[section].update(section_data)
        compute_data = data.get("compute")
        if isinstance(compute_data, list):
            merged_compute = [
                dict(item) for item in compute_data if isinstance(item, dict)
            ]
        sources.append(resolved)

    return LoadedConfig(
        workspace_root=workspace_root,
        overrides=overrides,
        app=_app_from_sections(merged_sections),
        compute=tuple(merged_compute),
        sources=tuple(sources),
    )


def load_config(path: Path | None) -> LoadedConfig:
    if path is None:
        return LoadedConfig(None, WorkspaceOverrides(), AppConfig(), (), ())
    return load_config_stack((path,))


def merge_workspace_overrides(*parts: WorkspaceOverrides) -> WorkspaceOverrides:
    merged = WorkspaceOverrides()
    for part in parts:
        merged = WorkspaceOverrides(
            intermediates=part.intermediates or merged.intermediates,
            notes=part.notes or merged.notes,
            media=part.media or merged.media,
            model_cache=part.model_cache or merged.model_cache,
            repo_clone_root=part.repo_clone_root or merged.repo_clone_root,
            templates=part.templates or merged.templates,
        )
    return merged


def _pick_root(cli_root: Path | None, env_root: str | None, cwd: Path) -> Path | None:
    if cli_root is not None:
        return cli_root.expanduser().resolve()
    if env_root:
        return Path(env_root).expanduser().resolve()
    default_root = (cwd / "vb-workspace").resolve()
    return default_root if default_root.exists() else None


def _config_candidates(
    cli_config: Path | None,
    *,
    explicit_root: Path | None,
    cwd: Path,
    xdg_config_home: str | None,
) -> tuple[Path, ...]:
    candidates: list[Path] = []
    if xdg_config_home:
        candidates.append(
            Path(xdg_config_home).expanduser().resolve() / "video-buddy" / "config.toml"
        )
    roots: list[Path] = []
    if explicit_root is not None:
        roots.append(explicit_root)
    roots.extend([cwd, (cwd / "vb-workspace").resolve()])
    seen: set[Path] = set()
    for root in roots:
        candidate = root / ".video-buddy.toml"
        if candidate in seen:
            continue
        seen.add(candidate)
        candidates.append(candidate)
    if cli_config is not None:
        candidates.append(cli_config.expanduser().resolve())
    return tuple(candidates)


def _parse_workspace_config(
    path: Path, data: dict[str, Any]
) -> tuple[Path | None, WorkspaceOverrides]:
    workspace_data = data.get("workspace", {})
    config_dir = path.parent
    workspace_root = _optional_path(workspace_data.get("root"), base_dir=config_dir)
    overrides = WorkspaceOverrides(
        intermediates=_optional_path(
            workspace_data.get("intermediates"), base_dir=config_dir
        ),
        notes=_optional_path(workspace_data.get("notes"), base_dir=config_dir),
        media=_optional_path(workspace_data.get("media"), base_dir=config_dir),
        model_cache=_optional_path(
            workspace_data.get("model_cache"), base_dir=config_dir
        ),
        repo_clone_root=_optional_path(
            workspace_data.get("repo_clone_root"), base_dir=config_dir
        ),
        templates=_optional_path(workspace_data.get("templates"), base_dir=config_dir),
    )
    return workspace_root, overrides


def _app_from_sections(sections: dict[str, dict[str, Any]]) -> AppConfig:
    notes_data = sections["notes"]
    whisper_data = sections["whisper"]
    frames_data = sections["frames"]
    youtube_data = sections["youtube"]
    tools_data = sections["tools"]
    return AppConfig(
        notes=NotesConfig(
            group_by=str(notes_data.get("group_by") or "flat"),
            template=str(notes_data.get("template") or "default"),
        ),
        whisper=WhisperConfig(
            model=str(whisper_data.get("model") or "auto"),
            device=str(whisper_data.get("device") or "auto"),
            compute_type=str(whisper_data.get("compute_type") or "auto"),
            engine=str(whisper_data.get("engine") or "faster-whisper"),
        ),
        frames=FramesConfig(
            max_per_video=int(frames_data.get("max_per_video") or 15),
            scene_detection_max_duration_s=int(
                frames_data.get("scene_detection_max_duration_s") or 600
            ),
            ocr=str(frames_data.get("ocr") or "auto"),
        ),
        youtube=YoutubeConfig(
            cookies_from_browser=str(youtube_data.get("cookies_from_browser") or ""),
            caption_retry_max=int(youtube_data.get("caption_retry_max") or 3),
        ),
        tools=ToolsConfig(
            ffmpeg=str(tools_data.get("ffmpeg") or "ffmpeg"),
            node=str(tools_data.get("node") or "node"),
            git=str(tools_data.get("git") or "git"),
            tesseract=str(tools_data.get("tesseract") or "tesseract"),
        ),
    )


def _validate_config(path: Path, data: object) -> None:
    if not isinstance(data, dict):
        raise SystemExit(
            f"Invalid config in {path}: top-level document must be a table"
        )
    for section, value in data.items():
        if section not in _VALID_SECTION_KEYS:
            raise SystemExit(f"Unknown config section in {path}: {section}")
        if section == "compute":
            if not isinstance(value, list):
                raise SystemExit(
                    f"Invalid config section in {path}: compute must be an array of tables"
                )
            continue
        if not isinstance(value, dict):
            raise SystemExit(
                f"Invalid config section in {path}: {section} must be a table"
            )
        unknown_keys = sorted(set(value) - _VALID_SECTION_KEYS[section])
        if unknown_keys:
            joined = ", ".join(unknown_keys)
            raise SystemExit(f"Unknown config key in {path}: [{section}] {joined}")


def _optional_path(raw: object, *, base_dir: Path) -> Path | None:
    if raw is None:
        return None
    if not isinstance(raw, str):
        raise SystemExit(f"Invalid path value in config: {raw!r}")
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()
