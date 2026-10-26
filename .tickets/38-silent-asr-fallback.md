---
id: "38"
title: "Prevent no-speech retries from publishing unsupported transcript text"
status: open
blocked_by: ["28"]
spec: "apply-build"
priority: high
validation_criteria:
  - "Regression fixtures reproduce digital-silence and tone-only outputs before the fix and verify the reviewed no-speech policy"
  - "Relevant transcription and worker tests plus pre-commit pass"
tags: ["workflow-spikes"]
---

# Prevent no-speech retries from publishing unsupported transcript text

## Intent source and context

Discovered while executing user-requested speech spike 15 on 2026-10-25. Read `docs/architecture/spikes/s4-speech-results.md`; raw `fallback-negatives.json` and frozen WAV bundles live on `codex/spike-speech-details`. Existing `workers/transcribe_worker.py::transcribe_audio` and `src/video_buddy/transcribe/pipeline.py::transcribe_audio` retry without VAD whenever the gated first pass is empty.

Real default-worker CLI runs on eight-second digital silence emitted “You” for base and turbo. Turbo emitted “Thank you.” from authored tones with a 29.98-second duration, beyond the input. Small was empty in both cases; that is no general immunity claim. The separate VAD-only word probe was empty for all models. No production fix is included in the spike. Frozen evidence/replay: `codex/spike-speech-details`, commit `b5030a893e465dd2d8aca532aa048b6d109e7e32`, `docs/architecture/spikes/speech-details/fallback-negatives.json`.

## What to build

After review 28 selects the no-speech/recovery contract, keep empty/no-speech evidence from becoming unsupported transcript instructions. Preserve genuine quiet/low-volume speech through an explicit, evidenced recovery policy rather than blindly retrying or suppressing all short text. Keep uncertain output and source provenance visible; reject impossible timestamp extents. Apply consistent policy to local and remote faster-whisper paths without assuming another engine has the same behavior.

## Acceptance criteria

- [ ] Reproduce default-worker unsupported output on frozen silence/tones and document model/settings variance.
- [ ] Verify no-speech results cannot silently become source-supported instructions under the reviewed policy.
- [ ] Retain legitimate quiet speech and disclose unqualified recovery cases; no blanket hallucination-immunity claim.
- [ ] Bound segment/word times to valid media extent with explicit failure/uncertainty behavior.
- [ ] Run relevant pipeline/worker regression checks and pre-commit; update user-facing recovery guidance.

## Out of scope

Automatically changing ASR defaults, promoting the spike worker flag, or claiming universal hallucination detection. Review 28 is a decision prerequisite, not blocked by this implementation ticket.
