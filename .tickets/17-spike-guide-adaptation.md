---
id: "17"
title: "Evaluate evidence-preserving adaptation to a target environment"
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

# Evaluate evidence-preserving adaptation to a target environment

## Intent source

User requested tickets and execution of the proposed spikes, prioritizing applying a technique or building something. This is spike S6 in [the spike plan](../docs/architecture/spike-plan.md).

## Context

Read [shared experiment contract](../docs/architecture/spike-plan.md#shared-experiment-contract), [architecture proposal](../docs/architecture/workflow-proposal.md), and [primary-source research](../docs/agents/research/video-workflow-architecture.md). Dashboard: `docs/architecture-dashboard.html`. Preserve existing unrelated working-tree changes. Production integration is out of scope.

## What to build

A reproducible comparison that resolves the deciding question below, or explicitly records the missing observation when evidence cannot settle it. No production feature or automatic winner is required.

**Deciding question:** can a source procedure be adapted to a different environment without hiding unsupported changes?

**Options:** A: source-faithful guide with explicit incompatibility gaps; B: two-layer guide with observed instructions and separately labeled adaptations, optionally supported by requested official documentation.

**Throwaway:** one tutorial with a known source/target version or platform mismatch. Keep evidence identical for source extraction; give the adaptation option a measured additional verification budget. Inspect proposed commands before authorized execution.

**Observe:** successful target result, mistaken version assumptions, fabricated flags, changed commands, provenance of each change and whether the reader can distinguish observed from adapted instructions.

**Decision:** promote adaptation only if the target walkthrough succeeds and all essential changes are visibly sourced or explicitly unverified. Otherwise ship the faithful guide plus gaps. A second model's agreement is not execution evidence.

**Budget:** half to one day. **Unlocks:** adaptation interface and revision/status rules. Depends on S1; use S2–S4 evidence if relevant.

## Acceptance criteria

- [ ] A durable report identifies the deciding question, actual compared options and frozen fixtures.
- [ ] Every evaluated option records environment, observations, costs and evidence locations.
- [ ] The report states the verdict and distinguishes observed results from unresolved limitations.
- [ ] Evidence supports the downstream user job; no integration or user-study success is claimed without observation.

## Execution record

Not started. Record the actual experiment branch and evidence paths when work begins.

## Reconciled remaining work (2026-10-25)

Evaluate target-platform/version adaptation separately from source observations, with official references for changes and a disposable target walkthrough. Keep unsupported changes visibly unverified. Research ticket 24 is complete; use its recorded contract. Final synthesis is ticket 28; no model/default or feature integration is authorized by a smoke result.

## Ticket 24 research execution contract (2026-10-25)

**Budget:** Half to one active day.

Use one frozen source/target version-platform mismatch. Compare faithful-with-gaps vs separately labeled adaptation. Record changed commands and official citations; inspect before authorized disposable execution. Score verified target checkpoints and unsupported essential changes. If no execution environment exists, leave success unresolved.

Record raw outputs, exact versions/configuration, failures and a per-job disposition. Report metrics even if they do not favor a candidate; no invented quality threshold. Research register: `docs/agents/research/open-questions.md`.
