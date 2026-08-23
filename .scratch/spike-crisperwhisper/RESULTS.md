# Spike: CrisperWhisper vs faster-whisper

**Date:** 2026-08-23  
**Audio:** `Qr3VsZYQy4s` — "How I released a game that has no assets" (33:10, Zanzlanz)  
**Hardware:** CPU only (no NVIDIA GPU available on this machine)

## Results Summary

| Metric | faster-whisper | CrisperWhisper | Winner |
|--------|---------------|----------------|--------|
| **Model** | base (74M) | turbo (809M) | — |
| **Speed** | 5.6 min (5.93x RT) | 42 min (0.79x RT) | faster-whisper (7.5x faster) |
| **Hallucinated repeats** | 17 segments | 0 segments | **CrisperWhisper** |
| **Word timestamps** | No (segment-level) | Yes (5113 words, per-word) | **CrisperWhisper** |
| **Verbatim fidelity** | Strips fillers | Captures [breath], stutters (s- s-) | **CrisperWhisper** |
| **Proper noun accuracy** | "Zanzlans" | "Zanz Land" | Tie (both wrong) |
| **Technical terms** | 88× "sine" | 83× "sine" | Tie |
| **Text quality** | "It's our genemy" | "archenemy" | **CrisperWhisper** |

## Key Observations

### 1. Hallucination Resistance (CrisperWhisper's killer win)

faster-whisper produced **17 exact-repeat segments** — short segments like "Okay." and "Whoa."
repeated multiple times in sequence. This is the classic Whisper hallucination on silence/background
noise. CrisperWhisper produced **zero** exact repeats, confirming its 3-tier hallucination
mitigation works.

For our digest workflow, hallucinated segments are actively harmful — they appear in the transcript
the agent uses to write breakdowns, potentially generating false quotes.

### 2. Word-Level Timestamps (unique to CrisperWhisper)

CrisperWhisper produced 5113 word timestamps with sub-second precision:
```
[0.34-0.42] "This"
[0.86-0.98] "is"
[0.98-1.08] "a"
[1.22-1.52] "sine"
```

faster-whisper only provides segment-level timestamps (~3-8s chunks). For timestamped quotes
in our notes, CrisperWhisper could enable clicking a word and jumping to that exact moment.

### 3. Verbatim Fidelity

CrisperWhisper captured:
- `[breath]` annotations (paralinguistic events)
- `s- s- signing off` (false start/stutter preserved)
- These were absent in faster-whisper output

This video had few natural disfluencies (scripted content), so the verbatim advantage was
minimal here. Would be more pronounced on podcast/interview content with lots of "uh/um."

### 4. Speed (faster-whisper's clear win)

CrisperWhisper is **7.5x slower** on CPU. However, this comparison is not apples-to-apples:
- faster-whisper used the `base` model (74M parameters)
- CrisperWhisper used the `turbo` model (809M parameters) — 11x larger

A fairer comparison would be faster-whisper with `large-v3-turbo` vs CrisperWhisper `turbo`
(same model size). On CPU, large-v3-turbo would likely also be ~40 min for 33 min audio.

**On GPU**, CrisperWhisper's speculative decoding would likely bring it to near-realtime.
The speed disadvantage is primarily a CPU story.

### 5. Transcript Quality

Both engines produced readable, accurate transcripts. Notable differences:
- CrisperWhisper got "archenemy" right where faster-whisper hallucinated "genemy"
- Both got the channel name wrong ("Zanzlans" vs "Zanz Land" — actual: "Zanzlanz")
- Text length difference (~4%: 27689 vs 26533 chars) likely from CrisperWhisper's
  verbatim annotations

## Limitations of This Spike

1. **Not apples-to-apples model comparison** — base (74M) vs turbo (809M)
2. **No YouTube caption reference** — YouTube rate-limiting prevented downloading captions for WER
3. **CPU only** — CrisperWhisper's speed advantage (speculative decoding) requires GPU
4. **Single video** — one data point, scripted content (not the hardest case for either engine)
5. **No long-form stress test** — the 99-min audio wasn't tested (would take ~80+ min on CPU)

## Recommendation

### For video-buddy's use case:

**Use faster-whisper (base/turbo) as default** for batch processing where speed matters and
YouTube captions are unavailable. Accept the occasional hallucination (17 repeats in 33 min is
manageable — downstream LLM agent can filter these).

**Use CrisperWhisper as premium engine** for:
1. **Long-form content (60+ min)** — hallucination resistance becomes critical
2. **Interview/podcast content** — verbatim mode preserves conversational texture
3. **Timestamp-sensitive work** — word-level timestamps enable precise quote attribution
4. **High-value single videos** — when you want the best possible transcript for a key video

### Integration priority:

The speed gap makes CrisperWhisper impractical for batch processing of 107 videos on CPU.
But for the `ingest` workflow (single video, higher quality expectations), it's a clear
quality upgrade at acceptable cost (42 min wait for a 33-min video).

**Revised ticket 03 scope:** Integration should focus on the single-video `ingest` path,
not the batch `digest` path. Make it opt-in via `--whisper-engine crisperwhisper` for when
the user wants maximum quality on one video.

### What would change the calculus:

- **GPU availability** — CrisperWhisper on GPU would likely be 5-10x faster
- **Model download caching** — first-run model download adds one-time setup cost
- **The 99-min test** — if hallucination resistance scales to long form as expected, that's
  the real differentiator for our "60+ min podcast" use case
