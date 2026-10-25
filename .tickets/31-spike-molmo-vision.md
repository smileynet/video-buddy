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

## Current execution evidence (2026-10-25)

Pinned Molmo2-4B checkpoint has4.85B F32 parameters (~19.4GB download). Testing NF4 language/BF16vision, max2crops/max64tokens image-only configuration. First missingeinops fixed; all-linear quantization exposed ByteLayerNorm failure because vision dtype comes from quantized patch-embedding weight. Preserve failure and retry with vision_backbone excluded from quantization. This is a runtime/configuration observation, not model-quality evidence. GUI/video specialists remain unrun.

## Comparison follow-up

Completed Molmo2NF4language/BF16vision at64/128tokens and same-query Qwen3VL2B BF16/128baseline. Dog/absent-elephant sanity checks both pass qualitatively. Browsersearch versusOSsearch is ambiguous, not an accuracywin. Molmo settings output remains incomplete at both limits; Qwen XML complete. Raw outputs and pinned configurations preserved. MolmoPoint video/GUI and task qualification remain unrun, so keep31inprogress. Evidence commit ce811ed8, provider reports under docs/architecture/spikes/.

## Completed local probe evidence

MolmoPointGUI8B andVid4B now ran with NF4language/BF16vision. Invalid wrong-entity/underspecified GUI pass preserved, corrected matching queries scored3/4 GUIvs4/4Qwen. Video processor preserved4supplied times but outputs had onlytime0positive points, even explicit allframes; absent elephantnone. No native-video/fullprecision/heldoutgeneralization. Bounded candidate comparison complete; window/temporal outcomes remain25/26. Raw evidence: `codex/spike-provider-coverage` commit `fc7caee6184942d39ca4cc5cc2c4d36a36498d44`.
