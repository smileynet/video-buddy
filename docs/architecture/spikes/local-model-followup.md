# Remaining local models: bounded follow-up

Date2026-10-25. Tickets23/31/34. Evidence branch `codex/spike-provider-coverage`, directory `docs/architecture/spikes/provider-coverage/`. **These are additional measured roles/limits, not final integration approval.**

## DINOv3 versus DINOv2

Pinned DINOv3 ViT-S/16 revision114c1379950215c8b35dfcd4e90a5c251dde0d32 and DINOv2-small ed25f3a31f01632728cabb09d1542f84ab7b0056 both ran on GPU. Full224px image resizing retained the changed text (nonzero processed pixel difference); default center-crop was disabled. DINOv3 register tokens were excluded before patch matching.

| Controlled observation | DINOv2 | DINOv3 |
|---|---|---|
| Five selected patch matches after a one-patch horizontal translation |5/5 exact|4/5 exact; one selected patch shifted an extra row|
| CLS cosine after port=8001 → port=8000 |0.9982|0.9871|

Each model shifted one of its own patches (14px versus16px), so these are not equal spatial-support accuracy samples. Cross-model cosine scales are not calibrated; the lower number is not proof of better semantic sensitivity. Five patches and one text change do not qualify video tracking/deduplication. Retain DINOv3 as optional correspondence research; this does not establish an embedding-only rule that preserves meaningful code/settings revisions. No new default role demonstrated.

## SAM3.1: API adapter and actual inference

Pinned source f1647e8d0c1d280991f4d1b7d974c2704537fe66 and checkpoint daa63191845a41281374e725f4c9e51c7a824460 ran on the existing Ubuntu WSL GPU runtime. An experiment-only wrapper drops offload_state_to_cpu only when false; a direct guard check rejects true. Upstream source files and production backend code were not patched. Compile/FlashAttention3/warmup disabled; checkpoint multiplex bucket16 retained. Earlier unpatched API failure remains preserved.

- Controlled dog: one photo translated0/10/20/30pixels, with a gray obstruction on frame2. One object ID persisted across four frames. Visual mask inspection also reveals included cat pixels; stable identity does not certify clean subject extent.
- Absent elephant on that controlled sequence: zero objects on all four frames.
- Diagram text prompt across four sparse real captured states: zero objects. This is a grounding failure at fixed settings; tracking cannot be evaluated without a discovered subject.
- A separate box-guided arm accepted the previous SAM2 panel seed and returned one initial mask, but subsequent propagation emitted zero objects on all four frames. Separate initial localization from retained trajectory output. No threshold/prompt tuning or universal inability is inferred.

Observed allocator peak~7.32GB for the three-session run, cached load~72.54s and total~98.56s. Not minimumVRAM or production latency. Controlled images are derived, not real continuous video. No annotated mask accuracy, long-video drift or task-completion outcome. Upstream load warnings remain a reproducibility caveat; raw output and masks are preserved.

Disposition: the API obstacle has an experimentally demonstrated workaround. Retain SAM3.1 as a conditional concept/tracking challenger; fixed diagram results and contaminated extent do not justify replacing boxes/OCR/SAM2 for the current guide job. Complete-state seeking remains25.

## Ai2 GUI specialist

Pinned MolmoPoint-GUI8B0337d39b721d0ce6fa9b315b158ac11c63e0dedc ran in an NF4-language/BF16vision, two-crop configuration using its actual grounding-token processor/decoder. Four scoped targets distinguish browser search, Windows search, Follow and Overview. This is pointing-only; no click is executed. Reference boxes are coarse manually inspected regions in one previously inspected public UI screenshot, not independent GUI qualification.

The initial download encountered insufficient space in the shared cache; the owned process was stopped and only its incomplete downloads removed. Retry uses process-local project scratch cache after checking free space. This is setup history, not a model-quality result. The initial query set also contained a wrong entity (Bill Gates) and an underspecified browser-search reference; that pass is preserved as invalid for scoring. Both models were rerun on the same corrected prompts before comparison.

