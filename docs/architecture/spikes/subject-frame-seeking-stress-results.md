# Frame seeking under scrolling, motion, occlusion and brief states

**Ticket 25 · 25 October 2026 · experiments, not integrated.** The earlier real-video result depended on grid alignment: at a four-frame budget, only **one of four offsets** retained all three code revisions. Controlled clips exposed failures in the original seeker too. A revised short-event/PSM7 diagnostic recovered all three clean states in each control with three selected frames, but it was changed after inspecting the fixtures and needs fresh validation.

## Scope and comparison

The end job remains preserving every instruction or confirmation someone needs to build and verify a result. A brief saved-setting message matters even when a longer unchanged screen is easier to sample.

This round adds four **authored UI controls**, each six seconds at 20 fps and 960×540, plus an offset/budget sweep on the earlier two real tutorial windows. The new 480 frames have renderer geometry/obstruction labels and exhaustive subject-crop sheets. They are not natural tutorial evidence. An exploratory real Python 113–125 second capture was inspected but not added to scored coverage; it does not establish natural scrolling/occlusion qualification.

Budgets are upper caps of **1,2,3,4,6,8** frames. Grid offsets are **0,.25,.5,.75** of one sampling interval, with request time `(i+offset)*duration/budget`. A grid keeps the whole image. It needs no spatial tracking, whereas a cropped seeker must keep the intended text in view. The 96 controlled and 48 real grid configurations are correlated views of six windows, not 144 independent trials.

| Selector | Subject association | State selection |
| --- | --- | --- |
| Earlier seeker | Fixed seed crop, or invariant-header template relocalization | Tesseract PSM13; exact-string groups supported by six total frames; descending frequency; sharpest crop per group |
| Tracking ablation | Static crop versus header template search | Same settings within each OCR pass |
| Event candidate | Header template search | Two consecutive identical OCR strings; preserve unique strings in first-occurrence order; sharpest representative |
| Diagnostic OCR pass | Same boxes, tracker and selection rules | Switch PSM13 to PSM7 after a clear-crop spot check exposed incorrect OCR |

The tracker consumes only the first manually seeded header and frame pixels. It never reads the renderer trajectory or target strings. An invariant header makes this an easy controlled association problem, not automatic subject discovery. No parameter sweep selected a best offset or budget.

## Real video: midpoint success was not robust to offset

Earlier source and corrected labels: [first matched-window report](subject-frame-seeking-results.md). The code window includes a roughly 0.534 second intermediate edit. These are the same previously inspected tutorial/domain, not new held-out footage. Grid variants map requests to the first source presentation time at or after each request.

| Frame cap | Filename: states covered at offsets 0/.25/.5/.75, out of 2 | Code: states covered at offsets 0/.25/.5/.75, out of 3 | Earlier seeker: filename / code |
| --- | --- | --- | --- |
| 1 | 0 / 0 / 1 / 1 | 1 / 1 / 1 / 1 | 1 / 1 |
| 2 | 1 / 1 / 1 / 2 | 1 / 2 / 2 / 2 | 2 / 1 |
| 3 | 1 / 2 / 2 / 2 | 2 / 2 / 2 / 3 | 2 / 2 |
| 4 | 2 / 2 / 2 / 2 | 2 / 2 / 3 / 2 | 2 / 3 |
| 6 | 2 / 2 / 2 / 2 | 3 / 2 / 3 / 3 | 2 / 3 |
| 8 | 2 / 2 / 2 / 2 | 3 / 3 / 2 / 3 | 2 / 3 |

More grid samples are not monotonically better because changing the budget also moves every sample. The seeker retained all code revisions from cap 4 upward in this sweep. That is a useful local difference from the grid, not a general accuracy ranking. Original exact code OCR remains 0/3; it was not silently corrected or rerun with the controlled diagnostic settings.

## Controlled stress results

The score is **clean, complete-state coverage**: all text glyphs visible, no renderer occlusion, predeclared severe-blur transition frames excluded. It is not a human readability measurement. Extent checks use the actual text bbox, not blank padding around a crop. The initial padded-viewport score and both OCR passes are retained for audit.

| Control | What changes | Grid coverage with cap 3, four offsets | Earlier tracked PSM13/frequency, cap 3 | Diagnostic tracked PSM7/events, cap 3 |
| --- | --- | --- | ---: | ---: |
| Scrolling | Viewport traverses three lines with clipped transitions | 3 / 3 / 3 / 3 | 3/3 | 3/3 |
| Motion + blur | Panel translates; eight transition frames deliberately blurred | 1 / 3 / 3 / 3 | 0/3 | 3/3 |
| Occlusion | Middle state clear only for 0.25 seconds after obstruction lifts | 2 / 2 / 2 / 2 | 2/3 | 3/3 |
| Brief UI state | Middle message lasts 0.20 seconds, four frames | 2 / 2 / 2 / 2 | 2/3 | 3/3 |

