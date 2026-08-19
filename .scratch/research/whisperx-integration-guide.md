# WhisperX Integration Guide

## Summary

WhisperX is a Python library built on Faster-Whisper that adds forced phoneme alignment (sub-100ms word-level timestamps via wav2vec2) and pyannote-based speaker diarization to OpenAI's Whisper ASR. The Python API follows a 3-step pipeline: transcribe → align → diarize, with explicit model lifecycle management (load, use, delete) to control GPU memory between stages. Key integration requirements include a HuggingFace token for diarization (gated pyannote models), CUDA for practical performance, and careful batch_size tuning to avoid OOM errors.

## Details

### Installation

```bash
# Option 1: pip (production)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install whisperx

# Option 2: From GitHub (latest features)
pip install git+https://github.com/m-bain/whisperx.git

# Option 3: uv (recommended by upstream as of 2025+)
uvx git+https://github.com/m-bain/whisperX.git

# Dev install
git clone https://github.com/m-bain/whisperX.git
cd whisperX
uv sync --all-extras --dev
```

**Python version:** 3.10 recommended for maximum compatibility (3.11 works on macOS with Homebrew).

**System dependencies:** ffmpeg, rust (same as openai/whisper).

**VRAM:** 6 GB minimum, 8 GB+ comfortable. CPU diarization is impractical for anything beyond very short clips.

### Python API Usage Patterns

The canonical pattern from the official README:

```python
import whisperx
import gc
import torch

device = "cuda"
audio_file = "audio.mp3"
batch_size = 16  # reduce if low on GPU mem
compute_type = "float16"  # "int8" for low VRAM (may reduce accuracy)

# --- Step 1: Transcribe ---
model = whisperx.load_model("large-v2", device, compute_type=compute_type)
audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size)
# result["segments"] contains segment-level text + rough timestamps
# result["language"] contains detected language code

# Free transcription model before loading alignment model
del model
gc.collect()
torch.cuda.empty_cache()

# --- Step 2: Align (word-level timestamps) ---
model_a, metadata = whisperx.load_align_model(
    language_code=result["language"], device=device
)
result = whisperx.align(
    result["segments"], model_a, metadata, audio, device,
    return_char_alignments=False
)
# result["segments"][i]["words"] now has per-word start/end times

# Free alignment model
del model_a
gc.collect()
torch.cuda.empty_cache()

# --- Step 3: Diarize (speaker labels) ---
from whisperx.diarize import DiarizationPipeline

diarize_model = DiarizationPipeline(token=HF_TOKEN, device=device)
diarize_segments = diarize_model(audio, min_speakers=2, max_speakers=4)
result = whisperx.assign_word_speakers(diarize_segments, result)
# result["segments"][i]["speaker"] = "SPEAKER_00" etc.
# result["segments"][i]["words"][j]["speaker"] = "SPEAKER_00" etc.
```

**Key API points:**
- `whisperx.load_model(model_name, device, compute_type=..., download_root=...)` — model_name: "tiny", "base", "small", "medium", "large-v2", "large-v3"
- `whisperx.load_audio(path)` — returns numpy array (16kHz mono)
- `model.transcribe(audio, batch_size=N)` — VAD-segmented batched inference
- `whisperx.load_align_model(language_code=..., device=...)` — auto-selects wav2vec2 model
- `whisperx.align(segments, model, metadata, audio, device)` — returns aligned result
- `DiarizationPipeline(token=..., device=...)` — wraps pyannote
- `whisperx.assign_word_speakers(diarize_segments, aligned_result)` — merges speaker labels into transcript

**Optional: save model locally:**
```python
model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root="/path/to/models/")
```

### Output Format

The `result` dict after all three steps:

```json
{
  "segments": [
    {
      "start": 0.52,
      "end": 3.84,
      "text": "Welcome to the show, today we are talking about local AI.",
      "speaker": "SPEAKER_00",
      "words": [
        {"word": "Welcome", "start": 0.52, "end": 0.91, "speaker": "SPEAKER_00"},
        {"word": "to", "start": 0.94, "end": 1.06, "speaker": "SPEAKER_00"},
        {"word": "the", "start": 1.08, "end": 1.18, "speaker": "SPEAKER_00"}
      ]
    }
  ],
  "language": "en"
}
```

**Notes on output:**
- Words that don't contain characters in the alignment model's dictionary (e.g., "2014." or "£13.60") cannot be aligned and won't have timing.
- Speaker labels are `SPEAKER_00`, `SPEAKER_01`, etc. — mapping to real names is a post-processing step.
- The `diarize_segments` return is a separate structure used internally for speaker assignment.

