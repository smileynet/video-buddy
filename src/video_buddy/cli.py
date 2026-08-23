from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .batch_digest import (
    _find_breakdown,
    compile_digest,
    fetch_digest_urls,
    load_urls,
    transcribe_manifest,
)
from .compute.registry import build_registry
from .concepts import process_concepts_file
from .config import CliWorkspaceArgs, ResolvedContext, resolve_context_from_sources
from .correlate.repo import correlate_video
from .fetch.article import fetch_article
from .fetch.youtube import extract_video_id, fetch_video
from .frames.capture import capture_video_frames, write_frames_metadata
from .frames.ocr import apply_ocr_to_metadata
from .models import (
    gpu_path_available,
    inspect_cache,
    install_selectors,
    parse_selector_args,
    remove_selectors,
)
from .render.finalize import finalize_note, upload_month
from .render.note import render_note
from .transcribe.pipeline import transcribe_video_json
from .workspace import annotated_config, workspace_gitignore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="video-buddy")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--json", action="store_true", help="Emit structured JSON to stdout."
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase stderr detail."
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    fetch_parser = subparsers.add_parser(
        "fetch", help="Fetch source metadata into the workspace."
    )
    fetch_parser.add_argument("url", help="Source URL.")
    _add_workspace_args(fetch_parser)
    fetch_parser.add_argument(
        "--cookies-from-browser",
        help="Browser profile name for authenticated YouTube fetches.",
    )
    fetch_parser.set_defaults(handler=_handle_fetch)

    transcribe_parser = subparsers.add_parser(
        "transcribe", help="Transcribe one or more fetched YouTube videos."
    )
    _add_workspace_args(transcribe_parser, include_backend=True)
    transcribe_parser.add_argument("video_ids", nargs="*", help="Fetched video ids.")
    transcribe_parser.add_argument(
        "--video-json", help="Transcribe a workspace-external video JSON file."
    )
    transcribe_parser.add_argument("--whisper-model", help="Override Whisper model.")
    transcribe_parser.add_argument(
        "--whisper-engine",
        choices=["faster-whisper", "whisperx", "crisperwhisper"],
        help="Transcription engine.",
    )
    transcribe_parser.add_argument(
        "--device", choices=["auto", "cpu", "cuda"], help="Execution device."
    )
    transcribe_parser.add_argument(
        "--compute-type",
        choices=["auto", "float16", "float32", "int8", "int8_float16"],
        help="Whisper compute type.",
    )
    transcribe_parser.set_defaults(handler=_handle_transcribe)

    frames_parser = subparsers.add_parser(
        "frames", help="Capture representative frames and optionally OCR them."
    )
    _add_workspace_args(frames_parser, include_backend=True)
    frames_parser.add_argument("video_ids", nargs="*", help="Fetched video ids.")
    frames_parser.add_argument(
        "--video-json", help="Capture frames from a workspace-external video JSON file."
    )
    frames_parser.add_argument(
        "--max-frames", type=int, help="Maximum number of selected frames."
    )
    frames_parser.add_argument("--ocr", choices=["auto", "off"], help="OCR mode.")
    frames_parser.add_argument(
        "--engine",
        choices=["easyocr", "tesseract"],
        help="Force a specific OCR engine.",
    )
    frames_parser.set_defaults(handler=_handle_frames)

    correlate_parser = subparsers.add_parser(
        "correlate", help="Match OCR frame text against referenced GitHub repositories."
    )
    _add_workspace_args(correlate_parser)
    correlate_parser.add_argument("video_ids", nargs="*", help="Fetched video ids.")
    correlate_parser.add_argument(
        "--video-json", help="Correlate from a workspace-external video JSON file."
    )
    correlate_parser.set_defaults(handler=_handle_correlate)

    render_parser = subparsers.add_parser(
        "render", help="Render a draft markdown note from fetched data."
    )
    _add_workspace_args(render_parser)
    render_parser.add_argument(
        "source_ids",
        nargs="*",
        help="Video ids or article source ids to render from workspace files.",
    )
    render_parser.add_argument(
        "--source-json", help="Render from a workspace-external source JSON file."
    )
    render_parser.add_argument(
        "--template",
        help="Template variant (`default`, `obsidian`) or a path to a custom template file.",
    )
    render_parser.set_defaults(handler=_handle_render)

    extract_parser = subparsers.add_parser(
        "extract-concepts",
        help="Create or update concept notes from agent-produced JSON.",
    )
    _add_workspace_args(extract_parser)
    extract_parser.add_argument(
        "source_ids",
        nargs="*",
        help="Video ids or source ids whose concepts JSON should be processed.",
    )
    extract_parser.add_argument("--source-json", help="Concept extraction JSON path.")
    extract_parser.set_defaults(handler=_handle_extract_concepts)

    finalize_parser = subparsers.add_parser(
        "finalize", help="Move rendered draft notes into the final notes directory."
    )
    _add_workspace_args(finalize_parser)
    finalize_parser.add_argument(
        "source_ids",
        nargs="*",
        help="Video ids or article source ids to finalize from workspace draft notes.",
    )
    finalize_parser.add_argument(
        "--source-json", help="Finalize from a workspace-external source JSON file."
    )
    finalize_parser.set_defaults(handler=_handle_finalize)

    ingest_parser = subparsers.add_parser(
        "ingest", help="Run the end-to-end ingest pipeline for a single URL."
    )
    ingest_parser.add_argument("url", help="Source URL.")
    _add_workspace_args(ingest_parser, include_backend=True)
    ingest_parser.add_argument(
        "--cookies-from-browser",
        help="Browser profile name for authenticated YouTube fetches.",
    )
    ingest_parser.add_argument("--whisper-model", help="Override Whisper model.")
    ingest_parser.add_argument(
        "--whisper-engine",
        choices=["faster-whisper", "whisperx", "crisperwhisper"],
        help="Transcription engine.",
    )
    ingest_parser.add_argument(
        "--device", choices=["auto", "cpu", "cuda"], help="Execution device."
    )
    ingest_parser.add_argument(
        "--compute-type",
        choices=["auto", "float16", "float32", "int8", "int8_float16"],
        help="Whisper compute type.",
    )
    ingest_parser.add_argument(
        "--max-frames", type=int, help="Maximum number of selected frames."
    )
    ingest_parser.add_argument("--ocr", choices=["auto", "off"], help="OCR mode.")
    ingest_parser.add_argument(
        "--engine",
        choices=["easyocr", "tesseract"],
        help="Force a specific OCR engine.",
    )
    ingest_parser.add_argument(
        "--template",
        help="Template variant (`default`, `obsidian`) or a path to a custom template file.",
    )
    ingest_parser.add_argument(
        "--no-frames", action="store_true", help="Skip frame capture and OCR."
    )
    ingest_parser.add_argument(
        "--no-whisper",
        action="store_true",
        help="Skip transcription if captions are missing.",
    )
    ingest_parser.set_defaults(handler=_handle_ingest)

    digest_parser = subparsers.add_parser(
        "digest", help="Batch digest workflow for YouTube URLs."
    )
    _add_workspace_args(digest_parser, include_backend=True)
    digest_subparsers = digest_parser.add_subparsers(
        dest="digest_command", metavar="DIGEST_COMMAND"
    )

    digest_fetch = digest_subparsers.add_parser(
        "fetch", help="Fetch a URL list into a digest manifest."
    )
    _add_workspace_args(digest_fetch, include_backend=True)
    digest_fetch.add_argument("input", help="URL list file path or - for stdin.")
    digest_fetch.add_argument(
        "--delay", type=float, default=0.0, help="Delay between fetches."
    )
    digest_fetch.add_argument(
        "--cookies-from-browser",
        help="Browser profile name for authenticated YouTube fetches.",
    )
    digest_fetch.set_defaults(handler=_handle_digest_fetch)

    digest_transcribe = digest_subparsers.add_parser(
        "transcribe", help="Transcribe captionless videos in a digest manifest."
    )
    _add_workspace_args(digest_transcribe, include_backend=True)
    digest_transcribe.add_argument("manifest", help="Digest manifest JSON path.")
    digest_transcribe.add_argument("--whisper-model", help="Override Whisper model.")
    digest_transcribe.add_argument(
        "--whisper-engine",
        choices=["faster-whisper", "whisperx", "crisperwhisper"],
        help="Transcription engine.",
    )
    digest_transcribe.add_argument(
        "--device", choices=["auto", "cpu", "cuda"], help="Execution device."
    )
    digest_transcribe.add_argument(
        "--compute-type",
        choices=["auto", "float16", "float32", "int8", "int8_float16"],
        help="Whisper compute type.",
    )
    digest_transcribe.set_defaults(handler=_handle_digest_transcribe)

    digest_compile = digest_subparsers.add_parser(
        "compile", help="Compile per-video summaries into a digest note."
    )
    _add_workspace_args(digest_compile)
    digest_compile.add_argument("manifest", help="Digest manifest JSON path.")
    digest_compile.add_argument(
        "--date", required=True, help="Digest date (YYYY-MM-DD)."
    )
    digest_compile.set_defaults(handler=_handle_digest_compile)

    digest_run = digest_subparsers.add_parser(
        "run", help="Run digest fetch and transcribe in one command."
    )
    _add_workspace_args(digest_run, include_backend=True)
    digest_run.add_argument("input", help="URL list file path or - for stdin.")
    digest_run.add_argument(
        "--delay", type=float, default=0.0, help="Delay between fetches."
    )
    digest_run.add_argument(
        "--cookies-from-browser",
        help="Browser profile name for authenticated YouTube fetches.",
    )
    digest_run.add_argument("--whisper-model", help="Override Whisper model.")
    digest_run.add_argument(
        "--whisper-engine",
        choices=["faster-whisper", "whisperx", "crisperwhisper"],
        help="Transcription engine.",
    )
    digest_run.add_argument(
        "--device", choices=["auto", "cpu", "cuda"], help="Execution device."
    )
    digest_run.add_argument(
        "--compute-type",
        choices=["auto", "float16", "float32", "int8", "int8_float16"],
        help="Whisper compute type.",
    )
    digest_run.set_defaults(handler=_handle_digest_run)

    init_parser = subparsers.add_parser(
        "init", help="Create a workspace skeleton and annotated config."
    )
    init_parser.add_argument(
        "dir", nargs="?", help="Workspace directory. Defaults to ./vb-workspace"
    )
    _add_workspace_args(init_parser)
    init_parser.add_argument(
        "--no-models",
        action="store_true",
        help="Skip model prefetch during initialization.",
    )
    init_parser.add_argument(
        "--models",
        nargs="+",
        help="Model selectors to install (comma-separated tokens accepted).",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Allow initialization into an existing non-empty directory.",
    )
    init_parser.set_defaults(handler=_handle_init)

    models_parser = subparsers.add_parser(
        "models", help="Inspect or manage cached models."
    )
    _add_workspace_args(models_parser)
    models_subparsers = models_parser.add_subparsers(
        dest="models_command", metavar="MODELS_COMMAND"
    )
    list_parser = models_subparsers.add_parser("list", help="Show cached model state.")
    list_parser.set_defaults(handler=_handle_models_list)
    install_parser = models_subparsers.add_parser(
        "install", help="Install model selectors into the cache."
    )
    install_parser.add_argument(
        "selectors",
        nargs="*",
        help="Bundle names or raw model names (comma-separated tokens accepted).",
    )
    install_parser.set_defaults(handler=_handle_models_install)
    remove_parser = models_subparsers.add_parser(
        "remove", help="Remove model selectors from the cache."
    )
    remove_parser.add_argument(
        "selectors",
        nargs="+",
        help="Bundle names or raw model names (comma-separated tokens accepted).",
    )
    remove_parser.set_defaults(handler=_handle_models_remove)

    backends_parser = subparsers.add_parser(
        "backends", help="List, probe, or deploy configured backends."
    )
    _add_workspace_args(backends_parser)
    backends_parser.set_defaults(handler=_handle_backends_list)
    backends_subparsers = backends_parser.add_subparsers(
        dest="backends_command", metavar="BACKENDS_COMMAND"
    )
    list_backends = backends_subparsers.add_parser(
        "list", help="List configured backend probe results."
    )
    list_backends.set_defaults(handler=_handle_backends_list)
    deploy_backends = backends_subparsers.add_parser(
        "deploy", help="Deploy worker scripts to an SSH backend."
    )
    deploy_backends.add_argument("name", help="Configured backend name.")
    deploy_backends.set_defaults(handler=_handle_backends_deploy)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help(sys.stderr)
        return 2
    try:
        return handler(args)
    except SystemExit as exc:
        if isinstance(exc.code, str):
            _emit_error(args, exc.code)
            return 1
        raise
    except Exception as exc:
        _emit_error(args, str(exc))
        return 1


