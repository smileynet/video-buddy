# S3: OCR on held-out real-video text

Date: 2026-10-25. Ticket 14. **Verdict: retain the existing baseline; retain PaddleOCR for full-frame qualification and Tesseract for supplied-region qualification. No universal replacement or human correction-time improvement established.**

## Evidence and comparison

Throwaway branch `codex/spike-real-video-ocr`, commit `4df4a8dfd9892ef6cc8bba075f9adc1aa58b98bc`. [Frozen frames, labels, raw outputs, probes and environment](https://github.com/smileynet/video-buddy/tree/4df4a8dfd9892ef6cc8bba075f9adc1aa58b98bc/docs/architecture/spikes/real-video-ocr). Label freeze `7899183`; tuning selections committed in `ceb0f21` before held-out inference. Prototype stays separate from the application.

30 visually transcribed regions from two real videos: Fireship Python in 100 Seconds (`x7X9w_GIm1s`) and the retained audio-synthesis source (`Qr3VsZYQy4s`). Ten tuning regions from five Python frames; 20 held-out regions from three later Python frames and one diagram frame. No overlapping tuning/test frame. Captures used the CLI's existing experimental S2 flags; this does not establish clean-main acquisition portability (ticket 22).

Compared Tesseract 5.4 CPU, EasyOCR 1.7.2 English GPU and PaddleOCR 3.7 PP-OCRv5 mobile English CPU. Tune native/2x crops for all and PSM7/13 for Tesseract; select using tuning exact-match, then edits, then lower scale/PSM. All selected native scale; Tesseract selected PSM13. Full-frame paths use native engine detection (Tesseract PSM11), then assign detected boxes to each single-line reference ROI by center and sort left to right. Preserve raw boxes/confidence and separate full-frame association from recognition on supplied crops.

## Measured result

Twenty held-out lines, 350 normalized reference characters. Whitespace collapsed, punctuation/case retained; indentation/executable-code validity not assessed.

| Configuration | Crop exact lines | Crop character errors | Full-frame exact lines | Full-frame character errors | Empty full-frame associations |
|---|---|---|---|---|---|
| Tesseract | 14/20 | 13 / 3.71% | 10/20 | 77 / 22.00% | 2 |
| EasyOCR | 9/20 | 25 / 7.14% | 13/20 | 15 / 4.29% | 0 |
| PaddleOCR | 11/20 | 24 / 6.86% | 16/20 | 7 / 2.00% | 0 |

Full-frame context sometimes helped compared with tight crops. All options made literal code errors: missing underscores/punctuation/equal signs and i/1 confusion. The selected/cursor-obstructed `print(i)` case was read as `brint(i)` by all three; it remains in the primary result without post-hoc relabeling or exclusion. A readable-looking line is not enough for an executable guide.

This changes the earlier synthetic smoke impression: the best role depends on input framing. Paddle is the leading full-frame challenger here; Tesseract is the leading supplied-crop challenger. Keep EasyOCR as the current baseline until review 28 evaluates compatibility, costs and broader evidence. No automatic per-region routing rule was tested.

## Costs and scoring correction

Windows 11, Python 3.12.10, RTX5070. EasyOCR GPU; Paddle CPU four threads/MKLDNN off; Tesseract CPU. Held-out crop/four-full-frame OCR seconds: Tesseract 1.64/1.41; EasyOCR 0.79/1.74; Paddle 4.21/16.89. Engines ran concurrently, cold/warm behavior and configurations differ; these are observations, not a speed ranking. EasyOCR/Paddle model load was 3.77/2.51 seconds; Tesseract process/model initialization is inside each OCR call. Crop file-open/resize timing is separately recorded. EasyOCR allocator peak ~2.28GB; CPU peak and whole-device/minimumVRAM were not measured. Existing dependency setup/download costs were excluded; versions and actual asset hashes are preserved.

An initial scoring rule sorted fragments by quantized vertical position, reordering pieces of the same line. Corrected all engines to left-to-right ordering within these single-line ROIs, without rerunning OCR or changing labels/configs. Initial outputs are retained under `attempts`; `rescore_lines.py` reproduces the correction. Reported counts are from corrected association.

## Validation and unresolved outcomes

Actual tuning and held-out inference completed for all three engines. Verified frozen pixel/label hashes unchanged, each engine has 20 crop and 20 full-frame region scores, and held-out crop configs match committed tuning choices. Pre-commit including secret checks passed on all experiment files. No production code or dependency integration.

This is a bounded source-correctness comparison, not full qualification: two selected English domains, large readable code/labels plus two small code lines, one visual annotator, no independent annotation or representative sampling. No measured human correction time, task completion, multilingual coverage, motion/blur/occlusion recall or statistical generalization. Edit counts are a literal correction proxy only. Region-empty counts are not annotated detector precision/recall. Crop punctuation errors remain meaningful despite whitespace normalization.

Tickets 25 and 23 continue complete-state/association and model qualification. Tickets 18/21 own correction/usability observations; ticket 28 decides whether to integrate any candidate. Close S3 with this bounded per-job verdict and leave those outcomes explicitly unresolved.
