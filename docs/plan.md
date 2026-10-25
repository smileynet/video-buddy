# Work plan

Ticket state projection, updated 2026-10-25. Ticket files are the detailed execution record.

Completed: **24 — Open research**, with a cited decision register and independent audit. Completed **14 — bounded real-video OCR comparison**. Current priority: **30–34 — current-provider comparisons**, alongside original model qualification23. Ticket 23 remains in progress; OCR14 has a bounded per-role verdict with human benefit unresolved. SAM 3 ran, SAM 3.1 has a session API blocker, DINOv3 access is now approved; inference pending. Final feature/integration/architecture review is ticket 28 after the primary qualification reports. Conditional tickets 19/20 remain backlog.

| id | title | status |
|---|---|---|
| 29 | Verify current provider models and comparison eligibility | ✅ done |
| 30 | Compare Gemini region grounding and temporal evidence | open |
| 31 | Compare Ai2 pointing tracking and interface grounding | in_progress |
| 32 | Compare YOLOE promptable detection and segmentation | in_progress |
| 33 | Compare hosted DINO-X grounding against local baselines | open |
| 34 | Evaluate NVIDIA reasoning for physical demonstration evidence | open |
| 24 | Resolve open research questions before the next spike round | ✅ done |
| 14 | Compare OCR for exact commands and settings | ✅ done |
| 23 | Compare image element models by downstream evidence jobs | in_progress |
| 25 | Find complete readable subject states by seeking within video windows | open |
| 26 | Compare ordered frames and video input for action evidence | open |
| 15 | Compare speech paths on implementation-critical details | open |
| 17 | Evaluate evidence-preserving adaptation to a target environment | open |
| 18 | Compare Markdown and adjacent-evidence review for blocked steps | open |
| 21 | Measure guide versus note usability with a fresh task performer | open |
| 27 | Qualify source acquisition and recovery before integration | open |
| 22 | Restore CLI startup in a clean checkout by resolving the missing breakdown helper | open |
| 28 | Review spike findings and decide app features and integration architecture | open |
| 07 | Re-transcribe rate-limited digest videos with CrisperWhisper on GPU | open |
| 08 | Make CrisperWhisper the default engine in workspace config | open |
| 09 | Add Vimeo source support (player URL + Referer) alongside YouTube | open |
| 10 | Verify downloaded video integrity with ffprobe (do not trust yt-dlp exit code) | open |
| 11 | Make batch digest resumable with --download-archive + archive-vs-disk reconciliation | open |
| 19 | Evaluate attribution only when it changes the next action | backlog |
| 20 | Evaluate retrieval when saved solutions become hard to find | backlog |
| 01 | Evaluate CrisperWhisper against current Whisper pipeline | ✅ done |
| 02 | Add WhisperX backend for word-level timestamps + diarization | ✅ done |
| 03 | Add CrisperWhisper isolated backend for verbatim + hallucination detection | ✅ done |
| 04 | Extend transcript JSON schema for word-level timestamps and disfluency metadata | ✅ done |
| 05 | Execute ASR benchmark: faster-whisper vs WhisperX vs CrisperWhisper on test corpus | ✅ done |
| 06 | Auto-select CrisperWhisper when monolith is reachable | ✅ done |
| 12 | Evaluate whether implementation guides improve task completion | ✅ done |
| 13 | Find the minimum visual evidence needed to reproduce actions | ✅ done |
| 16 | Choose a state store using interruption and concurrency probes | ✅ done |

## Spike ordering

12 (S1) → 13 (S2) → 14 (S3). Ticket 15 (S4), 17 (S6), and 18 (S7) depend on 12. Ticket 16 (S5) can run independently. Tickets 19 (S8) and 20 (S9) are conditional backlog, not required for the primary apply/build job.

A completed report can record an unresolved verdict, but do not treat it as approval to integrate. Existing tickets 08 (default ASR), 10 (integrity) and 11 (resume) overlap tool/state decisions; review the new findings before implementing their proposed approaches.

Latest evidence: [S2 results](architecture/spikes/s2-results.md). Ticket 22 tracks clean-checkout CLI startup; experimental helper/flags stay on the spike branch. A closed spike with an unresolved verdict does not validate a production feature.

Image-model evidence: [per-job results](architecture/spikes/image-model-results.md). Thirteen accessible configurations ran; SAM 3.1 has an upstream runtime blocker and DINOv3 access is now approved; inference pending. [OCR14 results](architecture/spikes/s3-ocr-results.md) cover20 held-out real lines; models23 still require remaining qualification.

Research 24 is complete: [decision register](agents/research/open-questions.md), [independent audit](agents/research/open-questions-audit.md). Remaining primary spikes: models 23, subject-window seeking 25, temporal evidence 26, speech 15, adaptation 17, review UX 18, fresh-performer usability 21, acquisition/recovery 27. Review 28 depends on these reports; it decides final scope and creates integration tickets. Conditional attribution/retrieval 19/20 are reviewed for deferral, without blocking the primary job.

## Expanded current-provider coverage

User priority: research29, then eligible provider comparisons30–34 alongside original model23. Gemini30, Ai2 31, YOLOE32, hosted DINO-X33 and NVIDIA34 must be explicitly measured, blocked or deferred before integration review28. No universal market coverage claim follows from the original shortlist.

Provider progress: research29 complete; YOLOE32 has bounded text/visual findings;31 has Molmo2NF4/Qwenimage probes but specialists/temporal qualification remain open.30/33 have no matching key after checked project/mise/HFCLI lookup;34 lacks a running supported reasoner endpoint. HF_TOKEN is saved in ignored.env.local and authenticated; distinct hosted API access remains unverified. Review28 retains these dependencies.
