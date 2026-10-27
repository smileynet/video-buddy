# Personal listening review and source-first guide

Prepared 27 October 2026. Tickets42/43 verify review artifacts, not human study results.

## Listening

Open **Blind listening comparison** on the dashboard. Choose a paragraph, listen to the common reference and anonymous A/B takes, rate clarity/naturalness/voice likeness, and save A/B/tie/neither/unsure preference. Assignment is randomized per review and kept across paragraphs/reloads. Reveal is enabled after saving a preference for that paragraph; later ratings with identities visible are labeled accordingly.

Browser localStorage holds drafts and saved preferences. No feedback is sent automatically or committed to Git. Copy/download JSON to share it. Export records the audio-set hash, neutral filenames, paragraph, ratings, preference, notes and hidden-label status. With storage blocked, state is page-only and the UI explains export. Starting another review retains saved history.

Five curated FLACs use first seed1729 takes from both frozen paragraphs and the common reference. One constant gain per clip matches a common RMS target with pitch/duration/words unchanged; RMS does not guarantee identical perceived loudness. Originals remain in the spike. Prior exposure, one reference and inspectable local sources mean this is a personal blind-label comparison, not an independent study or automatic quality score. No human preference was entered by the agent.

[Audio provenance](../../assets/listening/manifest.json) · [Behavior/retention](../../assets/listening/README.md) · [Original model comparison](local-narration-results.md).

## Teaching versus building

The primary guide teaches the source's decision framework and pipeline illustration in seven topics. Both A/B views have identical content/evidence; topic6 uses the settings frame at6:42. Understanding the source and applying its reasoning does not require building a program.

Our implementation plan is a separate optional worked-example companion. Its local TTS component was measured; its full joining/captioned-export workflow remains unbuilt. This source is a decision video with a pipeline illustration. For future sources that are actual worked walkthroughs, demonstrated steps remain primary and extensions stay labeled.

[Template](../../templates/video-guide.md), [agent guidance](../../agents/video-guide-authoring.md) and AGENTS.md distinguish learning, example execution and tool qualification. Proposing and executing an example are separate activities; use existing user authorization rather than quietly expanding authoring into a build. [Pinned source-first guide and companion](https://github.com/smileynet/video-buddy/tree/be4cbf793bedcd4ca21885ade9eec86053aed4a9/docs/architecture/spikes/review-ux).

## Checks

Fresh headless Chromium contexts verified anonymous playback, persisted drafts/assignment/preference, reveal gating, paragraph switching, retained history, sanitized receipt, JSON download, mobile and no page errors. Only synthetic QA responses were used and discarded; no actual user storage was inspected. Guide tests verified all seven topics match in A/B, source-frame alignment, optional companion status, links/mobile and note retention. Existing dashboard tabs pass. Online YouTube playback, human learning and human voice-quality outcomes remain unqualified.
