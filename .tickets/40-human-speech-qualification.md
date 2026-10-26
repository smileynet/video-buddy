---
id: "40"
title: "Qualify speech changes with human-verified commands, numbers and timing"
status: backlog
blocked_by: []
spec: "apply-build"
priority: low
validation_criteria:
  - "A bounded report separates human-verified references, model-reviewed references and publisher captions with frozen provenance"
  - "Matched task-critical errors and timing are reported without using duplicate captions or model agreement as truth"
tags: ["workflow-spikes"]
---

# Qualify speech changes with human-verified commands, numbers and timing

## Intent source and context

User request2026-10-25 authorized audio-model review of the55-second pack, keeping model-reviewed references distinct from human-verified ones. Ticket15 completed a bounded comparison with model-reviewed provisional references and an unresolved accuracy verdict. Read `docs/architecture/spikes/s4-model-reviewed-results.md`, earlier speech results and the frozen review-pack protocol. Model family difference, publisher hosting, manual caption classification and matching transcripts do not establish independent human truth.

## What to build

Reactivate only when review28 or a concrete failed apply/build task requires changing ASR defaults, trusting extracted executable commands/numeric settings, or adding alignment. Build a bounded independent reference set from real tutorial commands, numeric parameters (not just counts/filename digits), quiet speech and actual word boundaries. Have an anonymous listener check raw source, record uncertainty, canonical spoken-versus-executable mapping, incomplete/context-crossing targets and corrections. Retain separate publisher, machine-reviewed and human-verified records and their lineage.

Current55-second clips have been seen by reviewer/candidates and are development/diagnostic evidence. Add fresh locked references before any generalization claim. Do not tune candidates on changed labels and report them as held-out. Pin eligible runtime/checkpoint identities and compare matched captions, faster-whisper and CrisperWhisper only if its actual installed identity/terms/runtime are established. Add alignment only on observed evidence-location failures.

## Acceptance criteria

- [ ] Freeze independent human-checked command, numeric-parameter and timing references with uncertainty before candidate inference.
- [ ] Separate reference classes, review actor/model identity and shared caption lineage; no fabricated human attestation.
- [ ] Report critical omissions/additions/spelling, counts, WER/CER and actual boundary errors with corpus/budget limits.
- [ ] Mark absent/out-of-window words unscorable instead of treating a cue overlap or model agreement as truth.
- [ ] Record stage costs and actual correction/task effort where observed, plus an evidence-linked adopt/retain/reject/unresolved verdict.

## Deliberate deferral

Backlog research, not a blocker for review28 retaining the baseline and excluding unqualified features. Reactivate on the concrete trigger above; model-reviewed comparisons may proceed with explicit provisional labels. Ticket38 owns no-speech retry regression work and39 owns caption/reference provenance contracts. This ticket does not authorize production default changes or replace fresh-performer usability21.

## Out of scope

Automatically treating SenseVoice or another model as ground truth, universal engine rankings, synthetic-only qualification, and prototype promotion.
