---
id: "33"
title: "Compare hosted DINO-X grounding against local baselines"
status: open
blocked_by: ["29"]
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/spikes/provider-dinox-results.md records pinned identities, evidence and per-job disposition or a concrete unresolved limitation"
  - "tkt validate exits 0"
---

# Compare hosted DINO-X grounding against local baselines

## Context and intent

User request 2026-10-25: expand current-provider research, compare the gaps before final integration, and expose coverage on the dashboard. Read docs/agents/research/open-questions.md, docs/architecture/spikes/image-model-results.md, docs/architecture/spikes/s3-ocr-results.md and docs/plan.md. Primary job: apply/build and verify the result. Original evidence at codex/spike-image-models fd948102 and codex/spike-real-video-ocr 4df4a8d. Do not silently label all provider models tested.

## What to build

Evaluate current hosted DINO-X or provider-recommended grounding version against local Grounding DINO/SAM3 on identical frozen prompts/fixtures. Pin actual service model identifier and SDK/API version; do not equate local GroundingDINO weights with hosted1.5/1.6/DINO-X. Record false regions, absent subjects, region completeness, API cost/latency and literal text support. No configured service credential means untested access limitation; never substitute marketing numbers for a run.

**Budget:** one active day per provider family, setup/download separately recorded. Freeze prompts/fixture hashes and intended outputs before inference. Report the smallest supported role; do not tune on held-out windows or compare unmatched modalities as equal. Evidence branch codex/spike-provider-coverage; production integration remains ticket28.

## Acceptance criteria

- [ ] Record current explicit model/checkpoint/API identity and eligibility evidence, with dated primary citations.
- [ ] Preserve frozen inputs, raw predictions, configuration, costs and runtime failures for every executed comparison.
- [ ] Distinguish measured fit from untested, access-limited, hardware-limited and irrelevant options.
- [ ] Give a per-job disposition and the remaining deciding observation; update dashboard coverage.

## Out of scope

Automatic production integration, blanket provider endorsement, fetching private media or exposing credentials.

## Current execution evidence (2026-10-25)

No matching hosted IDEA credential exposed in current session; no API call or quality result. Local GroundingDINO is not a proxy for hostedDINO-XPro. User asked for config location. See docs/architecture/spikes/provider-dinox-results.md; keep open.