## NVIDIA current runtime eligibility

Pinned Cosmos3Edge344d602b128d1bbdacb43b08d0a3626f46343e29 config has architectureCosmos3EdgeForConditionalGeneration and no auto_map. The installed Transformers stack rejects cosmos3_edge; current upstream main AutoConfig registration also did not list it when checked. This does not prove vLLM cannot run it and is not a reason to upgrade the working Molmo environment blindly.

Read-only Docker/Podman server checks both failed (inactive engines). CLI-configured backend listing exposed only local. No current supported reasoner endpoint is available, so no NVIDIA inference/quality claim is made. Ticket34 remains open for the documented compatible serving path and a physical-action reference fixture; generation assets are not source evidence.

## Corrected GUI result

| Intended coarse target | MolmoPoint-GUI8B NF4 | Qwen3-VL2B BF16 |
|---|---|---|
| Google page query field below address bar |Inside|Inside|
| Windows taskbar Search field |Inside|Inside|
| Blue +Follow button on stock result |Outside|Inside|
| Outlined Overview pill |Inside|Inside|

Three of four versus four of four is target-box containment on one known image, not a general GUI accuracy estimate. Molmo uses its official grounding-token decoder to pixel coordinates; Qwen point coordinates are mapped from the0–1000 convention to3240×2160 pixels. One point inside the intended reference is required. No click executed. Different crop/pixel/precision settings, coarse references and corrected-after-inspection prompts preclude a universal winner. GUI observed allocator peak~9.18GB, cached load~60.56s/total~73.96s, versus Qwen~4.34GB/total~28.01s. These include load effects, not minimum memory or calibrated speed rankings. The heavier specialist did not demonstrate an advantage here; retain Qwen baseline pending broader job evidence.

## MolmoPoint video specialist

Pinned `allenai/MolmoPoint-Vid-4B` b331ed6c6352e6db967325493c6dae515541a919 ran NF4language/BF16vision with its actual video point decoder. Inputs were four predecoded frames with explicit relative times, with resampling disabled: controlled0/1/2/3seconds and real requested0/6/8/10seconds. This is not native decoding or exhaustive temporal coverage.

Both short track prompts and an explicit point-in-every-frame follow-up ran. Dog and diagram returned one point at time0 only; the absent elephant returned none. The three positive-frame timestamps after0 were not covered, even in the explicit arm. Outputs used15–21tokens, below the128limit, so these failures were not output-length exhaustion. A first-frame location is not a demonstrated trajectory. Retain as an optional sparse-localization candidate, not a replacement for propagation tracking in this configuration. Official special-token decoding differs from generic XML validation.

Observed allocator peak~4.96GB; cached initial arm load/total~22.17/25.74s, explicit arm~22.70/26.37s. No full-precision parity, long-video identity or human benefit established. All three Ai2 representatives now have bounded inference records; job-window qualification remains25 and native temporal comparison26.

## Evidence and verification

[Raw scripts, predictions, source/config manifests, masks and corrected GUI controls](https://github.com/smileynet/video-buddy/tree/fc7caee6184942d39ca4cc5cc2c4d36a36498d44/docs/architecture/spikes/provider-coverage), commit `fc7caee6184942d39ca4cc5cc2c4d36a36498d44`. [Controlled mask inspection](https://github.com/smileynet/video-buddy/blob/fc7caee6184942d39ca4cc5cc2c4d36a36498d44/docs/architecture/spikes/provider-coverage/sam31-controlled-contact.jpg). Verified both GUI runners used the corrected prompt manifest, SAM true-offload rejection/four-frame outputs, and preserved video timestamps. Pre-commit passed on all experiment files. Qwen pixel mapping follows its [official2D grounding cookbook](https://github.com/QwenLM/Qwen3-VL/blob/main/cookbooks/2d_grounding.ipynb), which specifies “relative coordinates ranging from 0 to 1000” (accessed2026-10-25).
