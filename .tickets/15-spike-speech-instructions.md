---
id: "15"
title: "Compare speech paths on implementation-critical details"
status: in_progress
blocked_by: ["12"]
spec: "apply-build"
priority: medium
tags: ["workflow-spikes"]
validation_criteria:
  - "A durable spike report records options, evidence and limitations"
  - "Every evaluated option records its fixture, environment and observations"
  - "The report states an adopt, retain, reject or unresolved verdict"
---

# Compare speech paths on implementation-critical details

## Intent source

User requested tickets and execution of the proposed spikes, prioritizing applying a technique or building something. This is spike S4 in [the spike plan](../docs/architecture/spike-plan.md).

## Context

Read [shared experiment contract](../docs/architecture/spike-plan.md#shared-experiment-contract), [architecture proposal](../docs/architecture/workflow-proposal.md), and [primary-source research](../docs/agents/research/video-workflow-architecture.md). Dashboard: `docs/architecture-dashboard.html`. Preserve existing unrelated working-tree changes. Production integration is out of scope.

## What to build

A reproducible comparison that resolves the deciding question below, or explicitly records the missing observation when evidence cannot settle it. No production feature or automatic winner is required.

**Deciding question:** which eligible configuration recovers the instructions and timings needed for these tasks?

**Options:** A: available captions; B: faster-whisper with word timestamps; C: exact installed CrisperWhisper distribution/model if eligible and available. Compare native timing against WhisperX alignment only on passages where native timing fails the evidence-location task.

**Throwaway:** manually reference short passages containing names, commands, numbers, silence and music. Compare ASR engines on matched hardware/model scale/settings where possible; report caption-source differences and unmatched configurations separately. Validate model/code licenses before treating an option as deployable.

**Observe:** critical-term/number errors, omissions/additions, WER/CER, timestamp boundary error, total elapsed time including transfer/preprocessing, memory and setup. Score transcript errors separately from alignment errors.

**Decision:** choose a default/fallback for the actual eligible deployment, not a universal winner. Keep captions if sufficient for orientation; do not present uncertain spoken commands as executable facts. Add forced alignment only if improved location accuracy is needed and observed.

**Budget:** one day. **Unlocks:** speech profile defaults, escalation and timing policy. Replaces conclusions, not historical measurements, from the old benchmark.

## Acceptance criteria

- [ ] A durable report identifies the deciding question, actual compared options and frozen fixtures.
- [ ] Every evaluated option records environment, observations, costs and evidence locations.
- [ ] The report states the verdict and distinguishes observed results from unresolved limitations.
- [ ] Evidence supports the downstream user job; no integration or user-study success is claimed without observation.

## Execution record

Not started. Record the actual experiment branch and evidence paths when work begins.

## Reconciled remaining work (2026-10-25)

Reassess earlier ASR benchmark conclusions using critical instruction/number recovery and evidence-location accuracy on matched passages. Preserve caption-source differences and model/license eligibility. Ticket 08 default change must await this verdict and final review 28. Research ticket 24 is complete; use its recorded contract. Final synthesis is ticket 28; no model/default or feature integration is authorized by a smoke result.

## Ticket 24 research execution contract (2026-10-25)

**Budget:** One active day.

Freeze short manually referenced instruction passages with names/numbers/commands plus silence/music. Compare eligible captions/faster-whisper/CrisperWhisper at disclosed hardware/scales; measure critical-term errors, omissions/additions and timestamp boundary errors separately. Compare alignment only on evidence-location failures. No universal default from old WER results.

Record raw outputs, exact versions/configuration, failures and a per-job disposition. Report metrics even if they do not favor a candidate; no invented quality threshold. Research register: `docs/agents/research/open-questions.md`.

### Installed speech identity before comparison

The committed worker defaults to model alias `turbo` and imports `crisperwhisper.CrisperWhisperModel`; neither pins a checkpoint nor proves the remote worker version. Capture installed package version, alias resolution, checkpoint revision and applicable weights terms for each eligible configured backend before scoring. Upstream v1 card redirects/supersession must not silently substitute v2; preserve historical benchmark identities. If runtime identity cannot be established, mark that option ineligible/unresolved rather than selecting a default.
