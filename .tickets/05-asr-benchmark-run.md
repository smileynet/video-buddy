---
id: "05"
title: "Execute ASR benchmark: faster-whisper vs WhisperX vs CrisperWhisper on test corpus"
status: open
blocked_by: ["02", "03"]
priority: high
---

# Execute ASR benchmark: faster-whisper vs WhisperX vs CrisperWhisper on test corpus

## Context

With all three backends integrated (tickets 02, 03), run the designed benchmark
(`.scratch/research/crisper-whisper-benchmark.md`) to validate adoption decisions with data.

Research indicates raw WER will be nearly identical (same base weights). Focus on:
- Verbatim fidelity (CrisperWhisper's killer feature)
- Word timestamp accuracy (both WhisperX and CrisperWhisper)
- Hallucination rate on long-form content
- Speed/memory tradeoffs

## What to build

1. Create `benchmark/` directory with runner scripts
2. Extract audio for 5 test corpus videos (if not already cached)
3. Run all three engines on each video, capturing output + timing
4. Compute metrics using `jiwer` + custom scripts
5. Generate comparison report

## Test corpus

| ID | Video | Duration | Purpose |
|----|-------|----------|---------|
| 4NOsCRhziv8 | Material Maker - Stylized Planks | 11.1m | Short, clear speech |
| ORgKY9AlybA | How to Detect AI Slop | 17.2m | Academic, technical vocab |
| B9bztU1sTFA | The Scanline Sweeper | 39.5m | Conference talk, dense |
| KSkcgIYQy0U | Formal methods with Hillel Wayne | 84.9m | Podcast, conversational |
| 8lF7HmQ_RgY | OpenClaw creator interview | 114.1m | Stress test, casual |

## Metrics

1. **WER** (normalized with whisper-normalizer) — confirm parity across engines
2. **Verbatim F1** — count preserved disfluencies in CrisperWhisper vs stripped in others
3. **Word timestamp MAE** — compare WhisperX and CrisperWhisper word boundaries
4. **Hallucination count** — segments with repetitive/confabulated content on 60+ min videos
5. **RTFx** — processing speed relative to audio duration
6. **Peak RSS** — memory usage on longest video

## Acceptance criteria

- [ ] `benchmark/` directory with reproducible scripts
- [ ] All 5 videos processed by all 3 engines (15 transcript outputs)
- [ ] Metrics computed and documented in `benchmark/results.md`
- [ ] Comparison table with per-video and aggregate numbers
- [ ] Clear recommendation: which engine for which use case
- [ ] Speed/memory data captured for capacity planning

## Validation criteria

- Results are reproducible (re-running produces same WER within ±0.1%)
- At least 3 manual spot-checks per engine to validate metric computation
- Report includes hardware specs and software versions for reproducibility
