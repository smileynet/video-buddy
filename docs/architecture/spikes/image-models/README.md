# Image-model job-fit spike: experimental evidence

2026-10-25. Tickets 14 and 23. Throwaway branch `codex/spike-image-models`; no inference code or dependency was integrated into the application. This is exploratory qualification, not a held-out production benchmark.

## What ran

OCR: Tesseract 5.4, EasyOCR 1.7.2 and PaddleOCR 3.7 with PP-OCRv5 mobile detection/English recognition. Vision: original SAM ViT-B, SAM 2.1 Hiera tiny, EfficientSAM-Ti, EfficientTAM-Ti 512, Grounding DINO tiny, Grounding DINO→SAM 2 composition, Florence-2-base-ft, OmniParser v3 detector and official icon-caption components, DINOv2-small, Qwen3-VL-2B-Instruct. SAM 2/EfficientTAM temporal propagation also ran on four captured diagram frames.

SAM 3, SAM 3.1 and DINOv3 ViT-S/16 were probed with the user's existing authenticated Hugging Face credential. All checkpoint requests returned gated-access 403. `gated-access.json` records the specific limitation; no inference or quality result is claimed for them. No credential is written to this evidence directory. The user was given the access-request links.

## Fixtures and scoring

`fixture-sources.json` records public source URLs and captured-video provenance; `fixture-hashes.json` freezes the exact image bytes. The real UI screenshot is from OmniParser's own demo assets; the natural-object photo is from Grounding DINO's example. These are potentially in-distribution/demo-favorable examples, not held-out tests. The diagram/settings frame is captured from Qr3VsZYQy4s at 116 seconds. The temporal panel sequence uses captured frames at 106,112,114,116 seconds preserved in the preceding S2 branch evidence.

`ocr-cases.json` fixes 30 controlled synthetic single-line text crops: five strings, two themes, three font sizes, plus one manually transcribed real settings crop. The Windows Consolas font is used. Normalization collapses whitespace only; case and punctuation matter. Scores are exact-line equality and Levenshtein character error divided by expected length. All configurations were tested without training/tuning on this set. There is no held-out split, representative real-video corpus or manual correction-time study. Tesseract uses single-line PSM 7; EasyOCR uses its default English GPU reader; Paddle uses its mobile detector/English recognizer on CPU. These compare configurations, not hardware-normalized throughput.

Masks have no pixel-level ground truth. Positive/negative seed checks and visual extent inspection expose ambiguity; they do not establish segmentation accuracy. Tracking has one manually seeded panel across four sparse real states, not continuous-video drift/occlusion qualification. DINO matching tests five patches under a synthetic one-patch image translation. Its separate CLS similarity test uses a one-character text change; it is not a dense-feature tracking evaluation.

## Files and reproduction

- `ocr_bench.py <tesseract|easyocr|paddle>` saves exact text, confidence/geometry where supplied, per-case time and scores.
- `vision_bench.py <sam|sam2|efficientsam|efficienttam|groundingdino|florence|dinov2|omniparser>` saves prompts, pinned checkpoint revisions where available, raw outputs, model-memory allocation and timings.
- `tracking_bench.py <groundedsam2|sam2_tracking|efficienttam_tracking>` saves masks and region extents.
- `omni_caption_bench.py` probes four manually selected detected controls using the official fine-tuned caption checkpoint. This does not run the complete package's OCR/box-merging/GUI-control stack.
- `qwen_bench.py` bounds image resolution and output length; it tests literal objects, exact settings transcription and UI description, not action execution.
- `source-revisions.json` pins upstream source clones used by editable installs; environment snapshots pin installed packages. Weights/caches are not committed.
- `attempts/` preserves the initial EfficientTAM compile failure, the DINO default-center-crop confound, and initial segmentation outputs. The final EfficientTAM run disables optional compilation because native Windows lacks Triton. DINO's final configuration retains the full image instead of cropping away left-aligned text.

Scripts expect their directory as `root`, with the working directory at the repo root. Set up isolated Python 3.12 environments (vision, paddle, qwen). Vision used torch 2.11.0+cu128/torchvision 0.26.0 and transformers 4.51.3; Qwen used the same torch and transformers 4.57.6. Paddle used its own CPU environment to avoid framework conflicts. Upstream SAM/SAM2/EfficientTAM source clones live in `.scratch/models/` at the recorded revisions. Install them without dependency changes; SAM2's optional CUDA extension was disabled with `SAM2_BUILD_CUDA=0`. EfficientSAM imports its recorded source clone and bundled tiny checkpoint. OmniParser's detector imports only `util/yolov9.py` rather than the entire application dependency stack.

Example runs (after preparing those environments and clones):

```powershell
.venvs/vision/Scripts/python.exe docs/architecture/spikes/image-models/ocr_bench.py easyocr
.venvs/paddle/Scripts/python.exe docs/architecture/spikes/image-models/ocr_bench.py paddle
.venvs/vision/Scripts/python.exe docs/architecture/spikes/image-models/vision_bench.py groundingdino
.venvs/vision/Scripts/python.exe docs/architecture/spikes/image-models/tracking_bench.py sam2_tracking
.venvs/qwen/Scripts/python.exe docs/architecture/spikes/image-models/qwen_bench.py
```

`hf_context.py` discovers existing credentials in standard Hugging Face state or the explicitly authorized user TOML locations and places the token only in the current process environment. It never persists or prints the token. No checkpoint-approval form was submitted by the experiment.

## Interpretation

Use the main-checkout results report for the provisional per-job retention recommendation. A model completing inference is not proof of adequate quality. A gated or failed setup is not a negative model-quality result. Single-run warm/cold timings and allocator memory are observations, not production latency/VRAM requirements. No automatic integration or wholesale retirement of an existing engine follows from this spike.
