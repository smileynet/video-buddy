# video-buddy

Turn YouTube videos, articles, and papers into finished Markdown notes through an agent-driven workflow.

video-buddy is for people who want to hand a source to an agent, let it run the ingest pipeline, and get back a usable note or digest without driving the scripts themselves.

## Quick start

Install the repo:

```bash
git clone https://github.com/smileynet/video-buddy.git
cd video-buddy
uv sync --extra gpu-ocr
```

Then use it through Claude Code:

1. Open this repository in Claude Code.
2. For one source, run `/intake <url>`.
3. For a backlog of YouTube links, run `/digest <urls.txt>`.
4. Let the agent do the rest.

The agent will create a workspace, run the pipeline, fill the note or digest content, and leave the finished output in `vb-workspace/notes/`.

If your Claude Code setup loads repo-local commands, this repo includes:
- `.claude/commands/intake.md`
- `.claude/commands/digest.md`

## What you get

For `/intake`, the finished note can include:
- a quick summary
- key concepts
- detailed notes
- transcript content
- representative frames
- OCR-derived observations
- repository references when the source points at code

For `/digest`, the finished output is a grouped digest note for a batch of YouTube videos.

## Requirements

Required:
- Python 3.10+
- `uv`
- `ffmpeg`
- `git`

Optional:
- `tesseract` for CPU OCR fallback
- `node` when using browser-cookie passthrough for restricted YouTube videos
- a CUDA-capable GPU if you want local GPU Whisper/EasyOCR performance

## How to work with the agent

Use the repo the way a normal user would:
- ask the agent to run `/intake <url>` for one source
- ask the agent to run `/digest <urls.txt>` for a batch
- review the finished note or digest in `vb-workspace/notes/`

You should not need to drive the pipeline step by step yourself.

## Claude Code setup

This repository includes agent-facing instructions in:
- `AGENTS.md`
- `.claude/commands/intake.md`
- `.claude/commands/digest.md`

Those files tell the agent how `/intake` and `/digest` map onto the CLI pipeline. The README is only the human-facing entry point.

## Need the lower-level details?

Most users should stay at the agent layer. If you are integrating another harness or driving the CLI directly, see:
- `AGENTS.md`
- `docs/output-schemas.md`
- `docs/implementation-status.md`
