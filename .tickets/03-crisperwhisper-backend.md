---
id: "03"
title: "Add CrisperWhisper isolated backend for verbatim + hallucination detection"
status: open
blocked_by: ["02"]
priority: high
---

# Add CrisperWhisper isolated backend for verbatim + hallucination detection

## Context

CrisperWhisper requires an isolated venv due to its forked ctranslate2 package conflicting with
faster-whisper. It offers unique capabilities: verbatim transcription (87.8% disfluency F1 vs
Whisper's 12%), 3-tier hallucination detection, 30ms word-level timestamps, and dual-mode
transcription (verbatim + intended simultaneously).

Research findings (`.scratch/research/crisper-whisper.md`, `.scratch/research/verbatim-transcription.md`):
- `ctranslate2-crisperwhisper` occupies same namespace as upstream — MUST be isolated
- The subprocess/isolated-venv pattern matches our existing SSH remote backend approach
- `transcribe_dual()` gives both verbatim and cleaned versions in one pass
- `verbatimize()` can retrofit existing transcripts with actual disfluencies from audio

## What to build

1. Create isolated venv at `.venvs/crisperwhisper/` with `crisperwhisper[ct2]`
2. Create `src/video_buddy/crisperwhisper_backend.py` — subprocess-based adapter
3. Runner script at `scripts/crisperwhisper_worker.py` (runs inside isolated venv)
4. Worker accepts audio path + config via JSON stdin, outputs transcript JSON to stdout
5. When `engine = "crisperwhisper"` in config, spawns subprocess in isolated venv
6. Support verbatim mode, dual mode, and standard mode via config
7. Integrate hallucination detection (report hallucination count in metadata)

## Acceptance criteria

- [ ] `.venvs/crisperwhisper/` created with working CrisperWhisper installation
- [ ] `uv run video-buddy transcribe --engine crisperwhisper <video_id>` produces transcript
- [ ] Verbatim mode preserves fillers (uh, um) and false starts in output
- [ ] Dual mode produces both `verbatim_text` and `intended_text` fields
- [ ] Hallucination detection metadata present (count of detected/mitigated hallucinations)
- [ ] Word-level timestamps at ≤50ms granularity in output
- [ ] Subprocess isolation verified (no import conflicts in main venv)
- [ ] Existing faster-whisper pipeline unaffected

## Validation criteria

- Run on a 60+ min video — verify no hallucinated repeated segments
- Compare verbatim output against manual spot-check (5 segments with audible fillers)
- Verify word timestamps against frame correlation data on at least one video
- Processing speed measured and documented
