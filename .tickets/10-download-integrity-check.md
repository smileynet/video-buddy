---
id: "10"
title: "Verify downloaded video integrity with ffprobe (do not trust yt-dlp exit code)"
status: open
blocked_by: []
priority: high
validation_criteria:
  - "download_video verifies the output via ffprobe: duration > 0 and has a video stream before returning"
  - "a truncated/zero-duration file raises instead of proceeding to frame extraction"
  - "covers the yt-dlp fragmented-download-marked-done truncation case"
---

# Verify downloaded video integrity with ffprobe (do not trust yt-dlp exit code)

## What to build

TBD

## Acceptance criteria

- [ ] TBD
