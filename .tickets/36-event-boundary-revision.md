---
id: "36"
title: "Spike revision boundaries for typing and scrolling without prefix budget loss"
status: in_progress
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

- [ ] Preserve the original failed candidate and report completed-state recall, missed revisions, redundancy and partial-prefix budget consumption for each challenger.
- [ ] Compare grid offsets0/.25/.5/.75 at caps1,2,3,4,6,8 with equivalent output caps and verified source times.
- [ ] Record text extent/association limitations and exact command/checkpoint recovery separately from visual recall.
- [ ] Validate the selected unchanged policy on newly frozen real windows; clearly separate development from validation.
- [ ] Report stage costs and remaining uncertainty; update dashboard, ticket25 and review28 without integrating the prototype.
