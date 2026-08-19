---
id: "02"
title: "Add WhisperX backend for word-level timestamps + diarization"
status: open
blocked_by: []
priority: high
---

# Add WhisperX backend for word-level timestamps + diarization

## Context

WhisperX runs on top of faster-whisper (no ctranslate2 conflict) and adds word-level timestamps
via wav2vec2 forced alignment plus optional speaker diarization via pyannote-audio. This is the
low-risk quick win — word timestamps without environment isolation.

Research findings (`.scratch/research/whisper-ecosystem.md`, `.scratch/research/word-timestamp-approaches.md`):
- WhisperX achieves 93.2% word precision at 200ms collar on Switchboard
- Runs at ~70x realtime with faster-whisper underneath
- Speaker diarization built-in (useful for interview/podcast content)
- No venv conflict — installs alongside existing faster-whisper

## What to build

1. Add `whisperx` as an optional dependency (`--extra whisperx` or similar)
2. Create `src/video_buddy/whisperx_backend.py` adapter
3. When `engine = "whisperx"` in config, run WhisperX pipeline instead of raw faster-whisper
4. Produce word-level timestamps in the transcript JSON (see ticket 04 for schema)
5. Optionally run diarization when `diarize = true` in config (requires HuggingFace token)
6. Fall back gracefully to faster-whisper if whisperx not installed

## Acceptance criteria

- [ ] `uv sync --extra whisperx` installs whisperx without breaking existing deps
- [ ] `uv run video-buddy transcribe --engine whisperx <video_id>` produces transcript with word-level timestamps
- [ ] Word timestamps are present in output JSON (schema per ticket 04)
- [ ] Diarization works when configured (speaker labels in output)
- [ ] Fallback to faster-whisper works when whisperx not installed
- [ ] Existing tests still pass (no regression)

## Validation criteria

- Transcript output includes `words` array with `start`, `end`, `text`, `confidence` per word
- Processing time within 2x of raw faster-whisper on same hardware
- At least one test video transcribed with word timestamps verified manually (spot-check 10 words)
