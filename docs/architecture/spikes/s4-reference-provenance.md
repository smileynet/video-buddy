# Speech references: caption origin verified, listening still required

**Ticket 15 · 25 October 2026 · provenance measured; new speech references unreviewed. No new model scores or default change.** The previous speech report remains [first-round evidence](s4-speech-results.md). This update resolves caption-origin and duplicate-reference questions, and prepares a bounded listening check rather than another proxy score.

## Verified caption origins

| Source | Selected current English track | Observed relation to publisher reference | What this establishes |
| --- | --- | --- | --- |
| Traversy Git crash course, earlier 852–868s probe | `automatic_captions`, en, URL `kind=asr`; no manual tracks | All frozen local cues match the explicit automatic-track download; 1,392 parsed cues overall | Original comparison used automatic captions, not independent human truth. |
| MIT Battlecode Git lecture, 2013 | YouTube `subtitles`, en, English; no `kind=asr` query | Official OCW VTT and YouTube VTT have all 959 parsed cue records equal, including times/text | A publisher/manual-classified track; matching copies do not independently validate each other. No per-file human-review certification. |
| CS50 Command Line, 2017 asset linked from current course page | YouTube `subtitles`, en, English; no `kind=asr` query | Both have371 cues; raw parsed objects differ, but HTML-decoded normalized word sequences are identical (3,694 words) | Formatting differences do not establish independent reference creation. Manual classification alone does not prove human review. |

These are fresh yt-dlp2026.10.21 metadata/explicit caption downloads plus repository parser checks, not assumptions from channel reputation. Compact JSON records retain hashes, selection rules and comparisons. Full metadata/signed caption URLs remain ignored. The current fetch schema loses track origin, which is now tracked as proposed integration ticket39 after review28.

## What independent research supports

[MIT's 2015 description](https://news.mit.edu/2015/3play-media-more-efficient-video-captioning-0408) documents an ASR-first workflow with contracted editors and managerial checking. [Current OCW Studio architecture](https://engineering.ol.mit.edu/system_architecture/ocw-studio/system-context/) identifies the transcript vendor relationship. These are institutional workflow observations, not certificates for the particular 2013/2017 files and not manually labeled acoustic word boundaries.

[Research findings](../../agents/research/speech-reference-provenance.md) and a [separate citation audit](../../agents/research/speech-reference-provenance-audit.md) preserve those historical boundaries. The audit passed9/10; its source-date correction was applied. Official hosting, a manual track flag, repeated captions and agreement with another ASR cannot replace the requested independent listening check.

## The concrete reference check

Three frozen source excerpts total55seconds. No new model prediction has been generated for them.

| Clip | Source time | What to check by listening |
| --- | --- | --- |
| MIT Git lecture | 21:07–21:38 | Actual wording of git status; number/phrase three times; action-order context |
| CS50 mkdir | 08:26–08:38 | mkdir, pset2, and the speaker's correction; do not rewrite speech into an ideal command |
| CS50 cp | 09:06–09:18 | cp, two arguments, source/destination wording |

These numeric examples cover counts and filename digits, not unseen ports, versions or numeric parameters. Publisher cue boundaries group words; only a listener can presently check actual target boundaries here. Record times relative to the exact audio clip with uncertainty. Source-video offsets remain nominal container positions.

**[Open the local listening pack](D:/.codex/worktrees/spike-state-comparison/video-buddy/docs/architecture/spikes/speech-details/reference-review.html).** It plays the clips offline, keeps the publisher draft collapsed, and exports anonymous review JSON. Nothing uploads or persists automatically. Listen, record literal words and any uncertainty, mark target times, then save the review. Partial/uncertain work stays explicitly unverified; music-only/silence cannot simultaneously be marked as containing spoken targets. The tool records an attestation, not proof that someone listened.

The local link points to this session's managed worktree, not a portable installation path. Pinned spike evidence and recovery instructions accompany ticket15. To replay elsewhere, extract `review-inputs-*.zip` into `.scratch/speech-details/provenance/review/` in that checkout and open `reference-review.html`. All three restored hashes and embedded-manifest consistency passed. Source-derived clips/text retain their publishers' [CC BY-NC-SA4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) terms and source credits; see the spike's `review-attribution.md`. No production feature or source-wide license endorsement follows.

## Music-only clarification

The user identified empty tracks as music-only. Exclude those designated tracks from spoken-command/number references and retain them as non-speech controls. The earlier authored digital-silence and tone fixtures remain separate synthetic controls. No production missing-caption classifier was added.

## Remaining gate and next execution

Ticket15 remains in progress. This session has no audio-listening tool, and no reviewed transcript/timestamp file or completed listening record was supplied. Therefore **independently checked spoken words and word timing have not yet been established**. The prepared publisher drafts are not promoted to that status. No new WER, number-accuracy or timing-accuracy result is claimed from them.

Next: complete the listening record, inspect it, lock the corrected reference and scoring policy before inference, then run the unchanged eligible candidates and caption tracks on these exact inputs. Treat duplicate reference lineage separately. Decide on alignment only if a measured evidence-location failure requires it. CrisperWhisper identity/runtime and representative numeric-parameter coverage remain explicit gaps. Review28 still gates any default or feature change;38 owns the observed no-speech retry failure and39 owns caption provenance preservation.

## Evidence and verification

Pinned [raw evidence / review pack,18cae9f](https://github.com/smileynet/video-buddy/tree/18cae9f23631a136cfe2a54108ae29c238ab6461/docs/architecture/spikes/speech-details). Existing54edit-distance checks and11original input restores still pass;3new unreviewed inputs restore with matching hashes and an embedded-manifest check. Offline review playback metadata/durations, partial exports, invalid timing ranges, music-only classification and mobile layout passed. Automated QA exports remain ignored and are explicitly not listening evidence. Dashboard four-tab/mobile/deep-link checks and pre-commit passed.

Final staged-artifact scope:15files,1,513,284logicalGit-blob bytes, complete metadata/content coverage and no findings; earlier commits/history/ignored originals were excluded. Three separate compact ZIPs retain the reference inputs under existing repository limits; no LFS/history change. Research verification incidentally refreshed the experimental environment; its worktree lock was restored and core versions remained1.2.1/4.7.1/2026.10.21. No new model inference followed that event; future comparisons must recheck runtime identity.
