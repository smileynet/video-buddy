# Transcript JSON schema

Transcript files (`transcript_<id>.json`) store the textual output of speech recognition. Two schema versions coexist; consumers auto-detect by checking the top-level JSON type.

## v1 (flat array)

Produced by: `faster-whisper` (default engine), YouTube caption passthrough.

```json
[
  {"start": 0.0, "duration": 3.5, "text": "Hello and welcome to the video"},
  {"start": 3.5, "duration": 4.2, "text": "Today we're going to talk about..."}
]
```

Fields (all required):

| Field | Type | Description |
|-------|------|-------------|
| `start` | float | Segment start time in seconds |
| `duration` | float | Segment duration in seconds |
| `text` | string | Transcribed text for this segment |

## v2 (object with metadata)

Produced by: `whisperx`, `crisperwhisper`.

```json
{
  "schema_version": "2.0",
  "metadata": {
    "engine": "crisperwhisper",
    "model": "turbo",
    "mode": "verbatim",
    "processing_time": 24.9,
    "audio_duration": 1990.0
  },
  "segments": [
    {
      "start": 0.34,
      "duration": 5.36,
      "text": "This is a sine wave and when you combine a bunch of them",
      "intended_text": "This is a sine wave, and when you combine a bunch of them",
      "words": [
        {"start": 0.34, "end": 0.42, "text": "This"},
        {"start": 0.86, "end": 0.98, "text": "is"},
        {"start": 0.98, "end": 1.08, "text": "a"},
        {"start": 1.22, "end": 1.52, "text": "sine"}
      ],
      "speaker": "SPEAKER_00"
    }
  ],
  "speakers": [
    {"id": "SPEAKER_00", "label": null}
  ]
}
```

### Top-level fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | ✓ | Always `"2.0"` |
| `metadata` | object | ✓ | Engine and processing info |
| `segments` | array | ✓ | Transcript segments (same shape as v1 entries) |
| `speakers` | array | | Speaker list (when diarization is available) |

### metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `engine` | string | ✓ | `"faster-whisper"`, `"whisperx"`, `"crisperwhisper"`, or `"captions"` |
| `model` | string | | Model name used (e.g. `"turbo"`, `"large-v3-turbo"`) |
| `mode` | string | | CrisperWhisper mode: `"verbatim"` or `"intended"` |
| `processing_time` | float | | Wall-clock seconds for transcription |
| `audio_duration` | float | | Audio length in seconds |

### segments[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `start` | float | ✓ | Segment start time in seconds |
| `duration` | float | ✓ | Segment duration in seconds |
| `text` | string | ✓ | Transcribed text (verbatim when engine supports it) |
| `intended_text` | string | | Cleaned text without disfluencies (CrisperWhisper dual mode) |
| `words` | array | | Word-level timestamps |
| `speaker` | string | | Speaker label (e.g. `"SPEAKER_00"`) |

### segments[].words[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `start` | float | ✓ | Word start time in seconds |
| `end` | float | ✓ | Word end time in seconds |
| `text` | string | ✓ | The word |
| `confidence` | float | | 0.0–1.0 recognition confidence |
| `is_disfluency` | bool | | Whether this word is a filler/stutter |

### speakers[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✓ | Speaker identifier (e.g. `"SPEAKER_00"`) |
| `label` | string | | Human-assigned name (null if unknown) |

## Detection and backward compatibility

`read_transcript(path)` normalizes both formats to a `list[dict]` of segments:

```python
data = json.loads(path.read_text())
if isinstance(data, list):    # v1: use as-is
    return data
if isinstance(data, dict):    # v2: extract segments
    return data.get("segments", [])
```

All downstream consumers (render, correlate, agent prompts) receive the normalized list. They access fields via `.get()` and tolerate extra keys, so v2 segments with `words`, `intended_text`, or `speaker` fields pass through without issue.

## Migration

- Existing v1 files do not need reprocessing.
- v1 is valid indefinitely — no deprecation planned.
- New engines produce v2 automatically.
- To upgrade a v1 file: re-transcribe with `--whisper-engine whisperx` or `--whisper-engine crisperwhisper`.
