# ASR Benchmark Practices & Methodologies

## Summary

Word Error Rate (WER) remains the industry-standard metric for comparing ASR engines, but modern best practice demands multiple complementary metrics (Semantic WER, Missed Entity Rate, cpWER for diarization), rigorous text normalization before scoring, and evaluation across diverse datasets that match real production conditions. The biggest methodological pitfalls are inadequate normalization (which inflates WER by penalizing formatting differences), corrupted ground truth transcripts, and evaluating on unrepresentative audio. The Open ASR Leaderboard (Hugging Face, 60+ models, 11 datasets) and Artificial Analysis AA-WER benchmark represent the current state of the art for reproducible, transparent ASR comparison.

## Details

### Standard Metrics

| Metric | Measures | Best For |
|--------|----------|----------|
| **WER** (Word Error Rate) | (Substitutions + Insertions + Deletions) / Reference Words | General benchmarking, single comparable number |
| **CER** (Character Error Rate) | Character-level edit distance | Non-space-delimited languages (CJK, Thai), alphanumeric codes |
| **Semantic WER** | Whether meaning is preserved (LLM-judged) | LLM pipelines, voice agents where exact wording doesn't matter |
| **MER** (Missed Entity Rate) | Accuracy on high-value tokens (names, numbers, domain terms) | Medical, legal, technical transcription |
| **cpWER** | Transcription + speaker attribution (concatenated min-permutation WER) | Multi-speaker audio, diarization quality |
| **cWER** (Content WER) | Separates genuine errors from valid stylistic variation | Fair evaluation when conventions differ (tense, spelling) |
| **RTFx** (Inverse Real-Time Factor) | Audio Duration / Transcription Time | Efficiency/speed comparison |
| **Ins/Del/Sub rates** | Breakdown of error types | Diagnosing specific failure modes |

### Standard Benchmark Datasets

| Dataset | Domain | Duration | Style |
|---------|--------|----------|-------|
| **LibriSpeech** (clean/other) | Audiobooks | ~10h test | Read speech |
| **GigaSpeech** | Audiobook, podcast, YouTube | 40h test | Read + spontaneous |
| **Earnings21/22** | Corporate earnings calls | 39h / 119h | Oratory, spontaneous, accented |
| **AMI Meeting Corpus** | Meetings | 9h | Spontaneous, multi-speaker |
| **VoxPopuli** | European Parliament | 5h | Oratory |
| **TED-LIUM v3** | TED Talks | 3h | Oratory |
| **SPGISpeech** | Financial meetings | 100h | Oratory, spontaneous |
| **FLEURS** | Wikipedia (multilingual) | 2-3.5h/lang | Read |
| **CoVoST-2** | Open domain (multilingual) | 5-23h/lang | Read |
| **Common Voice** | Crowdsourced recordings | Varies | Read |
| **AA-AgentTalk** (proprietary) | Voice agent conversations | ~250min | Conversational |

### Normalization (Critical Step)

Normalization removes surface-form differences so you compare transcription quality, not formatting conventions. Both reference and hypothesis MUST be normalized identically.

**Standard normalizer:** OpenAI's Whisper normalizer (`whisper-normalizer` package):
- Lowercase all text
- Remove punctuation
- Expand contractions ("won't" → "will not")
- Standardize numbers ("twenty-five" → "25")
- Remove filler words ("uh", "um", "mhm")
- Standardize spelling (colour → color)

**Extended normalizations** (Artificial Analysis, Gladia):
- Digit/phone-number grouping equivalence (303-775-4498 = 303 775 4498)
- Letter-separated name formats (S-I-N-G-H = S I N G H)
- Time formatting (7:00pm = 7pm)
- Unit abbreviations (mg/dL = milligrams per deciliter)
- Currency/percentage formatting
- Preserve meaning-bearing codes (F-150, W-2)

**Alternative:** Gladia's `gladia-normalization` library handles numbers more aggressively than Whisper's normalizer.

### Methodology Best Practices

1. **Define evaluation goal first** — what "good" means depends on use case (call centers need diarization accuracy; medical needs entity accuracy; voice agents need low deletion rate)
2. **Use representative audio** — benchmark on audio that matches real production traffic (accents, noise levels, domain vocabulary, speaker counts)
3. **Validate ground truth** — human transcripts contain 5-15% unnecessary inconsistency; bad references penalize better models for being correct
4. **Report multiple metrics** — WER alone treats all words equally; add MER for domain terms, cpWER for multi-speaker
5. **Aggregate correctly** — use audio-duration-weighted average WER so short clips don't bias results vs. longer files
6. **Evaluate streaming and batch separately** — different latency/accuracy tradeoffs
7. **Report alongside factors** — model size, hardware, batch size, quantization, decoding strategy all affect results

### Common Pitfalls

