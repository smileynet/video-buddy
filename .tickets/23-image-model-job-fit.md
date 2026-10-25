---
id: "23"
title: "Compare image element models by downstream evidence jobs"
status: done
blocked_by: []
spec: "apply-build"
priority: high
validation_criteria:
  - "Every researched model has a recorded run result or concrete unresolved access/runtime limitation"
  - "Compared jobs use frozen fixtures and preserve raw outputs, timings and environment"
  - "A per-job retention recommendation distinguishes measured evidence from untested candidates"
tags: ["workflow-spikes"]
---

# Compare image element models by downstream evidence jobs

## What to build

Compare every image-model family identified in `docs/agents/research/image-elements-and-frame-seeking.md` on its relevant evidence job, per the user's request to spike all models and decide which to retain. Separate actual inference outcomes, accessible-but-unrun options and concrete access/runtime limitations. Do not convert a setup failure into a quality judgment or automatically integrate experimental dependencies.

Use a frozen fixture set including real UI, captured video diagrams/settings, natural objects, and explicitly labeled controlled text/state-change cases. Existing OCR comparison is ticket 14; this ticket coordinates semantic detection, segmentation/tracking, screen parsing and correspondence. Preserve raw outputs, model IDs/revisions, prompts/seeds, timings, hardware, and environment. Experimental branch: `codex/spike-image-models`.

Coverage: Tesseract, EasyOCR, PaddleOCR; original SAM, SAM 2.1, EfficientSAM, EfficientTAM; SAM 3/3.1; Grounding DINO and its Grounded-SAM composition; Florence-2; OmniParser; DINOv2/v3. Choose a practical representative checkpoint per family, not every available size. Gated weights require existing approved access; never solicit pasted credentials.

## Acceptance criteria

- [x] Every researched family has actual inference evidence or an explicit unresolved access/runtime limitation.
- [x] Compared jobs use frozen fixtures and preserve raw outputs, timings, prompts and environments.
- [x] Recommendations distinguish measured job fit from untested candidates and synthetic smoke checks from real-domain evaluation.
- [x] Experimental code/dependencies stay on the spike branch; no production model integration is implied.

## Execution record

2026-10-25: [initial per-job results](../docs/architecture/spikes/image-model-results.md). Branch `codex/spike-image-models`, commit `16c970bacec751f96f2f4a68c73dfbeaf4289e9a`: 12 accessible configurations ran, plus composed grounding/segmentation and temporal probes. SAM 3, SAM 3.1 and DINOv3 returned gated-access 403 with a verified existing credential; awaiting user checkpoint approval, not classified as poor quality. Keep in progress. All recommendations are provisional; held-out real task windows remain required. Qwen3-VL 2B from the prior shortlist was also tested in an isolated environment.

Later access recheck: SAM 3 and SAM 3.1 approved using the existing credential; DINOv3 still 403. SAM 3 completed image inference on Ubuntu WSL after native Windows required Triton. Named animals/UI buttons found, but diagram/text prompts returned no regions; preserve it as an optional concept-search challenger. SAM 3.1 runtime qualification is underway; a four-object multiplex override mismatched the checkpoint, so the retry retains its required 16-object bucket size. No production integration.

Final SAM 3.1 retry retained checkpoint bucket size 16 and loaded weights, then failed in upstream start_session: init_state rejects offload_state_to_cpu. This is an explicit unresolved runtime/API limitation, not a tracking result. DINOv3 still awaits approval. SAM 3 completed inference; see updated results report. Keep in progress for remaining qualification.

Final additional evidence: `codex/spike-image-models` commit `fd948102c21f4d3b69a29c46cfd22c9366e9c874`, approved checkpoint probes, Linux environment, SAM 3 masks and SAM 3.1 failures. Pre-commit/secret checks passed; dashboard interaction, keyboard, mobile and local-link checks passed.

## Reconciled remaining work (2026-10-25)

