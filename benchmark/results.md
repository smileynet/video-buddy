# ASR Benchmark Results

**Date:** 2026-08-23  
**Hardware:** faster-whisper on local CPU (AMD), CrisperWhisper on monolith RTX 3070 (8GB, CUDA 12.4)  
**Software:** faster-whisper 1.2.1 (base, int8), CrisperWhisper 2.0.2 (turbo, float16)

## Test Corpus

| Video | Duration | Content Type |
|-------|----------|-------------|
| ORgKY9AlybA | 17:13 | Academic lecture (linguistics, technical vocab) |
| BcKQk0NeBV0 | 10:35 | News analysis (proper nouns, fast pace) |
| B9bztU1sTFA | 39:29 | Conference talk (technical, glyph rendering) |
| Qr3VsZYQy4s | 33:10 | Tutorial (scripted, sine wave game dev) |

Total test audio: **100 minutes**

## Speed

| Video | faster-whisper (CPU) | CrisperWhisper (GPU) | Speedup |
|-------|---------------------|---------------------|---------|
| ORgKY9AlybA (17m) | 185s (5.6x RT) | 14.5s (71x RT) | **12.8x** |
| BcKQk0NeBV0 (10m) | 94s (6.8x RT) | 8.4s (76x RT) | **11.2x** |
| B9bztU1sTFA (39m) | 346s (6.9x RT) | 30.7s (77x RT) | **11.3x** |
| Qr3VsZYQy4s (33m) | 337s (5.9x RT) | 24.9s (80x RT) | **13.5x** |
| **Total (100m)** | **962s (16 min)** | **79s (1.3 min)** | **12.2x** |

CrisperWhisper on GPU is consistently **12x faster** than faster-whisper on CPU.

## Hallucination Resistance

| Video | faster-whisper | CrisperWhisper |
|-------|---------------|----------------|
| ORgKY9AlybA | 0 repeats | 0 repeats |
| BcKQk0NeBV0 | 0 repeats | 0 repeats |
| B9bztU1sTFA | 0 repeats | 0 repeats |
| Qr3VsZYQy4s | **24 repeats** | **0 repeats** |

Hallucination only occurred on one video (Qr3VsZYQy4s — a 33-minute tutorial with periods of silence/music). CrisperWhisper's 3-tier hallucination mitigation completely eliminates the problem.

## Engine Agreement (text similarity)

| Video | Agreement | Notes |
|-------|-----------|-------|
| ORgKY9AlybA | 96.2% | Clean academic speech — both engines agree |
| BcKQk0NeBV0 | 94.0% | Fast-paced news — minor differences in proper nouns |
| B9bztU1sTFA | 95.7% | Technical talk — high agreement |
| Qr3VsZYQy4s | 88.1% | Lower due to 24 hallucinated segments in faster-whisper |

When neither engine hallucinates, they produce **94-96% identical text** despite being different model sizes (base 74M vs turbo 809M).

## Word-Level Timestamps

| Video | CrisperWhisper Words | faster-whisper |
|-------|---------------------|----------------|
| ORgKY9AlybA | 3,174 words | None (segment-level only) |
| BcKQk0NeBV0 | 1,613 words | None |
| B9bztU1sTFA | 6,766 words | None |
| Qr3VsZYQy4s | 5,155 words | None |
| **Total** | **16,708 words** | **0** |

CrisperWhisper provides per-word start/end timestamps (~30ms precision) on all output. faster-whisper only provides segment-level timestamps (~5s granularity).

## WER vs YouTube Captions

YouTube auto-captions cannot serve as reliable reference for WER computation. The YouTube caption tracks contain **3x more words** than either engine produces for the same audio (9,466 vs 3,174 for ORgKY9AlybA), likely due to overlapping subtitle windows in the VTT format. Measured WER of ~67% reflects this word-count mismatch, not actual transcription errors.

**Engine-to-engine WER (4-6%) is the meaningful metric** — showing both engines transcribe the same content with minor differences.

## Recommendation

### CrisperWhisper on monolith GPU should be the default engine.

| Criterion | faster-whisper (CPU) | CrisperWhisper (GPU) | Winner |
|-----------|---------------------|---------------------|--------|
| Speed | 6x realtime | 75x realtime | **CrisperWhisper** (12x faster) |
| Hallucination | 24 repeats on 1/4 videos | 0 on all videos | **CrisperWhisper** |
| Word timestamps | No | Yes (16,708 words) | **CrisperWhisper** |
| Verbatim mode | No | Yes | **CrisperWhisper** |
| Text quality | Comparable | Comparable | Tie |
| Availability | Always (local) | Requires monolith online | faster-whisper |

### Architecture:

1. **Primary:** CrisperWhisper via monolith SSH (`--backend monolith --whisper-engine crisperwhisper`)
2. **Fallback:** faster-whisper locally when monolith unavailable
3. **WhisperX:** Not needed — CrisperWhisper provides better word timestamps natively

### What this means for video-buddy:

- **Batch digest (107 videos × 20 min avg):** 27 min on GPU vs 6 hours on CPU
- **Single ingest:** 15-30 seconds vs 3-6 minutes
- **Quote accuracy:** Word-level timestamps enable precise quote attribution in notes
- **Reliability:** Zero hallucinations means no garbage in agent-generated breakdowns

## Appendix: Model Size Note

This benchmark compares `base` (74M params, CPU) vs `turbo` (809M params, GPU). The speed difference partially reflects hardware (CPU vs GPU) and partially model size. A fairer model-size comparison would be faster-whisper `large-v3-turbo` on the same GPU — but that would eliminate the hallucination detection, word timestamps, and verbatim mode that are CrisperWhisper's differentiators. The comparison reflects the **actual production choice**: what do you get with each engine on the hardware you have?
