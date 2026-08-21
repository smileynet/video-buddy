---
id: "02"
title: "Add WhisperX backend for word-level timestamps + diarization"
status: done
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

- [x] `uv sync --extra whisperx` installs whisperx without breaking existing deps
- [x] `uv run video-buddy transcribe --engine whisperx <video_id>` produces transcript with word-level timestamps
- [x] Word timestamps are present in output JSON (schema per ticket 04)
- [x] Diarization works when configured (speaker labels in output)
- [x] Fallback to faster-whisper works when whisperx not installed
- [x] Existing tests still pass (no regression)

## Validation criteria

- Transcript output includes `words` array with `start`, `end`, `text`, `confidence` per word
- Processing time within 2x of raw faster-whisper on same hardware
- At least one test video transcribed with word timestamps verified manually (spot-check 10 words)

## Implementation Notes (from research)

### API Pattern (3-step with memory management)
```python
model = whisperx.load_model("large-v2", device, compute_type=compute_type)
result = model.transcribe(audio, batch_size=batch_size)
del model; gc.collect(); torch.cuda.empty_cache()

model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device)
del model_a; gc.collect(); torch.cuda.empty_cache()

# Optional diarization (requires HF_TOKEN)
diarize_model = DiarizationPipeline(token=HF_TOKEN, device=device)
diarize_segments = diarize_model(audio)
result = whisperx.assign_word_speakers(diarize_segments, result)
```

### Known Gotchas
- PyTorch 2.6+ breaks torch.load — needs `weights_only=False` patch
- `huggingface_hub` renamed `use_auth_token` → `token`
- faster-whisper has memory leak in long-running processes (restart between large batches)
- `batch_size` must be tuned to VRAM (16 for 8GB, 8 for 6GB)
- Must explicitly `del model` + `gc.collect()` between pipeline stages
- Diarization requires accepting gated model licenses on HuggingFace (pyannote/speaker-diarization-3.1)

### Output maps to our schema v2 as:
- `result["segments"][i]["words"]` → `segments[i].words` (add confidence from alignment metadata)
- `result["segments"][i]["speaker"]` → `segments[i].speaker`
- Word format: `{word, start, end, speaker}` → remap to `{text, start, end, confidence, speaker}`

## Resolution (2026-08-21)

WhisperX engine integrated as optional backend. transcribe_video_json_whisperx() runs 3-step pipeline (transcribe→align→format) with memory management. Output is v2 schema with word-level timestamps. Graceful fallback to faster-whisper when not installed. CLI flag: --whisper-engine whisperx. Config: [whisper] engine = whisperx.
