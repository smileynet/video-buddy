---
id: "03"
title: "Add CrisperWhisper isolated backend for verbatim + hallucination detection"
status: open
blocked_by: ["02"]
priority: high
---

# Add CrisperWhisper as Default Transcription Engine (via monolith GPU)

## Context

**Spike results (2026-08-23) changed the architecture decision:**

| | faster-whisper (CPU) | CrisperWhisper (GPU, monolith) |
|---|---|---|
| 33 min audio | 5.6 min | **25 seconds** |
| RTF | 5.93x | **80x** |
| Hallucinations | 17 repeats | **0** |
| Word timestamps | No | **Yes (5154 words)** |
| Verbatim | No | **Yes** |

CrisperWhisper on monolith's RTX 3070 is 13x faster than faster-whisper on local CPU,
produces zero hallucinations, and provides word-level timestamps. It should be the
**default engine**, not an optional premium backend.

Monolith is already configured as a compute backend (`monolith-wifi.lan`, RTX 3070 8GB,
CUDA 12.4, CrisperWhisper 2.0.2 installed at `~/.venvs/crisperwhisper/`).

## What to build

1. Create `workers/crisperwhisper_worker.py` — remote worker (same contract as transcribe_worker.py)
2. Add `run_crisperwhisper()` method to `SshBackend` class
3. Update `_transcribe_path()` in cli.py to route to CrisperWhisper on SSH backend when available
4. Deploy worker to monolith
5. Make CrisperWhisper the default when monolith is available; fall back to faster-whisper when not

## Acceptance criteria

- [ ] `workers/crisperwhisper_worker.py` follows existing worker contract (args + --output file)
- [ ] `SshBackend.run_crisperwhisper()` method mirrors `run_whisper()` lifecycle
- [ ] `uv run video-buddy transcribe --backend monolith --whisper-engine crisperwhisper <id>` works
- [ ] Word-level timestamps present in v2 output JSON
- [ ] Verbatim mode preserves fillers and false starts
- [ ] Falls back to faster-whisper when monolith unavailable
- [ ] Existing tests pass (no regression)
- [ ] Worker deployed to monolith and probe passes

## Validation criteria

- Transcribe a 30+ min video via monolith in under 30 seconds
- Output contains word timestamps at sub-second granularity
- Zero hallucinated repeated segments in output
- End-to-end: ingest a video using CrisperWhisper → render note → verify timestamps in note
## Implementation Notes (from spike)

### Architecture: SSH Remote Worker (same as existing transcribe_worker.py)

No local subprocess isolation needed. CrisperWhisper runs on monolith via SSH,
same lifecycle as `run_whisper()`:

1. Upload audio to monolith temp dir
2. SSH execute: `~/.venvs/crisperwhisper/bin/python ~/video-buddy-worker/crisperwhisper_worker.py <audio> --output <path> --model turbo --mode verbatim`
3. Download result JSON
4. Cleanup remote temp dir

### Worker Script Contract (matches transcribe_worker.py)

```python
# workers/crisperwhisper_worker.py
# Args: audio_path --output <path> --model turbo --device auto --mode verbatim
# Output: v2 JSON to --output path
# Exit: 0 success, 1 failure (stderr for errors)
```

### Output Format (v2 schema with words)

```json
{
  "schema_version": "2.0",
  "metadata": {"engine": "crisperwhisper", "model": "turbo", "mode": "verbatim",
               "processing_time": 24.9, "audio_duration": 1990.0},
  "segments": [
    {"start": 0.34, "duration": 5.36, "text": "This is a sine wave...",
     "words": [{"start": 0.34, "end": 0.42, "text": "This"}, ...]}
  ]
}
```

### SshBackend.run_crisperwhisper()

```python
def run_crisperwhisper(self, audio_path: Path, *, model: str, device: str,
                       compute_type: str, mode: str = "verbatim") -> dict:
    # Same pattern as run_whisper() but:
    # - Uses ~/.venvs/crisperwhisper/bin/python instead of .venv/bin/python
    # - Calls crisperwhisper_worker.py instead of transcribe_worker.py
    # - Returns dict (v2) instead of list (v1)
    # - Adds --mode flag
```

### Engine Routing in _transcribe_path()

```python
if engine == "crisperwhisper" and backend is not None:
    result = backend.run_crisperwhisper(audio_path, model=model, device=device,
                                         compute_type=compute_type, mode=mode)
    return result  # v2 dict
elif engine == "crisperwhisper" and backend is None:
    # Local fallback: use isolated venv subprocess (if available)
    # OR fall back to faster-whisper with warning
```

### Monolith Setup (already done in spike)

- Host: `sam@monolith-wifi.lan`
- GPU: RTX 3070 8GB, CUDA 12.4
- Venv: `~/.venvs/crisperwhisper/` with crisperwhisper[ct2,convert] 2.0.2
- Worker dir: `~/video-buddy-worker/`
- Validated: 80x realtime on 33-min audio
