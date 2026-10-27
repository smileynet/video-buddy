# Local narration: Qwen3-TTS versus Chatterbox-Turbo

Measured **27 October 2026**, ticket 41. Both models completed the same short English task. **Chatterbox is the next local English trial for warm generation speed; Qwen used less process RAM. Listening quality remains an open decision.** No production default changed.

## What was compared

Two 34-word paragraphs taken verbatim from the narration sample, one shared 8.08-second official demo reference, two seeds and four cases per model. The reference is not the user or video creator. Qwen's cloning interface also receives the demo's published transcript. This is a native-interface comparison, not identical internal conditioning or sampling.

Windows, RTX 5070 with 12 GB VRAM, roughly 6.5 GB initially free, separate Python 3.12 environments. Models ran sequentially; other GPU users remained active. Qwen used its 0.6B Base checkpoint with requested SDPA/bfloat16. Chatterbox-Turbo used its normal generation/watermark path, with an explicit PyTorch override for this GPU. Exact checkpoint revisions, package versions, frozen protocol and all raw cases are retained.

## Results

| Measure | Qwen3-TTS 0.6B Base | Chatterbox-Turbo |
|---|---|---|
| Warm generation, three calls | 19.30–26.37 seconds | 3.17–3.45 seconds |
| Speech duration in those calls | 10.24–12.00 seconds | 12.40–13.16 seconds |
| Real-time factor: wall time / audio duration | 1.79–2.30 | 0.254–0.264 |
| Peak sampled process RAM, entire process | 2.35 GiB | 4.66 GiB |
| Peak Torch-allocated GPU memory in generation | 2.64 GiB | 3.13 GiB |
| Model load / reference preparation | 13.40 / 3.04 seconds | 61.41 / 14.99 seconds |
| First generation | 24.14 seconds | 4.34 seconds |
| ASR disagreement with intended text | 0 edits / 136 word presentations | 1 edit / 136 word presentations |

Lower real-time factor is faster: Chatterbox generated these warm cases faster than playback; Qwen generated them slower than playback. Initialization changes the one-off experience, so keep loading/reference preparation separate from warm generation. The models produce different durations/delivery. Three warm calls are a small observation, not a broad benchmark.

## Quality: listen alongside the machine checks

The dashboard now offers a [personal blind-label listening review](blind-listening-review.md): level-matched A/B takes, reference audio, three ratings and private saved/exported preference. No human preference has been collected by the agent. The implementation plan and model comparison are optional companions to the source-focused lesson.

All eight outputs were finite and unclipped. SenseVoiceSmall int8 / sherpa-onnx 1.13.6 decoded each waveform without the intended text as a prompt. After decoding, normalized transcripts were compared to the intended script. In Chatterbox's first outcome take, the recognizer returned **“attained”** for intended **“retained”**; its other takes matched. Qwen's four takes matched in this check.

That single disagreement could be generation or recognition error. It has not been independently adjudicated. Neither zero edit distance nor an unclipped waveform proves naturalness, pronunciation quality or speaker likeness. No human or instruction-following audio-model preference score was collected. These two ordinary English paragraphs do not stress numbers, code spelling, technical names, other languages or long-form continuity.

**Review the samples:** open “Measured local comparison and listening samples” in [the guide walkthrough](file:///D:/.codex/worktrees/spike-state-comparison/video-buddy/docs/architecture/spikes/review-ux/prototype.html?variant=A&revision=measured-v7). It plays the same outcome paragraph from each model and links all eight samples. Listen for word accuracy, clarity, pacing and reference likeness before selecting the voice. The retained FLAC files reproduce the generated PCM16 audio exactly.

## Setup effort and resource limits

Qwen needed an isolated package install and a Windows-friendly attention choice. Its missing SoX binary warning was nonfatal for this WAV path. Chatterbox needed a separate environment, pinned source packages and an explicit override from upstream Torch/torchaudio 2.6 to 2.11.0+cu128. The actual CUDA runs establish this tested configuration, not general Windows/package compatibility.

UV's reported resolve/prepare/install phase sums were about 70 seconds for Qwen and 303 seconds for Chatterbox. Full checkpoint snapshot downloads took 48.28 and 93.39 seconds, with 2.52 and 4.04 GB payloads. These are cached/file-copy-sensitive observations; Chatterbox's full snapshot includes additional weights not used by this path. Environment creation, diagnostics and authoring are excluded from the phase sums; active operator effort was not timed. An earlier cold import/CUDA probe took several minutes. Do not use these as minimum downloads or novice setup estimates.

Generation timings include each model's normal returned waveform processing, including Chatterbox watermarking, but exclude saving files. Model/reference preparation is reused and recorded separately. Precision and native sampling defaults differ. Device-wide memory peaks include other applications; allocator peaks omit non-Torch memory. Neither establishes minimum VRAM. No CPU, full captioned export, offline/network audit, energy cost or end-to-end privacy qualification.

## Disposition and next action

**Conditional preference:** try Chatterbox first for repeated short English local narration with the model kept loaded, if the samples pass your listening check and the dependency override is acceptable. It has a clear warm-speed advantage in this run, with greater process RAM and longer initialization.

**Retain Qwen:** its measured process RAM was lower and it remains a documented multilingual candidate. Only English was tested. Do not replace a model on the basis of ASR agreement alone.

The guide and dashboard now distinguish measured speed/resources from documentary support and human quality still to review. Ticket 18/21 retain reader/listening performance; ticket 28 remains the integration gate. There is no selected production engine or automatic installation/default change.

## Evidence and verification

[Pinned raw evidence and replay instructions](https://github.com/smileynet/video-buddy/tree/45e5ba848975958bce74c0f13624e1a112d92960/docs/architecture/spikes/local-narration). Inputs and runner were frozen at `e5004d9` before generation. The verifier checked frozen protocol/reference, all eight lossless audio/PCM hashes, case timing/shape, resource summaries and ASR linkage. Browser checks confirmed the same guide content, local listening players, mobile layout, step/note retention and no page errors. Pre-commit passed.

The bounded staged evidence inspection covered 21 files / 2,572,743 logical Git-blob bytes with complete metadata/content and no findings; this excludes the earlier freeze, ignored WAVs/environments/model caches and history. No model weights or source video are committed. Eight compact listening files are retained rather than a growing set of per-run media dumps.

[Runtime eligibility research](../../agents/research/local-tts-runtime-eligibility.md) records the upstream defaults and dependency restrictions; the actual requirements/results are the authority for this run.
