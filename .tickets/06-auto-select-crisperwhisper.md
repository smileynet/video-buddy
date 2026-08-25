---
id: "06"
title: "Auto-select CrisperWhisper when monolith is reachable"
status: open
blocked_by: []
priority: high
---

# Auto-select CrisperWhisper when monolith is reachable

## Context

The benchmark proved CrisperWhisper on monolith GPU is 12x faster and produces zero
hallucinations. But currently it requires explicit flags: `--backend monolith --whisper-engine
crisperwhisper`. Users shouldn't have to remember this — the system should auto-select the
best available engine.

## What to build

1. On transcription, probe configured backends for `crisperwhisper` capability
2. If a backend with CrisperWhisper is available and engine is `"auto"`, use it
3. If not available (monolith offline), fall back to local faster-whisper silently
4. Config: `[whisper] engine = "auto"` (new default, replaces `"faster-whisper"`)
5. Explicit `--whisper-engine faster-whisper` still forces local execution

## Acceptance criteria

- [ ] `engine = "auto"` probes backends and selects CrisperWhisper when available
- [ ] Falls back silently to faster-whisper when no CrisperWhisper backend reachable
- [ ] Explicit engine flag overrides auto-selection
- [ ] No extra latency when monolith is unreachable (probe timeout ≤ 5s)
- [ ] Existing tests pass

## Validation criteria

- With monolith online: `uv run video-buddy transcribe <id>` uses CrisperWhisper (check output metadata)
- With monolith offline: same command falls back to faster-whisper without error
- Probe caching: second transcription in same session doesn't re-probe