1. **Insufficient normalization** — penalizing "can't" vs "cannot" or "$50" vs "fifty dollars" as errors
2. **Corrupted ground truth** — human transcribers mishear words, normalize inconsistently, miss abbreviations; better models score worse against flawed references
3. **Unrepresentative datasets** — benchmarking call-center use on clean podcast audio overestimates production performance
4. **Single dataset evaluation** — no single dataset is sufficient; one curated result is marketing, many messy datasets is a forecast
5. **Ignoring formatting as errors** — comparing providers on raw transcripts when they format numbers/punctuation differently
6. **Not inspecting reference transcripts** — if reference contains text not in audio (e.g., "this audio is a recording of..."), it inflates WER for all providers
7. **Comparing across different normalizers** — changing normalization rules between references invalidates results
8. **Too few samples** — drawing conclusions from small test sets
9. **Averaging without slicing** — two systems can post similar average WER while failing on different error classes
10. **Ignoring long-form degradation** — models using chunking strategies for long audio may introduce errors at chunk boundaries

### Key Evaluation Tools

| Tool | Purpose |
|------|---------|
| **jiwer** (Python) | Standard WER/CER computation |
| **whisper-normalizer** (Python) | OpenAI's text normalization for English |
| **gladia-normalization** (Python) | Alternative normalizer with better number handling |
| **AssemblyAI Benchmark SDK** | Automated WER, MER, Semantic WER with batch evaluation |
| **Open ASR Leaderboard** (HuggingFace) | Reproducible benchmark harness, 60+ models, 11 datasets |
| **Artificial Analysis** | Independent WER testing across providers with AA-WER methodology |

### Current Top Performers (as of 2025-2026)

**Short-form English:** NVIDIA Canary Qwen 2.5B (5.63% avg WER), IBM Granite Speech 3.3 8B (5.74%)
**Long-form English:** ElevenLabs Scribe v1 (4.33%), RevAI Fusion (5.04%)
**Speed champions:** NVIDIA FastConformer CTC Large (6399x RTFx), NVIDIA Parakeet CTC 1.1B (2728x RTFx)
**Whisper Large v3:** 7.44% avg WER short-form, 6.43% long-form (baseline reference)

## Sources

- [Artificial Analysis: Speech to Text Benchmarking Methodology](https://artificialanalysis.ai/speech-to-text/methodology) — detailed methodology for WER evaluation, normalization, datasets, streaming metrics [L4:verified]
- [AssemblyAI: How to Evaluate Speech Recognition Models (July 2025)](https://www.assemblyai.com/blog/how-to-evaluate-speech-recognition-models) — comprehensive guide covering WER, Semantic WER, MER, cpWER, ground truth correction, practical framework [L5:verified]
- [Open ASR Leaderboard (arXiv 2510.06961)](https://arxiv.org/html/2510.06961v1) — reproducible benchmark, 60+ models, 11 datasets, standardized normalization, WER + RTFx [L4:verified]
- [Gladia: Benchmarking Guide](https://docs.gladia.io/chapters/pre-recorded-stt/benchmarking) — practical pitfalls, normalization importance, dataset selection guidance [L4:verified]
- [OpenAI Whisper Normalizer (GitHub)](https://github.com/openai/whisper/blob/main/whisper/normalizers/english.py) — de facto standard normalization implementation [L1:verified]
- [jiwer (Python package)](https://pypi.org/project/jiwer/) — standard WER computation library [L4:established]
- [Benchmark Contamination, Convention Mismatch, and an Honest Baseline (arXiv 2606.07608)](https://arxiv.org/html/2606.07608v1) — introduces cWER separating genuine errors from stylistic variation [L4:reported]
- [THU-SPMI ASR-Benchmarks (GitHub)](https://github.com/thu-spmi/ASR-Benchmarks) — tracking benchmarking results across widely-used datasets [L6:reported]
- [E2E Networks: Benchmarking Open ASR Models](https://www.e2enetworks.com/blog/benchmarking-asr-models-nvidia-l4-parakeet-whisper-nemotron) — practical considerations for batch size, precision, attention, decoding strategy [L5:reported]

## Open Questions

1. **Which normalizer to standardize on?** Whisper's normalizer is the de facto standard but has known limitations (weak number handling). Gladia and Artificial Analysis have extended it. No single community-standard exists yet.
2. **How to fairly compare streaming vs. batch?** Different providers implement forced endpointing differently; latency measurement methodology varies.
3. **Ground truth quality for our use case?** For video-buddy's YouTube transcription, ground truth from auto-captions is unreliable. Should we generate reference transcripts from a high-quality model and manually correct, or use existing datasets?
4. **Is WER even the right metric for video notes?** Since our output feeds an agent that writes summaries, Semantic WER or a downstream task metric (summary quality) might be more relevant than word-level accuracy.
5. **Long-form chunking effects?** Whisper's 30s context window means chunking is required for long videos. How much does chunking strategy affect quality vs. models with longer context (Conformer-based)?
6. **Cost of evaluation at scale?** Running Semantic WER requires an LLM judge per transcript, making it expensive for large-scale comparison. What's the minimum representative sample size?
