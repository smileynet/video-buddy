---
id: "06"
title: "Auto-select CrisperWhisper when monolith is reachable"
status: in_progress
blocked_by: []
priority: high
---

# Auto-select best available transcription engine

## Context

CrisperWhisper on a GPU backend is 12x faster with zero hallucinations, but currently requires
explicit `--backend monolith --whisper-engine crisperwhisper`. The system should auto-select the
best available engine based on configured backends, priorities, and reachability.

No machine names are hardcoded. The selection uses the existing `[[compute]]` config entries
with their `priority` field and `capabilities` list.

## What to build

1. Change default engine from `"faster-whisper"` to `"auto"`
2. Add `find_capable(capability)` to `BackendRegistry` — returns highest-priority reachable backend
3. Cache probe results per-process (avoid 107× probing in batch)
4. In `_transcribe_path`: when engine=auto + no explicit backend, find best and use it
5. Explicit `--whisper-engine` or `--backend` flags override auto-selection

## Acceptance criteria

- [ ] `engine = "auto"` probes backends by priority and selects CrisperWhisper when available
- [ ] Falls back silently to faster-whisper when no CrisperWhisper backend reachable
- [ ] Explicit engine/backend flags override auto-selection
- [ ] Probe results cached per process (batch of N videos → 1 probe, not N)
- [ ] Existing tests pass

## Validation criteria

- With backend online: transcribe uses CrisperWhisper (verify output metadata)
- With backend offline: falls back to faster-whisper without error (≤8s delay)
- Batch: 4+ videos in one command → only 1 probe occurs
