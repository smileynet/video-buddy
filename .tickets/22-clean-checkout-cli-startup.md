---
id: "22"
title: "Restore CLI startup in a clean checkout by resolving the missing breakdown helper"
status: open
blocked_by: []
priority: high
validation_criteria:
  - "A clean checkout can run uv run video-buddy --help without ImportError"
tags: ["workflow-spikes"]
---

# Restore CLI startup in a clean checkout by resolving the missing breakdown helper

## What to build

Given a clean checkout of current main, the CLI should load and show help. Discovered during S2 on 2026-10-25: `uv run video-buddy init --no-models` raised `ImportError: cannot import name '_find_breakdown' from 'video_buddy.batch_digest'`. `src/video_buddy/cli.py` imports that helper while the committed `batch_digest.py` lacks it. The primary checkout has an uncommitted implementation; do not overwrite or independently commit that user's pending work without reconciling it. The experimental branch copied the existing helper solely to unblock the spike.

Read `src/video_buddy/cli.py`, `src/video_buddy/batch_digest.py` and `tests/test_digest.py`. Source: actual clean-worktree execution while working ticket 13. Reconcile the intended helper and add a clean-entrypoint check rather than trusting an editable environment with pending fixes.

## Acceptance criteria

- [ ] A fresh checkout/environment can import the CLI and run `uv run video-buddy --help`.
- [ ] The helper's existing cross-date lookup behavior is preserved or intentionally documented.
- [ ] Relevant digest/CLI checks pass without relying on uncommitted primary-checkout files.
