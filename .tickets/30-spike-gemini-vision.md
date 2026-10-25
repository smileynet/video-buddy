---
id: "30"
title: "Compare Gemini region grounding and temporal evidence"
status: open
blocked_by: ["29"]
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/spikes/provider-gemini-results.md records pinned identities, evidence and per-job disposition or a concrete unresolved limitation"
  - "tkt validate exits 0"
---

# Compare Gemini region grounding and temporal evidence

## Context and intent

User request 2026-10-25: expand current-provider research, compare the gaps before final integration, and expose coverage on the dashboard. Read docs/agents/research/open-questions.md, docs/architecture/spikes/image-model-results.md, docs/architecture/spikes/s3-ocr-results.md and docs/plan.md. Primary job: apply/build and verify the result. Original evidence at codex/spike-image-models fd948102 and codex/spike-real-video-ocr 4df4a8d. Do not silently label all provider models tested.

## What to build

Compare the current eligible Gemini image-region/segmentation and video contracts against existing OCR/grounding and ordered-frame baselines. Use frozen public UI, code, diagram and negative-object fixtures; assess actual box/mask geometry, literal writing, unsupported labels and action order separately. Pin explicit API model version and response schema; record sampled times, request settings, cost and latency. Missing environment credentials means no call, not poor quality.

**Budget:** one active day per provider family, setup/download separately recorded. Freeze prompts/fixture hashes and intended outputs before inference. Report the smallest supported role; do not tune on held-out windows or compare unmatched modalities as equal. Evidence branch codex/spike-provider-coverage; production integration remains ticket28.

## Acceptance criteria

- [ ] Record current explicit model/checkpoint/API identity and eligibility evidence, with dated primary citations.
- [ ] Preserve frozen inputs, raw predictions, configuration, costs and runtime failures for every executed comparison.
- [ ] Distinguish measured fit from untested, access-limited, hardware-limited and irrelevant options.
- [ ] Give a per-job disposition and the remaining deciding observation; update dashboard coverage.

## Out of scope

Automatic production integration, blanket provider endorsement, fetching private media or exposing credentials.

## Current execution evidence (2026-10-25)

Current session has no exposed matching Google/Gemini credential. No API call or auth rejection observed; account/model availability and private config remain unverified. User asked for config location, never a pasted key. See docs/architecture/spikes/provider-gemini-results.md. Keep open pending access or explicit reviewed deferral.
