---
id: "14"
title: "Compare OCR for exact commands and settings"
status: in_progress
blocked_by: ["13"]
spec: "apply-build"
priority: medium
tags: ["workflow-spikes"]
validation_criteria:
  - "A durable spike report records options, evidence and limitations"
  - "Every evaluated option records its fixture, environment and observations"
  - "The report states an adopt, retain, reject or unresolved verdict"
---

# Compare OCR for exact commands and settings

## Intent source

User requested tickets and execution of the proposed spikes, prioritizing applying a technique or building something. This is spike S3 in [the spike plan](../docs/architecture/spike-plan.md).

## Context

Read [shared experiment contract](../docs/architecture/spike-plan.md#shared-experiment-contract), [architecture proposal](../docs/architecture/workflow-proposal.md), and [primary-source research](../docs/agents/research/video-workflow-architecture.md). Dashboard: `docs/architecture-dashboard.html`. Preserve existing unrelated working-tree changes. Production integration is out of scope.

## What to build

A reproducible comparison that resolves the deciding question below, or explicitly records the missing observation when evidence cannot settle it. No production feature or automatic winner is required.

**Deciding question:** can a better OCR path reduce manual correction of exact screen text?

**Options:** A: existing EasyOCR; B: tuned Tesseract with region/scale/segmentation settings; C: pinned PaddleOCR detection/recognition. Give each the same fixed full-frame and cropped inputs; report preprocessing and detection costs separately.

**Throwaway:** label a small reusable set of approximately 30 regions from S1/S2: terminal punctuation, code, numbers, small UI labels, dark themes and low contrast. Tune on a subset; score on held-out regions.

**Observe:** exact command/setting match, character errors, region misses, correction time, box retention, CPU/GPU memory and installation friction.

**Decision:** replace or route OCR only if held-out exact-text/correction outcomes improve at acceptable measured cost. Retain originals/crops and explicit uncertainty. No general document benchmark can win this comparison.

**Budget:** half to one day excluding downloads. **Unlocks:** OCR engine choice and result schema.

## Acceptance criteria

- [ ] A durable report identifies the deciding question, actual compared options and frozen fixtures.
- [ ] Every evaluated option records environment, observations, costs and evidence locations.
- [ ] The report states the verdict and distinguishes observed results from unresolved limitations.
- [ ] Evidence supports the downstream user job; no integration or user-study success is claimed without observation.

## Execution record

2026-10-25: exploratory Tesseract/EasyOCR/PaddleOCR runs completed on 30 controlled single-line crops plus one real settings crop. See [results](../docs/architecture/spikes/image-model-results.md) and branch `codex/spike-image-models`, commit `16c970bacec751f96f2f4a68c73dfbeaf4289e9a`. Exact controlled recovery: 23/30, 2/30, 28/30 respectively; Paddle also recovered the real crop exactly. No held-out real-video corpus or correction-time study yet; keep in progress rather than treating a smoke set as full qualification. Source/subject-aware seeking design is informed by the new image-element research.

## Reconciled remaining work (2026-10-25)

Complete held-out real-video OCR qualification: approximately 30 manually labeled terminal/code/settings/UI regions with tuning/held-out separation. Measure exact-match/CER, missed regions, preprocessing costs and correction effort. Synthetic smoke results alone do not select a default. Coordinate window labels with ticket 25. Research ticket 24 is next by explicit user instruction. Final synthesis is ticket 28; no model/default or feature integration is authorized by a smoke result.

## Ticket 24 research execution contract (2026-10-25)

**Budget:** One active day, excluding downloads; stop at a reproducible held-out result or name the missing corpus/participant constraint.

Freeze approximately 30 real regions covering code punctuation, numbers, terminal/UI themes, typing and blur. Declare tuning/held-out split before tuning; language scope starts English and records untested languages. Run identical full frames/crops through EasyOCR, Tesseract and Paddle; measure exact-match, CER, region misses, preprocessing/runtime/memory and observed correction effort. Label against source, never model consensus.

Record raw outputs, exact versions/configuration, failures and a per-job disposition. Report metrics even if they do not favor a candidate; no invented quality threshold. Research register: `docs/agents/research/open-questions.md`.

## Completed bounded real-video comparison (2026-10-25)

Report: `docs/architecture/spikes/s3-ocr-results.md`. Frozen30 regions,10 tuning/20 held-out, two actual source videos; configurations committed before held-out inference. Evidence branch `codex/spike-real-video-ocr`, commit `4df4a8dfd9892ef6cc8bba075f9adc1aa58b98bc`. Full-frame exact lines: Paddle16/20, Easy13/20, Tesseract10/20; supplied crops: Tesseract14/20, Paddle11/20, Easy9/20. Frozen hashes and selected-config consistency verified; all three inference runs and pre-commit passed. Scoring association correction and original outputs preserved. Verdict retain baseline pending28, retain separate full-frame/crop challengers. Human correction-time benefit, broader languages and motion/occlusion remain unresolved, owned by18/21/25; no production/default change.
