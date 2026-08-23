# Whisper Model Variant Intents & JTBD

Research date: 2026-08-23

---

## 1. Whisper Large-v3

**Parameters:** 1.55B | **VRAM:** ~10 GB | **Speed:** 1x baseline (A100)

### Design Intent
The flagship Whisper model. Trained on 680,000 hours of multilingual web audio with a 128-channel mel-spectrogram (up from 80 in v2). 32 decoder layers. Intended as the highest-accuracy general-purpose ASR system covering 99+ languages with zero-shot capability.

### JTBD: When to pick this model
- Maximum accuracy required on multilingual or noisy audio
- Non-English or code-switching transcription
- Medical, legal, or technical dictation with domain vocabulary
- Reference/baseline when benchmarking other models
- Situations where latency is acceptable (batch/offline processing)

### Known Strengths
- **Multilingual leader:** 99+ languages with automatic language ID
- **Robustness:** Handles diverse acoustic environments, accents, background noise, technical language
- **Zero-shot generalization:** No fine-tuning needed for most languages
- **Automatic punctuation/capitalization** across supported languages
- **Phrase-level timestamps** built-in

### Known Weaknesses
- **Hallucinations:** Whisper v3 hallucinates 4x more often than v2 on real-world data (Deepgram study). Generates fabricated text during silence or near-silence.
- **Speed:** Slowest of all variants (~1x real-time on M1, much faster on A100 but still baseline)
- **Resource hungry:** ~10 GB VRAM, thermal issues on laptops during sustained use
- **Timestamp precision:** Word-level timestamps via DTW are approximate; ~50ms+ boundary errors typical
- **Long-tail languages:** Performance varies significantly by language based on training data distribution

### Published Benchmarks
- 7.4% average WER on mixed benchmarks (Northflank, 2026)
- ~2.7% WER on clean English audio (reported in various sources)
- 7.88% WER on mixed real-world recordings
- Open ASR Leaderboard: near-identical to Turbo on English

---

## 2. Whisper Large-v3-Turbo

**Parameters:** 809M | **VRAM:** ~6 GB | **Speed:** ~8x large (A100), ~5x large (Apple Silicon)

### Design Intent
A speed-optimized derivative of large-v3. Decoder reduced from 32 layers to 4, dropping parameters from 1.55B to 809M. Fine-tuned for 2 additional epochs on transcription data only. Applies the same distillation principles as Distil-Whisper but from OpenAI directly, and retains multilingual capability.

### JTBD: When to pick this model
- Best general-purpose default for most users in 2026
- Multilingual transcription where speed matters more than the last 1% accuracy
- Interactive/near-real-time applications
- Hardware-constrained environments (8GB unified memory Macs)
- When you need 99+ language support but can't afford large-v3's latency

### Known Strengths
- **Speed:** 5-8x faster than large-v3 with minimal accuracy loss
- **Memory efficient:** ~6 GB VRAM (fits comfortably in 8 GB unified memory)
- **Multilingual:** Same 99+ language coverage as large-v3
- **Accuracy:** Within 1-2% WER of large-v3 on English, comparable to large-v2
- **216x real-time factor** on Groq infrastructure
- **~1% lower WER than Distil-Whisper** (per Groq)

### Known Weaknesses
- **No translation:** Translation data excluded from fine-tuning; translation performance degraded
- **Some language degradation:** Shows larger WER increase on Thai, Cantonese vs large-v3
- **Performs closer to large-v2 than large-v3** on some metrics
- **Still hallucinates** (inherits the v3 hallucination tendency, though mitigated by fewer decoder layers)
- **Timestamp accuracy** no better than large-v3

### Published Benchmarks
- 7.75% average WER on mixed benchmarks (Northflank)
- 7.83% English WER on Open ASR Leaderboard (WhisperNotes)
- 216x RTF on Groq
- ~5x faster than large-v3 on Apple Silicon (WhisperNotes)
- Near-identical accuracy to large-v3 on FLEURS (cleaner recordings)

---

## 3. Distil-Whisper (distil-large-v3)

**Parameters:** 756M | **VRAM:** ~5 GB | **Speed:** 6.3x large-v3

