# Subject-aware frame seeking: first matched-window comparison

**Latest follow-up:** [fresh real tutorial validation](subject-frame-seeking-real-validation.md) records a negative result for the frozen event candidate. [The intermediate stress comparison](subject-frame-seeking-stress-results.md) contains the earlier offset sweep and designed controls.

**Ticket 25 · 25 October 2026 · partial qualification, no integration.** On one held-out code window, crop/OCR seeking recovered all three visible revisions, but a four-frame time grid did too. The existing selector returned no frames. Dense capture alone did not fix its whole-image inclusion veto. Keep the simple time-grid control in future comparisons; no benefit over that control is established yet.

## What was compared

The job is to preserve evidence someone needs to reproduce a technique: complete filenames, code revisions and their order. “Recovered state” means a selected image visibly contains the entire labeled line. It does not mean the line is executable or OCR is exact.

Source: [Fireship, Python in 100 Seconds](https://www.youtube.com/watch?v=x7X9w_GIm1s). Decode every source frame inside two frozen windows, retaining presentation timestamps with FFmpeg showinfo: 59–63 seconds (120 frames, filename preparation) and 73–78 (150 frames, code revisions, evaluation). Both are 1920×1080, approximately 30fps. Every decoded crop is represented in the committed contact sheets. Source/file hashes, boxes, labels, all OCR outputs, capture logs and scripts are preserved in the evidence branch below.

One fixed subject box was manually seeded for each window. This deliberately tests seeking **after** subject identification; it does not qualify automatic detection, association or moving-camera tracking. The filename window is the tuning-role split; no threshold search was performed. The evaluation window was held out from configuration changes, but is in the same previously inspected tutorial/domain. One agent annotated and checked crops; no independent annotator.

The shared upper output budget was four frames per window:

| Option | Candidates and selection |
| --- | --- |
| Existing sparse | Existing core `extract_frames`, 2 fps, then unmodified `select_frames(max_frames=4)` |
| Dense existing | All decoded frames, same unmodified selector and cap |
| Time-grid control | Four midpoint seeks evenly spaced over the same window, via existing core extractor |
| Subject seek | All decoded frames; fixed crop, Tesseract PSM13, exact recognized-string groups supported by at least six frames; four most-supported groups; maximum crop Laplacian variance per group; restore time order |

The six-frame support is total frequency, not necessarily contiguous. Cursor variants and repeated OCR errors can become separate groups. OCR settings follow ticket 14's crop probe; there was no held-out parameter sweep. This is a throwaway baseline for subject seeking, not an optimal or complete temporal algorithm.

## Results

| Window / option | Selected | Visible states recovered | Missed revisions | Redundant state frames | Other frames |
| --- | ---: | ---: | --- | ---: | ---: |
| Filename / existing sparse | 0 | 0/2 | `hello.py`, `hello.ipynb` | 0 | 0 |
| Filename / dense existing | 0 | 0/2 | Both | 0 | 0 |
| Filename / time grid | 4 | 2/2 | None | 0 | 2 |
| Filename / subject seek | 4 | 2/2 | None | 2 | 0 |
| Held-out code / existing sparse | 0 | 0/3 | All | 0 | 0 |
| Held-out code / dense existing | 0 | 0/3 | All | 0 | 0 |
| Held-out code / time grid | 4 | 3/3 | None | 1 | 0 |
| Held-out code / subject seek | 4 | 3/3 | None | 1 | 0 |

The three code states are `hello = 'hi mom'`, the visible intermediate `hello, hola = 'hi mom'`, then `hello, hola = 'hi mom', 'hola mamá'`. The intermediate state is an unfinished instruction, retained to show the edit; it is not presented as valid unpacking code. Its visible span is about 0.534 seconds. Partial filename prefixes are not essential final states. A brief subject disappearance in the filename window is excluded from readable spans.

**Exact OCR recovery differs sharply from image coverage.** With whitespace collapsed but punctuation, case and accents retained, subject seeking recovered 1/2 filename strings exactly, versus 0/2 for the time grid. Both recovered 0/3 exact code strings. Curly quotes, cursor artifacts and a lost accent remain. No human correction time, successful execution or task-completion benefit was measured.

Full-size crop QA corrected an initially misread filename transition: notebook text begins at 61.5615 seconds, not 61.662. It also aligned span endpoints to actual presentation times rather than rounded milliseconds. The original score is retained as `initial-label-results.json`; only labels were corrected, with no algorithm/selection changes. Final values above supersede the initial tuning recall. No observed wrong subject region in these fixed boxes establishes a general association-error rate.

## Why the baseline was empty

Whole-image edge density was 0.301–1.008% in the filename window and 0.301–0.608% in the code window. The core requires 2% for `should_include`; its selection loop rejects excluded candidates while the selected count is below half the cap. With all candidates excluded it never fills that initial quota. This is a concrete failure for sparse text on a mostly empty editor, not a model comparison.

A **post-hoc diagnostic**, not a second held-out experiment, forced only that inclusion flag true while retaining ranking, whole-image hashes and buckets. Sparse selection then recovered 1/2 filename states and 3/3 code states. Dense selection recovered 1/2 and 2/3; the intermediate code revision disappeared. Density by itself is therefore insufficient. Ticket 35 owns a later reviewed fix and regression coverage; this spike changes no production default.

## Measured cost and constraints

Single sequential runs on Windows 11, Python 3.13.14, Tesseract 5.4.0.20240606. OCR/scoring used CPU; the RTX 5070 was not used. These timings include process startup and JPEG I/O and are not stable benchmark estimates.

| Stage, seconds | Filename | Held-out code |
| --- | ---: | ---: |
| All-frame decode + JPEG write | 0.304 | 0.344 |
| Crop load/quality/OCR combined | 9.674 | 15.294 |
| Of that, OCR subprocess time | 9.039 | 14.214 |
| Sparse 2 fps decode/write | 0.147 | 0.143 |
| Existing sparse selection | 1.474 | 0.159 |
| Existing dense selection | 2.004 | 2.418 |
| Four time-grid seeks/write | 0.430 | 0.431 |

Subject seeking considered 120/150 frames versus 8/10 sparse candidates and four time-grid output seeks. Time-grid OCR was only a separate output audit, not its selection cost. Detection/association were manual, tracking was absent, and peak RAM/process-tree memory was **not measured**. Do not turn absent measurements into zero cost. The first sparse timing includes cold imports. Capture/selection/OCR totals are different stages and should not be collapsed into a universal speed ranking.

Initial acquisition failed HTTP 403 with locked yt-dlp 2026.3.17. Updating the isolated environment to 2026.10.21 succeeded; `uv run --no-sync` was required because a normal frozen run restored the older installed version. No dependency lock or production acquisition behavior changed.

## Disposition and next evidence

Keep ticket 25 **in progress**. This first comparison establishes the selector failure, shows dense crop seeking can retain a brief intermediate edit, and shows a simple grid matches its held-out coverage here. It does not establish optimal frames, automatic subject search, revision-safe deduplication or general superiority.

| Question | Current answer / remaining work |
| --- | --- |
| Do boxes suffice? | For these stationary text lines, a box contains the complete subject. No mask benefit measured. |
| Should we add masks/tracking? | Unresolved for moving subjects, occlusion and competing elements. Prior SAM evidence is insufficient to infer a benefit here. |
| Does seeking beat the simple grid? | No observed recall advantage here. Add independently labeled brief states that fall between grid points; vary grid offset and budget before any winner claim. |
| Can we preserve diagram/settings instructions? | Exploratory 210-frame settings capture exists, but changing numeric values were not exhaustively labeled/scored. Still open. |
| Remaining corpus coverage | Real scrolling, blur, occlusion, moving/absent subjects and distinct diagram states; additional sources and independent label checks. |
| Remaining measurements | Detection/association and tracking costs/errors, peak memory, correction effort, and actual build/verification outcomes. |

Continue with a frozen moving/scrolling/brief-state corpus and a grid-offset/budget comparison. Require source-wide window discovery separately from within-window seeking. Keep final integration/architecture review 28 gated by these limits and the other open spikes.

## Durable evidence

- Raw prototype/evidence branch: `codex/spike-subject-frame-seeking`, commit [`63082cff1f7f74e99d38dd4a955fa74364b30803`](https://github.com/smileynet/video-buddy/tree/63082cff1f7f74e99d38dd4a955fa74364b30803/docs/architecture/spikes/subject-frame-seeking).
- [All 270 decoded subject crops, manifests, corrected labels, selected images, raw outputs and reproduction](https://github.com/smileynet/video-buddy/blob/63082cff1f7f74e99d38dd4a955fa74364b30803/docs/architecture/spikes/subject-frame-seeking/README.md).
- Verification: existing frame tests: 5 passed; capture counts, strictly increasing presentation times and window bounds checked; pre-commit passed after fixing a JSON final newline. No production integration or new API access required.
