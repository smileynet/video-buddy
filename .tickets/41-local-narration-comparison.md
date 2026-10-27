---
id: "41"
title: "Compare Qwen3-TTS and Chatterbox-Turbo for paragraph narration"
status: done
blocked_by: []
tags: ["workflow-spikes"]
validation_criteria:
  - "Frozen shared narration text/reference and exact model/configuration are recorded"
  - "Both candidates have executed outputs or explicit reproducible setup/runtime failures, with speed and resource evidence"
  - "A durable comparison separates measured checks, model/human listening and per-job disposition; guide/dashboard reflect the evidence"
---

# Compare Qwen3-TTS and Chatterbox-Turbo for paragraph narration

## What to build

Compare Qwen/Qwen3-TTS-12Hz-0.6B-Base and ResembleAI/chatterbox-turbo on identical English paragraphs from the narration guide and one shared official demonstration reference. Freeze text, reference hash/transcript, model revisions, seeds and evaluation plan before generation. Use separate isolated environments because upstream dependency pins differ. Record any GPU compatibility overrides explicitly.

Deciding question: which local candidate is a useful starting point for producing and revising this narration on available hardware, considering quality, setup burden, speed and resources? No production integration or universal winner. User authorized actual spike and guide/dashboard updates.

Run cold first generation and repeated warm cases under the same task, report first-use model load separately, generated duration/real-time factor, process RAM, GPU allocation and sampled total device use. Machine/ASR checks are distinct from blind audio-model review, reader self-report and human listening; do not claim voice fidelity or preference from transcription alone. Preserve generated WAVs for listening and compact replay evidence on an experimental branch. Credentials stay private; no paid generation. Local-only behavior is not established merely by local loading.

Experiment branch: codex/spike-local-narration. Environment start: local Windows RTX5070 12GB with approximately6.5GB free, Python3.12 isolated caches; no production dependencies changed. Model setup/runtime evidence pending. Shared reference is the Qwen official English demo, not the video creator's voice or the user's voice. Task text is extracted verbatim from the sample guide's outcome/mechanism paragraphs.

## Acceptance criteria

- [x] Shared inputs and protocol frozen before inference.
- [x] Both options have reproducible observed results or explicit unresolved failures.
- [x] Quality evidence and its reviewer/automation limitations are explicit.
- [x] Setup effort, speed, resource use and failures are documented; guide/dashboard/tickets updated.

## Resolution (2026-10-27)

Completed bounded English local narration comparison. Chatterbox warm generation 3.17-3.45s versus Qwen19.30-26.37s, with higher measured process RAM4.66 versus2.35GiB and longer initialization. Retain Qwen lower-memory/multilingual candidate; conditional Chatterbox English speed preference requires listening acceptance. Quality is machine text/waveform diagnostics and retained audio, not adjudicated human preference. Guide/dashboard updated; reader acceptance stays18/21 and integration28; no app default changed.

### Verification
1. ✓ Frozen shared narration text/reference and exact model/configuration are recorded — "Frozen shared protocol/reference and runner e5004d9; pinned Qwen/Chatterbox checkpoints, actual separate requirements and seeds retained."
2. ✓ Both candidates have executed outputs or explicit reproducible setup/runtime failures, with speed and resource evidence — "Both candidates completed four cases; raw results measure load, conditioning, generation, sampled RSS/device totals and allocator peaks. Eight lossless listening files verified against PCM hashes."
3. ✓ A durable comparison separates measured checks, model/human listening and per-job disposition; guide/dashboard reflect the evidence — "docs/architecture/spikes/local-narration-results.md and dashboard/guide record conditional speed/RAM disposition, setup override, ASR 0 versus 1 edits/136 word presentations, and no human quality winner; raw45e5ba848975958bce74c0f13624e1a112d92960."
