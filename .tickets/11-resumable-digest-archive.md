---
id: "11"
title: "Make batch digest resumable with --download-archive + archive-vs-disk reconciliation"
status: open
blocked_by: ["10"]
priority: medium
validation_criteria:
  - "batch digest downloads use yt-dlp --download-archive so re-runs skip completed items"
  - "a reconcile/repair step re-fetches items whose file is missing or fails the ffprobe integrity check"
  - "interrupting and re-running performs zero redundant downloads for completed, verified items"
---

# Make batch digest resumable with --download-archive + archive-vs-disk reconciliation

## Context

`batch_digest.py` caches resolved JSON and sleeps between items, but the actual video downloads
have no resume/skip mechanism — an interrupted batch re-does work. Field evidence (sibling CLVGM
project, spike 04) showed `yt-dlp --download-archive` makes a multi-item batch idempotent and
resumable (completed ids are skipped on re-run). It also surfaced a gotcha: the archive can mark
an id done while the file is later deleted or is truncated, so a naive re-run won't restore it.
The fix is a reconcile/repair step that trusts the ffprobe integrity check (ticket 10) over the
archive: drop the archive line for any missing/bad file and re-fetch it.

Blocked by 10 because the repair step depends on the integrity check being the source of truth.

## What to build

1. Thread a `--download-archive <path>` through the batch download so completed items are skipped
   on re-run (archive kept in a stable location).
2. A reconcile/repair pass: for each expected output that is missing or fails the ffprobe check,
   remove its archive line and re-download, then re-verify.
3. Idempotent: a batch that is fully present + verified performs zero downloads on re-run.

## Acceptance criteria

- [ ] Batch downloads record completed items in a `--download-archive` file
- [ ] Re-running an interrupted batch skips verified-complete items (zero redundant downloads)
- [ ] Reconcile re-fetches any missing/bad item and clears its stale archive line
- [ ] Reconcile on a fully-good batch is a no-op
