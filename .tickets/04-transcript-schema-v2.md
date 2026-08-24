---
id: "04"
title: "Extend transcript JSON schema for word-level timestamps and disfluency metadata"
status: in_progress
blocked_by: ["02"]
priority: high
---

# Extend transcript JSON schema for word-level timestamps and disfluency metadata

## Context

Our current transcript JSON is a flat array of `{start, duration, text}` segments (~5s granularity).
Word-level timestamps and verbatim metadata require extending this schema without breaking existing
consumers (the render, correlate, and agent-fill steps all read transcripts).

## What to build

1. Design schema v2 that extends (not replaces) the current format
2. Add optional `words` array per segment: `[{start, end, text, confidence, is_disfluency}]`
3. Add optional `metadata` object: `{engine, model, verbatim_mode, hallucination_count, duration_processed}`
4. Add optional `speakers` array when diarization is available
5. Maintain backward compatibility — existing code that reads `[{start, duration, text}]` still works
6. Update the `render` step to use word timestamps for finer transcript rendering when available

## Proposed Schema

```json
{
  "schema_version": "2.0",
  "metadata": {
    "engine": "whisperx|crisperwhisper|faster-whisper",
    "model": "large-v3-turbo",
    "verbatim_mode": false,
    "hallucination_count": 0,
    "processing_time_s": 45.2,
    "audio_duration_s": 600.0
  },
  "segments": [
    {
      "start": 0.0,
      "duration": 4.5,
      "text": "Hello and welcome to the video",
      "words": [
        {"start": 0.0, "end": 0.4, "text": "Hello", "confidence": 0.95},
        {"start": 0.5, "end": 0.7, "text": "and", "confidence": 0.98},
        {"start": 0.8, "end": 1.2, "text": "welcome", "confidence": 0.97}
      ],
      "speaker": "SPEAKER_00"
    }
  ],
  "speakers": [
    {"id": "SPEAKER_00", "label": null}
  ]
}
```

## Acceptance criteria

- [ ] Schema v2 documented in `docs/transcript-schema.md`
- [ ] Existing v1 transcripts (`[{start, duration, text}]`) still parse correctly
- [ ] New v2 transcripts include `schema_version`, `metadata`, and optional `words`/`speakers`
- [ ] `render` step produces finer timestamps when word data available
- [ ] `correlate` step can use word timestamps for tighter frame-transcript alignment
- [ ] Migration path: existing transcripts don't need reprocessing (v1 is valid v2 without optional fields)

## Validation criteria

- Round-trip test: write v2 JSON, read back, verify all fields preserved
- Backward compat test: v1 JSON still works in render/correlate/agent-fill
- At least one full pipeline run with v2 output (ingest → render → finalize)

## Implementation Notes (from research)

### Prior Art Survey
No industry standard exists, but common fields are consistent across:
- **Whisper native:** `segments[].words[].{word, start, end, probability}`
- **WhisperX:** `segments[].{speaker, words[].{word, start, end, speaker}}`
- **AssemblyAI:** milliseconds, `utterances[]`, letter-based speaker labels
- **Deepgram:** channel/alternative nesting, integer speaker IDs
- **STJ (v0.6.1):** MIT-licensed superset standard attempting unification

### Design Decisions
1. **Time unit:** Seconds as float (matches Whisper/WhisperX, easier math than ms)
2. **Word field name:** `text` not `word` (consistent with our segment format)
3. **Confidence:** 0.0-1.0 float (from token probability or alignment score)
4. **Speaker:** `SPEAKER_00` string labels (WhisperX convention, human-readable)
5. **Disfluency flag:** `is_disfluency: bool` per word (CrisperWhisper-specific)
6. **Backward compat:** v1 format (`[{start, duration, text}]`) detected by absence of
   `schema_version` key — treat as v1, wrap in segments array internally

### Schema Evolution Strategy
- v1: flat array (current) — no version field
- v2: object with `schema_version`, `metadata`, `segments` — auto-detected by type (object vs array)
- Reader checks: `isinstance(data, list)` → v1; `isinstance(data, dict)` → v2
- Never break v1 readers — all existing code continues to work on the `segments` array
