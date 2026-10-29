---
id: "18"
title: "Compare Markdown and adjacent-evidence review for blocked steps"
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

Started 2026-10-26. Prepared formative pack on codex/spike-review-ux, pinned commit2898fe9b7505b0d668661b531fc03b4a450bbe59, docs/architecture/spikes/review-ux/prototype.html and README.md. Durable preparation/limits: docs/architecture/spikes/s7-review-ux-preparation.md. Same guide/evidence in linear linked-document rendering and adjacent evidence; no backend or command execution. Browser checks and pre-commit passed. Reader invited; no human responses, comparative success/time result or winner yet. Ticket remains in_progress. Familiarity, repeated-task learning and HTML-baseline proxy limit interpretation;21 retains fresh task qualification.

## Reconciled remaining work (2026-10-25)

Observe evidence lookup, blocked-step correction and return-after-interruption with equivalent artifacts; compare Markdown/chat to an adjacent-evidence prototype. Keep mocked extraction controls labeled; coordinate participant needs with 21. Research ticket 24 is complete; use its recorded contract. Final synthesis is ticket 28; no model/default or feature integration is authorized by a smoke result.

## Ticket 24 research execution contract (2026-10-25)

**Budget:** Half an active day plus participant time.

Use identical completed artifact in linked Markdown/chat and adjacent-evidence view. Counterbalance tasks to locate setting, identify missing prerequisite, correct a step and resume. Record observed completion, evidence lookup time/actions and wrong support/tested interpretations. No participant means prepared protocol, not usability proof.

Record raw outputs, exact versions/configuration, failures and a per-job disposition. Report metrics even if they do not favor a candidate; no invented quality threshold. Research register: `docs/agents/research/open-questions.md`.

## Candidate fixture from17

Use `docs/architecture/spikes/s6-adaptation-results.md` and its frozen guide/provenance ledger as a candidate for distinguishing observed, documented-adapted and tested-here states. Native source-copy exit0/no-files and directory-conflict cases supply concrete blocked-step/recovery examples. Ticket17's same-agent walkthrough is not reader evidence; keep this study's source/format budgets and counterbalancing explicit.

## Narration fixture revision (2026-10-27)

User requested the sample guide in the walkthrough. Replaced Git task with seven-step narration guide for ABeo1kKueRs. A is linear linked guide; B is selected step beside matching source evidence. Same text, timestamps, opt-in player and full settings frame; notes/selected step retained on switch. Pinned codex/spike-review-ux commit b4bab3d14f281258a03ab117edb831a7e378d9a6, docs/architecture/spikes/review-ux. Previous fixture remains at2898fe9.

Offline browser/mobile, local links, step/content, opt-in player/pause, note/export, fixture hash and pre-commit checks passed. Hosted playback unverified with direct-link fallback. No reader evidence, paid generation or integration. Dashboard/report updated; remains in_progress for invited review.21 retains fresh-performer qualification.

## Shared teaching-format revision (2026-10-27)

User authorized the proposed format in both A/B views. Updated the same guide data for both: observable result, prerequisites/missing dependency, mechanism, seven Do/Why/Check steps, optional revision task with collapsed hint and success criteria, quick reference. Updated finalized workspace sample through CLI. Source/adapted/docs/test status remains explicit. Prototype pinned codex/spike-review-ux7fffe44da39afd5d20043393dc647434fb48ed37; dashboard and preparation report link the revision. Browser/mobile/content/notes/hint checks and pre-commit passed. No reader or voice-production result; remains in_progress awaiting review. Compare layout with identical v3 content, not v2 against v3.

## Researched gap-help revision (2026-10-27)

User requested related topics/prior art for incomplete guide areas. Both views and finalized narration sample now give Studio and official SDK/stitching starting routes, joining/timing components, concrete next action/check and remaining implementation work. Distinct researched-extension versus video/test labels preserved. Primary-source research and independent audit: docs/agents/research/narration-gap-starting-points{,-audit}.md; seven documentary findings supported. Pinned codex/spike-review-ux da5a7957c63830ab5bdd7cb644a8c3bcd908058d. Offline browser/mobile, shared guide hash, local evidence, note/step retention and pre-commit passed. No installed automation, paid generation, export/listening/timing result or new reader evidence. Hosted playback unverified. General gap-help pattern added to teaching-format proposal; no production integration. Remains in_progress awaiting review.

