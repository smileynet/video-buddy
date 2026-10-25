---
id: "18"
title: "Compare Markdown and adjacent-evidence review for blocked steps"
status: open
blocked_by: ["12"]
spec: "apply-build"
priority: medium
tags: ["workflow-spikes"]
validation_criteria:
  - "A durable spike report records options, evidence and limitations"
  - "Every evaluated option records its fixture, environment and observations"
  - "The report states an adopt, retain, reject or unresolved verdict"
---

# Compare Markdown and adjacent-evidence review for blocked steps

## Intent source

User requested tickets and execution of the proposed spikes, prioritizing applying a technique or building something. This is spike S7 in [the spike plan](../docs/architecture/spike-plan.md).

## Context

Read [shared experiment contract](../docs/architecture/spike-plan.md#shared-experiment-contract), [architecture proposal](../docs/architecture/workflow-proposal.md), and [primary-source research](../docs/agents/research/video-workflow-architecture.md). Dashboard: `docs/architecture-dashboard.html`. Preserve existing unrelated working-tree changes. Production integration is out of scope.

## What to build

A reproducible comparison that resolves the deciding question below, or explicitly records the missing observation when evidence cannot settle it. No production feature or automatic winner is required.

**Deciding question:** does a small review surface reduce the work needed to resolve a blocked guide step compared with Markdown/chat?

**Options:** A: Markdown/chat with timestamp and frame links; B: throwaway guide view with adjacent source evidence, visible gaps and “inspect this step / record my result” controls. Both use the same completed artifact; controls may simulate extraction requests but must be labeled.

**Throwaway:** ask a reader to locate an exact setting, identify an omitted prerequisite, correct one step and return after interruption. Observe behavior; do not ask which mockup looks nicer.

**Observe:** task completion, time/clicks to evidence, wrong interpretations, recovery success and ability to distinguish supported from tested.

**Decision:** build only the controls with demonstrated value. If linked Markdown is sufficient, retain it. A full application is not the default outcome.

**Budget:** half a day plus reader time. **Unlocks:** review UX scope. Depends on S1 artifacts; no backend integration required.

## Conditional spikes

### S8 — Does attribution change the next action?

Trigger only when conflicting instructions, decisions or named responsibilities matter. Compare no diarization, current sherpa-onnx and eligible pyannote Community-1 on the same labeled discussion. Measure correct attribution of consequential statements, overlap errors and correction effort, alongside DER/JER and runtime. Preserve raw overlap even if a display view uses exclusive turns. Acoustic clusters cannot establish names or owners. Promote diarization only if it reduces downstream misinterpretation. Budget: half to one day; independent of primary build-guide flow.

### S9 — Can the saved collection answer real implementation questions?

Trigger when finding prior solutions becomes a demonstrated bottleneck. Compare task-labeled files/current search against a rebuildable SQLite FTS5 index using approximately 20 real or representative queries, including exact commands and paraphrases. Measure correct evidence in the first results, time to usable answer, stale-version errors and source-link preservation. Only then compare embeddings/hybrid retrieval on the lexical failures. Budget: half a day for baseline/index, another half day only if a semantic comparison is justified. Unlocks retrieval, not canonical storage migration.

## Integration gate

For each spike, preserve the report and reproducible inputs separately from throwaway code. Record the branch/location actually used when experiments start; none exists yet. Review the evidence before selecting a winner. Integrate the smallest demonstrated improvement with compatibility checks and regression fixtures derived from failures. Keep unresolved options visible; installing a model or producing polished output is not a successful spike.

See [architecture proposal](workflow-proposal.md) and [tool research](../agents/research/video-workflow-architecture.md).

## Acceptance criteria

- [ ] A durable report identifies the deciding question, actual compared options and frozen fixtures.
- [ ] Every evaluated option records environment, observations, costs and evidence locations.
- [ ] The report states the verdict and distinguishes observed results from unresolved limitations.
- [ ] Evidence supports the downstream user job; no integration or user-study success is claimed without observation.

## Execution record

Not started. Record the actual experiment branch and evidence paths when work begins.

## Reconciled remaining work (2026-10-25)

Observe evidence lookup, blocked-step correction and return-after-interruption with equivalent artifacts; compare Markdown/chat to an adjacent-evidence prototype. Keep mocked extraction controls labeled; coordinate participant needs with 21. Research ticket 24 is next by explicit user instruction. Final synthesis is ticket 28; no model/default or feature integration is authorized by a smoke result.
