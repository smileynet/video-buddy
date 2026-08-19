# Verbatim/Disfluency-Preserving Transcription in ASR

## Summary

Verbatim transcription—preserving fillers, repetitions, false starts, and paralinguistic sounds—is an active research frontier in ASR as of mid-2026. The core insight from recent work is that large ASR models like Whisper already *encode* disfluency information but treat transcription style as an uncontrolled latent variable, causing up to 60% of reported WER to reflect style mismatch rather than actual recognition errors. CrisperWhisper 2.0 (Nyra Labs, July 2026) leads the field with 87.8 disfluency F1 across ten languages (93.5 for Pro), explicit verbatim/intended mode control, and 29.6ms word-boundary precision—ahead of all closed-source alternatives on the Nyra Verbatim Speech Benchmark.

## Details

### Why Verbatim Matters

- **Clinical assessment**: Disfluency patterns are diagnostic markers for neurological disorders, dementia, aphasia, and stuttering. Standard ASR that strips fillers loses clinically relevant signal.
- **Downstream NLP**: Verbatim transcripts enable disfluency analysis, speaking assessment, error analysis for language learners, and feedback systems.
- **Expressive TTS**: Paralinguistic annotations (laughter, sighs, filled pauses) improve naturalness in speech synthesis pipelines.
- **Accessibility**: People who stutter experience 19.8% WER and 23.8% truncation rates on production ASR—systems that omit disfluencies actively erase their speech patterns.
- **Evaluation integrity**: Without style-aware evaluation, benchmarks conflate content errors with transcription style choices, making it impossible to measure actual recognition quality.

### How Models Handle Disfluencies

**The problem**: Most ASR models are trained on heterogeneously annotated data that mixes verbatim and "intended" (cleaned) transcription styles without any control signal. This creates:
1. **Decoding instability** — beam search yields substantially different transcripts for disfluent speech (15% median character-level divergence in Whisper)
2. **Evaluation confounding** — up to 60% of reported WER on conversational benchmarks (AMI) reflects style mismatch, not recognition failure
3. **Ill-defined timing** — if a model inconsistently transcribes disfluencies, word-level timestamps become conceptually undefined

**Current approaches**:
- **Whisper (base)**: Omits most disfluencies inconsistently; 12% disfluency event F1
- **Post-hoc detection**: Separate filler-word classifiers after ASR (ASR+VAD mismatch, CTC alignment gaps)
- **Fine-tuning on verbatim data**: Works but risks catastrophic forgetting of general capabilities
- **Continual learning**: Emerging approach using LoRA + explicit disfluency tokens to add verbatim capability without forgetting (arXiv 2606.14391)
- **Soft-prompt tuning**: Can elicit disfluencies from pretrained models but lacks stable switching and paired supervision

### CrisperWhisper vs Others

**CrisperWhisper 2.0** (Nyra Labs, July 2026 paper: arXiv 2607.18934):
- Introduces "transcription policy as a latent variable" framework
- Uses discrete **mode tags** (decoder prefix tokens) to explicitly control verbatim vs intended output
- Key finding: training ONLY 27 new token embeddings (mode tags), with all 764M encoder/decoder parameters frozen, raises German disfluency F1 from 10% to 79% — proving the capability is already latent in Whisper
- Full fine-tuning achieves 94% German event F1 with zero German verbatim training data (English-only supervision, cross-lingual transfer)
- **Verbatimize** feature: given audio + clean transcript, inserts only the disfluencies actually present in the audio (rare-word recall jumps from 6.8% to 96.1%)
- Supervised cross-attention for word-level timing: 36ms MAE on read speech, 102ms on disfluent speech (beats forced alignment which degrades to 142-200ms on disfluent input)
- CTranslate2 runtime with speculative decoding and hallucination mitigation

**Benchmark results (Nyra Verbatim Speech Benchmark, 10 languages)**:

| # | System | Disfluency F1 |
|---|--------|---------------|
| 1 | CrisperWhisper 2.0 Pro | 93.5 |
| 2 | CrisperWhisper 2.0 | 87.8 |
| 3 | ElevenLabs Scribe v2 | 79.2 |
| 4 | Microsoft MAI-Transcribe-1.5 | 77.5 |
| 5 | CrisperWhisper 1.0 | 64.8 |
| 6 | Inworld STT | 59.5 |
| 7 | xAI Grok Speech-to-Text | 42.8 |
| 8 | Deepgram Nova-3 | 37.8 |
| 9 | Fish Audio ASR | 35.0 |
| 10 | AssemblyAI Universal-3 Pro | 30.5 |

