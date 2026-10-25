---
id: "35"
title: "Preserve useful low-edge code frames in frame selection"
status: open
blocked_by: ["28"]
tags: ["workflow-spikes"]
validation_criteria:
  - "Relevant frame selection tests pass, covering useful low-edge text and irrelevant/blank candidates"
  - "tkt validate exits 0"
---

# Preserve useful low-edge code frames in frame selection

## What to build

After review28 decides integration scope, fix the observed selection failure where all candidates have `should_include=false` and the initial quota rejects every frame. Preserve useful sparse code without admitting every blank screen. Compare a bounded fallback/subject-aware policy with the existing rank/hash/bucket behavior; do not promote ticket25's OCR prototype wholesale.

Evidence: `docs/architecture/spikes/subject-frame-seeking-results.md`, raw branch `codex/spike-subject-frame-seeking` commit `63082cff1f7f74e99d38dd4a955fa74364b30803`. Existing selector returned0frames on both59–63 and73–78second windows. Whole-image edge density stayed below2%. Forcing inclusion only was a post-hoc diagnostic, not an accepted implementation; it still missed revisions in some dense outputs.

## Acceptance criteria

- [ ] Reproduce the empty-selection failure with low-edge instructional evidence.
- [ ] Preserve required readable revisions without filling the budget with blank/irrelevant frames.
- [ ] Verify behavior at small budgets and for near-identical text revisions; report residual deduplication limitations.
- [ ] Run relevant frame tests and pre-commit on changed files; update documentation with the reviewed policy.
