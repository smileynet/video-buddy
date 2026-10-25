---
id: "36"
title: "Spike revision boundaries for typing and scrolling without prefix budget loss"
status: done
blocked_by: []
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "A revision-boundary comparison report records frozen development/validation split, all candidates, outcomes and limitations"
  - "tkt validate exits 0"
---

# Spike revision boundaries for typing and scrolling without prefix budget loss

## What to build

Compare revision/event boundaries that preserve completed commands and their verification evidence without spending the budget on typing prefixes. Intent: a user can apply the demonstrated technique and verify the result. No automatic production integration.

Premise reproduced in ticket25's fresh-source validation: the unchanged two-frame/first-string candidate selected eight prefix/OCR-variant frames before the completed add command, recovering0/3 scrolling states at every cap1–8. A stable window header did not recover the moving inner content. Report: `docs/architecture/spikes/subject-frame-seeking-real-validation.md`; raw `codex/spike-subject-frame-seeking` commit `181e209def0389a57b0b4192b4acb2447682f6e4`.

Use those now-observed windows for development only. Compare the frozen negative control, a simple grid across the same offsets/budgets, and meaningful competing boundary policies (for example typing-run completion with revision retention, or structured text-region change tracking). Preserve exact numbers/symbol changes and resulting status/context; avoid a quiet-period rule that loses brief confirmations. Distinguish source-window search, subject identity, text geometry and event completion. Prototype on an isolated spike branch.

Budget: one active day after corpus preparation. Freeze new validation windows and intended subjects before tuning/scoring; record manual input, unknown labels, failed candidates and cost. Coordinate with25's independent-label/motion/mask gaps instead of claiming new general qualification from the same tutorial.

## Acceptance criteria

- [x] Preserve the original failed candidate and report completed-state recall, missed revisions, redundancy and partial-prefix budget consumption for each challenger.
- [x] Compare grid offsets0/.25/.5/.75 at caps1,2,3,4,6,8 with equivalent output caps and verified source times.
- [x] Record text extent/association limitations and exact command/checkpoint recovery separately from visual recall.
- [x] Validate the selected unchanged policy on newly frozen real windows; clearly separate development from validation.
- [x] Report stage costs and remaining uncertainty; update dashboard, ticket25 and review28 without integrating the prototype.

## Execution evidence — 2026-10-25

Report: `docs/architecture/spikes/revision-boundary-results.md`. Raw branch `codex/spike-revision-boundaries`, commit `842189be2c9480a8c228c7d87917713dc5acb0be`. Windows reserved af29e5a, labels locked7b77096 before development, preferred policy/collector/references frozen55aeb15 before validation OCR. No validation retuning; normalized freeze contents verified unchanged.

Compared legacy event-time/full-context control, whole-viewport settled runs, command/response packets with unverified fallback, and grids at caps1,2,3,4,6,8 × offsets0/.25/.5/.75.180 development frames plus509 validation frames across a previously unscored same-source window and an edited other-source tutorial. Single-agent references/uncertainty remain explicit.

Development at cap4: legacy0/3 with4 prefix-only selections; settled2/3 with1 prefix-only; packets3/3 with0 prefix-only, and3/3 already at cap1. Preferred packets were chosen on this evidence. Locked terminal validation: packets2 confirmed/up to3 of4 at every cap, definitely missing final checkpoint; settled4/4 at cap4 and all four grid offsets4/4. Locked UI: settled and packet fallback3/3 at cap2, not execution evidence. Exact writing remains unreliable. Keep failed and conditional findings; do not adopt packets as default or swap preference after validation.

All144 actual grid requests matched decoded neighborhoods, with12 nominal index corrections recorded. Five frame tests passed;689 references/509 validation frames and parser/freeze/hash checks passed. Stage costs and sampled collector RSS88.7MiB recorded; human correction/task benefit not measured. Compact artifacts inspected; three local replay frames matched hashes. Dashboard,25 and28 updated; no production integration.

## Resolution (2026-10-25)

Completed bounded comparison without integration. Preferred packets improved development but missed a locked terminal checkpoint (2–3/4); settled runs and grid reached4/4 at cap4. Keep packets rejected as default and settled selection conditional; broader gaps remain25 and adoption remains28.

### Verification
1. ✓ A revision-boundary comparison report records frozen development/validation split, all candidates, outcomes and limitations — "Report docs/architecture/spikes/revision-boundary-results.md records all policies, development and locked validation, frozen commits, metrics, failures and limitations; raw spike commit842189b."
2. ✓ tkt validate exits 0 — "tkt validate passed with no findings; frame tests5 passed; freeze, parser,144 seek and dashboard checks passed."