**Other notable systems**:
- **Reverb** (Rev.ai): Continuous "verbatimicity" parameter, but English-only, no timing support
- **WhisperD** (arXiv 2505.21551): Fine-tuning Whisper specifically for dementia speech and filler word detection
- **Continual Learning approach** (arXiv 2606.14391): Uses CL with explicit disfluency tokens to avoid catastrophic forgetting when adapting to verbatim tasks
- **Dual-reference benchmarking** (arXiv 2606.31112): Proposes evaluating atypical speech against both verbatim and intended references

### Impact on Downstream Tasks

- **Speaking assessment**: Verbatim transcription is essential for automatic assessment of language learners—omitting hesitations loses the signal being measured
- **Clinical NLP**: Disfluency patterns in dementia, aphasia, and stuttering are diagnostic; clean transcripts erase the evidence
- **TTS training**: Spontaneous-style TTS needs disfluency-annotated data; verbatimize can generate this at scale from existing clean corpora
- **Conversational AI**: Understanding when users hesitate, self-correct, or use fillers provides pragmatic signals for dialogue systems
- **Content editing**: Products like Descript use filler detection for automated editing, but this requires detecting them first
- **Evaluation**: Style-aware evaluation (separating content errors from style differences) is necessary for honest ASR benchmarking

## Sources

- [CrisperWhisper 2.0 Paper — "Transcription Policy as a Latent Variable"](https://arxiv.org/abs/2607.18934) — The foundational paper for controllable verbatim ASR (July 2026)
- [CrisperWhisper 2.0 on HuggingFace](https://huggingface.co/nyralabs/CrisperWhisper2.0_turbo) — Model card with benchmarks, install, and API
- [CrisperWhisper PyPI package](https://pypi.org/project/crisperwhisper/0.1.2/) — Production Python package
- [Nyra Labs (nyra-labs.com)](https://nyra-labs.com/) — CrisperWhisper developers
- [CrisperWhisper 1.0 — "Accurate Timestamps on Verbatim Speech Transcriptions"](https://arxiv.org/html/2408.16589v1) — INTERSPEECH 2024 predecessor
- [Acoustically Precise Hesitation Tagging (arXiv 2506.04076)](https://arxiv.org/html/2506.04076v1) — Shows acoustic precision in hesitation tagging is essential for verbatim systems
- [Continual Learning for Disfluency-Aware ASR (arXiv 2606.14391)](https://arxiv.org/html/2606.14391) — CL approach to avoid forgetting when adding verbatim capability
- [Dual-Reference Benchmarking for Atypical ASR (arXiv 2606.31112)](https://arxiv.org/html/2606.31112) — Proposes evaluating against both verbatim and intended references
- [WhisperD: Dementia Speech Recognition and Filler Word Detection (arXiv 2505.21551)](https://arxiv.org/html/2505.21551v1) — Fine-tuning Whisper for clinical filler detection
- [Prompting Whisper for Verbatim Transcription (arXiv 2505.23627)](https://arxiv.org/abs/2505.23627) — Soft-prompt approach for verbatim and miscue detection
- [Nyra Verbatim Speech Benchmark](https://www.nyra-labs.com/research/nyra-verbatim-speech-benchmark) — Multi-language disfluency F1 evaluation framework

## Open Questions

1. **Non-commercial license barrier**: CrisperWhisper 2.0's open weights are under a non-commercial research license. What are the commercial alternatives that approach its verbatim quality? (ElevenLabs Scribe v2 and Microsoft MAI-Transcribe-1.5 score 77-79 F1 but are closed-source APIs.)

2. **Cross-lingual generalization beyond Germanic languages**: CrisperWhisper 2.0 demonstrated English→German zero-shot transfer. How well does the approach work for typologically distant languages (tonal languages, agglutinative languages)?

3. **Integration with video-buddy**: The current pipeline uses standard Whisper which strips disfluencies. Would verbatim mode improve or harm the note-generation workflow? Verbatim might be better for capturing speaker uncertainty and emphasis, but worse for clean note generation. A dual-mode approach (verbatim for analysis, intended for notes) could be ideal.

4. **Latency and resource requirements**: CrisperWhisper 2.0 large is 0.8B params. What's the real-world inference cost compared to standard Whisper? The speculative decoding (1.3-1.4x speedup) helps but it's still a large model.

5. **Verbatimize for corpus construction**: Could verbatimize be used retroactively on video-buddy's existing clean transcripts to recover disfluency information from the original audio? This could enrich existing notes without re-transcribing.

6. **Evaluation standards**: The Nyra Verbatim Speech Benchmark is from the same lab as CrisperWhisper. Are there independent benchmarks for verbatim ASR quality, or is the field waiting for community-driven evaluation?
