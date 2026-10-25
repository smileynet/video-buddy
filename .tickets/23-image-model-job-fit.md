---
id: "23"
title: "Compare image element models by downstream evidence jobs"
status: in_progress
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

- [ ] Every researched family has actual inference evidence or an explicit unresolved access/runtime limitation.
- [ ] Compared jobs use frozen fixtures and preserve raw outputs, timings, prompts and environments.
- [ ] Recommendations distinguish measured job fit from untested candidates and synthetic smoke checks from real-domain evaluation.
- [ ] Experimental code/dependencies stay on the spike branch; no production model integration is implied.

## Execution record

2026-10-25: [initial per-job results](../docs/architecture/spikes/image-model-results.md). Branch `codex/spike-image-models`, commit `16c970bacec751f96f2f4a68c73dfbeaf4289e9a`: 12 accessible configurations ran, plus composed grounding/segmentation and temporal probes. SAM 3, SAM 3.1 and DINOv3 returned gated-access 403 with a verified existing credential; awaiting user checkpoint approval, not classified as poor quality. Keep in progress. All recommendations are provisional; held-out real task windows remain required. Qwen3-VL 2B from the prior shortlist was also tested in an isolated environment.

Later access recheck: SAM 3 and SAM 3.1 approved using the existing credential; DINOv3 still 403. SAM 3 completed image inference on Ubuntu WSL after native Windows required Triton. Named animals/UI buttons found, but diagram/text prompts returned no regions; preserve it as an optional concept-search challenger. SAM 3.1 runtime qualification is underway; a four-object multiplex override mismatched the checkpoint, so the retry retains its required 16-object bucket size. No production integration.

Final SAM 3.1 retry retained checkpoint bucket size 16 and loaded weights, then failed in upstream start_session: init_state rejects offload_state_to_cpu. This is an explicit unresolved runtime/API limitation, not a tracking result. DINOv3 still awaits approval. SAM 3 completed inference; see updated results report. Keep in progress for remaining qualification.

Final additional evidence: `codex/spike-image-models` commit `fd948102c21f4d3b69a29c46cfd22c9366e9c874`, approved checkpoint probes, Linux environment, SAM 3 masks and SAM 3.1 failures. Pre-commit/secret checks passed; dashboard interaction, keyboard, mobile and local-link checks passed.

## Reconciled remaining work (2026-10-25)

Finish real-domain job qualification beyond upstream demo fixtures: UI controls, diagrams, natural objects, regional matching and subject tracking. SAM 3 ran; SAM 3.1 checkpoint loads but upstream start_session rejects offload_state_to_cpu; DINOv3 still gated. Research 24 owns compatibility/access/license investigation; this ticket owns inference probes. Preserve concrete unresolved limits and evaluate long-window drift/occlusion only where needed for ticket 25. Research ticket 24 is next by explicit user instruction. Final synthesis is ticket 28; no model/default or feature integration is authorized by a smoke result.