def _handle_init(args: argparse.Namespace) -> int:
    _validate_workspace_args(args)
    context = _resolve_context(args)
    workspace = context.workspace
    _refuse_non_empty_root(workspace.root, force=args.force)
    workspace.ensure_layout()
    if not workspace.config_path().exists():
        workspace.config_path().write_text(
            annotated_config(workspace), encoding="utf-8"
        )
    if not workspace.workspace_gitignore_path().exists():
        workspace.workspace_gitignore_path().write_text(
            workspace_gitignore(), encoding="utf-8"
        )
    selectors = parse_selector_args(args.models)
    warnings: list[str] = []
    if not args.no_models:
        report = install_selectors(selectors, model_cache=workspace.model_cache)
        _print_install_report(report)
        note = _gpu_ocr_fallback_note(selectors)
        if note:
            warnings.append(note)
            _note(args, note)
    _emit_success(
        args,
        verb="init",
        scope=str(workspace.root),
        path=str(workspace.root),
        warnings=warnings,
    )
    return 0


def _handle_fetch(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    workspace = context.workspace
    workspace.ensure_layout()
    cookies = (
        args.cookies_from_browser or context.config.youtube.cookies_from_browser or None
    )
    payload, output_path = _fetch_to_workspace(workspace, args.url, cookies)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
    )
    _emit_success(
        args,
        verb="fetch",
        scope=str(payload.get("video_id") or payload.get("source_id") or args.url),
        path=str(output_path),
        extra={"written": [str(output_path)]},
    )
    return 0


