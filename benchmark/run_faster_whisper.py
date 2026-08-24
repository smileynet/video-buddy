"""Run faster-whisper on benchmark audio files."""
import json
import time
import sys
from pathlib import Path

from faster_whisper import WhisperModel

AUDIO_DIR = Path("benchmark/audio")
OUTPUT_DIR = Path("benchmark/output/faster-whisper")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

model_name = "base"
device = "cpu"
compute_type = "int8"

print(f"Loading model: {model_name} ({device}, {compute_type})...", file=sys.stderr)
model = WhisperModel(model_name, device=device, compute_type=compute_type)

results_summary = []

for audio_file in sorted(AUDIO_DIR.glob("*.wav")):
    vid_id = audio_file.stem
    print(f"\nTranscribing {vid_id} ({audio_file.stat().st_size / 1024 / 1024:.0f}MB)...", file=sys.stderr)
    
    start = time.time()
    segments, info = model.transcribe(str(audio_file), vad_filter=True)
    
    captions = []
    for seg in segments:
        text = seg.text.strip()
        if text:
            captions.append({"start": seg.start, "end": seg.end, "duration": round(seg.end - seg.start, 3), "text": text})
    
    elapsed = time.time() - start
    
    # Check for hallucination (repeated segments)
    repeats = sum(1 for i in range(1, len(captions)) if captions[i]["text"] == captions[i-1]["text"])
    
    output = {
        "engine": "faster-whisper",
        "model": model_name,
        "device": device,
        "video_id": vid_id,
        "audio_duration": info.duration,
        "transcribe_time": round(elapsed, 2),
        "rtf": round(info.duration / elapsed, 2),
        "segment_count": len(captions),
        "hallucination_repeats": repeats,
        "full_text": " ".join(c["text"] for c in captions),
        "segments": captions,
    }
    
    (OUTPUT_DIR / f"{vid_id}.json").write_text(json.dumps(output, indent=2))
    
    summary = f"  {vid_id}: {elapsed:.1f}s ({info.duration/elapsed:.1f}x RT), {len(captions)} segs, {repeats} repeats"
    print(summary, file=sys.stderr)
    results_summary.append({"video_id": vid_id, "time": elapsed, "rtf": info.duration/elapsed, "segments": len(captions), "repeats": repeats})

print("\n=== SUMMARY ===", file=sys.stderr)
for r in results_summary:
    print(f"  {r['video_id']}: {r['time']:.0f}s, {r['rtf']:.1f}x RT, {r['repeats']} hallucinations", file=sys.stderr)
