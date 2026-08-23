# CrisperWhisper Independent Benchmarks & User Reports

## Summary

CrisperWhisper has **no truly independent third-party benchmarks** comparing it against standard Whisper/faster-whisper. All published accuracy numbers come from the vendor (Nyra Health/Nyra Labs) or their own papers and leaderboards. However, several data points exist:

1. **The Nyra Verbatim Speech Benchmark** (vendor-created leaderboard) shows CrisperWhisper 2.0 leading in disfluency F1 across 10 languages (87.8 F1 vs. next-best ElevenLabs at 79.2).
2. **One independent academic paper** (MDPI 2026, neurodegenerative disease detection) used CrisperWhisper as a component and reported it performed 5–7% below models using manual transcripts.
3. **GitHub issues** reveal real-world problems: German word repetition hallucinations, 30-second boundary artifacts, CT2/CUDA compilation issues, and missing module errors.
4. **The CT2 fork has a known, vendor-acknowledged timestamp accuracy limitation** — Nyra explicitly states they "do not guarantee the same timestamp accuracy" with the CTranslate2 variant.
5. **No head-to-head WER comparison** between CrisperWhisper and standard faster-whisper on identical benchmarks exists in any independent source found.

## Details

### Vendor-Claimed Benchmarks (NOT independently verified)

#### CrisperWhisper 1.0 (Interspeech 2024 paper, arxiv 2408.16589)

Source: Nyra Health authors (Wagner, Zusag, Thallinger). Published at Interspeech 2024.

- **Transcription:** 1st place on OpenASR Leaderboard for verbatim datasets (TED, AMI)
- **Timestamp accuracy (TIMIT):** 47 ms MAE with sharpening (vs. Whisper base at 203 ms, WhisperX at 66 ms)
- **Disfluency F1:** 73.2% on English DisfluencySpeech (vs. Whisper at 12.0%)
- **Training:** English and German only; model trained on ~3000h mixed data

These numbers appear in the vendor's own paper and repo. They use standard public datasets (TIMIT, AMI) but the evaluation code and pipeline are vendor-controlled.

#### CrisperWhisper 2.0 (arxiv 2607.18934, July 2026)

Source: Same Nyra Labs team. Whisper-medium fine-tune with mode tags.

- **Disfluency F1 (Nyra Verbatim Speech Benchmark, 10 languages):**
  - CrisperWhisper 2.0 Pro: 93.5
  - CrisperWhisper 2.0: 87.8
  - ElevenLabs Scribe v2: 79.2
  - Microsoft MAI-Transcribe-1.5: 77.5
  - CrisperWhisper 1.0 (EN/DE only): 64.8
  - Deepgram Nova-3: 37.8
  - AssemblyAI Universal-3 Pro: 30.5

- **Word-timing accuracy (TIMIT, read speech):**
  - CrisperWhisper 2.0: 29.6 ms MAE (best)
  - xAI Grok STT: 37.1 ms
  - WhisperX: 64.8 ms
  - Deepgram Nova-3: 63.3 ms

- **Word-timing accuracy (FluencyBank, disfluent speech):**
  - CrisperWhisper 2.0: 102 ms MAE
  - CrisperWhisper 1.0+sharpening: 122 ms
  - MFA (forced alignment): 142 ms
  - WhisperX: 200 ms

- **Speed claim:** 3–5x faster inference than CrisperWhisper 1.0 via speculative decoding on CT2

- **Verbatim WER (English DisfluencySpeech):** Not directly comparable to standard WER — they use "verbatim WER" against verbatim references, which includes disfluencies. Their paper shows standard Whisper gets 10.9% vWER because it omits disfluencies that ARE in the reference.

**Critical caveat:** The Nyra Verbatim Speech Benchmark is created by Nyra Labs themselves. The benchmark repo is at github.com/nyrahealth/nyra_verbatim_speech_benchmark. English and German use human-labeled evaluation sets; the other 8 languages use *synthetic* verbatim sets. This is NOT an independent evaluation.

### CrisperWhisper 2.0 Paper's Key Finding (Self-Reported)

