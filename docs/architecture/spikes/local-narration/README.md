# Local narration spike — ticket 41

Measured 27 October 2026. Freeze: `e5004d9`. No app integration.

Both candidates generated the same two 34-word English paragraphs from the sample guide, with two seeds and four cases each. They use the same 8.08 s official Qwen demo reference, standardized to mono 24 kHz PCM16. Qwen additionally uses that demo's published reference transcript, as its full cloning interface expects. The reference is neither the user's voice nor the video creator's voice.

| Observation | Qwen3-TTS 0.6B Base | Chatterbox-Turbo |
|---|---|---|
| Warm generation wall time (3 calls) |19.30–26.37s |3.17–3.45s |
| Output duration for those calls |10.24–12.00s |12.40–13.16s |
| Warm real-time factor (wall/audio; lower faster) |1.79–2.30 |0.254–0.264 |
| Sampled process peak RAM, entire process |2.35GiB |4.66GiB |
| Peak allocated CUDA memory, generation |2.64GiB |3.13GiB |
| Model-load phase |13.40s |61.41s |
| Reference conditioning |3.04s |14.99s |
| Waveform-only ASR disagreement with intended words |0 edits / 136 word presentations |1 edit / 136 word presentations |

All eight outputs are finite and unclipped at the model-output check. SenseVoiceSmall int8 / sherpa1.13.6 transcribed audio without the intended script as a prompt. Chatterbox's first outcome take yielded “attained” where the script says “retained”; other cases matched after normalization. This is ASR agreement, not independently adjudicated transcription or a naturalness/speaker-similarity score. Listen to retained samples; no human preference, fidelity or quality winner was established.

## Setup and scope

Windows, RTX 5070 / 12 GB, initially about 6.5 GB free; other GPU users remained active. Separate Python 3.12.10 environments, torch/torchaudio 2.11.0+cu128. Qwen PyPI 0.1.1, Transformers 4.57.3, requested SDPA/bfloat16 without FlashAttention. Chatterbox source commit 5de7a54aa4e5e2baadb0182dde554908b48b85c2, Transformers 5.2.0, official float32 path/default generation and watermark retained; Perth pinned ff1c8ac55a976971245cdd53c18d6131ca00d993. Chatterbox's upstream torch/torchaudio 2.6 pin was explicitly overridden for Blackwell. Actual requirements and model revisions are retained. No defaults were tuned against output quality.

Qwen installation used two package commands. Chatterbox used two commands plus explicit Torch/source overrides. UV reported package resolve/prepare/install phase totals of about 70 s and 303 s respectively; these are console phase sums, excluding environment creation, diagnostics and authoring. Active operator effort was not timed. Full snapshot downloads took 48.28 s / 93.39 s, payload 2.52 GB / 4.04 GB; these include repository files not all used by inference, including Chatterbox's additional s3gen weights. Warm caches, HTTP/cache state and Windows file-copy/scanning affect these observations. They are not minimum download or novice setup estimates.

A cold CUDA/import probe took several minutes before the frozen model run; the measured process imports/CUDA initialization were 8.89 s / 15.69 s. Model load and first conditioning may include filesystem/JIT effects. Model order was Qwen then Chatterbox, not counterbalanced. First generation was 24.14 s / 4.34 s. Four calls are one small run, not four independent datasets. Qwen's absent SoX executable warning was nonfatal for this local-WAV path; no binary or source workaround was needed. A preparation helper syntax error was fixed before freezing inputs, not a candidate-model failure.

Generation timing includes the returned waveform path, including Chatterbox's watermark; saving files is excluded. Conditioning is reused. Different native interfaces, precision, sampling defaults and output durations remain explicit. Sampled device totals 9344 MiB / 8953 MiB include other processes and cannot rank candidate VRAM. CUDA allocator peaks omit non-Torch memory and do not establish minimum hardware. The two plain-English paragraphs do not stress numbers, code spelling or technical names. The reference is supplied by Qwen; further permitted references are needed for broad voice-quality claims. No CPU, multilingual, long-script, full joining/caption export or end-to-end privacy qualification. Hub offline flags and local references were used; network behavior was not independently audited.

## Disposition

Prefer Chatterbox as the **next English local trial with the model kept loaded**, conditional on listening acceptance and willingness to maintain the tested Windows dependency override. It has a clear warm-generation speed advantage here, with greater measured process RAM and longer initialization. Retain Qwen as a lower-memory observed option and a documented multilingual candidate; only English was measured. No overall quality winner or production default. Keep both listening packs, carry human quality acceptance to the guide review, and retain final integration in ticket 28.

## Replay and retained evidence

Use an isolated environment; do not install these mutually incompatible Transformers versions into the app. Requirements record actual packages rather than promise a portable lock. Obtain the exact checkpoint revisions from protocol.json using Hugging Face, load their local snapshot directories and pass paths to run_model.py:

```text
<model-python> run_model.py --model qwen --snapshot <pinned-qwen-directory> --protocol protocol.json --out <new-output-directory>
<model-python> run_model.py --model chatterbox --snapshot <pinned-turbo-directory> --protocol protocol.json --out <new-output-directory>
<sherpa-python> check_text.py --audio <output-directory> --model <SenseVoice-model-directory> --protocol protocol.json --out <new-text-check.json>
```

Load one candidate at a time. Replay the eight lossless FLACs directly for listening, or decode them to PCM16 WAV for the checker. artifact-manifest.json stores per-file and decoded-PCM hashes; the verifier checks exact decoded audio against the retained raw hash receipts. Text protocol comparison uses parsed JSON, avoiding checkout line-ending differences. The reference and runner match the frozen Git inputs. verify.py checks the measurements/retention without rerunning generation.

Retain this compact protocol, requirements, measurements, verifier, reference and eight listening FLACs in the spike branch. Raw WAVs, setup environments, model snapshots and original float reference stay in ignored/cache locations; their storage is outside the retained Git evidence. No weights/source video/full environment are committed, no LFS/history rewriting or cloud-storage claim. Model acquisition and fresh generation require downloads/hardware and need not be byte-deterministic.
