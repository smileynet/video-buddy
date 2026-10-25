---
id: "28"
title: "Review spike findings and decide app features and integration architecture"
status: open
blocked_by: ["14", "15", "17", "18", "21", "23", "24", "25", "26", "27", "29", "30", "31", "32", "33", "34"]
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/integration-review.md contains a disposition and evidence link for each spike"
  - "tkt validate exits 0"
---

# Review spike findings and decide app features and integration architecture

## Intent source and context

User request 2026-10-25: review all spike findings, consider final integration, and review app features and architecture. Read docs/architecture/spike-plan.md, docs/architecture/workflow-proposal.md, docs/architecture/spikes/image-model-results.md and docs/plan.md. Primary job: apply a technique/build something and verify a result. All existing reports and prototype branches are evidence, not production implementations.

## What to build

A reviewable feature and architecture decision grounded in observed spike findings. Review acquisition, speech, OCR, subject seeking, temporal evidence, guides, adaptation, review UX, state/resume and result verification. For each component decide adopt, retain baseline, reject, unresolved or defer. Compare minimal CLI/agent/Markdown delivery with evidence-supported review UI. Define artifacts by their downstream use: steps, commands/settings, prerequisites, checkpoints, provenance and saved reusable solutions.

Review model eligibility, default/fallback routing, resource budgets, component boundaries, artifact contracts, uncertainty, correction flow, failure/recovery UX, installation and migration compatibility. Conditional attribution/retrieval tickets 19/20 need explicit trigger/disposition, not mandatory execution. Dependencies may close with an explicit unresolved verdict; corresponding features must then be excluded/deferred rather than represented as validated.

## Acceptance criteria

- [ ] docs/architecture/integration-review.md gives each spike an evidence-linked disposition.
- [ ] Retained app features and deferred scope are tied to user jobs and actual usability evidence.
- [ ] Architecture proposal and dashboard distinguish existing, supported experimental and proposed behavior.
- [ ] Component boundaries, routing, provenance, recovery and migration choices are explicit.
- [ ] Accepted findings become ordered implementation tickets with acceptance criteria and regression fixtures.
- [ ] Access, participant and runtime limitations remain visible in the recommendation.

## Out of scope

Production integration itself, automatically promoting prototype code, or selecting defaults from smoke results alone.

## Expanded provider coverage gate

Research29 and provider comparisons30–34 must have explicit reviewed dispositions before final integration. An unresolved provider experiment permits only an explicit deferral/exclusion, never an assertion of comprehensive market coverage. Reconcile these findings with original model23, seek25 and temporal26 results.

## Comparison follow-up

Review provider comparisons at their actual scope: YOLOEbounded natural/diagram observations, MolmoNF4general imagepoints vsQwenbaseline, and unrun specialist/hosted/runtime gaps. Require scoped referents and complete geometry before integrating; a generic search-field query can have multiple valid targets. Evidence commit ce811ed8, provider reports under docs/architecture/spikes/.
