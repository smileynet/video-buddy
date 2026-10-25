# Revised event boundaries: completed commands and checkpoints

**Ticket 36 · bounded comparison complete · no production integration.** Retaining full context and waiting for command boundaries helped the observed failure, but the preferred packet policy did not generalize cleanly. On locked terminal validation it retained **2 confirmed states, at most 3 of 4**, missing the final status checkpoint. At a four-frame cap, the settled-run policy and every tested grid offset retained **4/4**. Copy-ready command recovery remains unqualified.

## What was frozen

The job is to retain a completed instruction **and its result/checkpoint**, so someone can apply the technique and check their work. A pause in typing, a matched window header and a returned shell prompt do not independently establish that job is complete.

| Split | Source window | Scoped states |
| --- | --- | --- |
| Development, already observed | [Traversy Git crash course](https://www.youtube.com/watch?v=SWYqp7iY_Tc), 940–946s | Completed add/status commands and post-add status packet; 3 states |
| Locked same-source validation | Same tutorial, 856–864s, previously unscored | Completed unstage command, its response, status command and resulting status packet; 4 states |
| Locked other-source validation | [Fireship, Git Explained in 100 Seconds](https://www.youtube.com/watch?v=hwP7WQkmECE), 33–42s | Add/commit illustrations plus staged10/remaining0 UI state; 3 states |

Protocol/windows were reserved in `af29e5a`, references locked in `7b77096` before policy development, and the preferred policy/collector/references frozen in `55aeb15` **before validation OCR**. Normalized contents remained unchanged through validation. There are 180 development frames and 509 validation frames; the second source runs at approximately 29.97 fps, so it supplies 269 frames, not an assumed 270. No validation result was used to retune or replace the preferred policy.

References were checked by the same agent across exhaustive scoped crop sheets. Uncertain characters, scroll transitions and edited overlays remain labeled unknown and propagate into coverage bounds. This is not an independent human reference set. The second source uses edited command cards with UI footage; it does not prove execution of those commands.

## Competing policies

All policies return whole source images with the same maximum frame count. This explicitly gives the original event-time control full context too; it is a context ablation rather than silently comparing a narrow crop with a complete image.

| Policy | Selection rule | Limitation exposed |
| --- | --- | --- |
| Original event times | Unchanged two-frame/first-OCR-string selector; original PSM7/header matching, full-frame output ablation | Partial typing consumes early slots |
| Settled runs | Whole-viewport PSM6 OCR unchanged for at least 0.2 s; rank runs by duration, sharpest representative | A stable partial instruction or idle screen can outrank a short checkpoint |
| Command/response packets | New command followed by a later prompt; retain response context; greedy novelty selection | Initial-history counts and a 15%-of-viewport position rule lose repeated-command identity during scrolling |
| Packet fallback | When no packet is detected, use the unchanged settled policy and mark execution unverified | Captures visual context without acknowledgment or exact-text guarantees |
| Simple grid | Offsets 0,.25,.5,.75 of each sample interval | No guaranteed event coverage at low budgets |

The two new alternatives share PSM6 viewport observations. Relative to the original, OCR mode, context extent and boundary rules change together; this is not a boundary-only causal ablation or an OCR-engine ranking. No reference label or command-name vocabulary enters the policy module.

An initial **development-only setup failure** merged TSV rows containing quotes. CSV quoting was disabled for Tesseract TSV before the policy freeze, and the failed pass was retained. Validation used that corrected parser without further repairs. All successful raw TSV remains available.

## Development result and preferred-policy choice

At cap 1 the packet policy retained 3/3 states in a single full-context frame; settled runs and the original retained 0/3. At cap 4:

| Policy | Selected | Complete states | Redundant state occurrences | Prefix-only selections |
| --- | ---: | ---: | ---: | ---: |
| Original event times | 4 | 0/3 | 0 | 4 |
| Settled runs | 4 | 2/3 | 1 | 1 |
| Packets | 2 | 3/3 | 1 | 0 |

The packet policy's second image treated an OCR spacing variant as a different command. More context solved the development omission, but did not remove recognition/deduplication problems. Prefix-only counts are manually scoped development measurements; validation records them as **not measured**, not zero. Redundancy counts repeated state occurrences, which can exceed the number of images when an image contains several states.

Packets were selected for locked validation on this development evidence. That preference was not changed after validation favored the settled alternative on the terminal case.

## Locked validation

Confirmed coverage below uses lower bounds; full min/max counts are in the dashboard and raw results.

| Cap | Terminal grid offsets 0/.25/.5/.75, out of 4 | Settled | Preferred packets | Other-source UI grid, out of 3 | Settled / packet fallback |
| --- | --- | ---: | --- | --- | --- |
| 1 | 0 / 1 / 2 / 4 | 1/4 | 2–3/4 | 1 / 1 / 2 / 2 | 2/3 / 2/3 |
| 2 | 2 / 2 / 4 / 4 | 3/4 | 2–3/4 | 2 / 2 / 3 / 3 | 3/3 / 3/3 |
| 3 | 3 / 4 / 4 / 4 | 3/4 | 2–3/4 | 3 / 3 / 3 / 3 | 3/3 / 3/3 |
| 4 | 4 / 4 / 4 / 4 | 4/4 | 2–3/4 | 3 / 3 / 3 / 3 | 3/3 / 3/3 |
| 6 | 4 / 4 / 4 / 4 | 4/4 | 2–3/4 | 3 / 3 / 3 / 3 | 3/3 / 3/3 |
| 8 | 4 / 4 / 4 / 4 | 4/4 | 2–3/4 | 3 / 3 / 3 / 3 | 3/3 / 3/3 |

**The preferred policy missed the final terminal checkpoint at every cap.** It retained one earlier packet near 861.133 s. That image's newly typed status command is uncertain in the reference, hence 2–3/4 rather than a forced miss or success. Once the response appeared, the status line had scrolled upward: its new occurrence had the same count as the initial history and moved too little relative to the fixed 15% test. The policy therefore failed to recognize it as a new acknowledged event. No position threshold was changed to rescue this run.

At cap 4, the original event-time control retained 0–1/4 terminal states and 2–3/3 UI states. Settled runs retained 4/4 terminal states with four images and six redundant state occurrences. The packet policy used only one image, with no redundant state occurrence, but definitely omitted the checkpoint. The UI alternatives used two images with no redundant state occurrence. Low redundancy is not useful when required evidence is missing.

On the UI source, the packet policy found no acknowledged packet and invoked its frozen visual fallback. The3/3 visual result therefore does not validate command acknowledgment, terminal occurrence tracking or execution success.

## Exact writing and artifact usefulness

At cap 4 the settled terminal selection preserved all four visual states, but only the status command was exact in the common OCR audit:1 of3 literal targets (two commands and one literal response). Filename/quote errors remained. The packet selection's unstage command was recognized with a closing bracket in the filename; its response text was also inexact.

Neither UI command was recovered exactly by the shared viewport OCR at the two selected fallback frames. One string lost spacing and gained a spurious symbol; the later card moved partly outside the seeded OCR viewport, clipping command text and corrupting the emoji. The whole image remained visually useful. A correct image selection does not establish machine-extracted, copy-ready instructions.

The practical output should retain the complete frame, source time, raw writing and uncertainty, and keep a checkpoint explicitly unverified until its meaning is checked. A returned prompt establishes a boundary cue, not success. No human correction-time or task-completion benefit was measured.

## Cost, capture and storage checks

Single CPU runs, Tesseract 5.4.0, Python 3.13.14. Selection logic after OCR took under 0.01 s at cap 4; viewport OCR dominated.

| Stage | Development, 6 s | Locked terminal, 8 s | Locked UI, 9 s |
| --- | ---: | ---: | ---: |
| Decode/JPEG write, seconds | .230 | .271 | .520 |
| Common viewport OCR, seconds | 59.35 | 75.77 | 24.85 |
| Four midpoint core seeks, summed cached seconds | .378 | .376 | .454 |

The validation collector/children peaked at 88.7 MiB summed sampled RSS over 108.0 s of wall time, excluding decode, annotation, legacy selection and the monitor. Sampling was nominally 20 ms; shared pages may double count and short peaks may be missed. This is not complete-pipeline peak memory or a repeated latency benchmark. The grid does not need the common OCR audit to acquire its images; both new policies pay that foundation cost.

All 144 distinct grid requests were captured through the core CLI/extractor and matched decoded frames. Twelve nominal terminal indices required adjacent-frame corrections; final scoring uses the pixel-verified indices. Source/frame hashes, 689 reference observations, the 509-frame validation split and unchanged policy/collector/reference contents were checked. Existing frame tests: 5 passed, and pre-commit passed. Three frames replayed into a fresh empty capture folder matched their frozen hashes.

Compact code, references, compressed observations and three selected JPEG sheets remain on the spike branch. Large media and regenerable exhaustive sheets stay ignored locally, with retrieval commands/hashes; no remote source-backup claim. The final staged-artifact check covered 18 new candidates / 462,299 logical Git-blob bytes, with complete metadata/content coverage and no findings. It excluded prior freeze commits, history and ignored media, and made no storage-cost or reclaimability claim.

## Disposition

**Do not adopt the preferred packet heuristic as a default.** Keep full-context evidence and the original negative control. Settled selection is a useful bounded challenger, but these two windows do not establish a universal winner or copy-ready extraction. The cheap grid remains an important control, with lower-budget misses visible.

This closes ticket 36's bounded comparison. Ticket 25 retains independent-reference, broader-source, temporal occurrence identity, geometry/mask and task-level qualification gaps. Review 28 receives the negative/conditional verdict and remains the gate for app features and integration; no prototype source was promoted.

Raw reproduction and evidence: [`codex/spike-revision-boundaries`, commit 842189b](https://github.com/smileynet/video-buddy/tree/842189be2c9480a8c228c7d87917713dc5acb0be/docs/architecture/spikes/revision-boundaries).
