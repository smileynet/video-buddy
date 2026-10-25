---
id: "12"
title: "Evaluate whether implementation guides improve task completion"
status: done
blocked_by: []
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "A durable spike report records options, evidence and limitations"
  - "Every evaluated option records its fixture, environment and observations"
  - "The report states an adopt, retain, reject or unresolved verdict"
---

# Evaluate whether implementation guides improve task completion

## Intent source

User requested tickets and execution of the proposed spikes, prioritizing applying a technique or building something. This is spike S1 in [the spike plan](../docs/architecture/spike-plan.md).

## Context

Read [shared experiment contract](../docs/architecture/spike-plan.md#shared-experiment-contract), [architecture proposal](../docs/architecture/workflow-proposal.md), and [primary-source research](../docs/agents/research/video-workflow-architecture.md). Dashboard: `docs/architecture-dashboard.html`. Preserve existing unrelated working-tree changes. Production integration is out of scope.

## What to build

A reproducible comparison that resolves the deciding question below, or explicitly records the missing observation when evidence cannot settle it. No production feature or automatic winner is required.

**Deciding question:** does an implementation packet improve successful task completion enough to justify a new output contract?

**Options:** A: current detailed note; B: ordered implementation packet with prerequisites, versions, observed commands/settings, checkpoints and gaps. Give both the same evidence and generation budget so richer extraction does not confound format.

**Throwaway:** generate both artifacts for two tasks; have a reader perform the task in a disposable environment. Stop after the deciding tasks, rather than building a guide engine.

**Observe:** verified result, interventions, time to first successful checkpoint, time searching the source, missing prerequisites, unsupported instructions and evidence lookup effort.

**Decision:** promote a guide contract only if it improves completion or materially reduces help/source searching without introducing unsupported actions. If both fail because evidence is missing, route that failure to S2 rather than declaring the format ineffective.

**Budget:** one day plus task-performer time. **Unlocks:** output contract and highest-value missing evidence. No dependency on a new runner.

## Acceptance criteria

- [x] A durable report identifies the deciding question, actual compared options and frozen fixtures.
- [x] Every evaluated option records environment, observations, costs and evidence locations.
- [x] The report states the verdict and distinguishes observed results from unresolved limitations.
- [x] Evidence supports the downstream user job; no integration or user-study success is claimed without observation.

## Execution record

Started 2026-10-24. Throwaway branch `codex/spike-guide-comparison`, commit `bae31aadd0b6c90e60f77cc5f50f9c33bc030dea`. See [initial observations](../docs/architecture/spikes/s1-status.md): equal-content note/guide variants and a frozen transcript packet are prepared; a numerical checkpoint passes the quarter-turn formula and rejects a zero-offset control. Reader completion remains unmeasured; no format winner or production integration is claimed. Keep in progress until the remaining observations are addressed.

## Resolution (2026-10-25)

Bounded source/format feasibility investigation concluded with unresolved usability verdict. Numerical control observed, source gap identified, reader validation retained in ticket 21. No guide-format winner selected.

### Verification
1. ✓ A durable spike report records options, evidence and limitations — "docs/architecture/spikes/s1-status.md records both formats, frozen source and unresolved reader question"
2. ✓ Every evaluated option records its fixture, environment and observations — "bae31aa contains source hash, environment and numeric observations; source/capture limits are reported"
3. ✓ The report states an adopt, retain, reject or unresolved verdict — "Verdict remains unresolved; missing reader experiment is tracked in ticket 21, no integration claimed"
