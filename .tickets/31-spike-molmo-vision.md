---
id: "31"
title: "Compare Ai2 pointing tracking and interface grounding"
status: in_progress
blocked_by: ["29"]
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/spikes/provider-ai2-results.md records pinned identities, evidence and per-job disposition or a concrete unresolved limitation"
  - "tkt validate exits 0"
---

# Compare Ai2 pointing tracking and interface grounding

## Context and intent

User request 2026-10-25: expand current-provider research, compare the gaps before final integration, and expose coverage on the dashboard. Read docs/agents/research/open-questions.md, docs/architecture/spikes/image-model-results.md, docs/architecture/spikes/s3-ocr-results.md and docs/plan.md. Primary job: apply/build and verify the result. Original evidence at codex/spike-image-models fd948102 and codex/spike-real-video-ocr 4df4a8d. Do not silently label all provider models tested.

## What to build

Compare a practical current Molmo2/MolmoPoint checkpoint for image pointing and video subject identity, plus GUI-specialist checkpoint only if runtime eligible. Separate general video QA, pointing-only and GUI models; do not infer masks from points. Reuse UI/diagram/object fixtures and the same temporal windows. Record coordinates, wrong subjects, abstention, track switches, critical state recovery and resource/setup cost. Explicitly record if checkpoint size cannot fit available configured compute; do not silently quantize a different variant.

**Budget:** one active day per provider family, setup/download separately recorded. Freeze prompts/fixture hashes and intended outputs before inference. Report the smallest supported role; do not tune on held-out windows or compare unmatched modalities as equal. Evidence branch codex/spike-provider-coverage; production integration remains ticket28.

## Acceptance criteria

- [ ] Record current explicit model/checkpoint/API identity and eligibility evidence, with dated primary citations.
- [ ] Preserve frozen inputs, raw predictions, configuration, costs and runtime failures for every executed comparison.
- [ ] Distinguish measured fit from untested, access-limited, hardware-limited and irrelevant options.
- [ ] Give a per-job disposition and the remaining deciding observation; update dashboard coverage.

## Out of scope

Automatic production integration, blanket provider endorsement, fetching private media or exposing credentials.
