---
id: "27"
title: "Qualify source acquisition and recovery before integration"
status: open
blocked_by: []
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/spikes/acquisition-recovery-results.md exists and records evidence, limitations and a disposition for each scoped question"
  - "tkt validate exits 0"
---

# Qualify source acquisition and recovery before integration

## Context and intent

Intent source: user request on 2026-10-25 to capture every remaining spike, put open research next, then review integration, features and architecture. Read docs/architecture/spike-plan.md, docs/architecture/workflow-proposal.md and docs/architecture/spikes/image-model-results.md. Primary job: apply a technique/build something and verify the result. Preserve unrelated working-tree changes. Prototype code stays on isolated spike branches; no production integration in a spike.

## What to build

A reproducible acquisition qualification report showing whether users can obtain trustworthy source media and recover interrupted intake/batches.

Compare current acquisition to minimal integrity/recovery alternatives; do not assume yt-dlp exit status or ffprobe metadata proves decode integrity. Cover YouTube and Vimeo where eligible, player URL/Referer, expired/auth-required sources, interrupted/partial downloads, archive-vs-disk mismatch, changed configuration and resume without duplicated successful work. Reuse S5 state-store evidence instead of rerunning its 20 scenarios; test actual acquisition seams. Use deterministic local faults and public/user-authorized source samples. Sources: tickets 09/10/11, the state-store report referenced by ticket 16. A missing path must be resolved from ticket 16 before execution.

## Acceptance criteria

- [ ] Freeze source metadata/media hashes, backend versions and reproducible failure fixtures.
- [ ] Demonstrate detection of truncated or undecodable media beyond successful downloader exit status.
- [ ] Observe auth-required, retry, repair and resume states with artifact/edit preservation.
- [ ] Compare archive reconciliation and stage-state choices using real acquisition outputs.
- [ ] Update proposed approaches in tickets 09/10/11 from measured findings before implementation.

## Out of scope

Automatic production integration, unsupported winners, and invented user/quality measurements.
