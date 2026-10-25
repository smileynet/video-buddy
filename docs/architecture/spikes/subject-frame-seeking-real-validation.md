# Fresh real tutorial validation of frozen event seeking

**Latest follow-up:** [ticket 36 revision-boundary comparison](revision-boundary-results.md) tested two new alternatives and locked validation. Full context helped, but the preferred packet heuristic missed a later checkpoint; no default was adopted.

**Ticket 25 · 25 October 2026 · negative default-selection verdict, no integration.** The unchanged candidate that succeeded on designed controls failed to preserve the required scrolling states in a fresh tutorial: **0/3 at every tested cap from 1 to 8**. A whole-frame grid preserved all three at some offsets. Do not adopt this candidate as the production default. Ticket 36 owns a separate revision-boundary spike; this validation was not retuned.

## Fresh source and frozen contract

Source: [Traversy Media, Git & GitHub Crash Course For Beginners](https://www.youtube.com/watch?v=SWYqp7iY_Tc). This is a new source for the comparison, not a newly published video. Recorded software versions are historical evidence, not current installation recommendations.

Four natural windows cover terminal scrolling, browser camera zoom, installer obstruction and a context menu disappearing/reopening elsewhere. They contain 456 window-frame observations /405 unique source frames; the two browser windows overlap. Three cases have only one target state. These are correlated, purpose-selected windows from one tutorial, not a population benchmark.

Protocol, seed rectangles, reference labels and the frozen selector were committed at `834036e` **before inference**. The selector function is byte-identical to round2's `select()` (SHA-256 `48569e78870c74a6a97c603bc47d2ce98cc035d4b4f5d5360b554feed0aa65ae`). The candidate retained PSM7, two consecutive identical OCR strings, first-occurrence ranking, sharpest representative, and normalized template matching at 0.8. No parameter or OCR change followed the results. Seed/header and subject rectangles are manual inputs for each new source, not an added semantic detector or scale-aware tracker.

The build-and-verify job defines the important scrolling evidence: retain the completed add command, completed status command, and resulting status packet. A partial command is not a useful replacement for a completed command or its checkpoint.

| Case | Source seconds | Target / scope |
| --- | --- | --- |
| Scrolling | 940–946 | `git add .`, `git status`, and post-add status evidence; the required lines move inside the terminal |
| Motion | 480–485 | Downloading Git heading before/after desktop interruption and camera zoom; one repeated content state |
| Occlusion | 483.3–485 | Community navigation label covered by installer; a visibility probe, not a demonstrated essential build step |
| Brief UI | 576–578.5 | Git Bash Here menu item, disappearance and reappearance with changed position/hover rendering |

The brief-menu clip starts after the first menu is open. Its observed first appearance lasts about one second inside this window; do not treat that as its full dwell time or equate it with the earlier 0.20 second authored message. The terminal's final status is available only near the end of the window, but is not claimed to be short-lived in the full source.

## Matched budgets and offsets

Caps: **1,2,3,4,6,8**. Grid offsets: **0,.25,.5,.75** of a sample interval. Grids preserve full images; the candidate must retain the intended text inside its crop. Cap means an upper limit; the candidate need not fill it.

| Frame cap | Scrolling grid: states covered at offsets 0/.25/.5/.75, out of 3 | Frozen candidate |
| --- | --- | --- |
| 1 | 0 / 0 / 1 / 1 | 0/3 |
| 2 | 1 / 1 / 1 / 2 | 0/3 |
| 3 | 1 / 1 / 1 / 2 | 0/3 |
| 4 | 1 / 1 / 2 / 3 | 0/3 |
| 6 | 1 / 2 / 2 / 3 | 0/3 |
| 8 | 2 / 2 / 3 / 3 | 0/3 |

At cap 8, the candidate's eight chosen frames end at 941.933 seconds, before the completed add command at 942.067 seconds. Raw strings include partial typing and OCR variants. Two-frame persistence at 30 fps is only about 0.067 seconds; it is not an event-completion test. Earliest-string ranking spent the budget before the completed instructions. A stable window-header match did not establish that the useful inner content had been recovered.

| Other natural cases, cap 4 | Grid coverage at four offsets | Candidate | What this establishes |
| --- | --- | --- | --- |
| Motion, one state | 1 / 1 / 1 / 1 | 1/1 | Captured early heading; not continuous tracking through zoom |
| Occlusion, one state | 1 / 1 / 1 / 1 | 1/1 | Captured before obstruction; not recovery of hidden writing |
| Brief menu, one state | 1 / 1 / 1 / 1 | 1/1 | Captured first appearance; did not track the reopened menu |

The candidate's last accepted browser match was 483.5 seconds, before the later zoomed pose, and its last accepted menu match was 577.0 seconds, before the reopened menu. Early one-state recall therefore overstates temporal qualification. At a one-frame budget some grid offsets miss these cases or land on an uncertain fade; from cap3 upward all tested offsets cover the single state. The dashboard retains every budget/offset, including uncertainty intervals.

The saved browser heading's OCR was exact. The menu image was useful but its string read `Git Bach Here`; the Community string had a spurious leading quote. No completed command or status packet was retained by the candidate within the tested budgets. Visual-state coverage, exact writing, track retention and guide usefulness remain separate measures. No human correction effort or task-completion improvement was measured.

## Reference and capture checks

All scoped frame observations were reviewed through exhaustive crop sheets and selected full frames. Full-frame PSM11 supplied annotation proposals; the same agent corrected command boundaries and tiny menu text before candidate execution. This is **OCR-assisted, single-agent reference work**, not an independent human ground truth.

Nine terminal transition frames and two navigation extents retain uncertain geometry; eleven overlay/menu fade observations retain uncertain visibility. Known-visible text in a full frame can be scored even when its local extent is uncertain. Candidate coverage is reported as lower/upper bounds; uncertain observations are not forced misses. The scrolling0/3 result is unchanged by these bounds. Proposed labels, corrections and original annotations are all retained.

All 192 distinct grid requests were executed through the existing core extractor. 184 matched the nominal first-at/after decoded frame exactly; 8 matched an adjacent frame because of floating-point/request rounding and the extractor's three-decimal seek. The final grid scores use the pixel-verified indices. The nominal calculation remains available, and its correction did not change the coverage table above. Every actual seek matched a decoded frame exactly.

## Stage costs and limitations

Single sequential CPU run, Tesseract 5.4.0.20240606. Costs include JPEG I/O and OCR subprocess startup and are not repeated latency estimates.

| Stage | Scroll 180 frames | Motion 150 | Occlusion 51 | Menu 75 |
| --- | ---: | ---: | ---: | ---: |
| Dense decode/write, seconds | .230 | .215 | .146 | .165 |
| Template search, seconds | 1.965 | 1.595 | .459 | .766 |
| Accepted-crop OCR, seconds | 13.611 | 5.155 | .460 | 2.057 |
| Accepted template matches | 180 | 73 | 7 | 31 |
| Four midpoint core seeks, summed cached seconds | .372 | .373 | .373 | .395 |

Accepted-match counts include only this manually seeded primitive; they are not an association-accuracy score. Peak memory was not remeasured for this run. The previous collector's memory estimate must not be transferred to this source or to the complete pipeline. No segmentation/mask model was added. Independent references, multiple fresh tutorials, semantic subject association, mask benefit, source-wide discovery and human correction/task outcomes remain gaps.

## Disposition

**Reject the frozen candidate as a default selector.** Keep it as a reproducible negative control. Keep the time grid as a cheap baseline, with coverage gaps visible: it also misses the status checkpoint at many offsets.

Ticket 36 will compare event boundaries that distinguish typing prefixes from completed revisions, preserve result/checkpoint context, and account for text scrolling inside a stable window. These windows are now observed development evidence; a revised candidate needs new locked validation windows. Do not quietly turn this failed test into tuning evidence and keep calling it held-out.

Ticket 25 stays in progress for the broader qualification gaps; ticket 35 still owns the production selector's global inclusion veto. Review 28 now includes 36 and remains the gate for app features, architecture and integration. Prototype code remains separate from production.

Raw inputs, frozen source, labels, original and corrected grid mappings, OCR outputs, exact costs, screenshots and reproduction: [`codex/spike-subject-frame-seeking`, commit 181e209](https://github.com/smileynet/video-buddy/tree/181e209def0389a57b0b4192b4acb2447682f6e4/docs/architecture/spikes/subject-frame-seeking/round3). Existing frame tests: 5 passed; original selector hash, 456 observations/405 unique timestamps and all 192 actual seeks verified; pre-commit passed.
