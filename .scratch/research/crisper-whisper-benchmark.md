# CrisperWhisper Benchmark Design

## Objective

Compare CrisperWhisper vs our current faster-whisper pipeline across accuracy, timestamp
quality, speed, and integration feasibility using existing video-buddy corpus data.

## Methodology

### Reference Truth

YouTube captions (auto-generated or manual) serve as the baseline reference. These aren't
perfect ground truth, but they provide a consistent comparison point available for all
test videos. Both engines will be compared against this same reference.

**Important note:** Our existing `transcript_*.json` files for videos with captions are
just the YouTube captions reformatted — Whisper was never actually run on those. The
benchmark must run BOTH engines fresh on the raw audio.

### Test Corpus

| ID | Video | Duration | Content Type | Rationale |
|----|-------|----------|-------------|-----------|
| 4NOsCRhziv8 | Material Maker - Stylized Planks | 11.1m | Tutorial (clear speech) | Shortest candidate; single speaker |
| ORgKY9AlybA | How to Detect AI Slop | 17.2m | Lecture (academic) | Mid-length; articulate speaker, technical vocab |
| B9bztU1sTFA | The Scanline Sweeper | 39.5m | Conference talk (technical) | Long; dense technical terminology |
| KSkcgIYQy0U | Formal methods with Hillel Wayne | 84.9m | Podcast (conversational) | Very long; two speakers, natural speech |
| 8lF7HmQ_RgY | OpenClaw creator interview | 114.1m | Interview (casual) | Stress test; longest available, likely has fillers/stutters |

Gap: No short (<5 min) video with YouTube captions available. Consider ingesting a
conference lightning talk for this slot.

### Metrics

#### 1. Word Error Rate (WER)
Standard metric: `(S + D + I) / N` where S=substitutions, D=deletions, I=insertions, N=reference words.

```bash
# Tool: jiwer (pip install jiwer)
python -c "
import jiwer
ref = open('reference.txt').read()
hyp = open('hypothesis.txt').read()
print(jiwer.wer(ref, hyp))
"
```

Compare: faster-whisper WER vs CrisperWhisper WER vs YouTube captions (as self-reference = 0).

#### 2. Word Timestamp Accuracy (CrisperWhisper advantage)
CrisperWhisper claims ~30ms MAE for word boundaries. faster-whisper doesn't produce
word-level timestamps in our current pipeline (segment-level only).

Measurement:
- Extract word-level timestamps from CrisperWhisper output
- Compare segment boundaries between both engines and YouTube caption timestamps
- For frame-correlated videos, check if word timestamps align with visual transitions

#### 3. Verbatim Fidelity (CrisperWhisper advantage)
Count preserved disfluencies: "uh", "um", "like", false starts, repetitions.
- Run both engines on the same audio
- Count filler words in output vs audible fillers (manual spot-check on 5 segments per video)
- CrisperWhisper's `transcribe_dual()` should show verbatim vs intended side-by-side

#### 4. Hallucination Rate
Count hallucinated segments (repeated text, invented content, confabulated phrases).
- Run both on the 114-minute stress test
- Flag any segment where output doesn't match reference AND contains repetitive patterns

#### 5. Speed (RTF = Real-Time Factor)
```
RTF = audio_duration / processing_time
```
Measure for each engine on each test video. Test configurations:
- faster-whisper: CPU int8, GPU float16 (if available)
- CrisperWhisper CT2: same hardware configs
- CrisperWhisper Transformers: as fallback/portable option

#### 6. Memory Footprint
Peak RSS during transcription of the 114-minute video.
```bash
/usr/bin/time -v <command> 2>&1 | grep "Maximum resident"
```

## Execution Plan

### Phase 1: Environment Setup
```bash
# Create isolated CrisperWhisper environment
python -m venv .venvs/crisperwhisper
source .venvs/crisperwhisper/bin/activate
pip install crisperwhisper[ct2]  # or [transformers] if no Linux x86_64

# Verify model download
python -c "from crisperwhisper import CrisperWhisperModel; m = CrisperWhisperModel('nyrahealth/CrisperWhisper_turbo')"
```

### Phase 2: Audio Extraction
For each test video, extract raw audio (if not already cached):
```bash
# Audio files should already exist from prior Whisper runs in:
# vb-workspace/intermediates/audio_<id>.wav (or .mp3/.m4a)
# If not, use yt-dlp to re-extract
yt-dlp -x --audio-format wav -o "benchmark/audio_%(id)s.%(ext)s" "https://youtube.com/watch?v=<id>"
```

### Phase 3: Run Engines
```bash
# faster-whisper (in main venv)
uv run python benchmark/run_faster_whisper.py --model large-v3-turbo --device cpu --compute-type int8

# CrisperWhisper (in isolated venv)
source .venvs/crisperwhisper/bin/activate
python benchmark/run_crisper_whisper.py --model nyrahealth/CrisperWhisper_turbo
```

### Phase 4: Compute Metrics
```bash
python benchmark/compute_metrics.py \
  --reference benchmark/youtube_captions/ \
  --faster-whisper benchmark/faster_whisper_output/ \
  --crisper-whisper benchmark/crisper_whisper_output/
```

### Phase 5: Report
Generate comparison table with all metrics, per video and aggregated.

## Expected Outcomes

| Metric | faster-whisper (expected) | CrisperWhisper (expected) |
|--------|--------------------------|---------------------------|
| WER | ~5-10% (large-v3-turbo) | Similar or slightly better |
| Word timestamps | Segment-level only (~5s granularity) | Word-level, ~30ms MAE |
| Verbatim fidelity | Cleaned (no fillers) | High (87.8% disfluency F1) |
| Hallucinations | Occasional on long audio | Reduced (3-tier detection) |
| Speed (CPU) | ~3x realtime (int8) | Similar or faster (speculative) |
| Memory | ~2-4 GB (large-v3-turbo) | Likely similar |

## Decision Criteria

Adopt CrisperWhisper if:
1. WER is equal or better on our test corpus
2. Word-level timestamps are accurate enough to replace frame correlation for timestamp refinement
3. Integration path is feasible (separate venv backend, ~1 day implementation)
4. Speed regression is <2x on CPU (acceptable if word timestamps are the payoff)
5. Hallucination reduction is measurable on long-form content

Keep faster-whisper if:
- CrisperWhisper WER is noticeably worse
- The ctranslate2 fork causes operational headaches
- Speed regression is >3x without clear quality gain

## Integration Path (if adopted)

Preferred: **Separate backend** model (like existing SSH remote backend):
1. Create `crisperwhisper_backend.py` alongside existing `whisper_backend.py`
2. Isolated virtualenv at `.venvs/crisperwhisper/`
3. Backend spawns subprocess in that venv, reads JSON output
4. Config flag: `[whisper] engine = "crisperwhisper"` vs `"faster-whisper"`
5. Extend transcript JSON schema to include word-level timestamps when available

Fallback: **Transformers backend** (no ctranslate2 conflict, but slower, no speculative decoding).
