# Speech details comparison — ticket 15

**In progress: local eligibility preflight only. No quality comparison or default decision yet.** The user job is to recover instructions, numbers and their source moments so someone can build and verify a result. Speech accuracy alone is not task completion.

## Observed local prerequisites — 25 October 2026

Read-only probes in the existing isolated worktree `D:/.codex/worktrees/spike-state-comparison/video-buddy`, using its existing environment without lock/dependency changes:

| Check | Observed result | Meaning |
| --- | --- | --- |
| Installed packages | faster-whisper 1.2.1; CTranslate2 4.7.1; yt-dlp 2026.10.21 | Candidate runtime exists; not proof of successful inference. |
| CUDA enumeration | CTranslate2 reports one CUDA device | Model loading and GPU inference remain untested; no Torch installed here. |
| Configured backends, CLI `--json backends list` | Only local; available | No configured remote CrisperWhisper backend available in this workspace. No remote identity or availability inferred from historical machine names. |
| Optional engines | whisperx, crisperwhisper and torch absent | These options have no local inference result. Do not substitute another distribution/checkpoint under the historical name. |
| Cached base | Systran/faster-whisper-base, revision `ebe41f70d5b6dfa9166e2c581c45c9c0cfc57b66` | Cached candidate, 147,882,941 bytes reported by HF cache. |
| Cached small | Systran/faster-whisper-small, revision `536b0662742c02347bc0e980a01041f333bce120` | Cached candidate, 486,212,372 bytes. |
| Cached turbo | mobiuslabsgmbh/faster-whisper-large-v3-turbo, revision `0a363e9161cbc7ed1431c9597a8ceaf0c4f78fcf` | Cached candidate, 1,621,665,983 bytes. Conversion/model terms still need verification before eligibility. |

The production `transcribe_audio` calls `model.transcribe(..., vad_filter=True)` and retries without VAD when empty; it does not request word timestamps in that path. A word-timestamp spike must record that explicit setting rather than claim it is current behavior. The CLI probe runs on the experimental worktree with the previously documented startup helper; it does not close clean-checkout issue 22.

An initial package probe tried to import absent Torch and failed; CTranslate2 enumeration was then checked directly. An attempted worker file location was incorrect; resolve from the actual repository file list before examining remote alias behavior. Neither failure is an inference result.

## Next bounded execution

One active day overall; setup/download time separate. Before predictions, freeze a small matched set of public tutorial passages covering commands/names, numeric settings, silence and music, plus source-faithful manually checked reference text and instruction/evidence-location targets. Record hashes, exact source times, caption provenance, reference uncertainty and development/validation roles. Media acquisition/transcription use existing CLI mechanics; spike-only scoring/settings stay isolated.

Verify cached model code/weight terms and actual runtime identity first. Compare available captions with one eligible faster-whisper baseline using explicit word timestamps. Use the same audio and disclose compute/model mismatch if another eligible engine becomes available. CrisperWhisper remains unresolved until an installed distribution, checkpoint revision, terms and configured runtime are verified. Do not install an arbitrary similarly named package to manufacture coverage.

Score critical terms/numbers, omissions/additions, WER/CER and boundary error separately. Record transfer/preprocessing/inference elapsed time and memory with boundaries; no absent stage is zero cost. Evaluate WhisperX alignment only if a measured timing error prevents locating the required evidence. Keep unmatched or unavailable options explicit; no universal model ranking or usability claim.

## Current disposition

Continue preparation. No frozen reference set or scored predictions yet; no engine/default change. Ticket 08 and architecture review 28 must await the bounded findings and limitations.
