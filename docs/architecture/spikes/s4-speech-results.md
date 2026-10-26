# Speech details comparison — ticket 15

**Latest follow-up:** [audio-model review and bounded ticket15 disposition](s4-model-reviewed-results.md). User-authorized machine references were frozen before new Whisper comparisons; model-reviewed remains distinct from human-verified. Earlier [caption provenance](s4-reference-provenance.md) retains its historical scope.

**Measured first round; ticket 15 remains in progress. No default or production change.** Small retained all seven controlled instruction phrases; base and turbo each changed `git add` to `git at`. All three preserved the four controlled number/negation phrases. Natural read-speech errors favored turbo on four known-corpus passages, but that did not predict command reliability. A real tutorial/caption probe recovered only two of three task-backed terms for every option; independent auditory word/number references and timing remain unqualified.

## Eligibility and identity — checked 25 October 2026

All three pinned conversion model cards declare MIT and identify their upstream OpenAI model; installed faster-whisper 1.2.1 and CTranslate2 4.7.1 report MIT. These configurations were eligible for this local probe. This is not a blanket license review of every deployment dependency or a universal provider endorsement.

| Actual pinned conversion | Revision | Probe |
| --- | --- | --- |
| [Systran base](https://huggingface.co/Systran/faster-whisper-base/blob/ebe41f70d5b6dfa9166e2c581c45c9c0cfc57b66/README.md) | `ebe41f70d5b6dfa9166e2c581c45c9c0cfc57b66` | Ran |
| [Systran small](https://huggingface.co/Systran/faster-whisper-small/blob/536b0662742c02347bc0e980a01041f333bce120/README.md) | `536b0662742c02347bc0e980a01041f333bce120` | Ran |
| [Turbo conversion](https://huggingface.co/dropbox-dash/faster-whisper-large-v3-turbo/blob/0a363e9161cbc7ed1431c9597a8ceaf0c4f78fcf/README.md) | `0a363e9161cbc7ed1431c9597a8ceaf0c4f78fcf` | Ran using cached mobiuslabsgmbh namespace; card redirects to Dropbox |

Aliases were inspected but not used to load models. Raw outputs record hashes of actual model files and pinned model-card hashes. All candidates use CPU/int8, 8 threads, beam 5, English, temperature 0, word timestamps, VAD and the same remaining settings. Windows 11, 20 logical CPUs; no GPU inference claim. CTranslate2 saw one CUDA device, but that is not GPU execution evidence. Only local backend is configured. CrisperWhisper, WhisperX and Torch are absent here; no verified remote CrisperWhisper identity. Historical `turbo`/package-name claims do not establish an eligible current CrisperWhisper comparison. No similarly named package was substituted. See [faster-whisper's word timestamp contract](https://github.com/SYSTRAN/faster-whisper#word-level-timestamps) and [upstream terms](https://github.com/openai/whisper/blob/main/LICENSE).

## Frozen references and scope

The deciding question is whether speech preserves the instructions and source moments needed to build and check a result. Eleven distinct inputs total 104.678 seconds; configurations and replay runs are not independent tasks.

- Controlled freeze `9a23e51`, before predictions: one David development phrase, two Zira validation sequences (seven essential instruction phrases / 43 reference words), eight seconds digital silence, eight seconds authored tones, and pinned JFK audio/upstream timing check. Command phrases include add/status and a spelled filename; numbers include port 8080, timeout 30, Python 3.12 and “do not ... zero.”
- Controlled references are **authored intended TTS text**, not independently listened natural speech. Phrase spans use a declared waveform amplitude threshold; they are not phonetic word-boundary ground truth. Voices/clarity are deliberately limited. Tones are a deterministic negative control, not representative music.
- Natural extension freeze `07d746a`, before its predictions but after controlled results: first four consecutive LibriSpeech validation rows, speaker 1272, 33.055 seconds / 83 reference words, [published paired transcripts via HF](https://huggingface.co/datasets/hf-internal-testing/librispeech_asr_dummy). Same checkpoints/settings, no tuning. [LibriSpeech/OpenSLR 12](https://www.openslr.org/12) is CC BY 4.0. Cached dataset revision and item hashes are retained. These are known benchmark prose, not independent tutorial-domain validation; no session re-listening or word-boundary reference.
- JFK is a familiar upstream integration test, not a fresh accuracy corpus. Its [pinned upstream test](https://github.com/openai/whisper/blob/main/tests/test_transcribe.py) requires the word “Americans” to span 1.8 seconds. No full-transcript WER is reported for it.

Raw references, settings, frozen inputs, uncertainty and reproduction live on the spike branch. No source/model output was promoted into ground truth. Synthetic exact WAVs and natural clips, including the sixteen-second tutorial excerpt, are preserved in compact ZIP bundles; all eleven restored into empty temporary folders with matching hashes. Synthesis can vary between Windows installations, so exact replay uses the bundles.

## Critical commands and numbers

| CPU/int8 checkpoint | Command phrases | Number/negation phrases | Overall | Consequential failure |
| --- | ---: | ---: | ---: | --- |
| Base | 2/3 | 4/4 | 6/7 | `git add` → `git at` |
| Small | 3/3 | 4/4 | 7/7 | None observed in these controlled phrases |
| Turbo | 2/3 | 4/4 | 6/7 | `git add` → `git at` |

The score uses complete lexical phrase matches and aliases declared before predictions. It accepts specified spoken-number/numeral and filename representations; it is not proof of exact executable shell syntax or a valid target environment. No extracted command was executed. A fluent transcript or bigger model did not eliminate the command error.

Strict controlled WER is base 15/43 (34.9%), small 13/43 (30.2%), turbo 14/43 (32.6%). CER is 31.4%, 27.8%, 29.0%. Much of this is expected spoken-number/spelled-letter versus numeral/filename formatting, not lost instruction meaning. WER lowercases and removes punctuation but does not expand digits or abbreviations. Keep semantic instruction recovery separate; do not rank defaults from these WER values.

## Natural read-speech sanity check

| Checkpoint | Word errors / 83 | Sub / del / ins | WER | CER |
| --- | ---: | --- | ---: | ---: |
| Base | 6 | 5 / 0 / 1 | 7.2% | 4.8% |
| Small | 4 | 4 / 0 / 0 | 4.8% | 4.2% |
| Turbo | 3 | 3 / 0 / 0 | 3.6% | 3.2% |

This is one speaker and four known-corpus items, not an engine benchmark or tutorial-command winner. Proper-name/abbreviation representation affects scores. Natural and synthetic results are not pooled. No user correction time, successful build or usability benefit was observed.

## Real tutorial and available captions

Third-phase freeze `845991e`, before this clip's predictions: [Traversy Git tutorial](https://www.youtube.com/watch?v=SWYqp7iY_Tc), 852–868 seconds, sixteen seconds mono16k audio. Existing CLI fetch succeeded and returned 1,392 caption cues overall; only overlapping local cues are retained. The schema loses manual/automatic track identity, so eligibility/provenance remains incomplete. Cue overlap/repetition and edge-crossing context are explicit; captions are not WER or timing truth.

Three task terms were grounded in earlier full-context terminal inspection and frozen before speech predictions: cached option, index.html, git status. They are intended downstream source-task referents, **not independently heard transcript labels**. Same checkpoint/settings, no tuning after this result.

| Option | Source-task terms | Missing / altered term |
| --- | ---: | --- |
| Available captions | 2/3 | git status → get status |
| Base | 2/3 | git status → get status |
| Small | 2/3 | git status → get status |
| Turbo | 2/3 | git status → get status |

All preserve cached and index.html, but no option yields the exact Git command spelling. Small also renders the result “on tracked” instead of the visual checkpoint's untracked state; that is an unscored qualitative observation, not a new post-hoc target. Command/source and result verification need visual/context checks. No corrected transcript is silently counted as a raw prediction. No real-tutorial WER, spoken-number score or word-boundary accuracy is asserted from this task-term probe.

## Timing and evidence location

| Checkpoint | Recovered controlled phrases timed | Mean absolute envelope boundary error | Maximum | JFK 1.8-second check |
| --- | ---: | ---: | ---: | --- |
| Base | 6/7 | .243 s | .555 s | Pass |
| Small | 7/7 | .473 s | 1.506 s | Pass |
| Turbo | 6/7 | .302 s | .647 s | Pass |

Errors compare the union of matched word timestamps with the independently computed amplitude envelope; missing phrases are excluded from timing, not assigned zero error. Small's first word for one phrase starts about 1.5 seconds early, although the phrase ending remains close. This is useful evidence-location slack, not a calibrated phonetic timing estimate. A coarse link may still locate the instruction; no observed human evidence-lookup failure establishes a need for forced alignment. Native tutorial word accuracy and WhisperX benefit remain unresolved; alignment was not installed merely to produce another comparison.

## No-speech failure hidden by VAD-only scoring

The word-timestamp probe returned no text on both negatives for every model. The existing worker CLI retries without VAD when the first pass is empty, matching the source pipeline's fallback. This default route also differs from the explicit word probe in language/word-timestamp/default execution settings; it is a workflow check, not a matched VAD-only causal ablation. That default path produced:

| Checkpoint | Digital silence, 8 s | Authored tones, 8 s |
| --- | --- | --- |
| Base | “You”, reported 0–2 s | Empty |
| Small | Empty | Empty |
| Turbo | “You”, reported 0–2 s | “Thank you.”, reported 0–29.98 s |

These are unsupported additions; turbo's tonal caption even extends beyond the input duration. Six bounded negative runs do not estimate a general hallucination rate, and small's empty results do not prove immunity. **Ticket 38 owns a reviewed regression fix after review 28.** Do not equate an empty VAD-gated test with the production retry policy or present such text as source-demonstrated instructions.

## Cost and verification

Each fixture uses the existing worker CLI in a fresh process with a fresh model load; the spike-only word-JSON switch stays on the experiment branch. This is intentionally not warm batch throughput. Identity/hash scans and prior setup are excluded from the worker times below.

| Checkpoint | Controlled/JFK/negative worker wall, 55.623 s audio | Natural worker wall, 33.055 s audio | Combined inference only | Maximum sampled RSS across rounds |
| --- | ---: | ---: | ---: | ---: |
| Base | 7.33 s | 5.35 s | 4.22 s | 398 MiB |
| Small | 13.52 s | 10.71 s | 10.34 s | 720 MiB |
| Turbo | 33.51 s | 27.40 s | 30.16 s | 1960 MiB |

The cost table covers the original ten inputs; the real tutorial adds worker wall 1.57 / 2.84 / 7.55 seconds for base / small / turbo (inference .65 / 1.43 / 4.23 seconds), with no higher observed RSS than the earlier rounds. Model loads alone across the original ten invocations total 2.84 / 8.15 / 24.66 seconds. Single cached runs, not stable performance estimates; setup/download and model identity hashing are separate. Controlled preparation took 4.31 s. Natural fixture download/setup time was not separately measured; cached checkpoint download costs belong to earlier setup and are not zero-cost claims. RSS samples parent plus children every nominal 20 ms, excludes earlier imports/hash scans, may double-count shared pages and miss short peaks. No GPU memory, end-to-end intake or production batch-cost claim. Additional default-fallback run times remain separately in raw evidence.

The initial API output serialization failed, then a CLI harness was used so scored mechanics go through the repository worker. Pilot outputs and failure notes remain separate; no settings/reference/alias retuning. Fifty-four independent scalar edit-distance checks agreed with recorded WER/CER totals; original controlled protocol/references remained unchanged. Eleven input restore hashes passed. Relevant transcription tests: 8 passed. Pre-commit passed. No dependency lock or production code changed.

## Disposition and remaining work

**Retain the existing default pending review; no new winner adopted.** Small is a useful challenger on these controlled phrases; turbo improved this tiny prose WER while repeating the command error. Base remains cheaper in this CPU experiment, but speed does not make an altered command safe. Preserve raw speech, source links and uncertainty, and require visual/source confirmation for executable commands and important numbers.

Ticket 15 stays in progress because the natural tutorial portion is not qualified: freeze independently checked real spoken command/number references and word boundaries, establish caption track provenance and compare against that independent reference, and record whether an actual evidence-location failure warrants alignment. Caption provenance must be explicit; duplicated old caption windows cannot be accuracy truth. CrisperWhisper requires verified installed distribution, checkpoint and configured runtime or an explicit unresolved final disposition. The present controlled / known-corpus results cannot silently close these gaps. Ticket 08 default changes remain gated; review 28 consumes this report and ticket 38's observed failure.

Raw evidence: [`codex/spike-speech-details`, b5030a8](https://github.com/smileynet/video-buddy/tree/b5030a893e465dd2d8aca532aa048b6d109e7e32/docs/architecture/spikes/speech-details); `docs/architecture/spikes/speech-details/README.md` contains replay commands, retained inputs, versions and storage limits. Research claims above use dated primary model cards/runtime metadata; no comprehensive market-coverage claim.

Final staged-artifact inspection covered 11 final candidates / 471,772 logical Git-blob bytes, complete metadata/content coverage and no findings. This bounded check excluded earlier frozen commits and ignored media; it is not a repository/history or billing audit. Reference bundles have separate eleven-input restore checks. No LFS or history rewrite was introduced.
