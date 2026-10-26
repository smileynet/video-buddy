---
id: "39"
title: "Preserve caption origin and reference lineage in source artifacts"
status: open
blocked_by: ["28"]
spec: "apply-build"
priority: high
validation_criteria:
  - "Source-artifact fixtures distinguish publisher/manual, automatic, unknown and missing caption origins without inferring human review"
  - "Relevant fetch/schema compatibility tests and pre-commit pass"
tags: ["workflow-spikes"]
---

# Preserve caption origin and reference lineage in source artifacts

## Intent source and context

Discovered during user-requested ticket15 continuation2026-10-25. Read `docs/architecture/spikes/s4-reference-provenance.md` and `src/video_buddy/fetch/youtube.py::fetch_captions`. The function explicitly prefers manual English tracks, then automatic tracks, but returns only caption list and boolean. The source JSON loses namespace, selected language/kind and reference lineage. Fresh metadata verified the original Traversy track is ASR, while MIT/CS50 select manual-classified tracks; manual classification is not proof of human review. MIT official/YouTube cue records match; CS50 decoded word sequences match.

## What to build

After review28 decides artifact contracts, preserve enough caption provenance that consumers can distinguish track origin from human-review status and avoid treating duplicate publisher copies as independent validation. Record selected source namespace, language, kind/automatic indicator, track identity/content hash and observation time where available, with unknown/missing states. Keep publisher origin, review attestations and model-generated text separate. Represent model-reviewed provisional references with reviewer model/checkpoint and human_verified:false; a machine review must never create a human attestation. Do not persist signed caption URLs or unrelated full metadata by default. Preserve compatibility with older artifacts lacking provenance.

## Acceptance criteria

- [ ] Fixtures cover manual-preferred, automatic fallback, missing/unknown origin and older source artifacts.
- [ ] Consumers cannot label a track human-reviewed solely because it is in the manual namespace.
- [ ] Source/reference content identity or declared lineage is available for duplicate-reference checks without asserting independence from formatting differences.
- [ ] Signed URLs/private metadata are excluded from durable artifacts by default.
- [ ] Relevant fetch/schema compatibility checks and pre-commit pass; docs describe observed versus asserted review status.

## Out of scope

Automatic human-review certification, new ASR defaults, promoting experimental scripts, or changing note/digest output without the review28 contract decision. This is a post-review implementation proposal, not a blocker cycle for28.

## Evidence pointer

`codex/spike-speech-details`, commit `18cae9f23631a136cfe2a54108ae29c238ab6461`, compact caption-provenance and publisher-caption-provenance JSON. This ticket remains proposed implementation after28; no fetch API or source schema changed in the spike.