### Diarization Setup

**Prerequisites (one-time, per HuggingFace account):**

1. Create a HuggingFace account at https://huggingface.co
2. Accept the license agreement at:
   - https://huggingface.co/pyannote/speaker-diarization-3.1 (or speaker-diarization-community-1)
   - https://huggingface.co/pyannote/segmentation-3.0
3. Create a Read token at https://huggingface.co/settings/tokens
   - Must have: "Read access to contents of all public gated repos you can access"
4. Pass the token:
   - Python: `DiarizationPipeline(token="hf_xxx", device=device)`
   - CLI: `--hf_token hf_xxx`
   - Environment: `export HF_TOKEN=hf_xxx`

**Speaker count hints (dramatically improve accuracy):**
```python
diarize_segments = diarize_model(audio, min_speakers=2, max_speakers=2)  # podcast
diarize_segments = diarize_model(audio, min_speakers=2, max_speakers=8)  # meeting
```

**Accuracy expectations:**
- 2-3 clean speakers: 90-95%
- 4-6 speakers: 80-88%
- Crowded meetings with crosstalk: 70-80%

### Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `'NoneType' object has no attribute 'to'` | HF token invalid or license not accepted | Accept licenses at pyannote HF pages; verify token has gated-repo read permission |
| `Could not download pyannote model` | Same as above | Same as above |
| CUDA OOM | batch_size too high or model too large for VRAM | Reduce `batch_size` (try 4-8); use `compute_type="int8"`; use smaller model |
| `weights_only` / pickle errors | PyTorch 2.6+ changed `torch.load()` defaults | Monkey-patch: `torch.load = functools.wraps(torch.load)(lambda *a, **kw: original_load(*a, **{**kw, 'weights_only': False}))` |
| `use_auth_token` deprecation warning | `huggingface_hub` renamed param to `token` | Use `token=` instead of `use_auth_token=`; or monkey-patch `hf_hub_download` |
| Alignment model not found for language | No wav2vec2 model registered for that language | Transcription works but timestamps fall back to interpolated |
| `ModuleNotFoundError: No module named 'requests'` | Missing transitive dependency | `pip install requests` |
| WhisperX version mismatch with faster-whisper | Unpinned dependencies | Pin both in a venv; use exact version constraints |
| torchaudio backend deprecation warning | Future API change | Safe to ignore |
| `Model was trained with pyannote.audio 0.0.1` | Version mismatch in model metadata | Safe to ignore; backward compatible |

### Memory Management for Long Audio

WhisperX loads **three separate models** sequentially. On GPUs with limited VRAM (8-12 GB), you MUST unload each model before loading the next:

```python
# After transcription, before alignment:
del model
gc.collect()
torch.cuda.empty_cache()

# After alignment, before diarization:
del model_a
gc.collect()
torch.cuda.empty_cache()
```

**Critical: all three steps are required** (`del` + `gc.collect()` + `torch.cuda.empty_cache()`). `torch.cuda.empty_cache()` alone does NOT free memory held by Python references. The `del` removes the Python reference, `gc.collect()` runs the garbage collector, and `empty_cache()` returns freed CUDA memory to the allocator.

**Known issue:** Faster-whisper (the backend) has a reported memory leak where memory is not fully released even after `del` + cache clear. For long-running services, consider process-level isolation (spawn a subprocess per transcription) or periodic restarts.

**batch_size tuning:**
- RTX 4090 (24 GB): batch_size=32
- RTX 4070/3060 (8-12 GB): batch_size=8-16
- T4 (16 GB): batch_size=16-24
- If OOM, halve the batch_size

**compute_type options:**
- `float16` — best quality, highest VRAM
- `int8_float16` — reduced VRAM, minor quality loss
- `int8` — lowest VRAM, some quality degradation
- `float32` — CPU only

### Batch Processing (Multiple Files)

WhisperX doesn't have built-in multi-file batching. Pattern for processing archives:

```python
import whisperx
import gc
import torch

device = "cuda"
HF_TOKEN = "hf_xxx"
files = ["audio1.mp3", "audio2.mp3", ...]

# Load models once, process multiple files
model = whisperx.load_model("large-v3", device, compute_type="float16")

for audio_file in files:
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=16)
    # ... process result ...

# OR: for memory-constrained environments, reload per-file:
for audio_file in files:
    model = whisperx.load_model("large-v3", device, compute_type="float16")
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=16)
    
    del model; gc.collect(); torch.cuda.empty_cache()
    
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device)
    
    del model_a; gc.collect(); torch.cuda.empty_cache()
    
    diarize_model = DiarizationPipeline(token=HF_TOKEN, device=device)
    diarize_segments = diarize_model(audio)
    result = whisperx.assign_word_speakers(diarize_segments, result)
    
    del diarize_model; gc.collect(); torch.cuda.empty_cache()
    
    # Save result...
```

