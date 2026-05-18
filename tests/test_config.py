from __future__ import annotations

from pathlib import Path

import pytest

from video_buddy.config import (
    CliWorkspaceArgs,
    resolve_context_from_sources,
    resolve_workspace_from_sources,
)


def test_resolve_workspace_uses_env_when_no_cli_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "env-root"
    monkeypatch.setenv("VIDEO_BUDDY_WORKSPACE", str(root))

    workspace = resolve_workspace_from_sources(
        CliWorkspaceArgs(),
        cwd=tmp_path,
        env={"VIDEO_BUDDY_WORKSPACE": str(root)},
        xdg_cache_home=tmp_path / "cache",
    )

    assert workspace.root == root.resolve()


def test_resolve_workspace_prefers_cli_over_env(
    tmp_path: Path,
) -> None:
    cli_root = tmp_path / "cli-root"
    env_root = tmp_path / "env-root"

    workspace = resolve_workspace_from_sources(
        CliWorkspaceArgs(workspace=cli_root),
        cwd=tmp_path,
        env={"VIDEO_BUDDY_WORKSPACE": str(env_root)},
        xdg_cache_home=tmp_path / "cache",
    )

    assert workspace.root == cli_root.resolve()


def test_resolve_workspace_reads_config_overrides(tmp_path: Path) -> None:
    config_path = tmp_path / "video-buddy.toml"
    config_path.write_text(
        """
[workspace]
root = "configured-root"
notes = "notes-out"
media = "media-out"
model_cache = "models-out"
repo_clone_root = "repos-out"
""".strip(),
        encoding="utf-8",
    )

    workspace = resolve_workspace_from_sources(
        CliWorkspaceArgs(config=config_path),
        cwd=tmp_path,
        env={},
        xdg_cache_home=tmp_path / "cache",
    )

    assert workspace.root == (tmp_path / "configured-root").resolve()
    assert workspace.notes == (tmp_path / "notes-out").resolve()
    assert workspace.media == (tmp_path / "media-out").resolve()
    assert workspace.model_cache == (tmp_path / "models-out").resolve()
    assert workspace.repo_clone_root == (tmp_path / "repos-out").resolve()


def test_resolve_workspace_uses_cwd_local_config(tmp_path: Path) -> None:
    config_path = tmp_path / ".video-buddy.toml"
    config_path.write_text('[workspace]\nroot = "cwd-root"\n', encoding="utf-8")

    workspace = resolve_workspace_from_sources(
        CliWorkspaceArgs(),
        cwd=tmp_path,
        env={},
        xdg_cache_home=tmp_path / "cache",
    )

    assert workspace.root == (tmp_path / "cwd-root").resolve()


def test_resolve_workspace_uses_xdg_cache_home_env(tmp_path: Path) -> None:
    workspace = resolve_workspace_from_sources(
        CliWorkspaceArgs(workspace=tmp_path / "root"),
        cwd=tmp_path,
        env={"XDG_CACHE_HOME": str(tmp_path / "xdg-cache")},
    )

    assert (
        workspace.model_cache
        == (tmp_path / "xdg-cache" / "video-buddy" / "models").resolve()
    )


def test_resolve_workspace_rejects_unknown_config_key(tmp_path: Path) -> None:
    config_path = tmp_path / "video-buddy.toml"
    config_path.write_text(
        """
[workspace]
unknown = "boom"
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(SystemExit, match="Unknown config key"):
        resolve_workspace_from_sources(
            CliWorkspaceArgs(config=config_path),
            cwd=tmp_path,
            env={},
            xdg_cache_home=tmp_path / "cache",
        )


def test_resolve_workspace_rejects_invalid_toml(tmp_path: Path) -> None:
    config_path = tmp_path / "video-buddy.toml"
    config_path.write_text("[workspace\nroot = 'oops'", encoding="utf-8")

    with pytest.raises(SystemExit, match="Invalid TOML"):
        resolve_workspace_from_sources(
            CliWorkspaceArgs(config=config_path),
            cwd=tmp_path,
            env={},
            xdg_cache_home=tmp_path / "cache",
        )


def test_resolve_context_layers_xdg_then_workspace(tmp_path: Path) -> None:
    xdg_config = tmp_path / "xdg" / "video-buddy"
    xdg_config.mkdir(parents=True)
    (xdg_config / "config.toml").write_text(
        """
[notes]
template = "obsidian"
[whisper]
model = "small"
""".strip(),
        encoding="utf-8",
    )
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    (workspace_root / ".video-buddy.toml").write_text(
        """
[notes]
template = "default"
[frames]
max_per_video = 9
""".strip(),
        encoding="utf-8",
    )

    context = resolve_context_from_sources(
        CliWorkspaceArgs(workspace=workspace_root),
        cwd=tmp_path,
        env={"XDG_CONFIG_HOME": str(tmp_path / "xdg")},
        xdg_cache_home=tmp_path / "cache",
    )

    assert context.config.notes.template == "default"
    assert context.config.whisper.model == "small"
    assert context.config.frames.max_per_video == 9
