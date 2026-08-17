---
id: "01"
title: "Evaluate CrisperWhisper against current Whisper pipeline"
status: in_progress
blocked_by: []
priority: high
---

# Evaluate CrisperWhisper against current Whisper pipeline

## Context

CrisperWhisper (https://github.com/nyrahealth/CrisperWhisper) claims improved word-level timestamps
and verbatim transcription (filler words, stutters, false starts) over standard Whisper. This is
directly relevant to video-buddy's transcription pipeline which currently uses faster-whisper.

Our existing work includes:
- Whisper transcription via faster-whisper (CPU int8, GPU float16)
- Batch transcription for digest workflows (107+ videos processed)
- Remote backend support (SSH to GPU machines)
- YouTube caption fallback when available

## What to build

1. **Clone and explore** CrisperWhisper at `.references/CrisperWhisper/`
2. **Document** its architecture, model variants, and claimed improvements
3. **Design benchmark** comparing CrisperWhisper vs current faster-whisper pipeline:
   - Word-level timestamp accuracy (we have frames correlated to transcripts)
   - Verbatim fidelity (filler words, stutters, false starts)
   - Speed/throughput on CPU and GPU
   - Memory footprint
   - Integration complexity (can it replace faster-whisper as a backend?)
4. **Propose baseline eval** using existing transcribed videos as ground truth:
   - Select 5-10 videos from prior digests with YouTube captions as reference
   - Compare WER (word error rate) for both engines against YouTube captions
   - Compare timestamp alignment against frame correlation data
   - Measure processing time per minute of audio

## Acceptance criteria

- [ ] CrisperWhisper cloned to `.references/CrisperWhisper/`
- [ ] Architecture and capabilities documented in `.scratch/research/crisper-whisper.md`
- [ ] Benchmark design doc written to `.scratch/research/crisper-whisper-benchmark.md`
- [ ] Benchmark includes: test corpus selection, metrics, methodology, expected outcomes
- [ ] At least 3 videos identified from existing work as baseline test cases
- [ ] Integration path assessed (drop-in replacement? adapter needed? API differences?)

## Validation criteria

- Research doc cites actual source code / README from the cloned repo
- Benchmark design is executable (specific commands, specific files, measurable outputs)
- Test corpus includes at least one short (<5 min), one medium (10-20 min), and one long (>30 min) video
