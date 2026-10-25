---
id: "13"
title: "Find the minimum visual evidence needed to reproduce actions"
status: in_progress
blocked_by: ["12"]
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "A durable spike report records options, evidence and limitations"
  - "Every evaluated option records its fixture, environment and observations"
  - "The report states an adopt, retain, reject or unresolved verdict"
---

# Find the minimum visual evidence needed to reproduce actions

## Intent source

User requested tickets and execution of the proposed spikes, prioritizing applying a technique or building something. This is spike S2 in [the spike plan](../docs/architecture/spike-plan.md).

## Context

Read [shared experiment contract](../docs/architecture/spike-plan.md#shared-experiment-contract), [architecture proposal](../docs/architecture/workflow-proposal.md), and [primary-source research](../docs/agents/research/video-workflow-architecture.md). Dashboard: `docs/architecture-dashboard.html`. Preserve existing unrelated working-tree changes. Production integration is out of scope.

## What to build

A reproducible comparison that resolves the deciding question below, or explicitly records the missing observation when evidence cannot settle it. No production feature or automatic winner is required.

**Deciding question:** what is the least costly visual pass that recovers the actions needed to execute the task?

**Options:** A: current sparse selected frames; B: chapter/time coverage plus agent-requested nearby frames; C: targeted short clips or dense timestamped sequences. Use a harness that genuinely supports the supplied modality; an unsupported video input is not an evaluated option.

**Throwaway:** use the same transcript and two source segments containing a brief UI action and a non-text/state-change demonstration. Compare both equal-budget first passes and incremental cost to close each gap.

**Observe:** essential-action recall, action order, exact settings recovered, unsupported observations, unresolved gaps, frame/clip volume and latency.

**Decision:** keep sparse frames where adequate; add targeted follow-up if it closes gaps; add temporal input only where order/motion failures persist. A new vision model is justified only after the current harness's failure is demonstrated. Local Qwen3-VL is a conditional additional comparison, not a prerequisite.

**Budget:** one day. **Unlocks:** frame-request interface, temporal evidence needs and capability checks.

## Acceptance criteria

- [ ] A durable report identifies the deciding question, actual compared options and frozen fixtures.
- [ ] Every evaluated option records environment, observations, costs and evidence locations.
- [ ] The report states the verdict and distinguishes observed results from unresolved limitations.
- [ ] Evidence supports the downstream user job; no integration or user-study success is claimed without observation.

## Execution record

Ran bounded comparison on 2026-10-25. [Results](../docs/architecture/spikes/s2-results.md), branch `codex/spike-targeted-frames`, commit `08d238f7ee728a58e7b214cf127d33adc8757ffe`. Compared preceding sparse15, exploratory targeted8, dense36 timestamped stills and post-hoc targeted15 through the CLI. Targeted capture recovered waveform/coordinate/circle evidence, but exact square-wave coefficients remain unresolved. No universal minimum, speed gain, native-video model comparison or reader task-completion result is claimed. 15 relevant tests passed. Prototype stays off main; startup prerequisite tracked in ticket 22.
