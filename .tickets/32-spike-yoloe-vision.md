---
id: "32"
title: "Compare YOLOE promptable detection and segmentation"
status: done
blocked_by: ["29"]
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/spikes/provider-yoloe-results.md records pinned identities, evidence and per-job disposition or a concrete unresolved limitation"
  - "tkt validate exits 0"
---

# Compare YOLOE promptable detection and segmentation

## Context and intent

User request 2026-10-25: expand current-provider research, compare the gaps before final integration, and expose coverage on the dashboard. Read docs/agents/research/open-questions.md, docs/architecture/spikes/image-model-results.md, docs/architecture/spikes/s3-ocr-results.md and docs/plan.md. Primary job: apply/build and verify the result. Original evidence at codex/spike-image-models fd948102 and codex/spike-real-video-ocr 4df4a8d. Do not silently label all provider models tested.

## What to build

Evaluate current text/visual-prompt YOLOE against Grounding DINO and SAM3 for named regions. Representative current small segmentation checkpoint; preserve absent-subject checks. Use frozen natural-object, tutorial UI, diagram and text fixtures, same named prompts, default thresholds disclosed. Record intended extent, false positives, misses, raw boxes/masks/confidence and actual time/memory; no annotated IoU claim without masks. Compare boxes first before paying for masks.

**Budget:** one active day per provider family, setup/download separately recorded. Freeze prompts/fixture hashes and intended outputs before inference. Report the smallest supported role; do not tune on held-out windows or compare unmatched modalities as equal. Evidence branch codex/spike-provider-coverage; production integration remains ticket28.

## Acceptance criteria

- [x] Record current explicit model/checkpoint/API identity and eligibility evidence, with dated primary citations.
- [x] Preserve frozen inputs, raw predictions, configuration, costs and runtime failures for every executed comparison.
- [x] Distinguish measured fit from untested, access-limited, hardware-limited and irrelevant options.
- [x] Give a per-job disposition and the remaining deciding observation; update dashboard coverage.

## Out of scope

Automatic production integration, blanket provider endorsement, fetching private media or exposing credentials.

## Current execution evidence (2026-10-25)

YOLOE26s actual text-prompt probes at640/1280 and supplied-box probes at640 completed; same frozen images, negative elephant, raw boxes/masks/overlays captured. NoUIregions at eitherresolution; diagram at640 disappears1280. Manual code-panel seed recovers panel plus an extra almostfullframe. Broader held-out qualification remains25; report docs/architecture/spikes/provider-yoloe-results.md.

## Resolution (2026-10-25)

Completed bounded current YOLOE comparison; retain object/diagram challenger, no general UI role or integration approval. Broader state/held-out qualification remains25 and finalreview28.

### Verification
1. ✓ docs/architecture/spikes/provider-yoloe-results.md records pinned identities, evidence and per-job disposition or a concrete unresolved limitation — "docs/architecture/spikes/provider-yoloe-results.md records exact YOLOE26s/encoder hashes, text640/1280 and visual-seed outputs, qualitative baseline comparison and role-specific verdict"
2. ✓ tkt validate exits 0 — "tkt validate passed on expanded graph; experiment branch ce811ed8 preserves raw outputs, overlays, source/fixture identities, failures and passing pre-commit"
