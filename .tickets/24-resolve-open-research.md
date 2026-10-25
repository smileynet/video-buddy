---
id: "24"
title: "Resolve open research questions before the next spike round"
status: in_progress
blocked_by: []
spec: "apply-build"
priority: urgent
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/agents/research/open-questions.md exists and records evidence, limitations and a disposition for each scoped question"
  - "tkt validate exits 0"
---

# Resolve open research questions before the next spike round

## Context and intent

Intent source: user request on 2026-10-25 to capture every remaining spike, put open research next, then review integration, features and architecture. Read docs/architecture/spike-plan.md, docs/architecture/workflow-proposal.md and docs/architecture/spikes/image-model-results.md. Primary job: apply a technique/build something and verify the result. Preserve unrelated working-tree changes. Prototype code stays on isolated spike branches; no production integration in a spike.

## What to build

A cited research decision register that lets the next agent run bounded experiments without guessing model eligibility, supported runtimes or success criteria.

Inventory unanswered topics across both docs/agents/research reports and all spike reports. Cover SAM 3.1 session API/checkpoint compatibility; DINOv3 approval and supported runtime; exact code/checkpoint/component licenses including ASR and OmniParser; deployment/runtime and resource constraints; OCR languages and representative video corpus; subject association, quality scoring and state-change preservation; supported ordered-frame/native-video modalities; source acquisition/integrity/authentication/retry behavior; guide provenance, adaptation and result verification. Distinguish documented facts from local measurements and product hypotheses. Research primary sources at pinned revisions/dates; audit old findings against observed SAM 3 results. For every question provide evidence or an explicit unresolved limitation, and link its execution ticket. No new credential is needed for SAM 3/3.1. DINOv3 remains gated. This is explicitly the NEXT ticket by user instruction, ahead of resuming 14/23.

## Acceptance criteria

- [ ] Create docs/agents/research/open-questions.md with question, source/date/revision, finding, confidence, remaining observation and owning ticket.
- [ ] Every unresolved topic in existing reports is resolved, mapped to a spike, or explicitly deferred with a reason.
- [ ] Record SAM 3.1 API diagnosis and DINOv3 access status without exposing credentials or treating failures as quality results.
- [ ] Update affected tickets with executable experiment plans and predeclared metrics/budgets.
- [ ] Record source-supported code/checkpoint eligibility separately for each candidate component.

## Out of scope

Automatic production integration, unsupported winners, and invented user/quality measurements.
