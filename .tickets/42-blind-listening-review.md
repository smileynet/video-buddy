---
id: "42"
title: "Add a personal blind listening review to the dashboard"
status: done
blocked_by: []
validation_criteria:
  - "Anonymous paired playback, reference and ratings work before model reveal"
  - "Preference survives browser reload and exports without sending feedback"
  - "Audio provenance, limits and desktop/mobile behavior are verified"
tags: ["workflow-spikes"]
---

# Add a personal blind listening review to the dashboard

## What to build

User requested a dashboard comparison of Qwen3-TTS and Chatterbox-Turbo for clarity, naturalness and reference likeness, with recorded preference. Use frozen first takes of the same two paragraphs and the shared reference. Hide randomized model assignment until a preference is saved, then allow reveal. Keep personal feedback private in browser storage and offer a portable export. Preserve prior-exposure and level-matching limits; do not infer objective quality or collect feedback automatically.

Implemented under docs/assets/listening/ and the existing dashboard: five neutral-name constant-gain listening files, metadata/provenance, paired/reference playback, six explicit ratings, tie/neither/unsure preference, optional notes, stable assignment/drafts across reload, save/reveal, paragraph switching, history and JSON export. Audio remains timing/pitch unchanged; RMS matching is not guaranteed perceived-loudness matching.

Verified in fresh headless Chromium contexts only with synthetic QA responses; no actual human response is recorded in Git. No remote sends, API calls or model execution. Storage-policy failure falls back to page-only state with an export reminder.

## Acceptance criteria

- [x] Both paragraph pairs and reference play with neutral labels before reveal.
- [x] Explicit ratings/preference can be saved, retained across reload, revealed and exported.
- [x] Real user responses remain private and separate from synthetic QA or measured model receipts.
- [x] Mobile/desktop, media provenance and blinding limitations are documented.

## Resolution (2026-10-27)

Delivered personal blind-label dashboard listening panel for clarity/naturalness/likeness and private recorded preference. Level-matched first takes/reference, stable random assignment, explicit save/reveal and export. Browser storage/private download only, no human preference manufactured or automatic quality verdict. QA synthetic; prior exposure and inspectable source limits remain explicit.

### Verification
1. ✓ Anonymous paired playback, reference and ratings work before model reveal — "Dashboard reference and two neutral paragraph pairs; randomized consistent A/B assignment; explicit three-quality ratings and save-before-reveal checked in fresh Chromium."
2. ✓ Preference survives browser reload and exports without sending feedback — "Synthetic QA verified persisted assignment/drafts/preference, reveal receipt, JSON download, paragraph independence and history; no real user data inspected or sent."
3. ✓ Audio provenance, limits and desktop/mobile behavior are verified — "Five constant-gain assets with hashes/durations/provenance; desktop/mobile, offline playback, privacy/export and blinding limits documented in docs/architecture/spikes/blind-listening-review.md."
