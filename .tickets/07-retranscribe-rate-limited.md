---
id: "07"
title: "Re-transcribe rate-limited digest videos with CrisperWhisper on GPU"
status: open
blocked_by: ["06"]
priority: high
---

# Re-transcribe rate-limited digest videos with CrisperWhisper on GPU

## Context

The Aug 10-11 digests have 89 videos with metadata-only breakdowns because YouTube rate-limited
caption downloads. Now that:
1. YouTube downloads are fixed (yt-dlp 2026.08.19)
2. CrisperWhisper on monolith runs at 75x realtime

We can re-transcribe all 89 videos (~30 min total on GPU) and upgrade their breakdowns from
metadata stubs to full transcript-grounded analysis.

## What to build

1. Identify all videos with metadata-only breakdowns (no transcript or captions)
2. Download audio for each via yt-dlp
3. Transcribe via CrisperWhisper on monolith (batch, ~30 min total)
4. Write v2 transcripts with word timestamps
5. Re-run agent breakdown generation for upgraded videos
6. Replace metadata-only breakdowns with full transcript-grounded versions

## Acceptance criteria

- [ ] All 89 rate-limited videos identified
- [ ] Audio downloaded for all (yt-dlp 2026.08.19 working)
- [ ] CrisperWhisper transcripts generated for all (v2 schema with words)
- [ ] Breakdowns upgraded from metadata-only to transcript-grounded
- [ ] Digest notes recompiled with updated summaries

## Validation criteria

- Spot-check 3 upgraded breakdowns: contain timestamped quotes grounded in transcript
- Zero metadata-only stubs remaining in the 2026-08-10 and 2026-08-11 digest directories
- Total GPU processing time documented
