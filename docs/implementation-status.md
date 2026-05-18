# Implementation status and remaining work

_Last updated: 2026-05-17_

This document is the implementation-facing companion to `SPEC.md`. `SPEC.md` captures the full intended architecture; this file tracks what is already functional and what still needs to land before video-buddy can be treated as broadly shareable.

## Implemented now

### Workspace and config
- workspace creation via `init`
- layered config resolution:
  1. built-in defaults
  2. XDG config
  3. workspace config
  4. explicit `--config`
  5. CLI path overrides
- implemented config consumption for `[workspace]`, `[notes]`, `[whisper]`, `[frames]`, `[youtube]`, `[tools]`

### Model management
- bundle resolution and hardware-aware defaults
- `models list`
- `models install`
- `models remove`
- Whisper cache and EasyOCR cache paths wired into runtime use

### Fetch / transcribe / frames / correlate / render / finalize
- YouTube fetch
- article/paper fetch
- local transcribe
- local frames capture
- local OCR (`easyocr` / `tesseract` / `off`)
- basic GitHub correlation
- draft note rendering
- finalize into `notes/`

### Agent contract
- `--json` on implemented verbs
- companion prompt files under `intermediates/agent-prompts/`
- example Claude Code skill + `/intake` command

## Remaining work

### High priority before broader sharing
1. Validate the article/paper flow manually on a real public source, not just tests.
2. Add the remaining reference Claude Code artifacts if we want to advertise more than `/intake`.
3. Expand `docs/output-schemas.md` when new payload fields or richer error objects are added.
### Important but can follow first sharing
1. richer repo correlation heuristics than the current filename-and-identifier matching
2. richer JSON warning/error payloads per failure class
3. more Claude Code reference artifacts (`/digest`, `/batch-intake`) if we want to advertise those workflows explicitly

### Deferred architectural work
1. generalized ComputeBackend registry for all stages, beyond the current local/SSH transcribe and OCR execution paths
2. worker environment bootstrapping beyond file deployment
3. backend probing/status expansion (for example capability-specific diagnostics and non-SSH backends)

## Acceptance bar for “functionally shareable”
A fresh user should be able to:
1. clone the repo
2. install documented dependencies
3. run `video-buddy init`
4. process one public YouTube URL end-to-end
5. receive a finalized markdown note with transcript and frames
6. understand optional GPU/OCR features from the docs alone
Current status:
- YouTube path manually smoke-validated on 2026-05-17 with `fetch → transcribe → frames --ocr off → correlate → render → finalize` for `dQw4w9WgXcQ`.
- Re-validated on a second public engineering talk URL on 2026-05-17: `VMemhtlsoNk`.
- For `VMemhtlsoNk`, the draft note was also filled through the agent-owned sections (`Quick Summary`, `Key Concepts`, `Detailed Notes`) and finalized again, validating the intended human/agent handoff surface in addition to the mechanical CLI path.