### Design Intent
Community-built (Hugging Face) knowledge-distilled variant. Copies the entire encoder from large-v3 (frozen), uses only 2 decoder layers initialized from first and last layers of Whisper. Trained on 22k hours of pseudo-labeled English data spanning 10 domains with 18k+ speakers. Designed as a drop-in replacement for Whisper on English speech recognition AND as a speculative decoding assistant to large-v3.

### JTBD: When to pick this model
- English-only transcription where speed is critical
- Speculative decoding paired with large-v3 (2x speedup, mathematically identical outputs)
- Production English ASR on modest hardware
- When you need lower hallucination rates than large-v3
- Resource-constrained English-only deployments

### Known Strengths
- **Speed:** 6.3x faster than large-v3
- **Accuracy:** Within 1% WER of large-v3 on out-of-distribution English audio
- **Better on long-form:** Slightly outperforms large-v3 on long-form chunked audio with fewer repeated phrases
- **Less hallucination:** 1.3x fewer repeated 5-gram duplicates, 2.1% lower insertion error rate
- **Speculative decoding:** 2x speedup with guaranteed identical outputs when paired with large-v3
- **MIT licensed**

### Known Weaknesses
- **English only** — no multilingual support
- **No translation** capability
- Slightly worse on short-form than large-v3 (9.7% vs 8.4% short-form WER)
- Timestamp quality inherited from base Whisper (not improved)

### Published Benchmarks (from Hugging Face README)

| Model | Params | Rel. Latency | Short-Form WER | Long-Form WER |
|-------|--------|--------------|----------------|---------------|
| large-v3 | 1550M | 1.0x | **8.4** | 11.0 |
| distil-large-v3 | 756M | 6.3x | 9.7 | **10.8** |
| distil-large-v2 | 756M | 5.8x | 10.1 | 11.6 |
| distil-medium.en | 394M | **6.8x** | 11.1 | 12.4 |
| distil-small.en | **166M** | 5.6x | 12.1 | 12.8 |

---

## 4. Whisper Medium

**Parameters:** 769M | **VRAM:** ~5 GB | **Speed:** ~2x large

### Design Intent
A mid-size model balancing accuracy and compute cost. Designed for users who need good accuracy without the resource requirements of large. Has English-only (medium.en) and multilingual variants.

### JTBD: When to pick this model
- Professional English dictation in quiet environments
- Older hardware (original M1 with 8 GB) where large-v3-turbo causes memory pressure
- When multilingual support is needed but large models are too expensive
- CPU-based deployments where large models are impractical
- Legacy deployments (pre-turbo era) that haven't migrated

### Known Strengths
- Good accuracy/speed tradeoff for the pre-turbo era
- English-only variant (medium.en) slightly better on English than multilingual medium
- Fits in 5 GB VRAM — runs on consumer GPUs
- Reasonable multilingual performance

### Known Weaknesses
- **Largely superseded** by large-v3-turbo which is similar size (809M vs 769M) but significantly better
- Worse than large models on noisy audio, technical vocabulary, low-resource languages
- Still hallucinates on silence
- Multilingual performance noticeably weaker than large variants

### Published Benchmarks
- ~2x real-time on Apple Silicon M1
- WER several percentage points higher than large-v3 on most benchmarks
- ~5 GB VRAM

---

## 5. Whisper Small / Base / Tiny

### Small (244M parameters)
**VRAM:** ~2 GB | **Speed:** ~4x large (~6x real-time on M1)

**Design Intent:** Balanced performance for resource-constrained environments. The smallest model where accuracy is "good enough" for most dictation without being painful.

**JTBD:**
- Daily dictation on Intel Macs or battery-sensitive Apple Silicon use
- Edge devices with 2+ GB available
- Real-time applications where accuracy can be traded for latency
- When cost per inference matters (cloud deployments at scale)

**Strengths:** Good English accuracy for its size, runs well on CPU, small download (~461 MB)
**Weaknesses:** Noticeably worse on technical vocabulary, non-English, noisy audio. Higher hallucination rate.
**Benchmark:** ~12.1% WER on English (distil-small.en is comparable). Urdu study: 33.68% WER.

---

