# Audio-model review of real tutorial speech

**Ticket 15 · bounded comparison complete · 25 October 2026 · no production change.** A working local audio model reviewed all three frozen clips, and the Whisper candidates were compared after its output was locked. References remain **model-reviewed provisional, not human-verified**. Use the reviewer to expose disagreements; do not adopt its text as command ground truth or change ASR defaults from this result.

## The tool that actually ran

**SenseVoiceSmall int8,2024-07-17, through sherpa-onnx 1.13.6**, on Windows Python 3.13.14 / CPU. A separate `.venvs/audio-review` environment contains sherpa-onnx/core1.13.6, NumPy 2.5.4 and psutil7.2.2. The existing faster-whisper environment and production dependencies were preserved. No hosted API or credential was required; the audio stayed local.

The [versioned waveform example](https://raw.githubusercontent.com/k2-fsa/sherpa-onnx/v1.13.6/python-api-examples/offline-sense-voice-ctc-decode-files.py) and available Windows wheel were verified, then tested here. This is an audio recognizer from a different architecture family, not an instruction-following audio judge. Different model family does not establish independent training data or truth. It emits token time points rather than verified word intervals.

Software is Apache2.0; the checkpoint points to the custom [FunASR model agreement 1.1](https://raw.githubusercontent.com/modelscope/FunASR/main/MODEL_LICENSE), not Apache. The archive's model-name/source notices, terms hash, model/token hashes and versions are retained. This was attributed local reference/learning evaluation; production deployment eligibility remains a separate decision. [Primary-source research](../../agents/research/audio-model-reference-review.md) and its [independent citation audit](../../agents/research/audio-model-reference-review-audit.md) record eligibility and limitations. Version1.13.6 was a pinned candidate, not a latest-release claim.

## Frozen review and comparison

Inputs are the same55 seconds: MIT git status / three times (31s), CS50 mkdir / pset2 / correction (12s), and CS50 copy / two arguments (12s). Their existing hashes and publisher drafts were unchanged.

1. Protocol/eligibility freeze `e6a6de9`: waveform-only review, English flag, CPU with 8 threads, greedy decoding, no inverse text normalization. No publisher text, code-word hints, grammar or candidate transcript reached SenseVoice.
2. Raw-output/reference freeze `a18749f`: exact SenseVoice output retained before new candidate predictions. No spellings were silently repaired using publisher or Whisper text. Every reference carries `reference_type:model_reviewed_provisional` and `human_verified:false`.
3. Candidate comparison: the same pinned base/small/turbo conversions, faster-whisper 1.2.1 / CTranslate2 4.7.1, CPU/int8 and prior frozen settings. Worker CLIs ran three fresh processes per model. Caption origin and shared-publisher lineage stay explicit.

The human listening pack remains unfilled. None of this checks a human attestation or certifies independent acoustic truth. User-designated music-only tracks remain non-speech controls, distinct from prior authored silence/tones.

## What the audio review found

| Check | SenseVoice review | Whisper/caption observation | Disposition |
| --- | --- | --- | --- |
| git status | gi status | All three Whisper outputs and publisher captions contain git status | Reviewer code spelling is uncertain; do not automatically replace canonical commands with reviewer text. |
| mkdir / pset2 | mkd / pet2 | All three Whisper outputs and captions contain mkdir / pset2 | Audio access does not guarantee exact code/filename recovery. |
| three times / two arguments | Both present | Both present in all three candidates and captions | Narrow agreement on counts, not unseen port/version/configuration values or human accuracy. |
| Spoken correction | Review includes typed/an n/but | Small/turbo retain correction markers; base omits them | Source-faithful transcript and polished instructions are different artifacts. Actual word correctness still needs verification. |
| cp expected target | No literal cp in review | No literal cp in candidates or local caption text | Treat as an unscored reference/window problem. The publisher cue beginning at543.65s starts with Copy; the clip begins546s and model outputs start later in that sentence. Do not label absence a recognition error. |

Source/destination wording appears in the reviewed copy excerpt and candidates. It was not an extra post-hoc scored target. No corrected command was executed; no human task-completion or correction-time benefit was measured.

## Conditional transcript agreement — not accuracy

| Candidate | Edits versus180 SenseVoice-reference words | Conditional WER | Conditional CER |
| --- | ---: | ---: | ---: |
| Base | 19 | 10.6% | 5.3% |
| Small | 14 | 7.8% | 3.5% |
| Turbo | 19 | 10.6% | 8.0% |

Lower means closer to the frozen machine transcript, **not necessarily more correct**. This arithmetic penalizes git versus the reviewer's gi, for example. Case/punctuation are normalized; digits/abbreviations are not silently rewritten. These values cannot select an accuracy winner. Raw outputs and code/number diagnostics accompany them.

Caption full-transcript WER was deliberately not computed: each intersecting cue set overhangs the clip boundary, and the publisher/YouTube copies are not independent references. Canonical term presence is recorded separately, without forcing a word-level crop or scoring out-of-window words.

## Timing and duration limits

Only two numeric phrase starts match exactly between SenseVoice's token-derived words and the candidates. Across six pairs, Whisper starts are **0.16–0.24s earlier** than SenseVoice's token points. This is model-to-model timing disagreement, not boundary error. Code-spelling disagreements cannot be aligned by quietly correcting the reference. No verified word ends, human word-boundary accuracy or observed evidence-location failure supports adding forced alignment yet.

The [upstream direct-inference guidance](https://github.com/FunAudioLLM/SenseVoice) recommends inputs of 30 seconds or less. Sherpa accepted the31s clip and returned data through its end; this does not qualify a longer-duration contract. A separately labeled **post-hoc20s/12s overlapping diagnostic** retained similar gi spellings and changed some wording. It did not replace the frozen reference or candidate scores. This strengthens the caution against treating one recognition pass as truth.

## Cost and checks

One cached CPU run per option, not a repeated latency benchmark. SenseVoice downloaded a163,002,883-byte archive in2.70s; ONNX model size239,233,841bytes. Reviewer load0.91s, three inferences0.57s total; peak sampled root RSS423MiB. Download/setup/import/hash costs are separate. The bounded-window diagnostic is separate too.

| Candidate | Inference total | Worker wall total, including3 fresh processes | Model-load subtotal | Peak sampled parent+children RSS |
| --- | ---: | ---: | ---: | ---: |
| Base | 3.40s | 8.39s | 1.03s | 415MiB |
| Small | 7.83s | 12.18s | 2.56s | 666MiB |
| Turbo | 17.43s | 27.17s | 7.84s | 1954MiB |

Reviewer loads once, candidates reload per fixture; do not infer universal cross-engine speedups. RSS sampling is nominal20ms, can miss peaks and double-count shared pages, and is not full intake/GPU memory. No paid API or end-to-end cost comparison was performed.

Verification records tie reviewer model/token hashes to eligibility, confirm original audio hashes and reference freeze, keep all human flags false, and independently recompute18word/character edit totals. Existing input restore checks and worker/source tests remain separately recorded. No reference retuning, prototype promotion or production dependency change.

## Disposition and remaining gaps

**Complete ticket15 as a bounded, qualified comparison: retain baseline; no new default or reference authority adopted.** Model-assisted audio review is now demonstrated and useful for exposing uncertainty, corrections and a bad window assumption. Human-verified command truth, natural numeric parameters, actual word intervals, representative task outcomes and an eligible CrisperWhisper comparison remain unresolved.

Ticket 40 deliberately defers human-verified speech qualification until a proposed default, executable-command or alignment change requires it. Tickets 38/39 own reviewed no-speech recovery and provenance implementation proposals. Review 28 must distinguish publisher captions, raw model transcripts, model-reviewed references and human verification, and exclude claims beyond this evidence. The absence of a human reference is no longer a reason to block a clearly labeled model comparison; it remains a limit on what that comparison can establish.

Raw evidence: [`codex/spike-speech-details`,17ed579](https://github.com/smileynet/video-buddy/tree/17ed579dcb741e00d23f41712ed75e771a7a3b1f/docs/architecture/spikes/speech-details). Final verification and closure are recorded in ticket15. Earlier [speech results](s4-speech-results.md) and [caption-lineage findings](s4-reference-provenance.md) remain historical evidence with their original scopes.

Final checks:18independent edit-distance calculations, reviewer/model identity and3audio hashes passed with references unchanged from a18749f; original54score checks and14input restores still pass. A historical-score replay retained all3prior score hashes. Transcription tests8passed; pre-commit passed. Offline dashboard rows match raw metrics, human/provisional labels and deep links were checked on desktop/mobile, and the human review form remains unfilled. Comparison-result staging covered15files/238,598logicalGit-blob bytes, complete metadata/content and no findings; earlier freezes, model weights, history and ignored originals were outside that inspection. No LFS/history rewrite or production integration occurred.
