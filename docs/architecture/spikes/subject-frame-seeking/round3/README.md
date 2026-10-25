# Fresh real tutorial validation — frozen candidate

No production integration. Source: Traversy Media, [Git & GitHub Crash Course For Beginners](https://www.youtube.com/watch?v=SWYqp7iY_Tc). The source is newly acquired for this comparison, not a newly published tutorial. Source bytes/hash are in source-manifest.json; media is retained locally, not committed. Older software/version text is evidence of the recorded tutorial, not installation advice.

## Frozen experiment

Protocol, manual one-subject seeds, candidate function and reference labels were committed at834036e **before candidate inference**. `candidate_frozen.py` is byte-for-byte the select() function from round2 commit39275c6 (hash in protocol.json). No OCR mode, support count, rank, quality metric or template threshold changed: PSM7, two consecutive equal strings, first occurrence, sharpest representative, normalized template matching threshold0.8. Changing seed rectangles for a different source is the input adapter; it does not add scale search, semantic detection or a new tracker. collect.py reads no reference labels.

| Case | Source window | Scoped subject |
| --- | --- | --- |
| Scroll | 940–946s | Terminal's current command line, seeded at bottom; required states include completed add/status commands and the resulting multiline status evidence |
| Motion | 480–485s | Downloading Git heading during desktop/UAC interruption and camera zoom |
| Occlusion | 483.3–485s | Community navigation label covered by installer; overlaps motion window |
| Brief | 576–578.5s | Git Bash Here menu item; menu disappears, then reopens at a changed position/hover appearance |

456 window-frame observations represent405 unique source frames. Four windows from one source are correlated, and three cases contain only one state. Window selection used source surveys and displacement proposals to find the phenomena before candidate execution, not an outcome search. The navigation label is a geometry/visibility probe, not an established essential build step. The brief case starts while the first menu is already open; do not infer its full dwell time from this left-censored window.

## Reproduce

Use this branch's environment/FFmpeg/Tesseract5.4.0. Acquire the source through the experimental capture CLI's --download-source option, which reuses repo download mechanics. Full source hash must match. Then:

```powershell
uv run --no-sync python -m video_buddy.frames.spike_seek .scratch/seek-retained-source/SWYqp7iY_Tc.mp4 .scratch/seek-real-scroll3 940 946
uv run --no-sync python -m video_buddy.frames.spike_seek .scratch/seek-retained-source/SWYqp7iY_Tc.mp4 .scratch/seek-real-motion2 480 485
uv run --no-sync python -m video_buddy.frames.spike_seek .scratch/seek-retained-source/SWYqp7iY_Tc.mp4 .scratch/seek-real-occlusion3 483.3 485
uv run --no-sync python -m video_buddy.frames.spike_seek .scratch/seek-retained-source/SWYqp7iY_Tc.mp4 .scratch/seek-real-brief3 576 578.5
uv run --no-sync python docs/architecture/spikes/subject-frame-seeking/round3/collect.py
uv run --no-sync python docs/architecture/spikes/subject-frame-seeking/round3/audit_grid.py
uv run --no-sync python docs/architecture/spikes/subject-frame-seeking/round3/evaluate.py
```

Capture folders must not exist. Use committed reference.json for evaluation. To investigate annotation proposals, annotate.py recreates full-frame PSM11 TSV-derived lines; review_labels.py applies the recorded visual corrections. Neither is candidate tuning. The original proposals are retained losslessly as reference-proposals.json.gz. Inspect sheets include every window frame; filenames encode source presentation time. Individual JPEG hashes are retained in reference.json.

## Label limits and verified grid

Reference proposals used full-frame PSM11, followed by the same agent's visual inspection of every subject crop and selected full frames. Manual corrections are recorded, including small menu text that proposal OCR failed to read. This is not an independent human reference set. Terminal line geometry is uncertain for nine transition frames; two Community extents and eleven visibility/fade observations remain uncertain. Score intervals propagate these uncertainties. A full grid frame can establish known-visible text even when its local bbox is unknown.

All192 distinct grid requests were captured through the core extractor.184 matched the nominal first-at/after presentation time exactly;8 matched an adjacent decoded frame because of floating-point/request rounding and the extractor's three-decimal seek. The authoritative evaluator uses the pixel-verified index; nominal-grid-results.json retains the first calculation. Every actual seek matched a decoded frame exactly. No candidate output changed. Uncertain cases remain ranges, not forced failures.

## Evidence map

- reference.json / annotation-review.json: final labels, uncertainty, hashes, corrections; no selector output consumed in labeling.
- observations.json: all template confidence, accepted crop, OCR string, quality and measured stage time.
- candidate_frozen.py / protocol.json: unchanged algorithm and parameters, seed inputs, budget/offset contract.
- results.json: six budgets, four offsets, evidence indices, min/max coverage, redundancy and exact strings. Status-packet exact OCR is not meaningful as a one-line string. Shell-command exact matching removes one leading `$ ` only.
- grid-audit.json: actual seek/neighbor comparisons and costs, including all8 nominal-index corrections.
- *-inspect-*.jpg: exhaustive visual inspection sheets; *-comparison.jpg: cap4, midpoint grid versus frozen candidate with selected boxes.
- dashboard-data.json: exact compact min/max counts for the dashboard drill-in.
- source-manifest.json: source attribution/hash and correlated-frame counts.

This is one locked validation pass, not a latency benchmark or broad tutorial qualification. Independent annotation, additional sources, masks/semantic association, full-pipeline peak memory, human correction effort and task completion remain gaps. No new model installed, no provider credentials needed, and no retuning performed after inference. The candidate's scrolling failure is a negative result to preserve, not a reason to alter this run.
