# Word-Level Timestamp Accuracy in Speech Recognition

## Summary

Word-level timestamp accuracy in ASR depends heavily on the alignment approach: traditional GMM-HMM forced alignment (Montreal Forced Aligner) remains the gold standard at tight tolerances (41.6% accuracy at 10ms on TIMIT vs 22.4% for WhisperX), but modern approaches like CrisperWhisper's tokenizer-adjusted DTW and the "Whisper Has an Internal Word Aligner" attention-head filtering method are closing the gap at 20-100ms tolerance without requiring external models. The field is moving toward native timestamp generation (IBM Granite Speech 4.1, NeMo CTC/TDT models) that eliminates the two-pass pipeline entirely, achieving 30-80ms mean absolute error from a single inference pass.

## Detailed Approaches

### 1. Dynamic Time Warping (DTW) on Cross-Attention

**How it works:** Whisper's decoder cross-attention weights implicitly encode a soft alignment between output tokens and input audio frames. DTW finds the optimal monotonic path through this attention matrix to assign timestamps to each token.

**Implementations:**
- **Whisper built-in** (`--word_timestamps`): Uses DTW on cross-attention. Accuracy is loose — often 200ms+ tolerance, with known drift on long-form audio.
- **stable-ts** (jianfch/stable-ts): Modifies Whisper to stabilize cross-attention timestamps. Suppresses gaps, ensures chronological ordering, allows regrouping words into natural segments. Also supports forced alignment with an existing transcript.
- **whisper-timestamped**: Similar approach — DTW on cross-attention with confidence scores per word. Notes that this avoids the "language coverage" problem of wav2vec2 aligners since it uses Whisper's own multilingual representations.
- **CrisperWhisper** (nyra health, Interspeech 2024): Adjusts the tokenizer so DTW on cross-attention scores produces finer boundaries. Custom attention loss during training. Claims 30ms word boundaries. Also fine-tunes for verbatim transcription (fillers, stutters). v2.0 adds 3-5x faster inference.

**Key finding (ASRU 2025):** Yeh et al. ("Whisper Has an Internal Word Aligner") discovered that specific attention heads in Whisper capture accurate word alignments distinctively. Using character-level teacher forcing (not wordpieces) produces finer alignments. Their unsupervised head-filtering approach beats prior work at 20-100ms tolerance — stricter than the usual 200ms benchmark.

**Strengths:** No external model needed; works across all Whisper languages; single model.  
**Weaknesses:** Accuracy degrades with noise; standard DTW is loose (~200ms); requires careful head selection or tokenizer modification to reach <100ms.

### 2. Viterbi HMM (Traditional Forced Alignment)

**How it works:** A GMM-HMM acoustic model computes frame-level phoneme likelihoods, then a Viterbi algorithm finds the most probable state sequence (forced alignment path) given the known transcript. Classic approach from speech research for 30+ years.

**Key implementation:**
- **Montreal Forced Aligner (MFA):** Kaldi-based GMM-HMM system. Gold standard for phonetics research.

**Benchmark results (Rousso et al., Interspeech 2024):**
- TIMIT dataset at 10ms tolerance: MFA achieves **41.6% word-level accuracy** vs WhisperX at **22.4%**
- MFA outperformed both WhisperX and MMS (Massively Multilingual Speech) on TIMIT and Buckeye datasets
- At looser tolerances (50-200ms), the gap narrows but MFA still leads

**Strengths:** Highest precision at tight tolerances (<50ms); well-understood failure modes; decades of tooling.  
**Weaknesses:** Requires pre-trained acoustic model per language; separate from ASR (two-step pipeline); not end-to-end; pronunciation dictionaries needed.

### 3. CTC Forced Alignment (wav2vec2 / NeMo NFA)

**How it works:** A CTC-trained model (wav2vec2, Conformer-CTC, Parakeet) produces per-frame character/phoneme probabilities. Alignment is computed by finding the optimal path through the CTC lattice using dynamic programming (Viterbi on the CTC trellis).

