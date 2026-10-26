# Speech details — throwaway ticket 15 experiment

Question: which eligible configuration preserves commands, numbers and evidence location? No production integration.

Freeze 9a23e51: protocol, controlled references, cached model identities. Natural extension frozen in 07d746a before its predictions; settings/candidates unchanged. Natural sources are a known benchmark, not unseen tutorial-domain evaluation. First API pilot outputs are retained separately; scored outputs use the existing worker CLI with a spike-only word-JSON switch. That switch remains on this branch. Serialization and CLI correction did not retune model settings, references or lexical aliases.

## Replay

In this repo's existing environment with faster-whisper 1.2.1 / CTranslate2 4.7.1, extract both ZIPs into `.scratch/speech-details`. Ensure the exact three cached model revisions in `protocol.json` are available. Run:

```powershell
.venv/Scripts/python.exe docs/architecture/spikes/speech-details/run.py base
.venv/Scripts/python.exe docs/architecture/spikes/speech-details/run.py small
.venv/Scripts/python.exe docs/architecture/spikes/speech-details/run.py turbo
.venv/Scripts/python.exe docs/architecture/spikes/speech-details/run.py base --natural
.venv/Scripts/python.exe docs/architecture/spikes/speech-details/run.py small --natural
.venv/Scripts/python.exe docs/architecture/spikes/speech-details/run.py turbo --natural
.venv/Scripts/python.exe docs/architecture/spikes/speech-details/score.py
```

The runner invokes `workers/transcribe_worker.py` for every fixture, with an explicitly pinned local model and config. Per-clip model loads are included in worker wall time and reported separately. Silent/tonal fallback diagnostics in `fallback-negatives.json` use the unmodified default worker route without `--spike-config`; replay using that worker with the same local snapshot and input. The underlying source pipeline uses the same empty-result retry without VAD.

Scores keep synthetic intended-text WER separate from natural published-transcript WER; numeric formatting differences count under strict WER, while declared semantic aliases recognize equivalent numbers/filename spellings. Seven critical targets are complete instruction phrases, not seven independent commands/tasks. Phrase timing uses a waveform amplitude envelope, not human word boundaries. No native tutorial word timing or human correction benefit is qualified.

Natural dataset attribution: LibriSpeech ASR corpus, [OpenSLR 12](https://www.openslr.org/12), CC BY 4.0, via `hf-internal-testing/librispeech_asr_dummy`, cached revision recorded in `references-natural.json`; four consecutive validation items, speaker 1272. Audio/text content is unchanged. Natural JFK test source and pinned revision are in `references.json`; it is a familiar integration test, not independent model validation. `artifact-manifest.json` and restore checks cover retained reference bundles; ignored intermediates have no separate backup claim.

## Real tutorial extension

Freeze `845991e` reserved source 852–868 seconds and three task-backed terms before predictions. References are source-frame/task context and fetched captions, not independent auditory truth. Caption cues overlap clip edges and repeat; no caption WER or timing accuracy is computed. Same models/settings, no tuning. Run each option with `--tutorial`, then score. `tutorial-fixture.zip` retains the exact 16-second input for replay; this final storage decision supersedes the ignored-only retention plan in the frozen tutorial reference metadata. Credit: Traversy Media, Git & GitHub Crash Course For Beginners, https://www.youtube.com/watch?v=SWYqp7iY_Tc, excerpt 852–868 seconds, unchanged audio converted to mono16k for analysis. Source metadata was fetched through `video-buddy --json fetch`; stored caption provenance cannot identify manual versus automatic track. The full source remains ignored, without a separate backup claim.

All three models and available captions recover only two of three scoped task terms; all render the intended Git command as “get status.” That is a downstream exact-command gap, not a scored auditory word error. Small also renders the checkpoint “on tracked”; this is a qualitative observation, not an added post-hoc scoring target. Native word-boundary truth, natural numeric settings and human correction remain open. Run `verify.py` to check all eleven restored inputs and recorded score totals.
