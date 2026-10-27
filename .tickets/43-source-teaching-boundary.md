---
id: "43"
title: "Separate source teaching from optional worked examples"
status: done
blocked_by: []
validation_criteria:
  - "Primary narration guide teaches the source rather than requiring our build"
  - "Optional example scope and execution status are separate in both views"
  - "Reusable template and routed agent guidance preserve the source-type distinction"
tags: ["workflow-spikes"]
---

# Separate source teaching from optional worked examples

## What to build

User identified drift from teaching the video into implementing our own guide-related tools. Separate the video's learning content from optional worked examples and tool qualification. Preserve a source's worked walkthrough as main content when it actually demonstrates that example; do not force conceptual/decision videos into executable recipes.

Narration primary guide now teaches seven source ideas with evidence and reasoning checks. A/B content remains identical. Optional worked-example.md/html holds our implementation plan, model measurements and prerequisites; its local TTS component is measured, the complete captioned workflow remains unbuilt. The source settings frame moved to its matching pipeline topic6. Dashboard separates learning, optional implementation and blind tool evaluation. Reusable template and routed agent guidance capture source-type selection, optional builds only when requested and distinct learning/execution/tool-qualification results.

## Acceptance criteria

- [x] Primary narration content teaches source concepts and decisions without requiring an implementation.
- [x] Both views preserve the same source/evidence and link an explicitly optional, accurately staged companion.
- [x] Template, agent guidance and AGENTS.md route future work through source-type separation.
- [x] Guide/navigation/mobile checks pass and no new pipeline implementation is claimed.

## Resolution (2026-10-27)

Separated the video's teaching from our proposed implementation/model studies in primary A/B views and dashboard. Source worked walkthroughs remain primary when appropriate; additional examples are optional companions with explicit scope/status and execution only when requested. Routed reusable guidance/template updated. No new pipeline build or learner outcome claimed.

### Verification
1. ✓ Primary narration guide teaches the source rather than requiring our build — "Narration guide now teaches seven source concepts/decisions; source-first A/B parity, source-frame alignment and independent optional companion verified."
2. ✓ Optional example scope and execution status are separate in both views — "worked-example.md/html accurately state written plan with measured local-TTS component and unbuilt full export; source-learning companion pinned be4cbf793bedcd4ca21885ade9eec86053aed4a9."
3. ✓ Reusable template and routed agent guidance preserve the source-type distinction — "docs/templates/video-guide.md, docs/agents/video-guide-authoring.md and AGENTS.md distinguish concept/decision sources, source worked walkthroughs, optional proposed builds and tool qualification; checks passed."
