---
id: "26"
title: "Compare ordered frames and video input for action evidence"
status: open
blocked_by: []
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/spikes/temporal-evidence-results.md exists and records evidence, limitations and a disposition for each scoped question"
  - "tkt validate exits 0"
---

# Compare ordered frames and video input for action evidence

## Context and intent

Intent source: user request on 2026-10-25 to capture every remaining spike, put open research next, then review integration, features and architecture. Read docs/architecture/spike-plan.md, docs/architecture/workflow-proposal.md and docs/architecture/spikes/image-model-results.md. Primary job: apply a technique/build something and verify the result. Preserve unrelated working-tree changes. Prototype code stays on isolated spike branches; no production integration in a spike.

## What to build

A bounded verdict on when ordered stills suffice and when temporal/video input is necessary to reproduce an action.

Continue unresolved S2 modality comparison from ticket 13 and docs/architecture/spikes/s2-results.md. Compare equal-evidence ordered timestamped frames with targeted clips through a harness that actually supports video. Include a brief UI action and non-text motion/state-change sequence. Freeze reference action order and checkpoints; distinguish visual model capability from transport/API support. No unsupported modality is a tested option. Record incremental cost to close evidence gaps and a declared active timebox; candidate selection uses ticket 24 research.

## Acceptance criteria

- [ ] Preserve supported input contracts and exact model/API revisions and prompts.
- [ ] Score essential actions, order, transient states and unsupported claims against manual references.
- [ ] Report latency, frame/token volume, memory and total evidence acquisition cost.
- [ ] Record a per-job retain/escalate/unresolved verdict; unsupported video paths stay explicitly untested.

## Out of scope

Automatic production integration, unsupported winners, and invented user/quality measurements.

## Ticket 24 research execution contract (2026-10-25)

**Budget:** One active day, excluding setup/download.

Verify actual supported input modality before running. Freeze essential action/order labels and compare ordered timestamped stills to targeted clips at disclosed evidence/compute budgets. Report action/order/transient-state recall, unsupported claims and incremental cost to close gaps. If no supported native-video harness is available, record it untested rather than relabeling still input as video.

Record raw outputs, exact versions/configuration, failures and a per-job disposition. Report metrics even if they do not favor a candidate; no invented quality threshold. Research register: `docs/agents/research/open-questions.md`.

## Provider coverage expansion

Current-provider comparison is now explicit in29–34. Coordinate shared fixtures/metrics and consume those results rather than duplicating provider installs. Original tested shortlist is not comprehensive market coverage. Final integration28 depends on all coverage dispositions.
