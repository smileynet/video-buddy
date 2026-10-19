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

## Context

`frames/capture.py::download_video` currently wraps yt-dlp failures in `RuntimeError` and then
locates the output file, but it does not verify the file is actually complete/playable — a
zero/short-duration or stream-less file only surfaces later during scene detection (or not at
all). This matters because of a known yt-dlp behavior: a **fragmented (HLS/DASH) download missing
fragments can be marked "successful"** and (with `--download-archive`) recorded as done, leaving a
silently truncated file (yt-dlp issue #10808). Exit code 0 is therefore not proof of a good file.

Field evidence (sibling CLVGM project, spike 04): an ffprobe gate reliably distinguishes good
files (valid duration + video + audio streams) from a deliberately truncated one, and
`--abort-on-unavailable-fragment` makes truncation fail loudly instead of silently.

## What to build

1. After `download_video`, run an ffprobe check: format duration > 0 and at least a video stream
   present (audio if the pipeline needs it). Raise a clear error on failure.
2. Add `--abort-on-unavailable-fragment` to the yt-dlp options so missing fragments fail the
   download rather than producing a partial file.
3. Keep it fast (ffprobe reads container metadata; no full decode) so it is cheap per video.

## Acceptance criteria

- [ ] `download_video` returns only after ffprobe confirms duration > 0 and a video stream
- [ ] A truncated/zero-duration file raises before frame extraction runs
- [ ] yt-dlp options include `--abort-on-unavailable-fragment`
- [ ] Existing tests pass; a test simulates a bad file and asserts the raise
