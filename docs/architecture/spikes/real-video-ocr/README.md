# Real-video OCR throwaway experiment

Ticket14, frozen before OCR runs 2026-10-25. Branch codex/spike-real-video-ocr. No production integration.

Source acquisition/capture used the CLI: fetch x7X9w_GIm1s (Python in100Seconds, Fireship), frames --at30,40,50,60,70,80,90,100,110,120 --ocr off. Exact committed images are unmodified captures at30/40/60/70/80/90/100/120 seconds. Second source is retained Qr3VsZYQy4s at820.985 seconds, an audio-synthesis slide. Capture flags are experimental S2 flags, not shipped main CLI. Existing environment/workspace reused.

30 manually visually transcribed regions, no OCR-derived labels:10 tuning from five earlier Python passages;20 held-out from three later Python passages and the diagram slide. Split is by captured frame, no overlapping tuning/test image. Two videos only, same video style across some splits; not unseen-domain evaluation. Crops deliberately include legible lines, not random-frame prevalence. English only. No synthetic blur/degradation. Typing cursor and selection examples present; motion/blur/occlusion not qualified. All labels and original bytes frozen before inference; SHA256 in frozen-hashes.json. Inspect label-contact.jpg.

Compare EasyOCR1.7.2 English GPU, Tesseract5.4 English CPU, PaddleOCR3.7 PPv5mobileEnglish CPU in their existing isolated environments. Tune crop scale1 or2 (Lanczos) for all; Tesseract also PSM7 vs13. Choose by tuning exact recovery, then total Levenshtein edits, then smaller scale/PSM7. Freeze selection before held-out runs. Do not tune detector thresholds on held-out. Native full-frame detection uses engine defaults (Tesseract PSM11), measured separately; assign detected boxes to labeled regions by box center then sort by reading order. Full-frame box association can split/merge regions and is part of that measured path, not a pure recognizer comparison. Preserve raw boxes/text/confidence.

Whitespace collapsed for line scoring, punctuation/case retained. Indentation and exact original whitespace are NOT scored; these are line-text matches, not executable-code validity. Exact-match/CER and edit counts measure literal transcription only. Report empty associations and no-text results, not false claims of annotated detection IoU/recall. No participant correction time or task-completion study; edit counts are a proxy, not measured effort.

Record model load, preprocessing, OCR, full-frame vs crop cost separately. Timing single-run mixed cold/warm, CPU/GPU configurations differ; no universal speed/memory ranking. Preserve failures and allocator peak. Budget one active day excluding prior setup/downloads; bounded result may retain baseline or leave default choice unresolved.

## Observed bounded result

Held-out:20 regions/350 normalized reference characters from four frames. Tuning selections frozen in commit ceb0f21 before held-out inference; label/byte freeze commit7899183. All engines selected native scale; Tesseract selected PSM13 on crops, PSM11 on full frames. EasyOCR/Paddle crop PSM field is irrelevant (native engine defaults).

| Engine | Crop exact | Crop edits / micro CER | Full-frame exact | Full-frame edits / micro CER | Empty full-frame associations |
|---|---|---|---|---|---|
| Tesseract |14/20|13 /3.71%|10/20|77 /22.00%|2|
| EasyOCR |9/20|25 /7.14%|13/20|15 /4.29%|0|
| PaddleOCR |11/20|24 /6.86%|16/20|7 /2.00%|0|

**Verdict:** retain the current baseline pending final integration review28. Retain Paddle as a full-frame challenger and Tesseract as a supplied-region challenger. This reverses the universal-looking impression of the earlier synthetic smoke results. No automatic routing policy, wholesale replacement or improvement in actual human correction time was demonstrated. Full-frame context sometimes helped compared with tight crops. Missing punctuation, underscores, equal signs and i/1 confusion matter even when prose looks plausible. The cursor/selection on case18 is a shared hard case (all three read brint rather than labeled print); no post-hoc exclusion or label change was used to improve scores.

**Scoring repair:** initial full-frame association sorted fragments by quantized top-y then x, which reordered parts of the same line. Every reference ROI is single-line, so final association sorts included fragments by x only. This is a common harness correction after inspecting outputs, not OCR parameter tuning. Raw first-pass outputs are preserved under attempts/*-quantized-y.json; rescore_lines.py reproduces final scoring without another inference pass. Cases, pixel bytes and selected configs were unchanged.

**Costs:** single-run, concurrently executed engines and different CPU/GPU settings; not a latency ranking. Held-out20-crop/four-frame OCR seconds: Tesseract1.64/1.41, EasyOCR0.79/1.74, Paddle4.21/16.89. These include per-call conversion/serialization/invocation; crop file-open/resize time is separately recorded. Model-load fields: Easy3.77s, Paddle2.51s. Tesseract runs a separate process per invocation, so model initialization is included in its OCR seconds, not the near-zero outer load field. EasyOCR peak CUDA allocator2,275,004,416 bytes includes full-frame processing; whole-device/minimumVRAM and CPU peak memory were not measured. Prior setup/downloads are excluded; no full workflow throughput claim.

**Reproduce:** use the isolated environments documented in ../image-models/README.md. From repo root run bench.py ENGINE tune in the matching environment, inspect saved ENGINE-selection.json, then bench.py ENGINE heldout. Frozen configs/results are already committed for review. rescore_lines.py preserves initial ordering outputs; summarize.py recalculates counts and captures installed model asset hashes. vision-environment.txt, paddle-environment.txt and runtime-and-assets.json record versions and exact cached weights/traineddata hashes; weights themselves are not committed. build_fixtures.py recreates crops from committed frames, not downloaded originals.

**Limits left to integration review:** two selected English video domains,30 regions,20 test lines, a single visual annotator, no independent annotation, no blur/motion/occlusion population, no representative corpus confidence interval, no task-execution/correction study. Whitespace-normalized line matches are not valid-indentation/executable-code checks. No per-pixel detector ground truth or world-wide language verdict. More windows belong to25; real correction/usability observations belong to18/21. This ticket can close with a bounded per-job verdict and explicit unresolved human benefit, not production qualification.