### Base (74M parameters)
**VRAM:** ~1 GB | **Speed:** ~7x large (~16x real-time on M1)

**Design Intent:** Fast transcription with acceptable accuracy. Minimal resource footprint.

**JTBD:**
- Quick notes and short messages where speed > accuracy
- Casual dictation on any hardware
- IoT/embedded with modest compute
- Prototyping and development

**Strengths:** Very fast, minimal memory, instant feel on Apple Silicon
**Weaknesses:** Significant accuracy degradation vs small. Struggles with accents, noise, domain terms. Urdu study: 53.67% WER.
**Benchmark:** ~16x real-time on M1

---

### Tiny (39M parameters)
**VRAM:** ~1 GB | **Speed:** ~10x large (~32x real-time on M1)

**Design Intent:** Fastest possible inference with minimal resources. Proof-of-concept / demo tier.

**JTBD:**
- Real-time on extremely constrained hardware
- Live previews during recording
- When ANY transcription is better than none
- Free tier / trial experiences

**Strengths:** Near-instant inference, runs anywhere, ~75 MB download
**Weaknesses:** Highest error rate. Largest reverb penalty (15.5 pp WER increase). Struggles with anything beyond clean, close-mic English speech. Urdu study: 67.08% WER.
**Benchmark:** ~32x real-time on M1

---

## 6. CrisperWhisper

**Base model:** Fine-tuned from openai/whisper-large-v3
**Parameters:** ~2B (same encoder as large-v3, adjusted decoder)
**License:** CC-BY-NC-4.0 (non-commercial)
**Developed by:** Nyra Health / Nyra Labs (clinical speech analysis origin)
**Paper:** Accepted at INTERSPEECH 2024

### Relationship to Base Whisper
CrisperWhisper is a fine-tuned variant of Whisper large-v3 with three key modifications:
1. **Adjusted tokenizer** — retokenization ensures each token maps to either a word OR a pause/space, never both. This enables clean alignment for word-level timestamps via DTW.
2. **Custom attention loss** — trains the 15 best-performing decoder attention heads specifically for alignment accuracy using datasets with word-level timestamp annotations (AMI, TIMIT, CommonVoice with forced alignment).
3. **Verbatim training** — fine-tuned on high-quality verbatim transcription datasets to capture disfluencies, fillers, stutters, and false starts that standard Whisper suppresses.

Training is done in 3 stages: (1) adjust to new tokenizer on ~10,000h audio, (2) exclusively verbatim high-quality datasets, (3) continue with attention loss for 6,000 steps. Uses WavLM augmentations (random noise/speech injection).

