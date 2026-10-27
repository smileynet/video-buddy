# Personal blind listening review

The dashboard offers two paired paragraphs from local narration spike41 plus the common reference. This is a personal comparison of Qwen3-TTS and Chatterbox-Turbo, not a replication of the video's multi-model test.

## Audio and preparation

Five neutral-name FLAC files are curated playback references, not new generation results. The first seed1729 take for each paragraph/model was selected consistently. Original outputs and receipts remain pinned in the experimental spike. manifest.json records source/output hashes, durations and constant gains. Copies share an RMS target, with a common peak constraint and unchanged duration/pitch; no word, timing or dynamic edits. RMS matching does not guarantee identical perceived loudness. The official demo reference has different words from the narration and is not the user or video creator.

## Personal feedback

review.js randomizes the A/B assignment per review and preserves it across paragraphs/reloads. Ratings start blank; every quality can be rated1–5 or explicitly Not sure. Preference supports A, B, tie, neither and unsure. Save a preference before revealing identities. Later ratings after reveal are marked accordingly; starting a new review retains saved history. Prior familiarity and inspectable local sources mean this is UI-label blinding, not an independent research study.

Browser localStorage holds drafts, assignments and saved self-reports. No feedback is sent, copied to Git or automatically included in model findings. Copy/download JSON to share or retain it. If storage is blocked, the page states its memory-only limitation and offers export. This is a static review artifact, not an integrated application account or backend.

## Verification

Fresh headless Chromium tests used synthetic QA notes in a separate context. Verified reference/paired audio metadata, hidden identities, blank-input guard, score/preference capture, reload persistence, stable assignment, reveal after save, correctly labeled receipt, JSON download, independent paragraph drafts, retained history, mobile width and absence of page errors. No actual human score or preference is included in this repository. Source-first guide and optional companion have separate content/navigation checks.

## Retention

Retain this bounded playback set, manifest and review script in ordinary Git so the dashboard works offline from a fresh copy. Original measurements stay in their spike branch; model caches and additional runs are excluded. Do not commit exported personal ratings. No source video, model weights, LFS migration, history rewriting or storage-cost claim.
