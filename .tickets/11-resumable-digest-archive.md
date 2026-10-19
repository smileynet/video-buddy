---
id: "11"
title: "Make batch digest resumable with --download-archive + archive-vs-disk reconciliation"
status: open
blocked_by: []
priority: medium
validation_criteria:
  - "batch digest downloads use yt-dlp --download-archive so re-runs skip completed items"
  - "a reconcile/repair step re-fetches items whose file is missing or fails the ffprobe integrity check"
  - "interrupting and re-running performs zero redundant downloads for completed, verified items"
---

# Make batch digest resumable with --download-archive + archive-vs-disk reconciliation

## What to build

TBD

## Acceptance criteria

- [ ] TBD
