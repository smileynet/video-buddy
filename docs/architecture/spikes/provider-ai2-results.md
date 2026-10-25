# Ai2 Molmo2: memory-reduced image-pointing probe

Date2026-10-25. Ticket31 remains in progress for specialist/temporal qualification. **Status: actual Molmo2 inference observed; MolmoPoint video/GUI variants unrun. No provider-wide or integration verdict.**

## Pinned configuration

`allenai/Molmo2-4B`, revision `042abfa7a38879a376cec03d949eff0aefaa0600`. Tested Transformers4.57.6, torch2.11CUDA12.8, bitsandbytes0.50.2, Windows/RTX5070; card recipe4.57.1 differs. NF4 language weights, BF16 vision/compute, max2image crops and greedy decoding. This is a separate memory-reduced configuration, not evidence of full-precision parity. Original checkpoint contains4,850,869,200 F32 parameters (~19.4GB download). Exact source/config hashes and checkpoint cache identities are in the evidence manifest; weights are not committed.

The initial run lacked einops. After installing it, quantizing the vision path caused a Byte LayerNorm failure: the custom vision code derives its input dtype from patch-embedding weights, which are bytes when quantized. Excluding vision_backbone from quantization and using BF16 autocast enabled inference. Failed attempts are preserved. This was runtime/configuration repair, not model-quality tuning.

## Observed64-token arm

| Frozen fixture / query | Raw outcome | Bounded interpretation |
|---|---|---|
| Cat/dog: point to dog |Point output with633,333 normalized coordinates|Maps onto dog in the source image; no formal localization accuracy rate|
| Same photo: point to elephant |There are none.|Correct abstention on this absent-subject case|
| UI screenshot: point to search field |Point output with233,123 normalized coordinates|Maps inside the shown search field; no click/action success claimed|
| Diagram: point to harmonic settings text |Multiple point coordinates, incomplete sequence under64token limit|Geometry response is incomplete; do not consume as validated structured output|

These are points, not masks, boxes or exact OCR. The shared images are upstream demos/previously inspected figures, not a new held-out grounding corpus. No independent mask/point references, video identity, action-order or human task outcome is scored.

Load~72.53s cached after initial download, total~82.60s; observed allocator peak4,960,738,304 bytes. Per-query image processing/generation~0.77–4.76s. These are single-run costs, not minimumVRAM or production latency. CPU/whole-device peaks and quantization quality loss are unmeasured.

A128-token follow-up also ran. Dog/search coordinates and elephant abstention stayed the same; the diagram emitted128tokens and still lacked a complete closing coordinate sequence. This is an exploratory budget change, not a held-out improvement. Treat incomplete geometry as an invalid response rather than silently accepting its prefix. The128-arm cached load/total were~79.94/96.68s. Compare future specialist GUI/video checkpoints according to their actual output contracts and measured runtime fit. Ticket31 stays open; review28 cannot select all Ai2 models from this one general-model run.

Evidence branch `codex/spike-provider-coverage`, directory `docs/architecture/spikes/provider-coverage/`. [Current-provider research](../agents/research/open-questions.md#current-provider-coverage-expansion-2026-10-25) records exact alternative checkpoints and terms. Quantization does not remove third-party asset/notice obligations.

## Reproducible evidence

[Raw inputs/pointers, scripts, outputs, failures and environment](https://github.com/smileynet/video-buddy/tree/ce811ed8cd1864d347953ed4a08f0b141955ca95/docs/architecture/spikes/provider-coverage), branch `codex/spike-provider-coverage`, commit `ce811ed8cd1864d347953ed4a08f0b141955ca95`. Hosted/runtime reports preserve limited readiness probes only, not inference.

## Same-query Qwen baseline

Qwen3-VL2B BF16, pinned89644892, max262144pixels/128tokens ran the identical four prompts. Both pointed to the dog and abstained on elephant. Molmo pointed to browser search; Qwen pointed to Windows taskbar search. Both fields exist: the prompt is ambiguous, so neither choice establishes an accuracy winner. Qwen emitted complete settings point XML for the two visible rows; Molmo did not at64/128tokens. XML completeness is checked separately from coordinate/schema/semantic correctness in geometry-validation.json. Different crop/pixel budgets and precision prevent an architecture-wide quality or speed ranking. Qwen allocator peak4,337,127,424 bytes and cached total~22.64s are single-run observations.

Disposition: retain Molmo2 as a bounded coarse-pointing challenger only with strict response validation. No video/GUI-specialist, full-precision parity, task-completion or universal provider verdict.
