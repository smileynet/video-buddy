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
   - `path` is the draft note path (or breakdown path if enriching).
   - `steps` records the mechanical pipeline that already ran.
   - `needs_agent_fill = true` means the draft still needs prose.
   - `enrichment = true` means an existing digest breakdown was found; enrich it in-place.
3. **If enrichment is false (normal intake):**
   a. Read the draft note in `vb-workspace/intermediates/note_<id>.md`.
   b. Read the companion prompts in `vb-workspace/intermediates/agent-prompts/`.
   c. Fill these sections directly in the draft note:
      - Quick Summary
      - Key Concepts
      - Detailed Notes
      - Timestamps refinement when useful
   d. If you produced `vb-workspace/intermediates/concepts_<id>.json`, run `uv run video-buddy --json extract-concepts <id>`.
   e. Run `uv run video-buddy --json finalize <id>`.
   f. Return the final note path from the finalize payload.
4. **If enrichment is true (existing breakdown):**
   a. Read frame metadata from `vb-workspace/intermediates/frames_<id>/frames_meta.json`.
   b. Read the existing breakdown at `breakdown_path`.
   c. Replace the "Not yet processed" placeholder in Visual Notes with frame/OCR observations.
   d. Replace the "Not yet processed" placeholder in Source Code with correlation results.
   e. Return the breakdown path.

`ingest` already handles the mechanical branching:
- YouTube: fetch → transcribe → frames → correlate → render (or enrichment if breakdown exists)
- article/paper: fetch → render

## `/digest` end to end

User intent: turn a batch of YouTube URLs into a grouped digest with per-video breakdowns.

Linkage:
1. Run `uv run video-buddy --json digest run <urls.txt>` (or `digest fetch` + `digest transcribe` separately).
2. Read the manifest path from the JSON `path`.
3. For each manifest item:
   a. Check if a breakdown already exists at `vb-workspace/notes/digests/*/video_<id>.md`.
   b. If it exists: read its `## Summary` section and write to `vb-workspace/intermediates/summaries/video_<id>.md`.
   c. If new: read the transcript (from `vb-workspace/intermediates/transcript_<id>.json` or captions in `video_<id>.json`), write the breakdown to `vb-workspace/notes/digests/<date>/video_<id>.md`, and write the triage summary to `vb-workspace/intermediates/summaries/video_<id>.md`.
4. Run `uv run video-buddy --json digest compile <manifest.json> --date <YYYY-MM-DD>`.
5. Return the final digest path from the compile payload.

Post-digest actions (user-directed):
- **Enrich:** User says "enrich video X" or runs `/intake <url>`. Runs frames+correlate, agent edits breakdown in-place.
- **Cut:** User says "cut video X". Agent deletes the breakdown + transcript files and removes the entry from the digest note.

Digest is a transcript-based analysis workflow. Every video gets a full breakdown by default. The user cuts what's not worth keeping and optionally enriches select videos with visual processing.

## Agent-owned work

The CLI handles the mechanical pipeline. The agent owns:
- Quick Summary
- Key Concepts
- Detailed Notes
- per-video digest breakdowns (full analysis notes)
- per-video digest summaries (triage entries for the digest note)
- timestamp refinement when useful
- deciding whether OCR/correlation results are worth mentioning in the note
- editing breakdowns in-place during enrichment
- optional concept JSON generation when concept notes would help the user

## CLI contract

Use the CLI for all mechanical steps. Do not reimplement fetch, transcription, frame capture, correlation, rendering, concept file writes, or digest compilation in prompts.

Prefer `--json` so outputs stay machine-readable.

### Compute backends

Backend selection is config-driven via `[[compute]]` entries with `priority` and `capabilities`. Never hardcode machine names, Python paths, or priorities in source code. The system auto-selects the best available engine when `[whisper] engine = "auto"`.

Audio downloads produce webm format. Remote workers must convert to wav for engines that require it (CrisperWhisper worker handles this with ffmpeg).

YouTube download failures (HTTP 403) usually mean yt-dlp needs updating — YouTube periodically breaks older player client APIs.

Use these workspace paths, never invented ones:
- source JSON: `vb-workspace/intermediates/video_<id>.json` or `article_<source_id>.json`
- transcript JSON: `vb-workspace/intermediates/transcript_<id>.json`
- frames metadata: `vb-workspace/intermediates/frames_<id>/frames_meta.json`
- draft note: `vb-workspace/intermediates/note_<id>.md`
- companion prompts: `vb-workspace/intermediates/agent-prompts/`
- digest summaries: `vb-workspace/intermediates/summaries/video_<id>.md`
- digest breakdowns: `vb-workspace/notes/digests/<date>/video_<id>.md`
- digest transcripts: `vb-workspace/notes/digests/<date>/transcript_<id>.md`
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
- CrisperWhisper via configured SSH backends (requires `crisperwhisper` capability)

## Verification

When code or docs change, run the relevant tests you touched and `pre-commit` on changed files.

When validating the user workflow, prefer a real end-to-end `/intake` or `/digest` style run over isolated unit checks.
