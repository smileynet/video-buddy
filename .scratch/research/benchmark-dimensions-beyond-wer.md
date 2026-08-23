# Benchmark Dimensions Beyond WER for ASR Evaluation

## Summary

WER (Word Error Rate) measures raw word-level transcription accuracy but is insufficient for evaluating ASR engines in a video note-taking pipeline. For our use case—turning YouTube videos into Markdown notes with quotes, timestamps, and summaries—we need to measure at least 8 additional dimensions: timestamp accuracy, proper noun/technical jargon fidelity, punctuation and capitalization correctness, paragraph segmentation quality, hallucination resistance, multi-speaker handling, noise robustness, and code/non-English content handling. Modern evaluation literature (2024-2026) strongly converges on the view that "your metric stack is your product strategy"—metrics should be chosen to reflect what downstream consumers actually need.

## Dimensions

### 1. Timestamp Accuracy

**Why it matters for us:** Timestamps are used for quote attribution, linking notes back to source video, and building timestamp-indexed summaries. A 2-second drift makes quotes unattributable.

**How to measure:**
- Mean Absolute Error (MAE) of word-level timestamp boundaries vs. forced alignment ground truth
- Timestamp precision/recall: % of predicted word boundaries within ±50ms, ±100ms, ±200ms tolerance
- CrisperWhisper (2024) demonstrated that Whisper's default timestamps have significant drift, and that tokenizer adjustments + DTW on cross-attention scores improve precision substantially

**Key finding:** Modern ASR research (2607.18934) shows "transcription style (verbatim vs. intended) is an uncontrolled latent variable, causing... unreliable word-level timing." Timestamp errors range 20-120ms across languages with dedicated models (2505.15646).

**Benchmark approach:** Use a forced-alignment reference (e.g., Montreal Forced Aligner on clean segments) and compute MAE at word boundaries.

### 2. Technical Jargon and Proper Noun Accuracy (Missed Entity Rate)

**Why it matters for us:** YouTube tech videos reference library names, API calls, framework names, and people. "React" vs "react", "NumPy" vs "numb pie", "Kubernetes" vs anything Whisper hallucinates.

**How to measure:**
- **Missed Entity Rate (MER):** Accuracy specifically on high-value tokens (proper nouns, technical terms, acronyms)
- Entity-weighted WER: weight errors on named entities higher than filler words
- Domain-specific vocabulary accuracy (pre-defined term lists)

**Key finding:** AssemblyAI's evaluation framework (2026) elevates MER as the primary metric for domain-specific use. Apple's HEWER metric (2024) specifically classifies misspelled proper nouns as "major errors" that impact readability. Research on NBA commentary (2602.18966) showed 17% WER reduction by providing domain context—demonstrating that jargon accuracy is a separable, improvable dimension.

**Benchmark approach:** Build a term list per video domain (programming, data science, etc.), score entity-level accuracy separately from general WER.

### 3. Punctuation and Capitalization Accuracy

**Why it matters for us:** Markdown notes need proper sentences. Missing periods = run-on quotes. Wrong capitalization = unreadable output and broken proper nouns.

**How to measure:**
- Punctuation F1 (per punctuation type: period, comma, question mark)
- Capitalization accuracy (especially sentence-initial and proper noun capitalization)
- Apple's HEWER metric directly incorporates punctuation and capitalization into its scoring, counting each punctuation mark as a token

**Key finding:** Apple (2024) found that for podcasts with 9.2% WER, the HEWER (counting only meaning-changing errors, proper noun misspellings, and punctuation/capitalization errors) was just 1.4%—showing that most "errors" WER counts don't matter for readability, but the ones that DO matter (punctuation, caps, proper nouns) are invisible to standard WER.

**Benchmark approach:** Separate punctuation restoration accuracy from word accuracy. Measure F1 per punctuation type and case accuracy on proper nouns.

### 4. Paragraph Segmentation Quality

**Why it matters for us:** Raw transcripts are wall-of-text. The agent needs coherent paragraph breaks to write meaningful "Detailed Notes" sections. Poor segmentation = incoherent summaries.

**How to measure:**
- Boundary Similarity (BS) score
- Pk metric (standard for text segmentation)
- F1 on paragraph boundary prediction
- Human evaluation via Likert scale (1-5)

**Key finding:** Retkowski & Waibel (2025, arXiv 2512.24517) established the first benchmarks for paragraph segmentation in speech (TEDPara and YTSegPara). They showed that paragraph segmentation is an "underexplored" but critical dimension—human evaluators consistently prefer paragraph-segmented transcripts. LLM-based constrained decoding achieves human-level paragraph placement. Current ASR outputs typically deliver zero paragraph structure.

**Benchmark approach:** Use the TEDPara evaluation framework. For our pipeline, measure whether the ASR output or post-processing provides usable segment boundaries for the agent.

### 5. Hallucination Resistance

**Why it matters for us:** Whisper is known to hallucinate during silence, music, or non-speech segments—producing fluent but entirely fabricated text. This poisons notes with false content.

