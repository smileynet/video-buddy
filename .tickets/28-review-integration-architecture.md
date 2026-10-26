---
id: "28"
title: "Review spike findings and decide app features and integration architecture"
status: open
blocked_by: ["14", "15", "17", "18", "21", "23", "24", "25", "26", "27", "29", "30", "31", "32", "33", "34", "36"]
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/integration-review.md contains a disposition and evidence link for each spike"
  - "tkt validate exits 0"
---

# Review spike findings and decide app features and integration architecture

## Reconciled decision gates — 2026-10-25

Ticket 25 now exits through a linked evidence/limitations synthesis; ticket 37 holds deliberately deferred broader tracking research. Review may retain the baseline and exclude unqualified masks/tracking without executing 37. Do not claim those features are validated.

Required before final recommendations: bounded dispositions for speech 15, adaptation 17, review UX 18, fresh-performer usability 21, temporal evidence 26 and acquisition/recovery 27, plus closure of the frame synthesis 25. Unavailable participants or modalities yield an explicit unresolved verdict and constrained feature claims, never invented success. Providers 30/33/34 remain required access/runtime dispositions; their tests have not been waived or completed. Keep existing dependency edges until each ticket records its reviewed outcome. Ticket 22 is a clean-CLI prerequisite where a proposed experiment uses the production CLI; it is not a reason to overwrite pending user changes. Ticket 35 remains an implementation proposal after this review, not a circular prerequisite.

## Ticket36 bounded comparison completed

Consume `docs/architecture/spikes/revision-boundary-results.md`. Legacy, settled-run and command/response packet alternatives plus grid offsets/budgets were compared with180 development and509 locked validation frames. Preferred packets fixed the observed case but missed the later validation checkpoint (2–3/4); settled runs/grid reached4/4 at cap4. Other-source visual fallback and literal OCR remain separate from verified instructions. No policy retuned on validation; no new default adopted. Keep settled selection conditional and packet heuristic rejected as default;25 still owns wider temporal/geometry/reference/task gaps. Raw branch `codex/spike-revision-boundaries`, commit `842189be2c9480a8c228c7d87917713dc5acb0be`.

## Fresh real validation disposition — 2026-10-25

`docs/architecture/spikes/subject-frame-seeking-real-validation.md` supersedes the provisional positive controlled diagnostic for default selection. The unchanged candidate recovered0/3 required scrolling states on a fresh source at every tested cap1–8; prefixes consumed its output budget. Other one-state early captures did not qualify later zoom/menu retention. Do not adopt this candidate as default. New blocker36 owns revision-boundary alternatives and new locked validation; these observed windows become development evidence. Ticket25 retains independent-label, broader-source, mask/diagram and task-level gaps. Raw evidence branch `codex/spike-subject-frame-seeking`, commit `181e209def0389a57b0b4192b4acb2447682f6e4`.

## Ticket25 comparison evidence added 2026-10-25

Consume `docs/architecture/spikes/subject-frame-seeking-stress-results.md` alongside the first matched-window report. The real code grid result depends on offset; authored controls expose short-state and crop-tracking failures. The PSM7/event candidate was changed after inspecting controls, so it is not a held-out winner. Require fresh natural qualification before choosing a production selector/model composition. Ticket25 remains in progress; ticket35 owns the existing global inclusion-veto failure. Peak collector RSS is measured separately from full-pipeline memory. Preserve these limits when reviewing UX claims and integration scope.

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

## Speech first-round finding — 2026-10-25

Consume `docs/architecture/spikes/s4-speech-results.md`: known-corpus prose WER did not predict controlled command reliability, and default VAD-empty retry produced unsupported silent/tonal text, including a beyond-duration caption. Ticket38 is the post-review regression proposal. Ticket15 stays open for natural tutorial/caption qualification; do not treat its first round or a model's empty negative output as a validated default. No extra blocker38 edge is added: this review decides policy before implementation.

## Speech reference lineage — 2026-10-25

Consume `docs/architecture/spikes/s4-reference-provenance.md`. Original caption track is verified ASR; publisher/manual track labels do not certify human review. MIT matching cue records and CS50 matching decoded words cannot provide two independent validation references. Ticket15 has a55-second independent-listening pack but no completed human reference or new speech score. Ticket39 proposes durable caption provenance after this review; no blocker39 edge is added.

## Ticket15 bounded audio-model comparison completed

Consume `docs/architecture/spikes/s4-model-reviewed-results.md`: a runnable independent-family SenseVoice audio pass and locked machine-reference comparison now exist. Model-reviewed provisional remains distinct from human-verified. Its code spelling disagreements and token timing cannot certify exact commands or word boundaries; conditional WER is only agreement. Retain baseline and exclude unsupported exact-command/accuracy claims. Ticket40 defers human-verified qualification until a concrete speech/default/alignment change requires it. No automatic integration follows closure of15; preserve38/39 recovery/provenance proposals.

## Guide adaptation17 bounded disposition

Consume `docs/architecture/spikes/s6-adaptation-results.md`. Conditional native procedure succeeded with byte/type checkpoints, preserved existing work and stated its timestamp difference. Host already has touch; the no-GNU profile is declared, not a blanket PowerShell incompatibility. Source commands remain separate from documented adaptations and tested-here scopes. Exit0/no-files and Force truncation show why result postconditions and content preservation matter. No fresh-reader UX result or general translator is validated;18/21 remain required dispositions. Review contracts rather than promoting prototype scripts.
