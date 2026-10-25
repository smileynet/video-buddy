---
id: "34"
title: "Evaluate NVIDIA reasoning for physical demonstration evidence"
status: open
blocked_by: ["29"]
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/spikes/provider-nvidia-results.md records pinned identities, evidence and per-job disposition or a concrete unresolved limitation"
  - "tkt validate exits 0"
---

# Evaluate NVIDIA reasoning for physical demonstration evidence

## Context and intent

User request 2026-10-25: expand current-provider research, compare the gaps before final integration, and expose coverage on the dashboard. Read docs/agents/research/open-questions.md, docs/architecture/spikes/image-model-results.md, docs/architecture/spikes/s3-ocr-results.md and docs/plan.md. Primary job: apply/build and verify the result. Original evidence at codex/spike-image-models fd948102 and codex/spike-real-video-ocr 4df4a8d. Do not silently label all provider models tested.

## What to build

Assess current NVIDIA Cosmos reasoning successor/version for physical action/order evidence, only where it serves the apply/build job. First establish image/video contract and resource/code/checkpoint terms. Compare supported bounded physical/non-text sequence against Qwen/ordered frames, score reference action order and unsupported explanations. If no physical fixture or eligible runtime exists, explicitly defer with the deciding missing observation; no relevance claim from robotics marketing alone.

**Budget:** one active day per provider family, setup/download separately recorded. Freeze prompts/fixture hashes and intended outputs before inference. Report the smallest supported role; do not tune on held-out windows or compare unmatched modalities as equal. Evidence branch codex/spike-provider-coverage; production integration remains ticket28.

## Acceptance criteria

- [ ] Record current explicit model/checkpoint/API identity and eligibility evidence, with dated primary citations.
- [ ] Preserve frozen inputs, raw predictions, configuration, costs and runtime failures for every executed comparison.
- [ ] Distinguish measured fit from untested, access-limited, hardware-limited and irrelevant options.
- [ ] Give a per-job disposition and the remaining deciding observation; update dashboard coverage.

## Out of scope

Automatic production integration, blanket provider endorsement, fetching private media or exposing credentials.

## Current execution evidence (2026-10-25)

Pinned Cosmos3Edge metadata is accessible; read-only docker server check failed because Linux-engine pipe absent. No reasoner inference, hardware fit or physical-task quality claimed. Need eligible configured runtime and reference physical-action sequence; see docs/architecture/spikes/provider-nvidia-results.md. Keep open.

## Additional local prerequisite checks

Pinned Cosmos3Edge config rejected by installedTransformers; current upstream auto registry lackscosmos3 registration and config hasnoauto_map. Docker andPodman servers inactive; CLI-configured backendsonlylocal. Preserve cosmos-local-prerequisites.json. No inference/quality evidence; supported serving deployment and physical-action reference remain required.

## Completed local probe evidence

Additional prerequisite probes found no installed/upstreamAutoConfig registration forcosmos3_edge, noauto_map, both container serversinactive; configuredbackendsonlylocal andexistingstoppedPodmanVM2GBRAM. NoNVIDIAinferenceclaimed. Supported reasoner endpoint plusphysicalreferencefixture remain open. Raw evidence: `codex/spike-provider-coverage` commit `fc7caee6184942d39ca4cc5cc2c4d36a36498d44`.
