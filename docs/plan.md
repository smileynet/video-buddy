# Work plan

Ticket state projection, updated 2026-10-27. Ticket files are the detailed execution record.

Tickets **42/43 review artifacts complete**: [personal listening and source-first teaching](architecture/spikes/blind-listening-review.md). Rate anonymous audio and save/export a private preference. Primary teaching, optional builds and model qualification are separated; no human response was collected by the agent. Ticket18 remains a reader/layout question.

Ticket **41 bounded local narration comparison complete**: [findings and listening evidence](architecture/spikes/local-narration-results.md). Both candidates ran four cases on the same paragraphs/reference. Chatterbox warm generation was faster; Qwen used less process RAM. No human quality winner; machine-text disagreement remains for listening review. Guide/dashboard updated; no production engine/default integration.

Ticket **18 review packs prepared, reader review pending**: [procedure and limits](architecture/spikes/s7-review-ux-preparation.md). Narration, native-browser and a local members-source modeling guide now have linked/adjacent-evidence comparisons. Teaching and runnable examples stay separate; source moments, retained frames, recovery and exact-topic return are available. Browser checks establish behavior, not usability. No winner/integration. Next: collect formative reader feedback;21 retains fresh-performer qualification.

Ticket **17 bounded walkthrough complete**: [adaptation findings](architecture/spikes/s6-adaptation-results.md). The labeled native route creates the two source placeholders and preserves existing work in a declared no-GNU profile. Original lines work on the normal host; exit0/no-files and Force truncation controls reinforce postcondition checks. Reader comprehension remains18/21; no general translator or production integration.

Ticket **15 bounded comparison complete**: [audio-model review findings](architecture/spikes/s4-model-reviewed-results.md). SenseVoice reviewed the55-second pack; raw model references were frozen before Whisper comparisons and remain model-reviewed provisional, never human-verified. Code spelling and token timing limits prevent an accuracy/default winner. Human qualification is deliberately deferred in40;38/39 own recovery/provenance proposals.

Ticket **36 comparison complete**: [revision-boundary results](architecture/spikes/revision-boundary-results.md) separate 180 development frames from 509 locked validation frames. Preferred packets solved development but retained only2–3/4 terminal validation states; settled runs and the grid reached4/4 at cap4. Other-source UI reached3/3 visually via fallback, with inexact writing. No new default or integration. Ticket 25 is closed with an evidence-linked synthesis and explicit unresolved limits; broader tracking research is deliberately deferred to 37. Ticket 35 owns the production selector failure. Review28 consumes the negative/conditional verdict and still depends on the remaining spikes.

| id | title | status |
|---|---|---|
| 18 | Compare Markdown and adjacent-evidence review for blocked steps | open |
| 21 | Measure guide versus note usability with a fresh task performer | open |
| 26 | Compare ordered frames and video input for action evidence | open |
| 27 | Qualify source acquisition and recovery before integration | open |
| 22 | Restore CLI startup in a clean checkout by resolving the missing breakdown helper | open |
| 30 | Compare Gemini region grounding and temporal evidence | open |
| 33 | Compare hosted DINO-X grounding against local baselines | open |
| 34 | Evaluate NVIDIA reasoning for physical demonstration evidence | open |
| 28 | Review spike findings and decide app features and integration architecture | open |
| 35 | Preserve useful low-edge code frames in frame selection | open |
| 38 | Prevent no-speech retries from publishing unsupported transcript text | open |
| 39 | Preserve caption origin and reference lineage in source artifacts | open |
| 07 | Re-transcribe rate-limited digest videos with CrisperWhisper on GPU | open |
| 08 | Make CrisperWhisper the default engine in workspace config | open |
| 09 | Add Vimeo source support (player URL + Referer) alongside YouTube | open |
| 10 | Verify downloaded video integrity with ffprobe (do not trust yt-dlp exit code) | open |
| 11 | Make batch digest resumable with --download-archive + archive-vs-disk reconciliation | open |
| 37 | Qualify broader subject tracking only when a concrete task requires it | backlog |
| 40 | Qualify speech changes with human-verified commands, numbers and timing | backlog |
| 19 | Evaluate attribution only when it changes the next action | backlog |
| 20 | Evaluate retrieval when saved solutions become hard to find | backlog |
| 42 | Add a personal blind listening review to the dashboard | ✅ done |
| 43 | Separate source teaching from optional worked examples | ✅ done |
| 41 | Compare Qwen3-TTS and Chatterbox-Turbo for paragraph narration | ✅ done |
| 17 | Evaluate evidence-preserving adaptation to a target environment | ✅ done |
| 29 | Verify current provider models and comparison eligibility | ✅ done |
| 31 | Compare Ai2 pointing tracking and interface grounding | ✅ done |
| 32 | Compare YOLOE promptable detection and segmentation | ✅ done |
| 24 | Resolve open research questions before the next spike round | ✅ done |
| 14 | Compare OCR for exact commands and settings | ✅ done |
| 15 | Compare speech paths on implementation-critical details | ✅ done |
| 23 | Compare image element models by downstream evidence jobs | ✅ done |
| 36 | Spike revision boundaries for typing and scrolling without prefix budget loss | ✅ done |
| 25 | Find complete readable subject states by seeking within video windows | ✅ done |
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

Latest frame evidence: [locked revision-boundary comparison](architecture/spikes/revision-boundary-results.md). Earlier [S2 results](architecture/spikes/s2-results.md) remain a historical acquisition/selection probe. Ticket 22 tracks clean-checkout CLI startup; experimental helper/flags stay on the spike branch. A closed spike with an unresolved verdict does not validate a production feature.

Image-model evidence: [per-job results](architecture/spikes/image-model-results.md). DINOv3 and SAM3.1 now have bounded inference records. [OCR14 results](architecture/spikes/s3-ocr-results.md) cover20 held-out real lines; complete-state and task qualification remain25/26.

Research 24 is complete: [decision register](agents/research/open-questions.md), [independent audit](agents/research/open-questions-audit.md). Original model comparison23 has a bounded disposition. Frame evidence synthesis 25 is complete. Speech15 now has a bounded qualified disposition. Adaptation17 now has a conditional, scoped disposition. Remaining primary work: review UX18, fresh-performer usability 21, temporal evidence 26 and acquisition/recovery 27. This order finishes the live frame thread, then earlier commitments in the same workflow stream. Ticket 22 remains the clean-CLI prerequisite where needed. Broader tracking research 37 is deferred until a concrete failed task justifies it, alongside conditional 19/20. Review 28 depends on these reports; it decides final scope and creates integration tickets. Conditional attribution/retrieval 19/20 are reviewed for deferral, without blocking the primary job.

## Expanded current-provider coverage

User priority: research29, then eligible provider comparisons30–34 alongside original model23. Gemini30, Ai2 31, YOLOE32, hosted DINO-X33 and NVIDIA34 must be explicitly measured, blocked or deferred before integration review28. No universal market coverage claim follows from the original shortlist.

Provider progress: research29 complete; YOLOE32 has bounded text/visual findings;31 now has Molmo2 plusGUI/video specialist NF4 probes; dense trajectory and native-video qualification remain25/26.30/33 have no matching key after checked project/mise/HFCLI lookup;34 lacks a running supported reasoner endpoint. HF_TOKEN is saved in ignored.env.local and authenticated; distinct hosted API access remains unverified. Review28 retains these dependencies.