The 2607.18934 paper makes a compelling methodological argument:
- Up to 60% of reported WER on conversational benchmarks (like AMI) reflects **style mismatch** rather than recognition failure
- Standard Whisper's instability comes from treating transcription style as an uncontrolled latent variable
- Mode tags resolve this without new architecture

This is a vendor paper but the methodology (decomposing WER into content loss vs. style mismatch) is novel and reproducible by others.

### Independent/Third-Party Usage

#### MDPI Paper: Neurodegenerative Disease Detection (2026)

- **Source:** Independent academic paper (Computers journal, Vol 15, Issue 5)
- **Finding:** "The best-performing setup (Random Forest with CrisperWhisper transcription and Apple embeddings) achieved an accuracy of 85.4% and an AUC of 0.85. Performance was 5–7% below benchmark models relying on manual transcripts or server-based processing."
- **Interpretation:** CrisperWhisper was accurate enough for a downstream clinical classification task but still measurably worse than manual transcripts. This is the closest to an independent evaluation found.

#### CrisperWeaver (Third-Party Flutter App)

- **Source:** github.com/CrispStrobe/CrisperWeaver
- **What:** On-device speech-to-text Flutter app powered by CrispASR/ggml (related to whisper.cpp)
- **Note:** This is a GGML-based app, NOT the CrisperWhisper CT2/transformers model. Named similarly but different runtime. Build scripts expanded from ~30 to ~60 targets, suggesting active development complexity.

#### insanely-fast-crisperwhisper (Community Fork)

- **Source:** github.com/collectiveai-team/insanely-fast--crisperwhisper
- **Claim:** "Transcribe 150 minutes (2.5 hours) of audio in less than 98 seconds with OpenAI's Whisper Large v3"
- **Status:** Community project applying batched inference patterns from insanely-fast-whisper to CrisperWhisper. No independent accuracy comparison published.

#### Unsloth Quantized Version

- **Source:** huggingface.co/unsloth/CrisperWhisper
- **What:** Quantized/optimized version for inference. No benchmarks published with this variant.

### Known Issues (GitHub Issues, User Reports)

From github.com/nyrahealth/CrisperWhisper/issues (31 open issues as of Aug 2026):

| Issue | Date | Problem |
|-------|------|---------|
| #57 | Aug 23, 2026 | `ModuleNotFoundError: No module named 'ctranslate2'` — transformers backend fails because it erroneously tries to import CT2 |
| #49 | Aug 2, 2026 | Request for GGUF/C++ version (whisper.cpp compatible) — not available |
| #45 | Nov 1, 2025 | **Missing content: unstressed words** — model drops unstressed words |
| #44 | Oct 1, 2025 | Python type conversion error on function return |
| #43 | Sep 14, 2025 | Tensor dimension error on certain audio inputs |
| #41 | Jul 24, 2025 | **Word chunk overlap and duplicate timestamps at 30-second boundaries** |
| #40 | Jul 24, 2025 | **German transcription quality degradation — excessive word repetition** (hallucination) |
| #36 | May 27, 2025 | **CT2 package not compiled with CUDA support** — faster-whisper variant fails on GPU |

