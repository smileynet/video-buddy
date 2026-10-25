# Ultralytics YOLOE-26s: bounded provider comparison

Date2026-10-25. Ticket32. Experiment branch `codex/spike-provider-coverage`; raw evidence path `docs/architecture/spikes/provider-coverage/` on that branch. **Verdict: retain as an object/diagram challenger; no demonstrated general UI role or production integration.**

## Exact compared configuration

Ultralytics8.4.189, `yoloe-26s-seg.pt`, SHA256 `48f24206bc8680d60cbbfa296b0140da849669b9515058b72f5a945142df0654`; text encoder SHA256 `35d7f213e4d75f38514e4656ad3cb91158bd33e3805d8ac349f23b186f66982f`. Auxiliary CLIP source revision `7ffa84b3bfa40c42ecc1c77147a855e69cb2dd40`. Text class prompts, confidence0.25, GPU, image sizes640 and1280. Separate supplied-box arm at640. Source/license constraints are in [current-provider research](../agents/research/open-questions.md#current-provider-coverage-expansion-2026-10-25); AGPL code and auxiliary assets are not automatically eligible for every deployment.

Used unchanged frozen natural-object, settings/diagram, UI-demo images from earlier model experiments and a Python conditional frame from S3. Hashes, prompts, boxes, scores, masks/overlays, timing and package snapshot are preserved. The same named subjects were used where they overlap SAM3/Grounding DINO, but resolutions, thresholds and architectures differ. This is a bounded qualitative comparison, not equal-budget accuracy benchmarking.

## Observations

| Input / job |640 text prompts|1280 text prompts|Implication|
|---|---|---|---|
| Cat/dog + absent elephant |Cat and dog found, no elephant|Dog and two cat detections, no elephant|Natural-object sanity case passed; larger input added redundancy|
| Diagram and settings text |Diagram panel found, no text box|No returned regions|Resolution is not a monotonic quality improvement|
| UI search field/buttons/chart |No regions|No regions|No general UI role demonstrated at these fixed settings|
| Python code editor/text/button |One code line labeled code editor|Two code-editor regions plus text|A proposed label does not establish complete intended extent|

SAM3 found natural animals/UI buttons but not this diagram/text with its fixed prompts; GroundingDINO located the diagram/settings but over-expanded generic UI queries. YOLOE thus adds another distinct role candidate, not a universal winner.

With manual visual-box seeds, the search field still returned no region; the supplied Python-panel seed yielded a panel-sized object0 and an extra nearly full-frame object0. Visual seeding does not certify semantics, completeness or uniqueness. No threshold/prompt tuning on a held-out set was performed. The1280 and visual arms were exploratory follow-ups after seeing640 failures, not held-out improvements.

## Cost and limits

First run downloaded detector and text encoder and installed the CLIP dependency; initial attempt is preserved. Cached640 run total~4.96s, observed allocator peak331,639,296 bytes;1280~4.59s/345,768,448 bytes. Different warmup/caching makes these unsuitable for an FPS or size-efficiency claim. Whole-device memory and CPU peak were not measured. No pixel mask ground truth, complete UI reference, temporal drift, all-frame seeking or reader benefit exists here. Original public demos may favor their publishing models.

Broader state/negative/held-out qualification belongs to25 and the relevant provider ticket. Final review28 decides whether a supported role merits a production slice; no code/weights are merged into the application.

## Reproducible evidence

[Raw inputs/pointers, scripts, outputs, failures and environment](https://github.com/smileynet/video-buddy/tree/ce811ed8cd1864d347953ed4a08f0b141955ca95/docs/architecture/spikes/provider-coverage), branch `codex/spike-provider-coverage`, commit `ce811ed8cd1864d347953ed4a08f0b141955ca95`. Hosted/runtime reports preserve limited readiness probes only, not inference.
