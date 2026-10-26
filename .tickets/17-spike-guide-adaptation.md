---
id: "17"
title: "Evaluate evidence-preserving adaptation to a target environment"
status: done
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

- [x] A durable report identifies the deciding question, actual compared options and frozen fixtures.
- [x] Every evaluated option records environment, observations, costs and evidence locations.
- [x] The report states the verdict and distinguishes observed results from unresolved limitations.
- [x] Evidence supports the downstream user job; no integration or user-study success is claimed without observation.

## Execution record

Started2026-10-26. Branch `codex/spike-guide-adaptation`; freeze b442b1b contains shared source/frame, both guides, scoped target/profile, eight cases and runner before execution. Report: `docs/architecture/spikes/s6-adaptation-results.md`. Actual task is the source tutorial's two-file preparation, not the full Git workflow. Host touch is available; no-GNU native PowerShell is an explicit child-only profile. No production integration.

## Reconciled remaining work (2026-10-25)

Evaluate target-platform/version adaptation separately from source observations, with official references for changes and a disposable target walkthrough. Keep unsupported changes visibly unverified. Research ticket 24 is complete; use its recorded contract. Final synthesis is ticket 28; no model/default or feature integration is authorized by a smoke result.

## Ticket 24 research execution contract (2026-10-25)

**Budget:** Half to one active day.

Use one frozen source/target version-platform mismatch. Compare faithful-with-gaps vs separately labeled adaptation. Record changed commands and official citations; inspect before authorized disposable execution. Score verified target checkpoints and unsupported essential changes. If no execution environment exists, leave success unresolved.

Record raw outputs, exact versions/configuration, failures and a per-job disposition. Report metrics even if they do not favor a candidate; no invented quality threshold. Research register: `docs/agents/research/open-questions.md`.

## Bounded findings and limits

Two unchanged source lines work in Git Bash and host PowerShell where GNU touch exists. In the declared native-only child profile they create nothing despite process exit0. Labeled guarded New-Item adaptation creates both empty files, preserves a16-byte existing canary and fails explicitly on a directory conflict. A standalone Force negative control truncates the owned canary16→0. Source touch updates existing modification time while the adaptation leaves it unchanged; no full touch equivalence claimed.

All8frozen case expectations matched, including deliberate failures/negative controls; this is not8reader task successes. Independent persisted-file checks and frozen source/adapted code-block comparisons passed. All essential adaptation changes have source IDs/docs or explicit untested status. A source audit caught/withdrew an overbroad wildcard claim; fixed-name commands and outcomes did not change. No human comprehension/effort benefit, generic path, permissions, concurrency or full workflow qualification. Reader follow-ups18/21 and integration review28 retain these limits.

Disposition: conditional two-layer artifact contract for the declared tested profile; keep faithful-with-gaps fallback. No translator/default/product integration. Raw evidence: https://github.com/smileynet/video-buddy/tree/f305c9fe9f3f87f5c04bf6c27e92d600a67b4f01/docs/architecture/spikes/guide-adaptation. Verification: eight persisted cases, five exact-byte frozen text restores, source/adaptation code-block and provenance checks passed. Pre-commit and dashboard desktop/mobile checks passed. Final staged evidence scope: nine files, 51,941 logical Git-blob bytes; inspection complete with no findings, excluding earlier freeze/history/ignored media.

## Resolution (2026-10-26)

Completed bounded two-file adaptation comparison. Guarded native commands create missing files and preserve existing content; explicit native source failure can exit zero, while Force negative control truncates content. No general translator, reader advantage or production integration qualified. Report docs/architecture/spikes/s6-adaptation-results.md; pinned raw evidence f305c9fe9f3f87f5c04bf6c27e92d600a67b4f01.

### Verification
1. ✓ A durable spike report records options, evidence and limitations — "Durable S6 report and pinned raw evidence f305c9f record both guide options, eight cases and limitations."
2. ✓ Every evaluated option records its fixture, environment and observations — "Frozen protocol b442b1b records source, child profile, versions and expectations; independent persisted-file and five exact-byte restoration checks passed."
3. ✓ The report states an adopt, retain, reject or unresolved verdict — "Conditionally adopt separately labeled tested adaptations; retain faithful gaps fallback, reject blind rewriting and exit-code-only success; human usability and integration remain unresolved in 18/21/28."
