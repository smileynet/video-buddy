from __future__ import annotations

from pathlib import Path

from video_buddy.workspace import (
    Workspace,
    WorkspaceOverrides,
    annotated_config,
    workspace_gitignore,
)


def test_workspace_resolve_uses_expected_defaults(tmp_path: Path) -> None:
    workspace = Workspace.resolve(cwd=tmp_path, xdg_cache_home=tmp_path / "cache")

    assert workspace.root == (tmp_path / "vb-workspace").resolve()
    assert workspace.intermediates == (workspace.root / "intermediates").resolve()
    assert workspace.notes == (workspace.root / "notes").resolve()
    assert workspace.media == (workspace.notes / "media").resolve()
    assert (
        workspace.video_json("abc123def45")
        == workspace.intermediates / "video_abc123def45.json"
    )
    assert (
        workspace.article_json("web-abc123def456")
        == workspace.intermediates / "article_web-abc123def456.json"
    )
    assert (
        workspace.model_cache
        == (tmp_path / "cache" / "video-buddy" / "models").resolve()
    )
    assert (
        workspace.repo_clone_root
        == (tmp_path / "cache" / "video-buddy" / "repos").resolve()
    )


def test_workspace_resolve_honors_overrides(tmp_path: Path) -> None:
    root = tmp_path / "custom-root"
    overrides = WorkspaceOverrides(
        notes=tmp_path / "notes-out",
        media=tmp_path / "media-out",
        model_cache=tmp_path / "models-out",
        repo_clone_root=tmp_path / "repos-out",
        templates=tmp_path / "templates-out",
    )

    workspace = Workspace.resolve(
        root=root, overrides=overrides, cwd=tmp_path, xdg_cache_home=tmp_path / "cache"
    )

    assert workspace.root == root.resolve()
    assert workspace.notes == (tmp_path / "notes-out").resolve()
    assert workspace.media == (tmp_path / "media-out").resolve()
    assert workspace.model_cache == (tmp_path / "models-out").resolve()
    assert workspace.repo_clone_root == (tmp_path / "repos-out").resolve()
    assert workspace.templates == (tmp_path / "templates-out").resolve()


def test_annotated_config_includes_resolved_paths(tmp_path: Path) -> None:
    workspace = Workspace.resolve(cwd=tmp_path, xdg_cache_home=tmp_path / "cache")

    content = annotated_config(workspace)

    assert f'# root = "{workspace.root}"' in content
    assert '# harness = "claude-code"' in content
    assert '# type = "ssh"' in content


def test_workspace_gitignore_covers_generated_artifacts() -> None:
    content = workspace_gitignore()

    assert "intermediates/" in content
    assert ".env" in content