**How to measure:**
- Hallucination rate on non-speech segments (silence, music, applause)
- SHALLOW benchmark (2025, arXiv 2510.16567): 4-axis evaluation (lexical, phonetic, morphological, semantic)
- Insertion error rate (hallucinated words with no audio correlate)
- Detection: monitor for repeated phrases, text unrelated to audio context

**Key finding:** Whisper large-v3 hallucination rate on non-speech is 86.88% without mitigation (2606.07473). The SHALLOW framework found that WER correlation with actual error patterns "weakens substantially as WER increases"—meaning hallucinations are precisely the errors WER is worst at capturing. YouTube videos frequently have intro music, transitions, and silence that trigger hallucinations.

**Benchmark approach:** Include non-speech segments in test data. Measure insertion rate separately. Test with YouTube intros/outros/transitions.

### 6. Multi-Speaker Handling (Diarization)

**Why it matters for us:** Interview-style videos, panel discussions, and tutorials with multiple speakers need attribution for quotes. Even without full diarization, speaker change detection matters.

**How to measure:**
- **cpWER** (concatenated minimum-permutation WER): measures transcription + speaker attribution jointly
- Diarization Error Rate (DER): missed speech, false alarm, speaker confusion
- Speaker change detection F1

**Key finding:** AssemblyAI (2026): "You can score a perfect WER and still produce a transcript that's useless because it attributed the customer's words to the agent." Whisper itself does NOT do diarization—it requires a separate pipeline (pyannote, etc.). For our pipeline, even basic speaker-change markers would improve quote attribution in notes.

**Benchmark approach:** Test with multi-speaker YouTube content (interviews, panels). Measure cpWER when diarization pipeline is integrated. At minimum, measure WER degradation on overlapping speech.

### 7. Noise Robustness

**Why it matters for us:** YouTube audio quality varies enormously—from studio podcasts to conference talks with echo to screen recordings with keyboard noise.

**How to measure:**
- WER at various SNR levels (clean, 20dB, 10dB, 5dB)
- WER on specific noise types: background music, keyboard typing, room echo, compression artifacts
- Degradation curve: how much does WER increase per 5dB SNR drop?

**Key finding:** The SHALLOW benchmark and multiple 2025-2026 papers emphasize that model behavior diverges significantly from WER predictions "under degraded and challenging conditions." CrisperWhisper specifically targets robustness against "multiple speakers and background noise." YouTube compression and variable microphone quality are the dominant real-world noise source for our pipeline.

**Benchmark approach:** Test with real YouTube audio at various quality levels. Include screen recordings, conference talks, and outdoor content. Stratify results by audio quality tier.

### 8. Code Snippet / Alphanumeric Recognition

**Why it matters for us:** Programming tutorials dictate code. "def main colon" → `def main():`. Variable names, URLs, version numbers, shell commands—these are high-value content that standard ASR mangles.

**How to measure:**
- CER (Character Error Rate) on code-dictation segments
- Accuracy on alphanumeric sequences (URLs, version numbers, file paths)
- Recognition of programming keywords and syntax markers

**Key finding:** No established benchmark exists specifically for code dictation in ASR. However, the MER concept applies—code tokens are domain-specific high-value entities. CER is more appropriate than WER for code because single-character errors in variable names are catastrophic.

**Benchmark approach:** Collect segments where speakers dictate code or reference specific versions/URLs. Score with CER and exact-match on identified code tokens.

### 9. Non-English / Code-Switching Content

**Why it matters for us:** Tech videos mix English with terms from other languages, speaker accents vary, and some source content may be partially non-English.

**How to measure:**
- Code-switch WER: accuracy specifically on mixed-language utterances
- Per-accent WER stratification
- Language identification accuracy on segment level

