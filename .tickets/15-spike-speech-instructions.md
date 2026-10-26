---
id: "15"
title: "Compare speech paths on implementation-critical details"
status: done
blocked_by: ["12"]
spec: "apply-build"
priority: medium
tags: ["workflow-spikes"]
validation_criteria:
  - "A durable spike report records options, evidence and limitations"
  - "Every evaluated option records its fixture, environment and observations"
  - "The report states an adopt, retain, reject or unresolved verdict"
---

# Compare speech paths on implementation-critical details

## Intent source

User requested tickets and execution of the proposed spikes, prioritizing applying a technique or building something. This is spike S4 in [the spike plan](../docs/architecture/spike-plan.md).

## Context

Read [shared experiment contract](../docs/architecture/spike-plan.md#shared-experiment-contract), [architecture proposal](../docs/architecture/workflow-proposal.md), and [primary-source research](../docs/agents/research/video-workflow-architecture.md). Dashboard: `docs/architecture-dashboard.html`. Preserve existing unrelated working-tree changes. Production integration is out of scope.

## What to build

A reproducible comparison that resolves the deciding question below, or explicitly records the missing observation when evidence cannot settle it. No production feature or automatic winner is required.

**Deciding question:** which eligible configuration recovers the instructions and timings needed for these tasks?

**Options:** A: available captions; B: faster-whisper with word timestamps; C: exact installed CrisperWhisper distribution/model if eligible and available. Compare native timing against WhisperX alignment only on passages where native timing fails the evidence-location task.

**Throwaway:** manually reference short passages containing names, commands, numbers, silence and music. Compare ASR engines on matched hardware/model scale/settings where possible; report caption-source differences and unmatched configurations separately. Validate model/code licenses before treating an option as deployable.

**Observe:** critical-term/number errors, omissions/additions, WER/CER, timestamp boundary error, total elapsed time including transfer/preprocessing, memory and setup. Score transcript errors separately from alignment errors.

**Decision:** choose a default/fallback for the actual eligible deployment, not a universal winner. Keep captions if sufficient for orientation; do not present uncertain spoken commands as executable facts. Add forced alignment only if improved location accuracy is needed and observed.

**Budget:** one day. **Unlocks:** speech profile defaults, escalation and timing policy. Replaces conclusions, not historical measurements, from the old benchmark.

## Acceptance criteria

- [x] A durable report identifies the deciding question, actual compared options and frozen fixtures.
- [x] Every evaluated option records environment, observations, costs and evidence locations.
- [x] The report states the verdict and distinguishes observed results from unresolved limitations.
- [x] Evidence supports the downstream user job; no integration or user-study success is claimed without observation.

## Execution record

Started 2026-10-25 after user-directed closure of 25. Report: `docs/architecture/spikes/s4-speech-results.md`. Actual experiment branch `codex/spike-speech-details`, final raw commit `b5030a893e465dd2d8aca532aa048b6d109e7e32`; raw replay/code/references under `docs/architecture/spikes/speech-details/`. Three faster-whisper model scales ran; CrisperWhisper/WhisperX remain unavailable locally. This ticket remains in progress for independent natural spoken/number references and caption provenance; no ASR default changed.

## Reconciled remaining work (2026-10-25)

Reassess earlier ASR benchmark conclusions using critical instruction/number recovery and evidence-location accuracy on matched passages. Preserve caption-source differences and model/license eligibility. Ticket 08 default change must await this verdict and final review 28. Research ticket 24 is complete; use its recorded contract. Final synthesis is ticket 28; no model/default or feature integration is authorized by a smoke result.

## Ticket 24 research execution contract (2026-10-25)

**Budget:** One active day.

Freeze short manually referenced instruction passages with names/numbers/commands plus silence/music. Compare eligible captions/faster-whisper/CrisperWhisper at disclosed hardware/scales; measure critical-term errors, omissions/additions and timestamp boundary errors separately. Compare alignment only on evidence-location failures. No universal default from old WER results.

Record raw outputs, exact versions/configuration, failures and a per-job disposition. Report metrics even if they do not favor a candidate; no invented quality threshold. Research register: `docs/agents/research/open-questions.md`.

### Installed speech identity before comparison

The committed worker defaults to model alias `turbo` and imports `crisperwhisper.CrisperWhisperModel`; neither pins a checkpoint nor proves the remote worker version. Capture installed package version, alias resolution, checkpoint revision and applicable weights terms for each eligible configured backend before scoring. Upstream v1 card redirects/supersession must not silently substitute v2; preserve historical benchmark identities. If runtime identity cannot be established, mark that option ineligible/unresolved rather than selecting a default.

## Measured first comparison — 2026-10-25

Report: `docs/architecture/spikes/s4-speech-results.md`. Freeze controlled references/settings at 9a23e51; natural extension at 07d746a before its predictions. Three pinned MIT-declared faster-whisper conversions ran through the repository worker CLI at matched CPU/int8 settings. Ten inputs / 88.678 seconds include authored speech/negative controls, a familiar JFK timing check and four published-transcript LibriSpeech items. No retuning or synthetic reference presented as natural human truth.

Small recovered 7/7 controlled phrases, base/turbo 6/7 (`git add`→`git at`); all four number/negation phrases recovered. Natural prose WER: base6/83, small4/83, turbo3/83. Phrase timing is waveform-envelope location only; early start error up to1.506s, not calibrated natural word boundaries. Actual default-worker retry emitted unsupported text on silence/tones; ticket38 owns reviewed regression work. Three model versions are not three transcription engines. Captions absent for controlled fixtures, CrisperWhisper/WhisperX ineligible locally; no universal winner/default adopted.

Keep in progress: next freeze independently checked real tutorial command/number passages and spoken boundaries, compare eligible available captions, and decide alignment only from an observed evidence-location failure. Known-corpus prose and synthetic phrases do not satisfy that remaining natural tutorial qualification. Model/runtime access limitations may receive explicit unresolved final dispositions, never invented measurements. Raw final evidence: `codex/spike-speech-details`, `b5030a893e465dd2d8aca532aa048b6d109e7e32`. Transcription tests8passed; scoring checks54passed; ten restored media hashes matched.

### Real tutorial extension

Freeze845991e reserved852–868s of the Git tutorial before its speech predictions, using prior visual task referents rather than an auditory transcript. Existing fetch CLI returned captions with lost manual/automatic provenance and overlapping cues. Available captions and all three models each retained2/3 task terms; all rendered git status as get status. No real-tutorial WER or timing gold claimed. Natural numeric settings and independently checked spoken boundaries remain open. Eleven retained inputs now total104.678s; all11 restore hashes passed. No additional parameter tuning or default change.

## Caption provenance and independent-reference preparation — 2026-10-25

New decision record: `docs/architecture/spikes/s4-reference-provenance.md`. Original Git source has no manual caption tracks; explicit automatic en VTT is ASR and all scoped frozen cues match. MIT manual-classified YouTube and official publisher captions have959 equal parsed cue records; CS50 manual/publisher tracks have identical decoded3,694-word sequences despite formatting differences. Neither pair is two independent validations. Institutional MIT human-edit workflow does not certify these historical files or word boundaries. Citation research separately audited9/10 with source-date correction applied.

Prepared three new real tutorial excerpts (MIT status/three times; CS50 mkdir/pset2/self-correction; cp/two arguments),55seconds, fixed audio hashes, publisher-draft cues and an offline listening/export pack. No new predictions, WER or timing-accuracy claims. Three empty-folder restores and embedded-manifest hash checks passed. User clarification: designated empty tracks are music-only; exclude from spoken-reference scoring, keep as non-speech controls distinct from authored silence/tones.

Still requires independent listening: no audio-listening tool is available in this session and no reviewed spoken/timestamp record has been supplied. Next concrete step is the review pack, then lock corrected references before inference. Keep in progress; do not repeat proxy model runs to paper over that missing input. New39 owns provenance preservation after review28. Raw evidence/review pack: `codex/spike-speech-details`, commit `18cae9f23631a136cfe2a54108ae29c238ab6461`; `docs/architecture/spikes/speech-details/reference-review.html`. Original11-input checks and3new restores passed; offline review format/partial/invalid-bound/music classification checks passed. Final staged artifact scope15files/1,513,284logicalGit-blob bytes, complete metadata/content and no findings; excludes earlier commits/history/ignored originals.

## User-authorized audio-model continuation — final bounded disposition

The latest user request explicitly authorizes model-reviewed references distinct from human-verified ones. This supersedes the previous listening-only gate for machine-reference comparisons; it does not certify human accuracy.

`docs/architecture/spikes/s4-model-reviewed-results.md` records the executed SenseVoiceSmall int8 / sherpa-onnx1.13.6 audio-only review. Protocol/eligibility frozen e6a6de9; exact blind machine references frozen a18749f before candidate inference. All references preserve model-reviewed-provisional and human_verified:false; no publisher/candidate-driven spelling cleanup. Same three pinned Whisper candidates ran through worker CLIs on the same55seconds.

All three candidate outputs contain the five declared canonical strings for Git, mkdir, pset2 and the two number phrases. SenseVoice has gi/mkd/pet2 spelling disagreements; cp is an unscored boundary/reference problem. Conditional edits versus180 machine-reference words: base19,small14,turbo19; this is agreement, not actual accuracy. Six numeric-start pairs differ0.16–0.24s; token points are not human word boundaries. Source<=30s guidance and the31s input are explicit; a separate post-hoc20/12s diagnostic did not replace frozen references. The original human pack remains unfilled.

Disposition: bounded comparison complete, retain baseline, no new default/reference authority adopted. Model-assisted audio review is demonstrated; human-verified accuracy, representative numeric parameters, actual task outcomes and eligible CrisperWhisper remain unresolved, with deliberate follow-up40. Review28 consumes these limits;38/39 remain post-review implementation proposals. Final raw evidence: `codex/spike-speech-details`, `17ed579dcb741e00d23f41712ed75e771a7a3b1f`, speech-details README and model-review-comparison.json. Verification:18new independent score checks, model identity/3audio hashes and unchanged a18749f references;54prior score checks,14input restores,3unchanged historical score hashes;8transcription tests; pre-commit and offline dashboard/review-form checks passed. Result staging15files/238,598logicalGit-blob bytes inspected completely without findings, excluding earlier commits, weights/history/ignored originals.

## Resolution (2026-10-26)

Completed bounded speech comparison including blind SenseVoice audio review and frozen provisional references before candidate inference. Model-reviewed is explicitly not human-verified. Canonical code disagreements, conditional transcript agreement, token timing and boundary defects are recorded. Retain baseline; no winner/default/reference authority adopted. Human-verified qualification remains deliberately deferred40; recovery/provenance38/39 and integration review28 consume limits.

### Verification
1. ✓ A durable spike report records options, evidence and limitations — "s4-model-reviewed-results.md records options, frozen55second corpus and explicit machine/human limits; raw17ed579"
2. ✓ Every evaluated option records its fixture, environment and observations — "Per-option versions, settings, outputs, costs and failures in report/raw;8transcription tests,18new score checks,14restores,pre-commit and dashboard checks passed"
3. ✓ The report states an adopt, retain, reject or unresolved verdict — "Report disposition retains baseline, rejects model reference as authority, preserves unresolved human accuracy/Crisper/parameters;follow-up40;no default integration"
