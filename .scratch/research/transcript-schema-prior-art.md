# Transcript/Subtitle JSON Schema Prior Art

## Summary

There is no single industry-wide ASR transcript JSON schema standard, but a clear consensus exists around common fields: segments with start/end timestamps, word-level timing with confidence scores, and speaker labels. The STJ (Standard Transcription JSON) project is an explicit attempt at a superset standard (v0.6.1, MIT-licensed), while commercial APIs (Deepgram, AssemblyAI) and open-source tools (Whisper, WhisperX) each define their own structurally similar but incompatible formats.

## Details

### Whisper Native Format (OpenAI)

Output from `whisper --output_format json` with `word_timestamps=True`:

```json
{
  "text": "Full transcript text",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 5.5,
      "text": " Hello, how are you?",
      "words": [
        {
          "word": " Hello,",
          "start": 0.0,
          "end": 0.5,
          "probability": 0.95
        }
      ]
    }
  ],
  "language": "en"
}
```

Key fields:
- `segments[].id` — sequential integer
- `segments[].start` / `segments[].end` — seconds (float)
- `segments[].text` — segment text (leading space preserved)
- `segments[].words[].word` — word text with attached punctuation
- `segments[].words[].start` / `.end` — seconds (float)
- `segments[].words[].probability` — 0.0–1.0 token probability
- Top-level `language` — detected language code

No speaker diarization in native Whisper. Timestamps derived from cross-attention + DTW (word-level accuracy ~hundreds of ms drift without alignment).

### WhisperX Output Format

WhisperX adds forced phoneme alignment (wav2vec2) and pyannote diarization:

```json
{
  "segments": [
    {
      "start": 0.52,
      "end": 3.84,
      "text": "Welcome to the show.",
      "speaker": "SPEAKER_00",
      "words": [
        {
          "word": "Welcome",
          "start": 0.52,
          "end": 0.91,
          "speaker": "SPEAKER_00"
        }
      ]
    }
  ],
  "language": "en"
}
```

Key differences from base Whisper:
- `segments[].speaker` — speaker label (SPEAKER_00, SPEAKER_01, etc.)
- `words[].speaker` — per-word speaker assignment
- No `probability`/`confidence` at word level in default output
- Word timestamps are sub-100ms accurate (forced alignment)
- No segment `id` field

### AssemblyAI Format

Timestamps in **milliseconds** (not seconds). Speaker labels are letters (A, B, C...).

```json
{
  "id": "transcript-id",
  "status": "completed",
  "text": "Full transcript...",
  "words": [
    {
      "text": "Smoke",
      "speaker": "A",
      "start": 250,
      "end": 650,
      "confidence": 0.99
    }
  ],
  "utterances": [
    {
      "speaker": "A",
      "text": "Smoke from hundreds of wildfires...",
      "start": 250,
      "end": 28840,
      "confidence": 0.97,
      "words": [
        {
          "text": "Smoke",
          "speaker": "A",
          "start": 250,
          "end": 650,
          "confidence": 0.99
        }
      ]
    }
  ]
}
```

Key fields:
- Top-level `words[]` — flat word array with timing + speaker + confidence
- `utterances[]` — speaker-turn segments (only when `speaker_labels=true`)
- Timestamps in **milliseconds** (integer)
- `confidence` — 0.0–1.0 per word and per utterance
- `speaker` — alphabetic label (A, B, C...)

### Deepgram Format

Nested channel/alternative structure. Timestamps in seconds (float).

```json
{
  "metadata": { ... },
  "results": {
    "channels": [
      {
        "alternatives": [
          {
            "transcript": "four score and seven years ago...",
            "confidence": 0.88,
            "words": [
              {
                "word": "four",
                "start": 0.41916,
                "end": 0.85828,
                "confidence": 0.57894,
                "speaker": 0,
                "punctuated_word": "Four"
              }
            ]
          }
        ]
      }
    ],
    "utterances": [
      {
        "start": 0.41916,
        "end": 5.43012,
        "confidence": 0.88173,
        "channel": 0,
        "transcript": "four score and seven years ago...",
        "words": [...],
        "speaker": 0,
        "id": "uuid"
      }
    ]
  }
}
```

Key fields:
- `channels[].alternatives[]` — n-best hypothesis structure
- `words[].word` / `.start` / `.end` / `.confidence` / `.speaker`
- `words[].punctuated_word` — formatted version with punctuation
- `utterances[]` — semantic speech units (when `utterances=true`)
- `speaker` — integer (0, 1, 2...)
- Timestamps in seconds (float, high precision)
- `paragraphs` feature structures text into paragraph/sentence hierarchy

### WebVTT vs SRT Comparison

