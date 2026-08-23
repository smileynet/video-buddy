"""Run CrisperWhisper on test audio and capture output + timing."""
import json
import time
import sys
from pathlib import Path

audio_path = sys.argv[1]
output_path = sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else "verbatim"

from crisperwhisper import CrisperWhisperModel

print(f"Loading CrisperWhisper model: turbo (CPU)...", file=sys.stderr)
start_load = time.time()
model = CrisperWhisperModel("turbo", device="cpu", compute_type="int8")
load_time = time.time() - start_load
print(f"Model loaded in {load_time:.1f}s", file=sys.stderr)

print(f"Transcribing {audio_path} (mode={mode}, word_timestamps=True)...", file=sys.stderr)
start_transcribe = time.time()
result = model.transcribe(audio_path, mode=mode, word_timestamps=True)
transcribe_time = time.time() - start_transcribe
total_time = time.time() - start_load

# Extract word-level data
words = []
if result.words:
    for w in result.words:
        words.append({
            "start": w.start,
            "end": w.end,
            "text": w.word,
        })

# Build segments from the full text (split on sentence boundaries for comparison)
# CrisperWhisper returns .text as full transcript and .words for word-level
segments = []
if words:
    # Group words into ~5s segments for comparison with faster-whisper
    current_seg = {"start": words[0]["start"], "words": [], "texts": []}
    for w in words:
        current_seg["words"].append(w)
        current_seg["texts"].append(w["text"])
        if w["end"] - current_seg["start"] > 5.0:
            segments.append({
                "start": current_seg["start"],
                "end": w["end"],
                "duration": round(w["end"] - current_seg["start"], 3),
                "text": " ".join(current_seg["texts"]).strip(),
                "word_count": len(current_seg["words"]),
            })
            if len(words) > words.index(w) + 1:
                next_w = words[words.index(w) + 1]
                current_seg = {"start": next_w["start"], "words": [], "texts": []}
    # Flush remaining
    if current_seg["texts"]:
        segments.append({
            "start": current_seg["start"],
            "end": current_seg["words"][-1]["end"],
            "duration": round(current_seg["words"][-1]["end"] - current_seg["start"], 3),
            "text": " ".join(current_seg["texts"]).strip(),
            "word_count": len(current_seg["words"]),
        })

output = {
    "engine": "crisperwhisper",
    "model": "turbo",
    "mode": mode,
    "device": "cpu",
    "audio_duration": result.duration,
    "load_time_s": round(load_time, 2),
    "transcribe_time_s": round(transcribe_time, 2),
    "total_time_s": round(total_time, 2),
    "rtf": round(result.duration / transcribe_time, 2) if transcribe_time > 0 else 0,
    "processing_time_reported": result.processing_time,
    "segment_count": len(segments),
    "word_count": len(words),
    "full_text_length": len(result.text),
    "mode_reported": result.mode,
    "segments": segments,
    "words_sample": words[:50],  # First 50 words for inspection
}

Path(output_path).write_text(json.dumps(output, indent=2))
print(f"Done: {len(segments)} segments, {len(words)} words in {transcribe_time:.1f}s (RTF: {result.duration/transcribe_time:.2f}x)", file=sys.stderr)