### Specific JTBD That Base Whisper Doesn't Address
1. **Precise word-level timestamps** — ~30ms mean boundary error on read speech, ~41ms on conversational (vs Whisper's ~50-100ms+ with standard DTW). Critical for subtitle synchronization, clinical speech timing analysis, audio editing.
2. **Verbatim transcription** — captures every "um", "uh", stutter, false start, repetition. Standard Whisper follows an "intended speech" style that omits these. Critical for clinical speech assessment, legal proceedings, conversation analysis, UX research.
3. **Filler detection** — explicitly detects and categorizes fillers. Marked with [UM], [UH] etc.
4. **Disfluency-aware timestamps** — maintains timestamp precision even around pauses and disfluencies where standard Whisper's attention-based timing degrades badly.

### CrisperWhisper 2.0 (supersedes v1)
- 3-5x faster inference
- Adds "intended mode" (switch between verbatim and clean output)
- Hotwords support
- "Verbatimize" mode
- Seamless long-form
- Speculative decoding
- Available as turbo variant (nyralabs/CrisperWhisper2.0_turbo)
- pip install: `pip install crisperwhisper`

### Known Strengths
- **#1 on Open ASR Leaderboard** for verbatim datasets (TED, AMI)
- Average WER: 6.66% (vs Whisper large-v3's 7.7%) across 9 benchmarks
- Dramatically better on verbatim-style datasets: AMI 8.72% vs 16.01% (Whisper large-v3)
- Segmentation F1: 0.79 vs 0.66 (Whisper large-v3) on AMI IHM
- Word boundary accuracy: 30ms (read) / 41ms (conversational) — best available
- Hallucination mitigation (1% noise-only training samples force empty prediction)
- German + English trained (both languages validated)

### Known Limitations
- **Non-commercial license** (CC-BY-NC-4.0 for v1) — cannot use in commercial products without licensing
- **English and German only** — no other languages guaranteed
- **Larger than turbo** — same size as large-v3, so slower than turbo variants
- **Requires custom transformers fork** (v1) or `crisperwhisper` package
- **CTranslate2/faster-whisper compatibility:** timestamp accuracy NOT guaranteed with faster-whisper due to different implementation
- Slightly worse than large-v3 on some non-verbatim benchmarks (Earnings22: 12.37 vs 11.3, LibriSpeech other: 3.97 vs 3.91)
- v1 is deprecated in favor of 2.0

### Published Benchmarks (v1, Open ASR Leaderboard)

| Dataset | CrisperWhisper | Whisper Large-v3 |
|---------|----------------|------------------|
| AMI | **8.72** | 16.01 |
| Earnings22 | 12.37 | **11.3** |
| GigaSpeech | 10.27 | **10.02** |
| LibriSpeech clean | **1.74** | 2.03 |
| LibriSpeech other | 3.97 | **3.91** |
| SPGISpeech | **2.71** | 2.95 |
| TED-LIUM | **3.35** | 3.9 |
| VoxPopuli | **8.61** | 9.52 |
| CommonVoice | **8.19** | 9.67 |
| **Average WER** | **6.66** | 7.7 |

---

## Summary Decision Matrix

| Need | Best Pick | Runner-up |
|------|-----------|-----------|
| Multilingual, max accuracy | large-v3 | large-v3-turbo |
| General-purpose default (2026) | large-v3-turbo | distil-large-v3 (English) |
| English-only, speed matters | distil-large-v3 | large-v3-turbo |
| Verbatim transcription / timestamps | CrisperWhisper 2.0 | large-v3 |
| Speculative decoding (exact outputs) | distil-large-v3 + large-v3 | — |
| Constrained hardware (8 GB) | large-v3-turbo | small |
| Edge / mobile / embedded | tiny or base | Moonshine (non-Whisper) |
| Legacy / CPU-only | small | medium |

---

## Sources

- OpenAI Whisper GitHub: https://github.com/openai/whisper
- OpenAI Whisper model card: https://github.com/openai/whisper/blob/main/model-card.md
- Whisper Turbo release discussion: https://github.com/openai/whisper/discussions/2363
- Distil-Whisper GitHub: https://github.com/huggingface/distil-whisper
- Distil-Whisper paper (arXiv): https://arxiv.org/abs/2311.00430
- CrisperWhisper HuggingFace: https://huggingface.co/nyralabs/CrisperWhisper
- CrisperWhisper paper (arXiv, INTERSPEECH 2024): https://arxiv.org/abs/2408.16589
- CrisperWhisper 2.0 turbo: https://huggingface.co/nyralabs/CrisperWhisper2.0_turbo
- Northflank STT benchmark guide (Jan 2026): https://northflank.com/blog/best-open-source-speech-to-text-stt-model-in-2026-benchmarks
- Groq Whisper Turbo announcement: https://groq.com/blog/whisper-large-v3-turbo-now-available-on-groq-combining-speed-quality-for-speech-recognition
- Deepgram Whisper v3 hallucination study: https://deepgram.com/learn/whisper-v3-results
- WhisperNotes model benchmarks: https://whispernotes.app/whisper-models
- WhisperNotes Turbo vs V3: https://whispernotes.app/blog/introducing-whisper-large-v3-turbo
- Voibe Superwhisper model guide: https://www.getvoibe.com/resources/best-local-whisper-model-superwhisper/
- Whisper official model docs (Mintlify): https://openai-whisper.mintlify.app/concepts/models
- TuringPost Whisper overview (2026): https://www.turingpost.com/p/topic-15-inside-whisper-an-open-source-audio-model
- AssemblyAI vs OpenAI Whisper (2026): https://www.assemblyai.com/blog/comparing-universal-2-and-openai-whisper
