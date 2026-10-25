---
id: "21"
title: "Measure guide versus note usability with a fresh task performer"
status: open
blocked_by: []
spec: "apply-build"
priority: medium
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/spikes/guide-usability-results.md records observed usability or an explicit unresolved participant limitation"
---

# Measure guide versus note usability with a fresh task performer

## What to build

Given the prepared note/guide variants from ticket 12, observe fresh task performers using comparable evidence to complete two independent implementation tasks. Separate human usability from numerical/source correctness. Source intent: user prioritized applying a technique or building something; S1 could not measure reader performance.

Read `docs/architecture/spikes/s1-status.md` and `docs/architecture/spike-plan.md` (S1). The prepared artifacts and reviewer protocol are on branch `codex/spike-guide-comparison`, commit `bae31aa`. They cover two tasks from one conceptual source and are preparation, not a representative user study. Add command/UI tasks and counterbalance order before selecting a format winner. Fresh task-performer availability remains required for a measured usability verdict; source-evidence spikes can proceed independently.

## Acceptance criteria

- [ ] Report actual compared artifacts, frozen evidence and target environments.
- [ ] Record observed task completion, interventions and evidence lookups without fabricated timings.
- [ ] Report order/familiarity effects and participant limitations without personal identifying data.
- [ ] Select a format only if observed results support it; otherwise record an unresolved verdict.

## Reconciled remaining work (2026-10-25)

Promoted into the current qualification cycle for final review 28. Participant availability is an external execution limitation, not fabricated usability evidence. Prepare comparable command/UI tasks and a reproducible protocol; if a fresh performer is unavailable record an unresolved verdict and constrain final feature claims. Research ticket 24 is next by explicit user instruction. Final synthesis is ticket 28; no model/default or feature integration is authorized by a smoke result.
