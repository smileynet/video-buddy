# Current-provider throwaway comparisons

2026-10-25. Research29; provider tickets30–34. Branch codex/spike-provider-coverage. No production inference code, dependency or weights merged into the app.

Fixtures are unchanged committed files from sibling image-models and real-video-ocr evidence directories. Each run records fixture identity and prompt; YOLOE includes SHA256. Upstream demo photos/UI may favor their publishers; these are not a representative held-out detector corpus. Pixel masks have no annotated accuracy ground truth. Existing SAM3/GroundingDINO outputs are qualitative references with unmatched resolutions/thresholds, not a calibrated leaderboard.

YOLOE26s text probes at640/conf0.25 first;1280 and manual visual-box probes were exploratory follow-ups after viewing640 misses. Preserve those distinctions. Original download/setup run lives in attempts/yoloe-first-download.json. Cached runs, actual detector/text-encoder SHA256 and CLIPsource pin in yoloe.json. Overlays were visually inspected. No semantic text transcription or all-frame tracking is implied.

Molmo2-4B pinned042abfa7a38879a376cec03d949eff0aefaa0600 ran as an NF4-language/BF16-vision, max2-crops image-only candidate with64- and128-token arms. This is a separate memory-reduced configuration from full precision and from MolmoPoint video/GUI specialists. The checkpoint holds4,850,869,200 F32 parameters (~19.4GB download); the name4B is not a memory budget. Missing-einops initial attempt preserved. Quantizing vision made custom input dtype Byte and failed LayerNorm; excluding vision_backbone from quantization and BF16autocast enabled inference. Both setup failures are preserved, with no model-quality verdict from them. Tested package recipe deviates from card Transformers4.57.1 to existing4.57.6, recorded in environment snapshot. No temporal score from an image run.

Hosted Gemini/DINO-X calls were not attempted: no matching credential exposed in the probed session, other private configs/account/quota unverified. Config location requested, no keys printed. Docker CLI exists but server check fails (inactive Linux engine); no Cosmos3reasoner inference. access-and-runtime.json records these limited probes. Do not label all providers tested or infer quality from access/setup.

Reproduce from repo root using .venvs/vision for yoloe_bench.py [--imgsz1280] and yoloe_visual_bench.py; .venvs/qwen for molmo_bench.py. Installed snapshots pin dependencies; original setup was reused. Ultralytics may installCLIP/download a text encoder; script uses scratch model cache as its process working directory. Weights/cache files are excluded from evidence commits.

Per-job reports in main-checkout docs/architecture/spikes/provider-*-results.md state observed fit, limitations and outstanding deciding observations. Review28 owns integration after all required reports/dispositions; a completed bounded spike is not general task qualification.

Observed Molmo2:dog and search-field point outputs, absent-elephant abstention; diagram coordinate sequence remains incomplete at64 and128tokens (128-arm confirms generated_tokens128). Do not consume incomplete geometry as validated output. General model only; specialists/video/fullprecision still unrun. Per-query outputs and allocator/load observations preserved.

Credential lookup update: existing HF key verified through HF CLI and saved (by user request) to Git-ignored project/worktree.env.local. hf_context.py now checks project-local file and primary-checkout fallback before legacy discovery. User mise and standard alternate locations checked; no Gemini/DINO-X key found. No credential value is in evidence. Provider account/quota remain unverified.

Same-query Qwen3-VL2B BF16 baseline at128tokens also ran. Both models located dog and abstained on elephant. On the ambiguous search-field query, Molmo pointed to browser search and Qwen to Windows taskbar search; both fields exist, so this is not a justified accuracy winner. Qwen emitted complete XML for settings points; Molmo did not at64/128. geometry-validation.json checks XML completeness only, not semantic accuracy. Different pixel/crop/precision budgets preclude architecture-wide speed or quality ranking.

## Remaining local-model follow-up

DINOv2/v3 controlled feature probes, SAM3.1 false-only API adapter (true offload rejected), controlled positive/negative and sparse real diagram text/box arms, MolmoPointGUI8B and MolmoPointVid4B NF4language/BF16vision now ran. Raw scripts/outputs and corrected GUIquery manifest preserved. GUI hit3/4 coarse targets vsQwen4/4, one known screenshot. Initial wrong-entity/underspecified GUIquery pass is invalid for scoring and lives in attempts. Video specialist received four predecoded frames with explicit times, no resampling; returned only first-time positive points even with all-frame query. Not native-video or dense-track qualification. SAM masks show cat contamination despite stable dog ID.

GUI download initially hit shared-cache space limit; stopped only the owned process, removed its8incomplete files, retried in project scratch after free-space check. No existing complete cache files were removed. Actual checkpoints/manifests and cache routing captured; weight files remain ignored. Docker/Podman inactive and Cosmos3 config unsupported in installedHFstack; NVIDIA inference remains unrun.