**Implementations:**
- **WhisperX** (Bain et al., Interspeech 2023): Runs Whisper for transcription, then wav2vec2 BASE 960H for phoneme-level forced alignment via DTW over phoneme scores. Achieves **93.2% precision at 200ms collar** on Switchboard (vs Whisper's 85.4%). Up to 70x real-time with faster-whisper.
- **NeMo Forced Aligner (NFA):** NVIDIA's CTC-based aligner using Conformer/Parakeet models. Achieves **30-80ms MAE** (vs ~360ms for cross-attention DTW on the same model). Handles 1+ hour files. Used as teacher model to train Canary for native timestamps.
- **torchaudio forced alignment:** Reference implementation of Viterbi trellis-and-backtrack on wav2vec2 CTC output. PyTorch-native.
- **wav2vec2-rs** (Rust): CTC forced alignment with millisecond precision and confidence scores.

**Strengths:** Good accuracy (30-80ms); works with any CTC model; well-suited to known-transcript alignment.  
**Weaknesses:** Requires separate model (memory/compute); phoneme coverage limited by training language; fails on numbers/symbols/OOV words (WhisperX borrows neighbor timestamps); wav2vec2 less noise-robust than Whisper.

### 4. WhisperX (Full Pipeline)

**Architecture:** VAD (pyannote) → Cut & Merge → Batched Whisper → wav2vec2 forced alignment → optional pyannote diarization.

**Performance:**
- Word segmentation at 200ms collar: 93.2% precision, 65.4% recall (Switchboard); 84.1%/60.3% (AMI meetings)
- Speed: up to 70x real-time (large-v2 + faster-whisper)
- Language: 99 languages for transcription, ~30 for alignment (limited by available wav2vec2 models)

**Known failure modes:**
- Numbers, symbols, currency amounts — aligner has no phonemes, falls back to neighbor timestamps
- wav2vec2 alignment degrades faster than Whisper transcription in noisy conditions
- Pipeline complexity: 3 models, HuggingFace token for pyannote, version conflicts

### 5. stable-ts

**Architecture:** Modifies Whisper's inference to extract and stabilize cross-attention timestamps. Also supports forced alignment with a provided transcript (combining with external alignment models).

**Approach differences from WhisperX:**
- Uses Whisper's own cross-attention (no external alignment model needed)
- Suppresses timestamp gaps, ensures monotonic ordering
- Can force-align to a ground-truth transcript (useful when you have a source-of-truth text)
- Works across all Whisper-supported languages (no wav2vec2 language limitation)
- Lower precision than WhisperX at tight tolerances but much simpler pipeline

**Use case:** When you need word timestamps across many languages without maintaining wav2vec2 alignment models per language, or when you have an existing transcript to align against.

### 6. Native Timestamp Models (Emerging)

**IBM Granite Speech 4.1 2B Plus:**
- Single-pass autoregressive model that emits `<|timestamp|>` tokens alongside transcription
- Claims to beat customized WhisperX on word-level timestamps (IBM benchmark, not independently verified)
- Speaker diarization native (no pyannote needed)
- Limitation: only 5 languages (EN, FR, DE, ES, PT)
- Base model: 5.33% WER on HF Open ASR Leaderboard (#1 as of May 2026)

**NeMo CTC/TDT models (Parakeet-TDT v3):**
- Token-and-Duration Transducer emits timestamps natively for every token
- No forced alignment needed — just `timestamps=True` in transcribe()
- ~80x real-time
- CTC forced alignment (NFA) available as teacher for training other models

**Gradient-Based Alignment (arXiv 2607.06831):**
- Works with ANY ASR model (CTC, transducer, AED, speech LLMs)
- Uses gradient of the loss w.r.t. input to find token boundaries
- Newest approach (July 2026) — no published benchmarks against established methods yet

## Accuracy Comparison Table

| Method | Tolerance | Metric | Dataset | Score |
|--------|-----------|--------|---------|-------|
| MFA (GMM-HMM) | 10ms | Word accuracy | TIMIT | 41.6% |
| WhisperX (wav2vec2) | 10ms | Word accuracy | TIMIT | 22.4% |
| WhisperX | 200ms collar | Precision | Switchboard | 93.2% |
| Whisper native | 200ms collar | Precision | Switchboard | 85.4% |
| WhisperX | 200ms collar | Precision | AMI meetings | 84.1% |
| NeMo NFA (CTC) | — | MAE | General | 30-80ms |
| Cross-attention DTW | — | MAE | General | ~360ms |
| CrisperWhisper | — | Word boundary | General | ~30ms (claimed) |
| Internal Aligner (Yeh 2025) | 20-100ms | — | — | Beats prior work |
| NeMo Canary (trained w/ NFA teacher) | — | Precision/Recall | 4 languages | 80-90% |

## Sources

1. Rousso et al. "Tradition or Innovation: A Comparison of Modern ASR Methods for Forced Alignment." Interspeech 2024. https://arxiv.org/abs/2406.19363
2. Bain et al. "WhisperX: Time-Accurate Speech Transcription of Long-Form Audio." Interspeech 2023. https://arxiv.org/abs/2303.00747
3. Yeh et al. "Whisper Has an Internal Word Aligner." ASRU 2025. https://arxiv.org/abs/2509.09987
4. Zusag et al. "CrisperWhisper: Accurate Timestamps on Verbatim Speech Transcriptions." Interspeech 2024. https://arxiv.org/abs/2408.16589
5. stable-ts GitHub repository. https://github.com/jianfch/stable-ts
6. WhisperX GitHub repository. https://github.com/m-bain/whisperX
7. NeMo Forced Aligner documentation. https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/tools/nemo_forced_aligner.html
8. IBM Granite Speech 4.1 vs WhisperX comparison (MindStudio, May 2026). https://www.mindstudio.ai/blog/granite-speech-4-1-vs-whisper-x-word-timestamps
9. Forasoft "WhisperX Deep-Dive" (May 2026). https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/whisperx-diarization-word-level-timestamps
10. "Gradient-Based Speech-to-Text Alignment for Any ASR Model." July 2026. https://arxiv.org/html/2607.06831v1
11. "Word Level Timestamp Generation for ASR and Translation" (NeMo Canary). https://arxiv.org/html/2505.15646v1
12. CrisperWhisper on HuggingFace (nyralabs). https://huggingface.co/nyralabs/CrisperWhisper
13. NeMo Parakeet-TDT v3 gist (native timestamps). https://gist.github.com/lokafinnsw/95727707f542a64efc18040aefe47751

## Open Questions

1. **video-buddy relevance:** Given video-buddy uses Whisper + WhisperX-style alignment, would switching to CrisperWhisper's tokenizer adjustment or the "Internal Word Aligner" attention-head filtering give better timestamps without adding pipeline complexity?
2. **Tolerance requirement:** What tolerance does video-buddy actually need? For subtitle/karaoke sync, <100ms matters. For "jump to this part of the video" search, 200-500ms is fine.
3. **NeMo CTC vs WhisperX:** NFA achieves 30-80ms MAE vs WhisperX's ~200ms collar baseline. Would integrating NFA as the alignment step (replacing wav2vec2) improve results for video-buddy?
4. **Granite Speech viability:** Single-pass native timestamps eliminate pipeline complexity entirely, but only 5 languages. If video-buddy is English-only or near-only, is this worth evaluating?
5. **stable-ts for transcript alignment:** video-buddy already has transcripts from Whisper — could stable-ts's force-align-to-transcript mode produce better word timestamps than WhisperX's phoneme alignment for the specific case where the transcript is already known?
6. **Benchmark gap:** Most papers evaluate on clean speech (TIMIT, LibriSpeech, Switchboard). YouTube audio is far noisier — are any benchmarks representative of real YouTube content quality?
7. **CrisperWhisper 2.0 maturity:** v2.0 claims 3-5x faster inference + better accuracy. Is it stable enough for production pipelines? Last checked: pip-installable as `crisperwhisper` package.
