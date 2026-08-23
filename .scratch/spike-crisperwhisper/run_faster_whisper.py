"""Run faster-whisper on test audio and capture output + timing."""
import json
import time
import sys
from pathlib import Path

audio_path = sys.argv[1]
output_path = sys.argv[2]

from faster_whisper import WhisperModel

print(f"Loading model: base (CPU, int8)...", file=sys.stderr)
start_load = time.time()
model = WhisperModel("base", device="cpu", compute_type="int8")
load_time = time.time() - start_load
print(f"Model loaded in {load_time:.1f}s", file=sys.stderr)

print(f"Transcribing {audio_path}...", file=sys.stderr)
start_transcribe = time.time()
segments, info = model.transcribe(audio_path, vad_filter=True)

results = []
for seg in segments:
    results.append({
        "start": seg.start,
        "end": seg.end,
        "duration": round(seg.end - seg.start, 3),
        "text": seg.text.strip(),
    })

transcribe_time = time.time() - start_transcribe
total_time = time.time() - start_load

output = {
    "engine": "faster-whisper",
    "model": "base",
    "device": "cpu",
    "compute_type": "int8",
    "audio_duration": info.duration,
    "load_time_s": round(load_time, 2),
    "transcribe_time_s": round(transcribe_time, 2),
    "total_time_s": round(total_time, 2),
    "rtf": round(info.duration / transcribe_time, 2),
    "segment_count": len(results),
    "segments": results,
}

Path(output_path).write_text(json.dumps(output, indent=2))
print(f"Done: {len(results)} segments in {transcribe_time:.1f}s (RTF: {info.duration/transcribe_time:.2f}x)", file=sys.stderr)
