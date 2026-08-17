# CrisperWhisper: Architecture & Capabilities

## Overview

CrisperWhisper 2.0 by Nyra Health/Labs. A fork of Whisper with controllable verbatim/intended
speech recognition, improved word-level timestamps, hallucination detection, and speculative
decoding. MIT code; weights non-commercial (commercial license available).

## Key Differences from faster-whisper

| Feature | faster-whisper | CrisperWhisper |
|---------|---------------|----------------|
| Backend | upstream ctranslate2 | forked ctranslate2-crisperwhisper |
| Word timestamps | DTW-based alignment | Viterbi HMM with blank states, ~30ms MAE |
| Verbatim mode | No | Yes (fillers, stutters, false starts preserved) |
| Hallucination detection | No | 3-tier: n-gram blocking, context repair, post-hoc loop |
| Speculative decoding | No | Yes, adaptive K, 5.3x RTF speedup |
| Forced alignment | No | Yes, transcribe-then-align via difflib |
| Dual transcription | No | Yes (verbatim + intended simultaneously) |
| Model variants | upstream large-v3, turbo, etc. | Custom fine-tuned: large/turbo/medium/small + Pro |

## Architecture

### Engine (engine.py)
Core transcription engine. Handles segmentation, VAD, and orchestrates the pipeline:
audio → mel features → decode (with optional speculative) → word timing → result

### Word Timing (word_timing.py)
The major differentiator. Uses Viterbi HMM alignment with:
- Virtual blank states between words
- Blank probabilities derived from mel energy (gamma=3, penalty=3)
- Attention sharpened to power 5.0
- Inter-word gap splitting at 100ms threshold
- Result: ~29.6ms word-boundary MAE (vs faster-whisper's ~60-100ms)

### Forced Alignment (forced_align.py)
Transcribe-then-align approach:
1. Transcribe with word_timestamps=True
2. Align reference text via difflib.SequenceMatcher
3. Substitutions inherit hypothesis spans
4. Insertions interpolated proportional to word length

### Hallucination Detection (hallucination.py)
Three tiers:
1. Real-time n-gram blocking during step-by-step decoding
2. Context repair: rewind-and-escape with max 3 repairs per segment
3. Post-hoc loop detection as safety net

Thresholds: {1-gram: 8 reps, 2-gram: 8, 3-gram: 4, 4-gram: 3, 5-gram: 3}

### Speculative Decoding (speculative.py)
Uses a smaller "draft" model to propose tokens, validated by the main model.
Adaptive K (number of speculative tokens). Claims 5.3x RTF speedup.

## Models Available

| Model | Size | Use Case |
|-------|------|----------|
| large | Full size | Best accuracy |
| turbo | Distilled | Speed/accuracy balance |
| medium | Medium | Lower resource |
| small | Small | Edge/mobile |
| *-pro | + hotword boosting | Domain-specific vocabulary |

## Published Benchmarks

- Disfluency F1: 87.8% (93.5% Pro)
- Word timing MAE: 29.6ms
- RTF with CT2+speculative: 5.3x faster than realtime

## API Surface

```python
from crisperwhisper import CrisperWhisperModel

model = CrisperWhisperModel("nyrahealth/CrisperWhisper_turbo")
result = model.transcribe("audio.wav", word_timestamps=True)

# Access word-level data
for word in result.words:
    print(f"[{word.start:.2f}-{word.end:.2f}] {word.text}")

# Dual mode (verbatim + intended)
dual = model.transcribe_dual("audio.wav")

# Forced alignment
aligned = model.forced_align("audio.wav", "reference transcript text")

# Verbatimize existing text
verbatim = model.verbatimize("audio.wav", "clean text")
```

## Dependencies & Installation

```bash
pip install crisperwhisper              # base (tokenizers, numpy, soundfile)
pip install crisperwhisper[ct2]         # CTranslate2 backend (Linux x86_64 only)
pip install crisperwhisper[transformers] # HuggingFace backend (portable)
```

**⚠️ Critical conflict**: The `ct2` extra installs `ctranslate2-crisperwhisper` which occupies
the same `ctranslate2` namespace as upstream. Cannot coexist with faster-whisper in the same
Python environment. Would need a separate venv or container.

## Integration Assessment

### Drop-in replacement?
**No.** Different API (`CrisperWhisperModel` vs `WhisperModel`), different output structure
(`TranscriptionResult.words` vs segments generator), and conflicting ctranslate2 package.

### Adapter needed?
**Yes.** Would need:
1. Separate venv or container (due to ctranslate2 conflict)
2. Adapter layer mapping CrisperWhisper output to our `{start, duration, text}` segment format
3. Word-level timestamp data would be a new capability (our current pipeline only captures segments)

### Integration paths:
1. **Separate backend** — like our SSH remote backend, run CrisperWhisper in its own env
2. **Container** — Docker image with CrisperWhisper, called as a service
3. **Transformers backend** — avoids the ctranslate2 conflict but loses speculative decoding speed
