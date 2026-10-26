# Subject-aware frame seeking: first matched-window comparison

**Final synthesis:** [ticket 25 disposition](#final-ticket-25-synthesis--25-october-2026) closes the bounded comparison with findings and explicit gaps. **Latest experiment:** [revised boundaries](revision-boundary-results.md). **Earlier follow-up:** [fresh real tutorial validation](subject-frame-seeking-real-validation.md) records a negative result for the frozen event candidate. [The intermediate stress comparison](subject-frame-seeking-stress-results.md) contains the earlier offset sweep and designed controls.

**Ticket 25 · 25 October 2026 · bounded comparison complete, no integration.** On one held-out code window, crop/OCR seeking recovered all three visible revisions, but a four-frame time grid did too. The existing selector returned no frames. Dense capture alone did not fix its whole-image inclusion veto. Keep the simple time-grid control in future comparisons; no benefit over that control is established yet.

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

## Final ticket 25 synthesis — 25 October 2026

**Bounded comparison complete. Retain current production behavior; no new selector or model is adopted.** Seeking can preserve useful revisions, but no general quality/cost advantage over the simple time-grid control was established. Ticket 36's packet candidate failed locked validation. Settled-run selection remains a conditional challenger, not a default.

The original tables above are first-round observations, not pooled accuracy. The later rounds use different windows, policies and reference certainty; configurations and overlapping frames are not independent trials.

| Evidence round | Finding | Decision limit |
| --- | --- | --- |
| First matched windows (this report) | Seek and grid both retained 3/3 code states at cap 4; production selector retained zero. Both exact-code OCR 0/3. | Stationary seeded boxes, same source, no independent reference. Ticket 35 owns the production veto failure after review 28. |
| [Controlled stress and offset sweep](subject-frame-seeking-stress-results.md) | Grid depended on offset/budget. Post-hoc tracked/event diagnostic retained 12/12 authored states/strings; original motion policy failed. | Diagnostic changed after controls; authored invariant-header tracking does not qualify natural subject association. |
| [Fresh natural validation](subject-frame-seeking-real-validation.md) | Unchanged event candidate retained 0/3 scrolling states at every tested cap 1–8; partial strings consumed the budget. | Other early one-state captures did not qualify later zoom, occlusion or menu reappearance. Reject this candidate as default. |
| [Revised boundaries, ticket 36](revision-boundary-results.md) | 180 development / 509 locked validation frames. Packets: 3/3 development but only 2 confirmed, at most 3/4 terminal validation states at every cap. Settled/grid: 4/4 terminal at cap 4. UI fallback: 3/3 visual states at cap 2. | Repeated-command occurrence identity lost the final checkpoint. UI is edited demonstration evidence, not command execution. Settled policy was not substituted as preferred after validation. |

### Acceptance-criterion disposition

| Scoped question | Evidence and answer | Remaining gap / owner |
| --- | --- | --- |
| Complete-state recall | Exhaustive scoped decoded-frame references support the per-round counts above; locked validation retains uncertainty bounds. | References are same-agent/OCR-assisted, not independently adjudicated. Wider-source generalization is unqualified; 37 requires new independent references if activated. |
| Missed revisions, duplicates, wrong associations | Initial seek/grid each had one redundant code frame. Prefix budget loss and packet occurrence failure are explicit misses. Ticket 36 settled cap-4 terminal output had six redundant state occurrences; packets had none but missed a checkpoint. | Seeded boxes and easy controlled header tracking cannot establish a general association error rate. Repeated-command/history-loss and dynamic geometry remain 37. |
| Exact settings/commands and correction effort | Initial exact code 0/3; ticket 36 settled terminal OCR 1/3 literal targets, with filename/quote errors; neither selected UI command exact. Retain full frames, timestamps, raw text and uncertainty. | No measured human correction time or successful build outcome. Task outcomes remain 21; blocked-step correction UX remains 18. Do not present OCR as copy-ready commands. |
| Frame count and stage costs/memory | First code crop/OCR 15.294 s plus .344 s decode versus .431 s grid acquisition. Ticket 36 validation OCR 75.77 + 24.85 s, versus .376/.454 s four-grid acquisition per window. Collector RSS 88.7 MiB; controlled round 83.8 MiB. | Single runs, different stage boundaries; grid OCR audit is separate from acquisition. Manual detection has no measured automated detection cost; no full-pipeline memory or absent-stage zero-cost claim. |
| Boxes versus masks/tracking | Seeded stationary boxes contained the first text subjects. Tracking helped one authored moving-header fixture. Existing model probes did not demonstrate a mask benefit for this job. | Moving extent, occlusion, competing referents, diagram/settings completeness and source-wide discovery remain explicitly unqualified in 37. Modality/action-order comparison remains 26. |

### Closure and integration constraints

The bounded exit accepts negative and unresolved dispositions; it does not certify an optimal selector. No more inference is required to close 25. Broader tracking research is deliberately deferred in ticket 37 until a concrete task failure warrants one frozen question and new locked references. No broad tracking, mask or semantic-association feature is validated by this closure.

Review 28 must retain these limits when deciding architecture and features. Ticket 35 remains a separate post-review production fix; 26 covers ordered stills versus supported video; 21/18 cover observed user outcomes and correction. Keep checkpoints explicitly unverified until their meaning/result is checked. A returned prompt, readable frame or low redundancy does not prove successful execution.

## Durable evidence

- Raw prototype/evidence branch: `codex/spike-subject-frame-seeking`, commit [`63082cff1f7f74e99d38dd4a955fa74364b30803`](https://github.com/smileynet/video-buddy/tree/63082cff1f7f74e99d38dd4a955fa74364b30803/docs/architecture/spikes/subject-frame-seeking).
- [All 270 decoded subject crops, manifests, corrected labels, selected images, raw outputs and reproduction](https://github.com/smileynet/video-buddy/blob/63082cff1f7f74e99d38dd4a955fa74364b30803/docs/architecture/spikes/subject-frame-seeking/README.md).
- Verification: existing frame tests: 5 passed; capture counts, strictly increasing presentation times and window bounds checked; pre-commit passed after fixing a JSON final newline. No production integration or new API access required.
