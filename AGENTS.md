# Agent Instructions

## Primary workflow

This repo is intended to be used through an agent. The human gives you a source or a batch, and you drive the CLI.

Before either workflow:
1. Ensure the Python environment exists (`uv sync`, with `--extra gpu-ocr` when available and useful).
2. Ensure the workspace exists. If `./vb-workspace/` is missing, run `uv run video-buddy init`.

## `/intake` end to end

User intent: turn one URL into one finished note.

Preferred linkage:
1. Run `uv run video-buddy --json ingest <url>`.
2. Read the JSON result:
   - `path` is the draft note path.
   - `steps` records the mechanical pipeline that already ran.
   - `needs_agent_fill = true` means the draft still needs prose.
3. Read the draft note in `vb-workspace/intermediates/note_<id>.md`.
4. Read the companion prompts in `vb-workspace/intermediates/agent-prompts/`.
5. Fill these sections directly in the draft note:
   - Quick Summary
   - Key Concepts
   - Detailed Notes
   - Timestamps refinement when useful
6. If you produced `vb-workspace/intermediates/concepts_<id>.json`, run `uv run video-buddy --json extract-concepts <id>`.
7. Run `uv run video-buddy --json finalize <id>`.
8. Return the final note path from the finalize payload.

`ingest` already handles the mechanical branching:
- YouTube: fetch → transcribe → frames → correlate → render
- article/paper: fetch → render

## `/digest` end to end

User intent: turn a batch of YouTube URLs into one grouped digest note.

Linkage:
1. Run `uv run video-buddy --json digest fetch <urls.txt>`.
2. Read the manifest path from the JSON `path`.
3. Run `uv run video-buddy --json digest transcribe <manifest.json>`.
4. For each manifest item, read the fetched artifacts and write `vb-workspace/intermediates/summaries/video_<id>.md`.
5. Run `uv run video-buddy --json digest compile <manifest.json> --date <YYYY-MM-DD>`.
6. Return the final digest path from the compile payload.

Digest is a triage workflow. Do not expand it into full per-video notes unless the user asks.

## Agent-owned work

The CLI handles the mechanical pipeline. The agent owns:
- Quick Summary
- Key Concepts
- Detailed Notes
- per-video digest summaries
- timestamp refinement when useful
- deciding whether OCR/correlation results are worth mentioning in the note
- optional concept JSON generation when concept notes would help the user

## CLI contract

Use the CLI for all mechanical steps. Do not reimplement fetch, transcription, frame capture, correlation, rendering, concept file writes, or digest compilation in prompts.

Prefer `--json` so outputs stay machine-readable.

Use these workspace paths, never invented ones:
- source JSON: `vb-workspace/intermediates/video_<id>.json` or `article_<source_id>.json`
- transcript JSON: `vb-workspace/intermediates/transcript_<id>.json`
- frames metadata: `vb-workspace/intermediates/frames_<id>/frames_meta.json`
- draft note: `vb-workspace/intermediates/note_<id>.md`
- companion prompts: `vb-workspace/intermediates/agent-prompts/`
- digest summaries: `vb-workspace/intermediates/summaries/video_<id>.md`
- final notes: `vb-workspace/notes/`
- final digests: `vb-workspace/notes/digests/`

## Current command availability

Implemented now:
- `init`
- `models {list,install,remove}`
- `fetch`
- `transcribe`
- `frames`
- `correlate`
- `render`
- `extract-concepts`
- `finalize`
- `ingest`
- `digest {fetch,transcribe,compile,run}`
- `backends {list,deploy}`

Remote execution support exists for:
- Whisper via configured SSH backends
- EasyOCR via configured SSH backends

## Verification

When code or docs change, run the relevant tests you touched and `pre-commit` on changed files.

When validating the user workflow, prefer a real end-to-end `/intake` or `/digest` style run over isolated unit checks.
