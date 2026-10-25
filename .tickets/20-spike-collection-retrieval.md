---
id: "20"
title: "Evaluate retrieval when saved solutions become hard to find"
status: backlog
blocked_by: []
spec: "apply-build"
priority: low
tags: ["workflow-spikes"]
validation_criteria:
  - "A durable spike report records options, evidence and limitations"
  - "Every evaluated option records its fixture, environment and observations"
  - "The report states an adopt, retain, reject or unresolved verdict"
---

# Evaluate retrieval when saved solutions become hard to find

## Intent source

User requested tickets and execution of the proposed spikes, prioritizing applying a technique or building something. This is spike S9 in [the spike plan](../docs/architecture/spike-plan.md).

## Context

Read [shared experiment contract](../docs/architecture/spike-plan.md#shared-experiment-contract), [architecture proposal](../docs/architecture/workflow-proposal.md), and [primary-source research](../docs/agents/research/video-workflow-architecture.md). Dashboard: `docs/architecture-dashboard.html`. Preserve existing unrelated working-tree changes. Production integration is out of scope.

## What to build

A reproducible comparison that resolves the deciding question below, or explicitly records the missing observation when evidence cannot settle it. No production feature or automatic winner is required.

Trigger when finding prior solutions becomes a demonstrated bottleneck. Compare task-labeled files/current search against a rebuildable SQLite FTS5 index using approximately 20 real or representative queries, including exact commands and paraphrases. Measure correct evidence in the first results, time to usable answer, stale-version errors and source-link preservation. Only then compare embeddings/hybrid retrieval on the lexical failures. Budget: half a day for baseline/index, another half day only if a semantic comparison is justified. Unlocks retrieval, not canonical storage migration.

## Acceptance criteria

- [ ] A durable report identifies the deciding question, actual compared options and frozen fixtures.
- [ ] Every evaluated option records environment, observations, costs and evidence locations.
- [ ] The report states the verdict and distinguishes observed results from unresolved limitations.
- [ ] Evidence supports the downstream user job; no integration or user-study success is claimed without observation.

## Execution record

Not started. Record the actual experiment branch and evidence paths when work begins.
