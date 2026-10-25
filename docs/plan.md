# Work plan

Ticket state projection, updated 2026-10-25. Ticket files are the detailed execution record.

Next experiment: ticket 14 (OCR); S1/S2 closed with bounded findings, with human usability still unresolved in ticket 21. [Spike definitions](architecture/spike-plan.md), [S1 evidence](architecture/spikes/s1-status.md), [dashboard](architecture-dashboard.html). Do not integrate a proposed feature before its relevant experiment reports an evidence-backed verdict.

| id | title | status |
|---|---|---|
| 01 | Evaluate CrisperWhisper against current Whisper pipeline | ✅ done |
| 02 | Add WhisperX backend for word-level timestamps + diarization | ✅ done |
| 03 | Add CrisperWhisper isolated backend for verbatim + hallucination detection | ✅ done |
| 04 | Extend transcript JSON schema for word-level timestamps and disfluency metadata | ✅ done |
| 05 | Execute ASR benchmark: faster-whisper vs WhisperX vs CrisperWhisper on test corpus | ✅ done |
| 06 | Auto-select CrisperWhisper when monolith is reachable | ✅ done |
| 07 | Re-transcribe rate-limited digest videos with CrisperWhisper on GPU | open |
| 08 | Make CrisperWhisper the default engine in workspace config | open |
| 09 | Add Vimeo source support (player URL + Referer) alongside YouTube | open |
| 10 | Verify downloaded video integrity with ffprobe (do not trust yt-dlp exit code) | open |
| 11 | Make batch digest resumable with --download-archive + archive-vs-disk reconciliation | open |
| 12 | Evaluate whether implementation guides improve task completion | ✅ done |
| 13 | Find the minimum visual evidence needed to reproduce actions | ✅ done |
| 14 | Compare OCR for exact commands and settings | open |
| 15 | Compare speech paths on implementation-critical details | open |
| 16 | Choose a state store using interruption and concurrency probes | ✅ done |
| 17 | Evaluate evidence-preserving adaptation to a target environment | open |
| 18 | Compare Markdown and adjacent-evidence review for blocked steps | open |
| 19 | Evaluate attribution only when it changes the next action | backlog |
| 20 | Evaluate retrieval when saved solutions become hard to find | backlog |
| 21 | Measure guide versus note usability with a fresh task performer | backlog |
| 22 | Restore CLI startup in a clean checkout by resolving the missing breakdown helper | open |

## Spike ordering

12 (S1) → 13 (S2) → 14 (S3). Ticket 15 (S4), 17 (S6), and 18 (S7) depend on 12. Ticket 16 (S5) can run independently. Tickets 19 (S8) and 20 (S9) are conditional backlog, not required for the primary apply/build job.

A completed report can record an unresolved verdict, but do not treat it as approval to integrate. Existing tickets 08 (default ASR), 10 (integrity) and 11 (resume) overlap tool/state decisions; review the new findings before implementing their proposed approaches.

Latest evidence: [S2 results](architecture/spikes/s2-results.md). Ticket 22 tracks clean-checkout CLI startup; experimental helper/flags stay on the spike branch. A closed spike with an unresolved verdict does not validate a production feature.
