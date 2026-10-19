---
id: "09"
title: "Add Vimeo source support (player URL + Referer) alongside YouTube"
status: open
blocked_by: []
priority: medium
validation_criteria:
  - "a Vimeo embed (player.vimeo.com/video/<id>) resolves and downloads via yt-dlp with --referer"
  - "extract_video_id / fetch path recognizes vimeo.com and player.vimeo.com URLs"
  - "existing YouTube path and tests remain green"
---

# Add Vimeo source support (player URL + Referer) alongside YouTube

## Context

video-buddy is currently YouTube-only (`fetch/youtube.py` is the sole URL resolver; a workspace
grep for `vimeo` returns nothing). A lot of course/embedded content lives on Vimeo. Field
evidence from a sibling project (CLVGM course extraction): Vimeo embeds are commonly
**domain-privacy restricted** and resolve cleanly when you (a) target the embed URL
`https://player.vimeo.com/video/<id>` — NOT `https://vimeo.com/<id>`, which 404s for private
embeds — and (b) pass `--referer <embedding-page-url>`. No cookies were needed when the referer
matched the whitelisted domain. yt-dlp returns HLS/DASH (not progressive), which it muxes via
ffmpeg automatically.

## What to build

1. Recognize Vimeo URLs in the fetch/resolve path (both `vimeo.com/<id>` and
   `player.vimeo.com/video/<id>`), extracting the numeric id.
2. When downloading a Vimeo source, target the player URL and set yt-dlp `referer` to the
   embedding page (configurable; fall back to the player URL).
3. Keep the existing format selection but ensure it yields best AVC video + audio muxed to mp4.
4. Make the host (youtube|vimeo) explicit in whatever metadata/manifest the pipeline emits.

## Acceptance criteria

- [ ] A `player.vimeo.com/video/<id>` source downloads a playable mp4 via yt-dlp + `--referer`
- [ ] URL recognition handles `vimeo.com/<id>` and `player.vimeo.com/video/<id>`
- [ ] Bare `vimeo.com/<id>` for a private embed is handled/skipped gracefully (documented)
- [ ] Existing YouTube tests still pass; a Vimeo test (mock or live) is added

## Notes

Progressive MP4 is often absent on modern Vimeo; rely on yt-dlp's HLS/DASH handling + ffmpeg mux.
Format selector that worked in the field: `bv*[vcodec^=avc]+ba/b --merge-output-format mp4`.