The diagnostic is **post-hoc**, on the same already observed controls. Its 12/12 selected state strings were also exact under whitespace-only normalization, with no duplicate, obstructed or incomplete selection at cap 3. This contrasts with the untouched real-code result; artificial stage labels are much easier than code punctuation and accents.

The same PSM7 pass separates the effects:

- **Scrolling:** static/frequency, tracked/frequency and tracked/events all 3/3. Tracking adds no coverage for a stationary viewport here.
- **Motion:** static/frequency 0/3 (three incomplete crops), tracked/frequency 3/3 and tracked/events 3/3. Relocalization matters; a mask was not needed in this controlled case.
- **Occlusion and brief message:** static/frequency and tracked/frequency both 2/3, tracked/events 3/3. Six-frame support discards the five-frame/four-frame middle-state evidence. No mask can recover text hidden throughout a selected instant; the useful operation was finding a later clear instant.

Four-frame grids recovered the occlusion control at one of four offsets and the brief control at none. At cap 8, two of four offsets covered the occlusion control and one covered the brief control. Larger caps still did not guarantee complete evidence. All offset/budget values and the weaker original event-selector outputs remain in raw results. The dashboard drill-in compares the grid, earlier frequency seeker and PSM7 event diagnostic.

Header matching gave correct viewport geometry on all accepted controlled matches: 120/120 for each stationary clip, 112/112 for motion, with eight abstentions during its predeclared blur. No wrong match was observed in this easy fixture. Full subject disappearance, repeated identical headers, scale/appearance change and natural occlusion remain unqualified.

## Costs and verification

Single CPU runs on the same Windows 11 machine; no GPU model loaded. Tesseract 5.4.0, Python 3.13.14 and dependency/FFmpeg versions are preserved in the raw manifest.

| Stage, seconds | Scroll | Motion | Occlusion | Brief |
| --- | ---: | ---: | ---: | ---: |
| All 120 frames: decode/JPEG write | .129 | .130 | .129 | .128 |
| Template relocalization, PSM7 pass | 1.005 | 1.102 | 1.096 | .992 |
| Tracked crop OCR, PSM7 pass | 8.681 | 8.441 | 8.629 | 8.615 |
| Three midpoint core seeks, summed cached measurements | .215 | .235 | .234 | .226 |

OCR time includes subprocess startup. Exact identical static/tracked boxes share OCR work within a frame, so their logical costs must not be added. Decode, crop selection overhead and OCR are separate stages; this is not a repeated latency or energy benchmark. The grid can seek directly without dense decoding/OCR; the common decoded pool was used for fair scoring.

The diagnostic collector plus its children peaked at **83.8 MiB summed sampled RSS** (original pass 82.0 MiB). Sampling was nominally 20 ms, can miss short peaks, and may double-count shared pages. Encoding/decoding and the monitor process are excluded. This does not qualify production peak RAM or VRAM.

All 192 distinct controlled grid requests were executed through the existing core FFmpeg extractor. Each matched its expected common-decoded frame with zero mean absolute pixel difference. Relevant existing frame tests: 5 passed; all 480 labels/timestamps, every sweep configuration and selected-frame bounds checked. Pre-commit passed. No production source behavior changed.

## Decision and next work

Keep the simple grid as a cheap control and initial view, but do not promise complete instructional coverage from a fixed budget or a single offset. Preserve short candidate events and exact revisions separately from frequency/sharpness. Relocalize when a subject moves; request masks only where their extent can improve the downstream evidence. Show unsupported or missing states in the guide rather than filling them from inference.

**Ticket 25 stays in progress.** Next freeze fresh natural scrolling, movement, occlusion and transient UI windows, with independent label checks, before retuning. Validate the PSM7/event candidate on those windows, including OCR variants, false/absent subjects and ambiguous repeated panels. Diagram/settings completeness, mask benefit, source-wide window discovery, human correction effort, task success and complete pipeline memory remain gaps. Ticket 35 still owns the production selector failure; review 28 still gates architecture and integration.

Raw reproduction, authored videos, every crop, selected full-frame comparisons, both OCR passes, grid audits and sweeps: [`codex/spike-subject-frame-seeking`, commit 39275c6](https://github.com/smileynet/video-buddy/tree/39275c6072e85be74640c292310858202809a659/docs/architecture/spikes/subject-frame-seeking/round2).