## Proactive guide and decision revision v5 (2026-10-27)

User requested the tone cleanup throughout, Alternative starting points label and explicit fit/complexity/cost weighting. Entire shared guide rewritten with action/check emphasis. Recommends ElevenLabs Studio for a first hosted short narration; provider, product, limited free exploration versus paid own-voice features explicit. SDK+joining is one automation route with additional coding/upkeep; paid generation persists. Local-only excludes both hosted paths. Pricing research and independent audit capture offer/renewal and headline/account-rate distinctions. Both views use the same seven steps and evidence; no reader or production winner. Pinned codex/spike-review-ux f445286b4ca4ad8c8652d0fa8e671de7f506c57e. Offline/mobile/parity/notes/labels and pre-commit passed. Remains in_progress for review;21 retains fresh-performer task.

## Local alternatives, disclosure and reusable guidance (2026-10-27)

User identified the missing concrete local options and requested reusable capture. Added Qwen3-TTS0.6BBase and Chatterbox-Turbo documented cloning candidates; no inference or hardware/offline/privacy qualification. Primary research/audit under docs/agents/research/narration-local-starting-points{,-audit}.md. Split optional comparison, local setup, automation and API mapping into useful callouts while keeping recommendation/fit/cost/blockers visible. Pinned codex/spike-review-ux521affef738586bce3e079f96032c6730c0f3338. Both views and finalized sample share v6. Offline/mobile/parity/disclosure and pre-commit checks passed. No new reader result.

Reusable docs/templates/video-guide.md and docs/agents/video-guide-authoring.md are routed from AGENTS.md. Cover proactive wording, source/research/adaptation/test labels, gap research, concrete hosted/local candidates, qualitative fit/complexity/total-cost choices and disclosure hierarchy. CLI remains mechanical owner; no product generation/schema integration. Remains in_progress awaiting review;21/28 retain performance/integration decisions.

## Local narration evidence from41

User-authorized Qwen3-TTS/Chatterbox-Turbo execution now has docs/architecture/spikes/local-narration-results.md and pinned raw/listening evidence. Same two English paragraphs/reference, four cases each. Chatterbox faster warm generation, higher process RAM/longer initialization; Qwen lower measured RAM. ASR agreement is not listening quality; first Chatterbox retained/attained disagreement remains unadjudicated. Both guide layouts have the same measured findings/audio. Keep human acceptance distinct from model timing/ASR and from layout benefit. No production defaults or integration. Source protocol frozen e5004d9; retained results45e5ba848975958bce74c0f13624e1a112d92960.

## Source-first and personal listening review

Tickets42/43 add private blind-label listening and refocus primary A/B content on the video. Implementation is a separate optional companion, partly executed only at the local TTS component. Source worked walkthroughs remain primary when that is the source type. UI tests used synthetic responses; no human results manufactured. Personal records stay private until shared. Layout, learning, example execution and model preference are distinct evidence. Prototype/companion pinned be4cbf793bedcd4ca21885ade9eec86053aed4a9. See docs/architecture/spikes/blind-listening-review.md.

## HTML deliverable clarification — October 28, 2026

User explicitly clarified that learning guides should be rich HTML. The installed and tracked video-guide skill now requires HTML as the primary deliverable, review of existing guides before drafting, responsive reading hierarchy, keyboard disclosures and presentation checks. Project guidance and templates are synchronized; portable references retain conditional Video Buddy CLI handling. Skill validators and pre-commit passed. This format decision is a user preference, not evidence that one A/B layout improves learning. Reader observations remain pending; ticket18 stays in_progress. Ticket45 captures the unfinished Claude Code HTML lesson separately from the completed skill correction.