Finish real-domain job qualification beyond upstream demo fixtures: UI controls, diagrams, natural objects, regional matching and subject tracking. SAM 3 ran; SAM 3.1 checkpoint loads but upstream start_session rejects offload_state_to_cpu; DINOv3 still gated. Research 24 owns compatibility/access/license investigation; this ticket owns inference probes. Preserve concrete unresolved limits and evaluate long-window drift/occlusion only where needed for ticket 25. Research ticket 24 is next by explicit user instruction. Final synthesis is ticket 28; no model/default or feature integration is authorized by a smoke result.

## Ticket 24 research execution contract (2026-10-25)

**Budget:** One active day for remaining model qualification, excluding checkpoint downloads.

Access rechecked 2026-10-25: SAM3, SAM3.1 AND DINOv3 now approved; no new credential action. DINOv3 pinned model revision114c1379950215c8b35dfcd4e90a5c251dde0d32. Reuse real-domain fixtures with explicit job labels, compare DINOv2/v3 patch association and text-revision sensitivity, not just CLS similarity. SAM3.1 source f1647e8d0c1d280991f4d1b7d974c2704537fe66 has confirmed caller/callee mismatch: start_session passes offload_state_to_cpu, multiplex init_state lacks it/**kwargs. Experimental shim may omit FALSE only and must reject TRUE; keep checkpoint multiplex_count16. Preserve unpatched failure and shim diff. Test no-object and nonempty subject propagation, drift/occlusion and extent, not only successful loading. This is a bounded experiment, not a production backend patch.

Record raw outputs, exact versions/configuration, failures and a per-job disposition. Report metrics even if they do not favor a candidate; no invented quality threshold. Research register: `docs/agents/research/open-questions.md`.

### Component eligibility gate

Record exact code, checkpoint and dependency notices independently. OmniParser original icon_detect, icon_detect_v3, caption weights and root code are separate assets; a README badge is not a license for the whole stack. Use only components whose exact terms are established for the intended deployment; unknown eligibility stays unresolved. See the ticket 24 register for pinned sources. No blanket commercial eligibility claim follows from an MIT detector notice.

## Provider coverage expansion

Current-provider comparison is now explicit in29–34. Coordinate shared fixtures/metrics and consume those results rather than duplicating provider installs. Original tested shortlist is not comprehensive market coverage. Final integration28 depends on all coverage dispositions.

## Local follow-up (2026-10-25)

DINOv3 inference completed against DINOv2 controls:4/5vs5/5 selected translated patches; one-character CLS0.9871vs0.9982, uncalibrated scales. SAM3.1 false-only adapter enabled three actual sessions and a box follow-up: controlleddog IDstable with cat-mask contamination, absent-elephant0objects, realdiagram text/box0objects. See docs/architecture/spikes/local-model-followup.md. No production patch or universal dedup/tracker verdict; task-window qualification remains25.

## Completed local probe evidence

Completed bounded original-family comparison after DINOv3 and SAM3.1 inference. SAM3.1 boxseed yielded initial panel mask but no propagated IDs; distinguish that from textgroundingnone. All original families now have inference or preserved limitations; downstream held-out complete-state work remains25, not an inferred production approval. Raw evidence: `codex/spike-provider-coverage` commit `fc7caee6184942d39ca4cc5cc2c4d36a36498d44`.

## Resolution (2026-10-25)

Completed bounded original image-model comparison with DINOv3 and SAM3.1 follow-up; observed limits remain explicit, held-out job-window qualification continues25.

### Verification
1. ✓ Every researched model has a recorded run result or concrete unresolved access/runtime limitation — "docs/architecture/spikes/local-model-followup.md completes DINOv3 and SAM3.1 observed inference; all original candidate families have raw runs or explicit limitations"
2. ✓ Compared jobs use frozen fixtures and preserve raw outputs, timings and environment — "codex/spike-provider-coverage fc7caee preserves inputs, manifests, corrected controls, masks, per-frame outputs, timing and failures; pre-commit passes"
3. ✓ A per-job retention recommendation distinguishes measured evidence from untested candidates — "Per-role verdicts retain conditional candidates and leave extent, state completeness and task benefit to25/26/28; no production integration"
