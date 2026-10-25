---
id: "19"
title: "Evaluate attribution only when it changes the next action"
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

# Evaluate attribution only when it changes the next action

## Intent source

User requested tickets and execution of the proposed spikes, prioritizing applying a technique or building something. This is spike S8 in [the spike plan](../docs/architecture/spike-plan.md).

## Context

Read [shared experiment contract](../docs/architecture/spike-plan.md#shared-experiment-contract), [architecture proposal](../docs/architecture/workflow-proposal.md), and [primary-source research](../docs/agents/research/video-workflow-architecture.md). Dashboard: `docs/architecture-dashboard.html`. Preserve existing unrelated working-tree changes. Production integration is out of scope.

## What to build

A reproducible comparison that resolves the deciding question below, or explicitly records the missing observation when evidence cannot settle it. No production feature or automatic winner is required.

Trigger only when conflicting instructions, decisions or named responsibilities matter. Compare no diarization, current sherpa-onnx and eligible pyannote Community-1 on the same labeled discussion. Measure correct attribution of consequential statements, overlap errors and correction effort, alongside DER/JER and runtime. Preserve raw overlap even if a display view uses exclusive turns. Acoustic clusters cannot establish names or owners. Promote diarization only if it reduces downstream misinterpretation. Budget: half to one day; independent of primary build-guide flow.

## Acceptance criteria

- [ ] A durable report identifies the deciding question, actual compared options and frozen fixtures.
- [ ] Every evaluated option records environment, observations, costs and evidence locations.
- [ ] The report states the verdict and distinguishes observed results from unresolved limitations.
- [ ] Evidence supports the downstream user job; no integration or user-study success is claimed without observation.

## Execution record

Not started. Record the actual experiment branch and evidence paths when work begins.
