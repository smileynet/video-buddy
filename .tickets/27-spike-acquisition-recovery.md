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

## Ticket 24 research execution contract (2026-10-25)

**Budget:** One active day.

Use local deterministic corruption/interruption fixtures plus authorized live YouTube/Vimeo samples where accessible. Compare downloader success, ffprobe structure and full decode of the bounded fixture; archive/disk reconciliation and safe retry/resume. Record invalid-media detection, duplicate work, lost edits, auth-required behavior and stage recovery. Reuse S5 findings, do not claim container probing proves every frame decodes.

Record raw outputs, exact versions/configuration, failures and a per-job disposition. Report metrics even if they do not favor a candidate; no invented quality threshold. Research register: `docs/agents/research/open-questions.md`.

### State-store scope boundary

S5 used one global Windows writer lock and immediate process-exit injection. Its 20/20 observations do not qualify Linux locks, network filesystems, power loss, multi-source throughput, or edits beyond a sidecar. Test per-source concurrent acquisition for the intended deployment; record unsupported platforms. Reopen the store choice only if these actual requirements invalidate the bounded file approach.

## Additional acquisition observation — October 28, 2026

During intake of public video P3TCZ2xrvbo, default ingest downloaded video/audio, then failed because no OCR engine was installed. Retrying the CLI with --ocr off downloaded media again before completing frames/correlation/render. The agent directly inspected selected frames instead. Include this missing-optional-engine/configuration retry in the existing acquisition/recovery qualification; determine whether configuration preflight or retained-media reuse avoids repeat acquisition. This single observation does not establish a general cache bug or justify changing production download behavior during wrap-up.
