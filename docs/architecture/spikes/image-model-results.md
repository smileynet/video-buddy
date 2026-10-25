# Image-model job-fit spike: initial retention decisions

Date: 2026-10-25. Tickets [14](../../../.tickets/14-spike-ocr-exact-text.md) and [23](../../../.tickets/23-image-model-job-fit.md). **Exploratory inference completed for 13 accessible configurations; SAM 3.1 has an unresolved runtime compatibility failure and DINOv3 remains gated.** These are per-job shortlist recommendations, not approval to integrate new dependencies or a claim of production-quality validation.

## Evidence and environment

Throwaway branch `codex/spike-image-models`, commit `fd948102c21f4d3b69a29c46cfd22c9366e9c874`. [Evidence directory](https://github.com/smileynet/video-buddy/tree/fd948102c21f4d3b69a29c46cfd22c9366e9c874/docs/architecture/spikes/image-models) contains runnable probes, frozen images/hashes, exact prompts, checkpoint/source revisions, raw outputs, masks, timing/memory observations and environment snapshots. No prototype code/weights were merged into the application.

Windows, Python 3.12.10, RTX 5070 12 GB with roughly 8 GB initially free. Vision used torch 2.11.0+cu128 and transformers 4.51.3; Qwen had an isolated transformers 4.57.6 environment. PaddleOCR used a separate CPU environment. Timing includes a mixture of first-download/load and cached runs; do not rank engines by total seconds here. CUDA memory fields are per-process allocator peaks, not minimum VRAM requirements or whole-device peaks.

Fixtures: 30 synthetic single-line crops (five strings × two themes × three sizes), one manually transcribed video settings crop, one real UI screenshot from OmniParser's own demo, one natural-object photo from Grounding DINO's example, and four real diagram frames from the previous spike. The public demo examples may favor those models and are not held-out. This is not the planned representative corpus of terminal/UI video regions. There is no reader study, mask ground truth, latency distribution or full subject-aware frame selector yet.

## Provisional per-job shortlist

| Job | Keep for the next qualification round | Observation and restriction |
|---|---|---|
| Exact code/settings text | **PaddleOCR mobile English**; **Tesseract** as low-dependency fallback | Paddle recovered 28/30 controlled strings and the real crop exactly; Tesseract recovered 23/30 and missed the real crop. Needs a real-video held-out corpus before replacing defaults. |
| Locate named objects/diagram regions | **Grounding DINO tiny** | Located cat/dog, diagram and settings row. Generic UI prompts produced nearly full-screen boxes: do not use as the UI-control detector without task-specific rejection/validation. |
| Identify UI elements | **OmniParser v3 detector** | Produced individual control boxes in the demo screenshot. Detector output is not a verified function/action label; full OCR merging and GUI execution were not evaluated. |
| Isolate a named subject with a mask | **Grounding DINO → SAM 2.1** composition | Box-prompted masks separated dog/cat and isolated diagram/text panel. No annotated segmentation accuracy; use boxes alone where sufficient. |
| Follow an already located panel | **EfficientTAM-Ti 512** as low-memory challenger; **SAM 2.1 tiny** as comparison/fallback | Both followed the panel across four sparse source frames. Observed allocator peaks ~239 MB vs ~609 MB; differing model/resolution settings confound any efficiency generalization. No long-video/occlusion qualification. |
| Local semantic explanation | **Qwen3-VL 2B**, optional | Named animals, rejected absent elephant, read settings correctly, described UI layout. Also misdescribed an icon; never treat explanation as exact OCR or verified action evidence. Allocator peak ~4.34 GB in this bounded run. Existing external agent remains the default interpretation owner. |
| Regional visual correspondence | **DINOv2-small**, optional only if simple association fails | Found 5/5 selected patch correspondences under a controlled one-patch translation. Whole-image similarity was 0.9982 after a one-character setting change: unsuitable as the sole text-revision dedup key. Real correspondence/drift remains unqualified. |

“Keep” means retain the candidate for its demonstrated role. It does not mean all these models should be loaded into every run. Start with OCR boxes or a known region; add semantic detection, masks and tracking only when the requested evidence needs them.

## Remaining model dispositions

| Model/configuration | Actual disposition |
|---|---|
| EasyOCR 1.7.2 English GPU | Ran. Exact 2/30 on these controlled crops; real crop had character errors. Retain the existing application baseline pending broader qualification, but it is not the leading exact-text candidate in this set. Its detection/recognition defaults and box-to-text merging differ from the other configurations; do not generalize the result to all OCR domains/languages. |
| Original SAM ViT-B | Ran. Highest-scored point-prompt mask included the negative seed, while a lower-scored candidate excluded it. Prompt/candidate validation and intended granularity matter. No extra default role demonstrated beyond the newer composition; do not declare the model universally inferior. |
| EfficientSAM-Ti | Ran. All three masks in this particular point-prompt run included the negative seed. Deprioritize for this prompt/fixture until investigated; one sanity case is insufficient to reject it globally. |
| Florence-2-base-ft | Ran object detection, dense region caption and region OCR. Named cat/dog, but dense UI caption collapsed to “computer monitor”; settings transcription contained errors. Deprioritize for fine UI parsing and exact OCR in the current shortlist. Other Florence variants/tasks are not disqualified. |
| SAM 3 | Ran on Ubuntu WSL after native Windows import required Triton. Found cat/dog and rejected elephant; returned 15 UI button boxes and two search-field boxes. No regions for diagram, text or line chart at the fixed default settings. Dog had an additional broad high-scoring box. Retain as an optional concept-search challenger, not a universal region detector. Allocator peak ~4.58 GB. |
| SAM 3.1 | Approved checkpoint loaded on Ubuntu WSL, but upstream session creation passes unsupported `offload_state_to_cpu` to the multiplex model. Initial four-object bucket override mismatched checkpoint tensors; retaining required bucket size 16 resolved that first issue. No tracking inference/quality verdict; retain as blocked challenger pending upstream API repair. |
| DINOv3 ViT-S/16 | Same concrete access limitation; no inference/quality result. Pending approved access. |

The user's existing Hugging Face credential was found in authorized user TOML settings and authenticated successfully. Its value was neither displayed nor persisted in evidence. Authentication does not imply per-model approval. SAM 3 and SAM 3.1 are now approved; DINOv3 still returns 403. Model access pages: [SAM 3](https://huggingface.co/facebook/sam3), [SAM 3.1](https://huggingface.co/facebook/sam3.1), [DINOv3](https://huggingface.co/facebook/dinov3-vits16-pretrain-lvd1689m). Do not download unapproved mirrors to bypass these gates.

## OCR observations

Whitespace was collapsed for scoring; case/punctuation were preserved. No tuning/held-out split was performed. Tesseract used single-line PSM 7, EasyOCR used its English GPU reader, Paddle used PP-OCRv5 mobile detection and English recognition on CPU with four threads and MKLDNN disabled.

| Configuration | Exact controlled lines | Mean character error on controls | Real settings crop |
|---|---:|---:|---|
| Tesseract | 23/30 | 1.76% | Not exact; CER 20% |
| EasyOCR | 2/30 | 11.07% | Not exact; CER 7.5% |
| PaddleOCR | 28/30 | 0.29% | Exact |

Qwen also transcribed the one real crop exactly; Florence's general region OCR did not. They did not run the full 30-case OCR comparison, so do not insert them into that table as equivalent benchmark contestants. Exact-string recovery is not command safety or semantic correctness.

## Other concrete findings

- The Grounding DINO natural-object prompt included absent “elephant”; no elephant box was returned. On the UI screenshot, its “search input field” box covered almost the whole viewport. Model-domain routing is necessary.
- OmniParser's detector returned 140 regions at the tested threshold, including useful controls and additional/overlapping regions; region count is not precision/recall. The official icon-caption component returned “Overview” and “Images”, “Add Follow.”, and the poor search-field description “Performational”. Keep literal OCR and inferred function distinct. Its v3 detector was downloaded from a pinned accessible revision; earlier version/license notices still require exact-asset review before integration.
- Point prompts can select a nose/face rather than the whole animal. SAM 2/EfficientTAM point masks and original SAM candidates cannot be fairly interpreted without desired granularity. The named-box composition produced the intended animal separation in visual inspection.
- EfficientTAM initially failed because its default image configuration enabled optional compilation with no native Windows Triton backend. Disabling that configuration option enabled both image and tracking runs. The initial failure is preserved; it is not a model-quality defect.
- DINO's default center crop initially erased the left-aligned text, yielding a misleading unchanged feature result. The final run disabled center cropping and confirmed nonzero processed pixel differences. Preprocessing must be part of every model comparison.
- Qwen described the Follow button as having a white arrow, while the source shows a plus. A plausible semantic answer is not an exact visual observation. Outputs require evidence checks even when another task succeeds.

## Reproduction and review

See the branch README and per-family scripts. [Segmentation comparisons](https://github.com/smileynet/video-buddy/blob/fd948102c21f4d3b69a29c46cfd22c9366e9c874/docs/architecture/spikes/image-models/segmentation-contact.jpg), [tracking comparisons](https://github.com/smileynet/video-buddy/blob/fd948102c21f4d3b69a29c46cfd22c9366e9c874/docs/architecture/spikes/image-models/tracking-contact.jpg), and [UI detector overlay](https://github.com/smileynet/video-buddy/blob/fd948102c21f4d3b69a29c46cfd22c9366e9c874/docs/architecture/spikes/image-models/omniparser-overlay.jpg) preserve the inspected outputs. Pre-commit and secret scanning passed on the captured experiment files.

## Work still required before integration

1. Obtain DINOv3 approval and resolve SAM 3.1 upstream session compatibility, then run those checkpoints against the same relevant fixtures; keep ticket 23 in progress until those observations or an explicit user decision to exclude them exists.
2. Finish ticket 14 with independent real video text regions and held-out windows, including typing, scrolling, blur, obstruction, punctuation and language needs. The synthetic smoke set does not satisfy that full quality bar.
3. Compare subject-aware box seeking against optional masks/tracking using exhaustive annotation in short windows. Measure readable complete-state recall, missed revisions and actual correction effort; mask quality alone is not success.
4. Review one isolated candidate per job for implementation. Preserve raw evidence and abstention; do not integrate the complete upstream demo stacks or all shortlisted models by default.

## Access recheck during ticket 24 (2026-10-25)

DINOv3 checkpoint access is now approved with the existing credential: `facebook/dinov3-vits16-pretrain-lvd1689m`, revision `114c1379950215c8b35dfcd4e90a5c251dde0d32`, authenticated metadata request succeeded. Earlier 403 results above remain the historical experiment state, not the current blocker. Inference remains pending in ticket 23. SAM 3.1 caller/callee incompatibility is confirmed in current upstream revision `f1647e8d0c1d280991f4d1b7d974c2704537fe66`; see the ticket 24 research register for source references and a bounded experimental workaround.