**Key finding:** AssemblyAI (2026): "A model can score beautifully on separate English and Spanish test sets and still break the moment a speaker mixes them in one breath." Universal-3.5 Pro achieves 7.69% normalized WER on code-switched audio across 5 language pairs. Whisper evaluation across accents (2024, Evaluating OpenAI's Whisper) shows "native English accents demonstrate higher accuracy than non-native accents" with notable associations to L1 typology.

**Benchmark approach:** Include accented English content and videos with occasional non-English terms. Measure WER stratified by speaker accent profile.

### 10. Semantic WER (Meaning Preservation)

**Why it matters for us:** Our pipeline feeds transcripts to an LLM agent for summarization. The agent doesn't care about "cannot" vs "can't"—it cares whether meaning is preserved. Traditional WER penalizes harmless variations.

**How to measure:**
- Use a reasoning model to judge whether model output and reference convey the same information
- NLI-based (Natural Language Inference) approaches: does the transcript entail the reference meaning?
- LLM-as-judge pairwise comparison

**Key finding:** AssemblyAI (2026): "An LLM doesn't care whether the transcript says 'cannot' or 'can't'; it extracts the same meaning either way. Traditional WER penalizes that harmless difference just as hard as a genuine error." The 2025 paper (2506.16528) on aligning ASR evaluation with human judgments achieved 0.890 correlation with human judgments by "prioritizing intelligibility over error-based measures."

**Benchmark approach:** For a subset of test data, have an LLM judge semantic equivalence between ASR output and reference. Report Semantic WER alongside traditional WER to show the "real" error rate for our downstream use.

## Proposed Evaluation Matrix for video-buddy

| Dimension | Priority | Metric | Tooling |
|-----------|----------|--------|---------|
| Word accuracy | High | WER (normalized) | jiwer, whisper_normalizer |
| Timestamp accuracy | High | MAE at word boundaries | Montreal Forced Aligner as reference |
| Proper noun / jargon | High | Missed Entity Rate | Custom term lists per domain |
| Punctuation / caps | High | Punct F1, HEWER | Custom scorer |
| Hallucination | High | Insertion rate + non-speech hallucination rate | Segment classification |
| Paragraph segmentation | Medium | Boundary Similarity, Pk | segeval library |
| Multi-speaker | Medium | cpWER (when diarization available) | pyannote + jiwer |
| Noise robustness | Medium | WER stratified by SNR | ffmpeg for SNR estimation |
| Code recognition | Medium | CER on code segments | Custom |
| Semantic equivalence | Low | Semantic WER via LLM judge | Claude/GPT evaluation |
| Code-switching | Low | Separate WER on mixed-lang segments | whisper_normalizer |

## Sources

1. AssemblyAI (2026). "How to evaluate speech recognition models." https://www.assemblyai.com/blog/how-to-evaluate-speech-recognition-models — Comprehensive modern guide covering WER, Semantic WER, MER, cpWER, CER, code-switching, ground truth quality.

2. Apple ML Research (2024). "Humanizing Word Error Rate for ASR Transcript Readability and Accessibility." https://machinelearning.apple.com/research/humanizing-wer — HEWER metric focusing on readability-impacting errors (proper nouns, punctuation, capitalization).

3. Retkowski & Waibel (2025). "Paragraph Segmentation Revisited: Towards a Standard Task for Structuring Speech." arXiv:2512.24517 — First benchmarks for paragraph segmentation in speech (TEDPara, YTSegPara).

4. CrisperWhisper / Zusag et al. (2024). "Accurate Timestamps on Verbatim Speech Transcriptions." Interspeech 2024 — Tokenizer adjustments for improved word-level timestamp precision.

5. SHALLOW Benchmark (2025). "Hallucination Benchmark for Speech Foundation Models." arXiv:2510.16567 — 4-axis hallucination evaluation (lexical, phonetic, morphological, semantic).

6. Wagner et al. (2026). "From Text Metrics to Model Internals: A Study of Whisper ASR Hallucination Detection." arXiv:2606.23060 — Hallucination detection via decoder representations.

7. Sarvam AI (2025). "Indic ASR evaluation: beyond WER to LLM & semantic metrics." https://www.sarvam.ai/blogs/evaluating-indian-language-asr — LLM-WER, Intent Score, Entity Preservation Score.

8. Aligning ASR Evaluation (2025). arXiv:2506.16528 — 0.890 correlation with human judgments using intelligibility-focused metrics.

9. Open ASR Leaderboard (2025). arXiv:2510.06961 — Standardized WER + RTFx evaluation across 86 systems, 12 datasets.

10. "Activating Controllable Verbatim ASR with Word-Level Timing" (2026). arXiv:2607.18934 — Transcription style as latent variable causing timing unreliability.

11. "Whisper: Courtside Edition" (2026). arXiv:2602.18966 — 17% WER reduction on NBA commentary via LLM-generated domain context.

12. Hugging Face Audio Course. "Evaluation metrics for ASR." https://huggingface.co/learn/audio-course/en/chapter5/evaluation — Practical primer on WER calculation.

## Open Questions

1. **Timestamp evaluation ground truth:** What's the most practical way to generate forced-alignment ground truth for YouTube audio at scale? Montreal Forced Aligner requires clean audio + transcript pairs.

2. **Code dictation benchmarks:** No public benchmark exists for evaluating ASR on spoken code. Should we build a small internal one from programming tutorial segments?

3. **Hallucination vs. deletion tradeoff:** Aggressive hallucination filtering (VAD gating) may cause deletions of quiet speech. What's the right balance for note-taking where completeness matters?

4. **Semantic WER cost:** LLM-as-judge evaluation is expensive. Is it worth running on every benchmark iteration, or only for final model selection?

5. **Paragraph segmentation ownership:** Should paragraph quality be measured as an ASR benchmark dimension, or is it purely a post-processing concern our pipeline already handles via the agent?

6. **Multi-engine strategy:** Different engines may excel on different dimensions (e.g., Whisper for WER, AssemblyAI for diarization). Should the benchmark inform a routing strategy rather than a single-engine choice?

7. **YouTube-specific audio artifacts:** Compression, auto-gain, noise gates—should we benchmark specifically on YouTube's audio codec output vs. raw source audio?