**For massive archives (1000+ hours):** Use process-level parallelism (multiprocessing with one GPU per worker) or queue-based architecture. The VAD batching handles long single files well, but multi-file parallelism must be managed externally.

### Important Behavioral Notes

- `--condition_on_prev_text` is `False` by default in WhisperX (reduces hallucination vs. vanilla Whisper)
- VAD preprocessing is always on (reduces hallucination, enables batching)
- Transcription runs `--without_timestamps True` internally for batched inference — this can cause minor differences vs. vanilla Whisper output
- Overlapping speech is not handled well by either Whisper or WhisperX
- Language-specific alignment requires a matching wav2vec2 model (auto-selected for major languages; falls back to interpolation otherwise)
- The `progress_callback` parameter was recently added to `transcribe` and `align` (as of mid-2025)

### CLI Quick Reference

```bash
# Basic transcription
whisperx audio.mp3 --model large-v3

# Full pipeline with diarization
whisperx audio.mp3 \
    --model large-v3 \
    --diarize \
    --hf_token $HF_TOKEN \
    --min_speakers 2 --max_speakers 4 \
    --language en \
    --batch_size 16 \
    --compute_type float16 \
    --output_format all \
    --highlight_words True

# CPU mode (Mac/no GPU)
whisperx audio.mp3 --compute_type int8 --device cpu
```

## Sources

1. [WhisperX GitHub (m-bain/whisperX)](https://github.com/m-bain/whisperX) — Official repo, README with canonical Python usage [L4:verified]
2. [LocalAIMaster WhisperX Guide (2026)](https://localaimaster.com/blog/whisperx-guide) — Comprehensive tutorial with benchmarks, output format examples, troubleshooting [L5:reported]
3. [WhisperX Installation Guide (Windows, Jan 2026)](https://gist.github.com/Foadsf/6136e054f4dc813d8e39db7a123ca2f0) — Detailed Windows setup with PyTorch 2.6+ compatibility patches [L6:reported]
4. [WhisperX Paper (INTERSPEECH 2023)](https://arxiv.org/abs/2303.00747) — Academic paper with architecture details and benchmarks [L4:verified]
5. [pyannote/segmentation-3.0 on HuggingFace](https://huggingface.co/pyannote/segmentation-3.0) — Required gated model for diarization [L4:verified]
6. [CUDA OOM Issue #388](https://github.com/m-bain/whisperX/issues/388) — Memory management discussion, gc.collect patterns [L6:reported]
7. [Faster-whisper memory leak Issue #660](https://github.com/SYSTRAN/faster-whisper/issues/660) — Known backend memory retention issue [L6:reported]
8. [Arch Linux Forum: WhisperX CUDA usage](https://bbs.archlinux.org/viewtopic.php?id=297699) — Real-world gc.collect pattern example [L6:reported]

## Open Questions

1. **video-buddy integration path:** Should WhisperX replace the current Whisper backend entirely, or be an optional "enhanced" path activated when word-level timestamps are needed?
2. **Remote execution:** The existing SSH backend model works for vanilla Whisper — does WhisperX's multi-model pipeline (transcribe→align→diarize) work well over SSH, or does the sequential model loading make it impractical without a persistent daemon?
3. **Model caching across runs:** First run downloads ~3-5 GB of models to `~/.cache/huggingface/` and `~/.cache/torch/`. For the remote backend, are these cached on the remote machine, or re-downloaded each invocation?
4. **speaker-diarization-community-1 vs speaker-diarization-3.1:** The upstream README now references `speaker-diarization-community-1` (CC-BY-4.0) while older guides reference `speaker-diarization-3.1`. Which should video-buddy target? The community model is permissively licensed.
5. **Progress callback:** The recently added `progress_callback` parameter — what's its signature? Could be useful for video-buddy's JSON progress reporting.
6. **Alignment model availability:** For non-English content, which languages actually have good alignment models? The DEFAULT_ALIGN_MODELS_HF list in alignment.py is the source of truth.
7. **faster-whisper memory leak:** For a CLI tool that processes one file and exits, this is fine. But if video-buddy ever becomes a long-running service, the backend memory leak needs a mitigation strategy (process isolation).