| Feature | SRT | WebVTT |
|---------|-----|--------|
| File extension | .srt | .vtt |
| Header | None | `WEBVTT` required |
| Timestamp separator | `,` (ms) | `.` (ms) |
| Timestamp format | `HH:MM:SS,mmm` | `HH:MM:SS.mmm` |
| Styling | None (limited italic via HTML) | CSS inline styling, `::cue` |
| Positioning | None | `position`, `line`, `align` |
| Speaker tags | Convention: `[Name]` prefix | `<v Name>text</v>` |
| Browser native | No (`<track>` won't read) | Yes (HTML5 `<track>`) |
| Cue identifiers | Sequential numbers | Optional arbitrary strings |
| Metadata/chapters | No | Yes (NOTE, chapters) |

Both are plain-text, line-oriented, timestamped subtitle formats. SRT is more universally accepted by video editors and platforms; VTT is the web standard.

### Common Fields Across All Schemas

| Field | Whisper | WhisperX | AssemblyAI | Deepgram | STJ |
|-------|---------|----------|------------|----------|-----|
| segment start | ✓ (sec) | ✓ (sec) | ✓ (ms) | ✓ (sec) | ✓ (sec) |
| segment end | ✓ (sec) | ✓ (sec) | ✓ (ms) | ✓ (sec) | ✓ (sec) |
| segment text | ✓ | ✓ | ✓ | ✓ | ✓ |
| word text | ✓ | ✓ | ✓ | ✓ | ✓ |
| word start | ✓ (sec) | ✓ (sec) | ✓ (ms) | ✓ (sec) | ✓ (sec) |
| word end | ✓ (sec) | ✓ (sec) | ✓ (ms) | ✓ (sec) | ✓ (sec) |
| word confidence | ✓ (probability) | ✗ | ✓ | ✓ | ✓ (optional) |
| segment confidence | ✗ | ✗ | ✓ | ✓ | ✓ (optional) |
| speaker label | ✗ | ✓ | ✓ | ✓ | ✓ (optional) |
| language | ✓ (top-level) | ✓ (top-level) | ✓ (top-level) | ✓ | ✓ (per-segment) |

**Universal minimum:** `{text, start, end}` at segment level; `{word/text, start, end}` at word level.

### Speaker Diarization Representation

| Provider | Speaker field | Label format | Granularity |
|----------|--------------|--------------|-------------|
| WhisperX | `speaker` | `SPEAKER_00`, `SPEAKER_01` | per-segment + per-word |
| AssemblyAI | `speaker` | `A`, `B`, `C` | per-utterance + per-word |
| Deepgram | `speaker` | `0`, `1`, `2` (integer) | per-utterance + per-word |
| STJ | `speaker_id` | arbitrary string (ref to speakers list) | per-segment |

Common pattern: speaker label at both segment/utterance level AND word level, allowing mid-segment speaker changes to be represented.

### STJ (Standard Transcription JSON) — Proposed Standard

Version 0.6.1 (2025-11-15). MIT licensed. Aims to be a superset of SRT, WebVTT, TTML, SSA/ASS.

Key design decisions:
- Root structure: `{ "stj": { "version": "...", "metadata": {...}, "transcript": {...} } }`
- `transcript.speakers[]` — speaker registry with id + optional name
- `transcript.segments[]` — ordered by start time, no overlap allowed
- `transcript.styles[]` — format-agnostic styling definitions
- `word_timing_mode` — explicit: "complete", "partial", or "none"
- Per-segment `language` for multilingual transcripts
- `confidence` allows `null` (scoring attempted but failed) vs omitted (not attempted)
- Extensions mechanism for vendor-specific data
- Times in seconds with max 3 decimal places (millisecond precision)
- File extension: `.stjson` / `.stj`
- MIME type: `application/vnd.stj+json`

### NVIDIA NeMo Manifest Format

Used for training data, not output:
```json
{"audio_filepath": "/path/to/audio.wav", "text": "the transcription", "duration": 23.147}
```
One JSON object per line. Minimal fields for batch processing.

### Unified Audio Schema (UAS) — 2026 Research

Academic proposal (ACL Findings 2026) organizing audio into:
- Transcription
- Paralinguistics (emotion, tone)
- Non-linguistic Events (music, applause)

Not yet adopted in production tools.

## Sources

- Whisper word timestamps docs: https://openai-whisper.mintlify.app/guides/word-timestamps
- WhisperX guide (2026): https://localaimaster.com/blog/whisperx-guide
- WhisperX GitHub: https://github.com/m-bain/whisperX
- STJ specification v0.6.1: https://github.com/yaniv-golan/STJ/blob/main/spec/latest/stj-specification.md
- AssemblyAI speaker diarization: https://www.assemblyai.com/docs/speech-to-text/speaker-diarization/
- Deepgram utterances: https://developers.deepgram.com/docs/utterances
- Deepgram paragraphs: https://developers.deepgram.com/docs/paragraphs
- Subtitle format comparison: https://brasstranscripts.com/blog/transcription-file-formats-decision-guide-2026
- VTT vs SRT (dev-focused): https://liveapi.com/blog/vtt-vs-srt/
- UAS paper: https://arxiv.org/abs/2604.12506
- NVIDIA NeMo datasets: https://github.com/NVIDIA/NeMo/blob/main/docs/source/asr/datasets.rst

## Open Questions

1. **Time unit divergence:** AssemblyAI uses milliseconds (int), everyone else uses seconds (float). Is there a reason to prefer one over the other for a unified format?
2. **STJ adoption:** The STJ format is comprehensive but has near-zero stars/forks on GitHub. Is anyone actually using it in production?
3. **Confidence semantics:** Whisper uses "probability" (token avg), others use "confidence" — are these comparable? What's the threshold for "low confidence" across systems?
4. **Speaker label persistence:** How should speaker identity be tracked across multiple files/sessions (same speaker in different recordings)?
5. **Streaming vs final:** Deepgram's streaming format (interim results, `is_final`) differs from batch — should a unified schema account for both modes?
6. **Paragraph/chapter segmentation:** Deepgram and AssemblyAI offer paragraph-level grouping above segments. Should this be a standard tier?
7. **Non-speech events:** Only STJ and UAS explicitly handle `[Music]`, `[Applause]` etc. Most formats leave these as text-in-segment with no semantic markup.