Key user-reported problems:
1. **German hallucination/repetition** (#40) — model produces excessive word repetitions in German
2. **30-second boundary artifacts** (#41) — word chunks overlap and timestamps duplicate at segment boundaries
3. **CT2 CUDA compilation issues** (#36) — the custom CTranslate2 fork doesn't ship with CUDA in all environments
4. **Missing unstressed words** (#45) — verbatim model still drops some content

### CT2 Fork: Known Limitations

**Vendor-acknowledged (from HuggingFace model card, nyrahealth/faster_CrisperWhisper):**

> "WARNING — this is the converted CrisperWhisper model into CTranslate2 to be compatible with faster whisper framework. However, due to the different implementation of the timestamp calculation in faster whisper or more precisely CTranslate2 **we do not guarantee the same timestamp accuracy** as with the transformers implementation. The transcription accuracy and filler detection should work as expected."

This means:
- **Transcription accuracy:** Expected to be equivalent between CT2 and transformers backends
- **Filler detection:** Expected to be equivalent
- **Timestamp accuracy:** NOT guaranteed — different DTW implementation in CT2 may degrade word boundary precision

For CrisperWhisper 2.0, they ship a custom package `ctranslate2-crisperwhisper` (PyPI) which is a forked CT2 with modifications. This adds a dependency management burden vs. standard faster-whisper which uses upstream CT2.

### Speed Benchmarks

No independent speed comparison found. Vendor claims:
- CrisperWhisper 2.0 is "3–5x faster" than v1.0 via speculative decoding (using turbo as draft model)
- The CT2 backend supports int8/float16 quantization (same as standard faster-whisper)
- Speculative decoding yields "1.4x" additional speedup over standard CT2

For context from independent sources:
- Standard faster-whisper is ~4x faster than OpenAI Whisper on GPU (widely verified)
- CrisperWhisper adds overhead for the verbatim tokenizer adjustments and attention loss features

### Production Deployment Stories

**No public production deployment testimonials found** outside of Nyra Health's own clinical applications (dementia assessment, aphasia classification referenced in their papers).

The PyPI package (`crisperwhisper`) was first published in June 2026 (v0.1.0) and most recently updated to v2.0.1 in July 2026. Monthly HuggingFace downloads for the turbo model: ~11,000. The older faster_CrisperWhisper: ~368 downloads/month.

## Sources

| Source | URL | Type |
|--------|-----|------|
| CrisperWhisper 1.0 paper (Interspeech 2024) | https://arxiv.org/abs/2408.16589 | Vendor paper, peer-reviewed |
| CrisperWhisper 2.0 paper (July 2026) | https://arxiv.org/abs/2607.18934 | Vendor paper, preprint |
| CrisperWhisper 2.0 Turbo model card | https://huggingface.co/nyralabs/CrisperWhisper2.0_turbo | Vendor |
| faster_CrisperWhisper model card (CT2 warning) | https://huggingface.co/nyrahealth/faster_CrisperWhisper | Vendor |
| GitHub Issues | https://github.com/nyrahealth/CrisperWhisper/issues | User reports |
| MDPI neurodegenerative disease paper | https://www.mdpi.com/2073-431X/15/5/287 | Independent academic |
| Nyra Verbatim Speech Benchmark | https://www.nyra-labs.com/research/nyra-verbatim-speech-benchmark | Vendor benchmark |
| ctranslate2-crisperwhisper PyPI | https://pypi.org/project/ctranslate2-crisperwhisper/ | Package |
| crisperwhisper PyPI | https://pypi.org/project/crisperwhisper/ | Package |
| insanely-fast-crisperwhisper | https://github.com/collectiveai-team/insanely-fast--crisperwhisper | Community |
| Nyra Labs website | https://nyra-labs.com/ | Vendor |

## Open Questions

1. **No independent WER comparison exists.** Nobody outside Nyra has published a head-to-head WER test on a standard benchmark (LibriSpeech, Common Voice) comparing CrisperWhisper to standard Whisper large-v3. The vendor's own benchmarks focus on *verbatim* WER and disfluency F1, which are different metrics than what most users care about.

2. **Is the CT2 fork maintained long-term?** The custom `ctranslate2-crisperwhisper` package is pinned to a specific CT2 fork. If upstream CT2 evolves (or is abandoned — SYSTRAN's faster-whisper has been less active), this fork could become a maintenance burden.

3. **How does CrisperWhisper perform on non-English, non-German languages in practice?** The 2.0 paper shows benchmark numbers for 10 languages but 8 of those use *synthetic* evaluation sets, not human-labeled ground truth.

4. **What is the real-world speed overhead vs. standard faster-whisper?** No independent benchmarks measure this. The verbatim tokenizer, attention supervision, and hallucination mitigation likely add some overhead.

5. **Does the model's verbatim bias cause problems for downstream NLP?** CrisperWhisper inserts fillers, repetitions, and cut-off markers. For note-taking, summarization, or search use cases, this verbatim output may need post-processing that standard Whisper's "clean" output avoids.

6. **License restriction:** Non-commercial research license only. Commercial use requires a paid license from Nyra. This limits production adoption visibility — commercial users can't share results publicly without Nyra's involvement.

7. **GGUF/whisper.cpp compatibility:** Not available (Issue #49). Users wanting CPU-only or edge deployment on non-NVIDIA hardware have no path.
