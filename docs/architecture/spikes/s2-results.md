# S2 visual evidence: bounded comparison results

Date: 2026-10-25. Ticket: [13](../../../.tickets/13-spike-visual-evidence.md). Source: YouTube Qr3VsZYQy4s. Verdict: **targeted follow-up is a useful candidate; a universal minimum frame budget is unresolved.** No production integration is approved by this report.

## Question, options and evidence

Which visual pass recovers the facts needed to reproduce an action? Compared the preceding 15-frame source-wide sparse capture (A), 8 transcript-targeted frames followed by a post-hoc 15-frame refinement (B), and a 36-frame one-second sequence around the same two passages (C). OCR was off; the same agent inspected the images with transcript context. This is an adaptive reconnaissance comparison, not blinded semantic-recall benchmarking or a reader study.

Experimental branch: `codex/spike-targeted-frames`, commit `08d238f7ee728a58e7b214cf127d33adc8757ffe`. Artifacts are under `docs/architecture/spikes/s2-visual-comparison/`: commands/limitations in README, environment snapshot, experimental dependency lock, frame metadata, contact sheets, five full-resolution frames and machine-readable observations.

[Inspect the dense sequence](https://github.com/smileynet/video-buddy/blob/08d238f7ee728a58e7b214cf127d33adc8757ffe/docs/architecture/spikes/s2-visual-comparison/dense-contact.jpg) and [final targeted set](https://github.com/smileynet/video-buddy/blob/08d238f7ee728a58e7b214cf127d33adc8757ffe/docs/architecture/spikes/s2-visual-comparison/targeted-contact.jpg).

Retained source: 340,721,074 bytes, SHA-256 `21792d2ee0f5e506be088a448f7eb3ec3d07af6cea2a0839bbb576a8b00c4ba7`. Mechanical work ran through the repo CLI. The spike adds isolated `frames --at <seconds...> --media-file <file>` controls, reusing existing extraction/scoring functions while bypassing ranking/deduplication for explicitly requested frames. These flags are not in production.

## Observations

| Option | Evidence volume | Observed result | Capture wall time |
|---|---|---|---|
| A: source-wide sparse | 15 selected / 200 candidates | Earliest frame 174.148s; none inside either target passage | Not measured in the preceding run |
| B0: exploratory targeted | 8 frames, 73–82s and 98–110s | Recovers waveform states and coordinate diagram; ends before clearly circular trace | 13.44s |
| C: dense timestamps | 36 frames, 72–86s and 96–116s | Recovers state order, circular trace, and a later numeric harmonic row | 17.29s |
| B1: post-hoc targeted | 15 frames across C's same windows | Retains the inspected waveform/coordinate/circle facts and later row with fewer images | 18.62s |

Times include process startup, local-media probing/extraction and scoring. They exclude download, agent image inspection and OCR. Runs were sequential on cached local media with different command wrappers (`uv run` versus direct environment Python for B1); timings do not isolate a sampler advantage. B1 was slower despite fewer frames, so no speed claim follows.

### What was actually visible

- 73/76s: component waves above a sawtooth-like combined shape. 79/82s: the lower shape changes toward a square wave. No exact harmonic coefficient table is visible in the inspected waveform frames.
- 98s: empty diagram panel; 102s: one coordinate relationship; 106/110s: two coordinate links and an evolving trace.
- 112–114s: circular trace with the dot in different positions. This adds visible support to the spoken quarter-turn relationship.
- 116s: top row reads `harmonic=1 amplitude=1.0000 phase=0.0000`. A faint second row remains uncertain. These later values are not evidence for the earlier square-wave recipe.

The original missing square-wave implementation remains missing: a familiar output shape does not establish exact coefficients, signs, phase convention or executable code. Do not fill that gap using model knowledge and label it source-observed.

## Decision inputs

Retain source-wide sparse selection for overview images, but treat its coverage as insufficient for individual guide steps. Candidate next interface: an evidence request containing source ID, time window and missing fact, followed by timestamped images and an explicit “gap resolved / unresolved” observation. Preserve requested frames even if they resemble each other; a transition can be precisely what a perceptual deduplicator removes.

Extending the time window recovered a fact missed by B0. Because B0 and C also differ in coverage, density alone did not earn the credit. B1's post-hoc success suggests selective follow-up can reduce inspection volume for these known facts, but needs held-out UI/terminal tasks before selecting a production default. No need to change the vision provider has been demonstrated by this source.

## Limits and prerequisites

One conceptual animation supplies two passages, not the planned independent UI and non-text tasks. No exact-settings recall rate, source-wide essential-action recall, task-completion improvement, minimum sampling budget or optimal model is established. Native video understanding was not evaluated: C is a timestamped still sequence. Metadata records requested seek positions, not independently checked presentation times.

Clean committed main could not initially import the CLI because `_find_breakdown` was absent from `batch_digest.py`; the spike copied the existing primary-checkout helper. Tracked separately in [ticket 22](../../../.tickets/22-clean-checkout-cli-startup.md). Retained download used the primary checkout's existing uncommitted `fetch --download-video` capability; committed main lacks that flag. These are explicit experimental prerequisites, not features delivered by this spike.

Checks on the spike branch: `tests/test_frames.py` and `tests/test_cli.py`: **15 passed**. Pre-commit passed after formatting. The default frame call preserves its previous argument surface; only experimental flags pass the new options.

## Next experiment

Proceed to OCR comparison (ticket 14) using genuinely text-bearing UI/terminal regions, not diagrams with no text. Include the 116s row as one small numeric-label example; it is not a representative OCR corpus. Reader completion remains tracked in ticket 21. Keep all prototype code on the experimental branch and review the limits before any integration.
