---
id: "16"
title: "Choose a state store using interruption and concurrency probes"
status: open
blocked_by: []
spec: "apply-build"
priority: medium
tags: ["workflow-spikes"]
validation_criteria:
  - "A durable spike report records options, evidence and limitations"
  - "Every evaluated option records its fixture, environment and observations"
  - "The report states an adopt, retain, reject or unresolved verdict"
---

# Choose a state store using interruption and concurrency probes

## Intent source

User requested tickets and execution of the proposed spikes, prioritizing applying a technique or building something. This is spike S5 in [the spike plan](../docs/architecture/spike-plan.md).

## Context

Read [shared experiment contract](../docs/architecture/spike-plan.md#shared-experiment-contract), [architecture proposal](../docs/architecture/workflow-proposal.md), and [primary-source research](../docs/agents/research/video-workflow-architecture.md). Dashboard: `docs/architecture-dashboard.html`. Preserve existing unrelated working-tree changes. Production integration is out of scope.

## What to build

A reproducible comparison that resolves the deciding question below, or explicitly records the missing observation when evidence cannot settle it. No production feature or automatic winner is required.

**Deciding question:** can atomic JSON manifests safely support intended concurrency, or is transactional state already necessary?

**Options:** A: file manifest, atomic writes and per-job locks; B: SQLite transactions with artifact files outside the database. Implement the same tiny stage interface, not the full production pipeline.

**Throwaway:** dummy acquisition/speech/analysis stages plus one small real media fixture. Inject interruption after acquisition, during artifact writing and before completion state; delete/corrupt an artifact; change configuration; start duplicate same-source jobs; simulate failed authentication and a failed optional stage.

**Observe:** stale-state detection, correct invalidation, duplicate downloads, lost edits, concurrent writer behavior, repairability, implementation complexity and stage-specific recovery messages. A readable ffprobe result alone does not establish full decode integrity.

**Decision:** prefer the simpler implementation that passes all intended failure/concurrency cases. Choose SQLite if necessary transactional guarantees cannot be achieved cleanly with file ownership and locks. Neither option justifies a distributed queue.

**Budget:** one day. **Unlocks:** durable runner/store choice. Can run independently of model spikes; integrate only after S1 defines outputs.

## Acceptance criteria

- [ ] A durable report identifies the deciding question, actual compared options and frozen fixtures.
- [ ] Every evaluated option records environment, observations, costs and evidence locations.
- [ ] The report states the verdict and distinguishes observed results from unresolved limitations.
- [ ] Evidence supports the downstream user job; no integration or user-study success is claimed without observation.

## Execution record

Not started. Record the actual experiment branch and evidence paths when work begins.