def _handle_transcribe(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    outputs = []
    for video_id, video_json_path in _transcribe_targets(args, context.workspace):
        captions = _transcribe_path(args, context, video_json_path)
        output_path = context.workspace.transcript_json(video_id)
        output_path.write_text(
            json.dumps(captions, indent=2, sort_keys=True), encoding="utf-8"
        )
        outputs.append({"scope": video_id, "path": str(output_path)})
    _emit_outputs(args, verb="transcribe", outputs=outputs)
    return 0


def _handle_frames(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    cfg = context.config.frames
    tool_cfg = context.config.tools
    outputs = []
    backend = _resolve_backend(args, context)
    for video_id, video_json_path in _transcribe_targets(args, context.workspace):
        payload = json.loads(video_json_path.read_text(encoding="utf-8"))
        cookies = (
            payload.get("cookies_from_browser")
            or context.config.youtube.cookies_from_browser
            or None
        )
        metadata = capture_video_frames(
            video_id,
            media_dir=context.workspace.media_for(video_id),
            max_frames=args.max_frames
            if args.max_frames is not None
            else cfg.max_per_video,
            cookies_from_browser=cookies,
            ffmpeg_bin=tool_cfg.ffmpeg,
            scene_detection_max_duration_s=cfg.scene_detection_max_duration_s,
        )
        metadata = _apply_ocr(args, context, backend, video_id, metadata)
        metadata_path = context.workspace.frames_meta(video_id)
        write_frames_metadata(metadata_path, metadata)
        outputs.append({"scope": video_id, "path": str(metadata_path)})
    _emit_outputs(args, verb="frames", outputs=outputs)
    return 0


def _handle_correlate(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    outputs = []
    for video_id, video_json_path in _transcribe_targets(args, context.workspace):
        correlate_video(
            video_json_path,
            context.workspace.frames_meta(video_id),
            repo_clone_root=context.workspace.repo_clone_root,
        )
        outputs.append(
            {"scope": video_id, "path": str(context.workspace.frames_meta(video_id))}
        )
    _emit_outputs(args, verb="correlate", outputs=outputs)
    return 0


def _handle_render(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    template = _resolve_template_arg(args.template or context.config.notes.template)
    outputs = []
    for source_id, source_json_path in _render_targets(args, context.workspace):
        payload = _load_render_payload(source_id, source_json_path, context.workspace)
        note_path = context.workspace.draft_note(source_id)
        note_path.write_text(render_note(payload, template=template), encoding="utf-8")
        _write_companion_prompts(context.workspace, source_id, payload, note_path)
        outputs.append({"scope": source_id, "path": str(note_path)})
    _emit_outputs(args, verb="render", outputs=outputs)
    return 0


def _handle_extract_concepts(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    outputs = []
    if args.source_json:
        source_ids = [Path(args.source_json).stem.replace("concepts_", "")]
    else:
        source_ids = args.source_ids
    if not source_ids:
        raise SystemExit("Provide one or more source ids or --source-json.")
    for source_id in source_ids:
        concepts_json_path = (
            Path(args.source_json).expanduser().resolve()
            if args.source_json
            else context.workspace.concepts_json(source_id)
        )
        payload = _load_render_payload(
            source_id,
            _source_json_for_id(context.workspace, source_id),
            context.workspace,
        )
        title = str(payload.get("title") or source_id)
        slug = _draft_slug_from_path(context.workspace.draft_note(source_id))
        summary = process_concepts_file(
            concepts_json_path,
            concepts_dir=context.workspace.notes / "concepts",
            source_title=title,
            source_slug=slug,
        )
        result_path = context.workspace.concept_result_json(source_id)
        result_path.write_text(
            json.dumps(
                {
                    "created": list(summary.created),
                    "updated": list(summary.updated),
                    "tags": list(summary.tags),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        outputs.append({"scope": source_id, "path": str(result_path)})
    _emit_outputs(args, verb="extract-concepts", outputs=outputs)
    return 0


def _handle_finalize(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    outputs = []
    for source_id, source_json_path in _render_targets(args, context.workspace):
        payload = json.loads(source_json_path.read_text(encoding="utf-8"))
        month = (
            upload_month(payload)
            if context.config.notes.group_by == "upload_month"
            else None
        )
        destination = finalize_note(
            payload,
            context.workspace.draft_note(source_id),
            notes_root=context.workspace.notes,
            month=month,
        )
        outputs.append({"scope": source_id, "path": str(destination)})
    _emit_outputs(args, verb="finalize", outputs=outputs)
    return 0


def _handle_ingest(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    steps: list[dict[str, Any]] = []
    context.workspace.ensure_layout()
    payload, source_path = _fetch_to_workspace(
        context.workspace,
        args.url,
        args.cookies_from_browser
        or context.config.youtube.cookies_from_browser
        or None,
    )
    source_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
    )
    scope = str(payload.get("video_id") or payload.get("source_id") or args.url)
    steps.append({"verb": "fetch", "scope": scope, "path": str(source_path)})
    if "video_id" in payload:
        video_id = str(payload["video_id"])
        if not args.no_whisper:
            captions = _transcribe_path(args, context, source_path)
            transcript_path = context.workspace.transcript_json(video_id)
            transcript_path.write_text(
                json.dumps(captions, indent=2, sort_keys=True), encoding="utf-8"
            )
            steps.append(
                {"verb": "transcribe", "scope": video_id, "path": str(transcript_path)}
            )

        # Check for existing digest breakdown — enrichment path
        existing_breakdown = _find_breakdown(context.workspace, "", video_id)

        if not args.no_frames:
            metadata = capture_video_frames(
                video_id,
                media_dir=context.workspace.media_for(video_id),
                max_frames=args.max_frames
                if args.max_frames is not None
                else context.config.frames.max_per_video,
                cookies_from_browser=payload.get("cookies_from_browser")
                or context.config.youtube.cookies_from_browser
                or None,
                ffmpeg_bin=context.config.tools.ffmpeg,
                scene_detection_max_duration_s=context.config.frames.scene_detection_max_duration_s,
            )
            metadata = _apply_ocr(
                args, context, _resolve_backend(args, context), video_id, metadata
            )
            metadata_path = context.workspace.frames_meta(video_id)
            write_frames_metadata(metadata_path, metadata)
            steps.append(
                {"verb": "frames", "scope": video_id, "path": str(metadata_path)}
            )
            correlate_video(
                source_path,
                metadata_path,
                repo_clone_root=context.workspace.repo_clone_root,
            )
            steps.append(
                {"verb": "correlate", "scope": video_id, "path": str(metadata_path)}
            )

        if existing_breakdown:
            # Enrichment path: breakdown already exists, skip render/finalize
            payload_out = {
                "schema_version": "1.0",
                "verb": "ingest",
                "scope": scope,
                "path": str(existing_breakdown),
                "warnings": [],
                "steps": steps,
                "needs_agent_fill": True,
                "enrichment": True,
                "breakdown_path": str(existing_breakdown),
            }
            _emit_payload(args, payload_out)
            return 0

        render_payload = _load_render_payload(video_id, source_path, context.workspace)
        note_path = context.workspace.draft_note(video_id)
        note_path.write_text(
            render_note(
                render_payload,
                template=_resolve_template_arg(
                    args.template or context.config.notes.template
                ),
            ),
            encoding="utf-8",
        )
        _write_companion_prompts(context.workspace, video_id, render_payload, note_path)
        steps.append({"verb": "render", "scope": video_id, "path": str(note_path)})
    else:
        source_id = str(payload["source_id"])
        note_path = context.workspace.draft_note(source_id)
        note_path.write_text(
            render_note(
                payload,
                template=_resolve_template_arg(
                    args.template or context.config.notes.template
                ),
            ),
            encoding="utf-8",
        )
        _write_companion_prompts(context.workspace, source_id, payload, note_path)
        steps.append({"verb": "render", "scope": source_id, "path": str(note_path)})
    payload_out = {
        "schema_version": "1.0",
        "verb": "ingest",
        "scope": scope,
        "path": steps[-1]["path"],
        "warnings": [],
        "steps": steps,
        "needs_agent_fill": True,
    }
    _emit_payload(args, payload_out)
    return 0


def _handle_digest_fetch(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    urls = load_urls(args.input)
    manifest, manifest_path = fetch_digest_urls(
        urls,
        workspace=context.workspace,
        cookies_from_browser=args.cookies_from_browser
        or context.config.youtube.cookies_from_browser
        or None,
        delay=args.delay,
    )
    _emit_success(
        args,
        verb="digest.fetch",
        scope=str(manifest_path),
        path=str(manifest_path),
        extra={"counts": manifest["counts"]},
    )
    return 0


def _handle_digest_transcribe(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    manifest, manifest_path = transcribe_manifest(
        Path(args.manifest).expanduser().resolve(),
        workspace=context.workspace,
        transcribe_fn=lambda path: _transcribe_path(args, context, path),
    )
    _emit_success(
        args,
        verb="digest.transcribe",
        scope=str(manifest_path),
        path=str(manifest_path),
        extra={"counts": manifest.get("counts", {})},
    )
    return 0


def _handle_digest_compile(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    result, digest_path = compile_digest(
        Path(args.manifest).expanduser().resolve(),
        workspace=context.workspace,
        day=args.date,
    )
    _emit_success(
        args,
        verb="digest.compile",
        scope=args.date,
        path=str(digest_path),
        warnings=[f"missing summaries: {', '.join(result['missing_summaries'])}"]
        if result.get("missing_summaries")
        else [],
        extra=result,
    )
    return 0


def _handle_digest_run(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    urls = load_urls(args.input)
    manifest, manifest_path = fetch_digest_urls(
        urls,
        workspace=context.workspace,
        cookies_from_browser=args.cookies_from_browser
        or context.config.youtube.cookies_from_browser
        or None,
        delay=args.delay,
    )
    manifest, manifest_path = transcribe_manifest(
        manifest_path,
        workspace=context.workspace,
        transcribe_fn=lambda path: _transcribe_path(args, context, path),
    )
    _emit_success(
        args,
        verb="digest.run",
        scope=str(manifest_path),
        path=str(manifest_path),
        extra={"counts": manifest.get("counts", {})},
    )
    return 0


def _handle_models_list(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    report = inspect_cache(context.workspace.model_cache)
    _emit_payload(
        args,
        {
            "schema_version": "1.0",
            "verb": "models.list",
            "scope": str(context.workspace.model_cache),
            "path": str(context.workspace.model_cache),
            "warnings": [],
            "whisper_models": list(report.whisper_models),
            "easyocr_en_cached": report.easyocr_en_cached,
        },
    )
    return 0


def _handle_models_install(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    selectors = parse_selector_args(args.selectors)
    report = install_selectors(selectors, model_cache=context.workspace.model_cache)
    _print_install_report(report)
    warnings = [note for note in [_gpu_ocr_fallback_note(selectors)] if note]
    for note in warnings:
        _note(args, note)
    _emit_success(
        args,
        verb="models.install",
        scope=str(context.workspace.model_cache),
        path=str(context.workspace.model_cache),
        warnings=warnings,
    )
    return 0


def _handle_models_remove(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    report = remove_selectors(
        parse_selector_args(args.selectors) or [],
        model_cache=context.workspace.model_cache,
    )
    warnings = ["tesseract_requirement=manual"] if report.tesseract_required else []
    _emit_success(
        args,
        verb="models.remove",
        scope=str(context.workspace.model_cache),
        path=str(context.workspace.model_cache),
        warnings=warnings,
    )
    return 0


def _handle_backends_list(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    registry = build_registry(list(context.compute))
    probes = registry.all_probes()
    if args.json:
        _emit_payload(
            args,
            {
                "schema_version": "1.0",
                "verb": "backends.list",
                "scope": "backends",
                "path": "backends",
                "warnings": [],
                "backends": [
                    {
                        "name": probe.name,
                        "available": probe.available,
                        "reason": probe.reason,
                    }
                    for probe in probes
                ],
            },
        )
    else:
        for probe in probes:
            print(
                f"{probe.name}\t{'ready' if probe.available else 'unavailable'}\t{probe.reason}"
            )
    return 0


def _handle_backends_deploy(args: argparse.Namespace) -> int:
    context = _resolve_context(args)
    registry = build_registry(list(context.compute))
    backend = registry.get(args.name)
    if backend is None:
        raise SystemExit(f"Unknown backend: {args.name}")
    result = backend.deploy(workers_dir=_repo_root() / "workers")
    if args.json:
        _emit_payload(
            args,
            {
                "schema_version": "1.0",
                "verb": "backends.deploy",
                "scope": backend.name,
                "path": backend.name,
                "warnings": [],
                "available": result.available,
                "reason": result.reason,
            },
        )
    else:
        print(
            f"{backend.name}\t{'ready' if result.available else 'unavailable'}\t{result.reason}"
        )
    return 0


def _add_workspace_args(
    parser: argparse.ArgumentParser, *, include_backend: bool = False
) -> None:
    parser.add_argument("--workspace", help="Workspace root override.")
    parser.add_argument(
        "--config", help="Config file to load after default config layers."
    )
    parser.add_argument("--notes-dir", help="Override notes output directory.")
    parser.add_argument("--intermediates", help="Override intermediates directory.")
    parser.add_argument("--media-dir", help="Override media directory.")
    parser.add_argument("--model-cache", help="Override shared model cache directory.")
    parser.add_argument(
        "--repo-clone-root", help="Override repository clone cache directory."
    )
    parser.add_argument("--templates", help="Override template directory.")
    if include_backend:
        parser.add_argument("--backend", help="Force a specific backend name.")


def _resolve_context(args: argparse.Namespace) -> ResolvedContext:
    return resolve_context_from_sources(
        CliWorkspaceArgs(
            workspace=_path_or_none(
                getattr(args, "workspace", None) or getattr(args, "dir", None)
            ),
            config=_path_or_none(getattr(args, "config", None)),
            notes_dir=_path_or_none(getattr(args, "notes_dir", None)),
            intermediates=_path_or_none(getattr(args, "intermediates", None)),
            media_dir=_path_or_none(getattr(args, "media_dir", None)),
            model_cache=_path_or_none(getattr(args, "model_cache", None)),
            repo_clone_root=_path_or_none(getattr(args, "repo_clone_root", None)),
            templates=_path_or_none(getattr(args, "templates", None)),
        )
    )


def _fetch_to_workspace(workspace, url: str, cookies_from_browser: str | None):
    try:
        video_id = extract_video_id(url)
    except ValueError:
        payload = fetch_article(url=url)
        return payload, workspace.article_json(payload["source_id"])
    payload = fetch_video(url, cookies_from_browser=cookies_from_browser)
    return payload, workspace.video_json(video_id)


def _transcribe_targets(args: argparse.Namespace, workspace) -> list[tuple[str, Path]]:
    if getattr(args, "video_json", None):
        path = Path(args.video_json).expanduser().resolve()
        payload = json.loads(path.read_text(encoding="utf-8"))
        video_id = str(payload.get("video_id") or "").strip()
        if not video_id:
            raise SystemExit(f"video_json is missing video_id: {path}")
        return [(video_id, path)]
    if not getattr(args, "video_ids", None):
        raise SystemExit("Provide one or more video ids or --video-json.")
    return [(video_id, workspace.video_json(video_id)) for video_id in args.video_ids]


def _render_targets(args: argparse.Namespace, workspace) -> list[tuple[str, Path]]:
    if getattr(args, "source_json", None):
        path = Path(args.source_json).expanduser().resolve()
        payload = json.loads(path.read_text(encoding="utf-8"))
        source_id = str(
            payload.get("video_id") or payload.get("source_id") or ""
        ).strip()
        if not source_id:
            raise SystemExit(f"source_json is missing video_id/source_id: {path}")
        return [(source_id, path)]
    if not getattr(args, "source_ids", None):
        raise SystemExit("Provide one or more source ids or --source-json.")
    targets = []
    for source_id in args.source_ids:
        video_json = workspace.video_json(source_id)
        article_json = workspace.article_json(source_id)
        if video_json.exists():
            targets.append((source_id, video_json))
        elif article_json.exists():
            targets.append((source_id, article_json))
        else:
            raise SystemExit(f"No source JSON found for id: {source_id}")
    return targets


def _resolve_template_arg(template: str | None) -> str:
    template = template or "default"
    if template in {"default", "obsidian"}:
        return template
    path = Path(template).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Template file not found: {path}")
    return path.read_text(encoding="utf-8")


def _load_render_payload(source_id: str, source_json_path: Path, workspace) -> dict:
    payload = json.loads(source_json_path.read_text(encoding="utf-8"))
    if "video_id" in payload:
        transcript_path = workspace.transcript_json(source_id)
        if transcript_path.exists():
            from .transcribe.pipeline import read_transcript

            payload = {
                **payload,
                "captions": read_transcript(transcript_path),
            }
        frames_meta_path = workspace.frames_meta(source_id)
        if frames_meta_path.exists():
            frames_meta = json.loads(frames_meta_path.read_text(encoding="utf-8"))
            payload = {**payload, "frames": frames_meta.get("frames", [])}
    return payload


def _write_companion_prompts(
    workspace, source_id: str, payload: dict, note_path: Path
) -> None:
    prompts = {
        "summary": "Fill the Quick Summary section in the draft note with 2-3 concise sentences grounded only in the source material.",
        "concepts": "Fill the Key Concepts section in the draft note as a concise markdown bullet list of the core concepts and why they matter here.",
        "detailed-notes": "Fill the Detailed Notes section in the draft note with clear sectioned notes based only on the source material.",
        "timestamps": "Fill the Timestamps section in the draft note as a markdown bullet list of notable moments from the source material.",
    }
    title = str(
        payload.get("title")
        or payload.get("video_id")
        or payload.get("source_id")
        or ""
    )
    for kind, instruction in prompts.items():
        prompt_path = workspace.agent_prompt(source_id, kind)
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path.write_text(
            "\n".join(
                [
                    f"# Task: {kind}",
                    "",
                    instruction,
                    "",
                    f"Draft note path: {note_path}",
                    f"Title: {title}",
                    "",
                    "Write your result back into the draft note or companion JSON according to the contract.",
                ]
            ),
            encoding="utf-8",
        )


def _resolve_backend(args: argparse.Namespace, context: ResolvedContext):
    name = getattr(args, "backend", None)
    if not name or name == "local":
        return None
    registry = build_registry(list(context.compute))
    backend = registry.get(name)
    if backend is None:
        raise SystemExit(f"Unknown backend: {name}")
    probe = backend.probe()
    if not probe.available:
        raise SystemExit(f"Backend unavailable: {probe.reason}")
    return backend


def _transcribe_path(
    args: argparse.Namespace, context: ResolvedContext, video_json_path: Path
) -> list[dict] | dict:
    backend = _resolve_backend(args, context)
    engine = getattr(args, "whisper_engine", None) or context.config.whisper.engine
    model = args.whisper_model or _none_if_auto(context.config.whisper.model)
    device = args.device or context.config.whisper.device
    compute_type = args.compute_type or context.config.whisper.compute_type

    if engine == "whisperx" and backend is None:
        from .transcribe.pipeline import transcribe_video_json_whisperx

        return transcribe_video_json_whisperx(
            video_json_path,
            model_name=model,
            device=device,
            compute_type=compute_type,
            model_cache=context.workspace.model_cache,
        )

    if backend is None:
        return transcribe_video_json(
            video_json_path,
            model_name=model,
            device=device,
            compute_type=compute_type,
            model_cache=context.workspace.model_cache,
        )
    payload = json.loads(video_json_path.read_text(encoding="utf-8"))
    if payload.get("has_captions") and payload.get("captions"):
        return transcribe_video_json(
            video_json_path,
            model_name=model,
            device=device,
            compute_type=compute_type,
            model_cache=context.workspace.model_cache,
        )
    import tempfile
    from .transcribe.pipeline import (
        default_compute_type,
        default_model_name,
        detect_device,
        download_audio,
    )

    resolved_device = detect_device() if device == "auto" else device
    resolved_compute_type = (
        default_compute_type(resolved_device)
        if compute_type == "auto"
        else compute_type
    )
    resolved_model = model or default_model_name(resolved_device)
    with tempfile.TemporaryDirectory() as tmp_dir:
        audio_path = download_audio(
            f"https://www.youtube.com/watch?v={payload['video_id']}",
            Path(tmp_dir),
            cookies_from_browser=payload.get("cookies_from_browser") or None,
        )
        if engine == "crisperwhisper" and hasattr(backend, "run_crisperwhisper"):
            return backend.run_crisperwhisper(
                audio_path,
                model=resolved_model,
                device=resolved_device,
                compute_type=resolved_compute_type,
            )
        return backend.run_whisper(
            audio_path,
            model=resolved_model,
            device=resolved_device,
            compute_type=resolved_compute_type,
        )


def _apply_ocr(
    args: argparse.Namespace,
    context: ResolvedContext,
    backend,
    video_id: str,
    metadata: dict,
) -> dict:
    ocr_mode = args.ocr or context.config.frames.ocr
    if ocr_mode == "off":
        return metadata
    if backend is None:
        return apply_ocr_to_metadata(
            context.workspace.media_for(video_id),
            metadata,
            ocr_mode=ocr_mode,
            engine=args.engine,
            model_dir=context.workspace.model_cache / "easyocr",
            tesseract_cmd=context.config.tools.tesseract,
        )
    frame_names = [
        str(frame.get("filename"))
        for frame in metadata.get("frames", [])
        if isinstance(frame, dict) and frame.get("should_ocr") and frame.get("filename")
    ]
    if not frame_names:
        return metadata
    if args.engine == "tesseract":
        return apply_ocr_to_metadata(
            context.workspace.media_for(video_id),
            metadata,
            ocr_mode=ocr_mode,
            engine="tesseract",
            model_dir=context.workspace.model_cache / "easyocr",
            tesseract_cmd=context.config.tools.tesseract,
        )
    results = backend.run_easyocr(context.workspace.media_for(video_id), frame_names)
    for frame in metadata.get("frames", []):
        if not isinstance(frame, dict):
            continue
        result = results.get(str(frame.get("filename")))
        if not result:
            continue
        frame["ocr_text"] = str(result.get("text", "")).strip()
        frame["ocr_confidence"] = round(float(result.get("confidence", 0.0)), 3)
        frame["ocr_engine"] = f"{backend.name}:easyocr"
    return metadata


def _gpu_ocr_fallback_note(selectors: list[str] | None) -> str | None:
    if selectors is not None or gpu_path_available():
        return None
    return "EasyOCR unavailable; default model install skipped easyocr-en and OCR will fall back to remote EasyOCR or local Tesseract."


def _print_install_report(report) -> None:
    if report.whisper_models:
        print(f"installed_whisper={','.join(report.whisper_models)}", file=sys.stderr)
    if report.easyocr_en:
        print("installed_easyocr_en=yes", file=sys.stderr)
    if report.tesseract_required:
        print("tesseract_requirement=manual-install-system-binary", file=sys.stderr)


def _emit_outputs(
    args: argparse.Namespace, *, verb: str, outputs: list[dict[str, str]]
) -> None:
    if len(outputs) == 1:
        output = outputs[0]
        _emit_success(
            args,
            verb=verb,
            scope=output["scope"],
            path=output["path"],
            extra={"written": [output["path"]]},
        )
        return
    _emit_payload(
        args,
        {
            "schema_version": "1.0",
            "verb": verb,
            "scope": "batch",
            "path": outputs[0]["path"] if outputs else "",
            "warnings": [],
            "written": [item["path"] for item in outputs],
            "outputs": outputs,
        },
    )


def _emit_success(
    args: argparse.Namespace,
    *,
    verb: str,
    scope: str,
    path: str,
    warnings: list[str] | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "verb": verb,
        "scope": scope,
        "path": path,
        "warnings": warnings or [],
    }
    if extra:
        payload.update(extra)
    _emit_payload(args, payload)


def _emit_payload(args: argparse.Namespace, payload: dict[str, Any]) -> None:
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload.get("path") or payload.get("verb", "ok"))


def _emit_error(args: argparse.Namespace, message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    if getattr(args, "json", False):
        print(
            json.dumps(
                {"schema_version": "1.0", "error": message}, indent=2, sort_keys=True
            )
        )


def _note(args: argparse.Namespace, message: str) -> None:
    if getattr(args, "verbose", 0) > 0:
        print(message, file=sys.stderr)


def _validate_workspace_args(args: argparse.Namespace) -> None:
    if args.workspace and getattr(args, "dir", None):
        workspace = _path_or_none(args.workspace)
        positional = _path_or_none(args.dir)
        if workspace != positional:
            raise SystemExit(
                "Pass either init <dir> or --workspace <dir>, not both with different values."
            )


def _refuse_non_empty_root(root: Path, *, force: bool) -> None:
    if force:
        return
    if not root.exists():
        return
    if any(root.iterdir()):
        raise SystemExit(
            f"Refusing to initialize non-empty directory: {root}. Pass --force to continue."
        )


def _none_if_auto(value: str) -> str | None:
    return None if value == "auto" else value


def _path_or_none(value: str | None) -> Path | None:
    return None if value is None else Path(value).expanduser()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _draft_slug_from_path(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.stem.replace("note_", "")


def _source_json_for_id(workspace, source_id: str) -> Path:
    video_json = workspace.video_json(source_id)
    if video_json.exists():
        return video_json
    article_json = workspace.article_json(source_id)
    if article_json.exists():
        return article_json
    raise SystemExit(f"No source JSON found for id: {source_id}")
