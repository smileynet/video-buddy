---
id: "25"
title: "Find complete readable subject states by seeking within video windows"
status: open
blocked_by: []
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/spikes/subject-frame-seeking-results.md exists and records evidence, limitations and a disposition for each scoped question"
  - "tkt validate exits 0"
---

# Find complete readable subject states by seeking within video windows

## Context and intent

Intent source: user request on 2026-10-25 to capture every remaining spike, put open research next, then review integration, features and architecture. Read docs/architecture/spike-plan.md, docs/architecture/workflow-proposal.md and docs/architecture/spikes/image-model-results.md. Primary job: apply a technique/build something and verify the result. Preserve unrelated working-tree changes. Prototype code stays on isolated spike branches; no production integration in a spike.

## What to build

Evidence that seeking across all decoded frames inside a subject window recovers complete readable states better than the existing sparse strategy.

Compare sparse/time-selected baseline, dense box/crop scoring, and optional masks/tracking on the SAME short frozen windows. Detect a subject once, associate it over the window, seek optimal frame(s), preserve distinct revisions and action order. Include typing, scrolling, blur, occlusion, slide/diagram updates and brief UI states. Use CLI/source capture mechanics rather than reinventing acquisition. Exhaustively annotate essential readable states within bounded windows; split tuning and held-out windows. Use provisional ticket 14/23 candidates, disclose partial qualification; their final completion is not required to start this joint experiment. Record deciding question, total active budget, modality/settings/hardware and all failures before comparing.

## Acceptance criteria

- [ ] Report complete-state recall against exhaustive window labels.
- [ ] Report missed revisions, duplicate evidence and wrong subject associations.
- [ ] Report exact settings/command recovery and human correction effort where observed.
- [ ] Compare frame count, decode/detection/recognition/tracking cost and memory separately.
- [ ] Show whether boxes suffice and where masks/tracking add measurable benefit; retain explicit gaps.

## Out of scope

Automatic production integration, unsupported winners, and invented user/quality measurements.
