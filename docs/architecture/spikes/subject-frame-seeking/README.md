# Ticket 25 throwaway evidence

Question: does dense seeking inside a known subject recover more complete readable revisions than the existing selector or an equal-output time grid?

Branch: `codex/spike-subject-frame-seeking`. No production integration. Both scored windows are from Fireship's Python in 100 Seconds, `x7X9w_GIm1s`. Source SHA-256 is in results.json; source bytes are not committed.

## Reproduce

Use this branch, install the repo environment, FFmpeg and Tesseract 5.4.0. The original locked yt-dlp 2026.3.17 returned HTTP403. Upgrade only the experimental environment to 2026.10.21 and use `uv run --no-sync` to prevent resync reverting that upgrade. No lockfile was changed.

```powershell
uv run --no-sync python -m video_buddy.frames.spike_seek x7X9w_GIm1s .scratch/seek-python-tune-current 59 63 --download-source
uv run --no-sync python -m video_buddy.frames.spike_seek .scratch/seek-retained-source/x7X9w_GIm1s.mp4 .scratch/seek-python-revisions 73 78
uv run --no-sync python docs/architecture/spikes/subject-frame-seeking/compare.py
```

Output folders must not exist. Capture reuses repo download mechanics and exposes a throwaway module CLI for FFmpeg every-frame decode. `copyts`, trim, passthrough and showinfo retain source presentation times. All 120/150 frames are represented in contact sheets, capture metadata and SHA-256 manifests. JPEG bytes may vary with FFmpeg build; compare presentation times and visual states as well as hashes.

`compare.py` uses the final corrected labels; the preserved `initial-label-results.json` contains the original scoring outputs with a mistaken tuning transition boundary. `finalize.py` intentionally reads that retained original run, rescores corrected labels without changing selections, captures four real time-grid stills via the existing core extractor, and records selected crop OCR. It requires contact sheets named `all-crops.jpg` and the tuning `boundaries.jpg` already present in the capture folders. Those inspection artifacts are committed here; they are not required to run the selector. `diagnose.py` performs the explicitly post-hoc global-veto bypass. It does not patch production code.

The initial timing pass used fixed manually seeded boxes, Tesseract PSM13 from ticket14's crop probe, six-frame total OCR-string support and a four-output cap. There was no threshold sweep. Support need not be contiguous; recurrent errors can therefore survive. Labels preserve the visible intermediate two-name/one-value line even though it would not execute as a valid unpacking example. Partial filename prefixes are excluded. Repeated same-text states are one revision; the brief disappearance at 62.129–62.229 seconds is not a new instruction.

The two windows are split by role, not unseen video/domain. One agent inspected all crops and corrected boundaries using full-size crops after the first score. No independent annotator or human task study. Exact OCR comparison retains case, punctuation and accents, and collapses whitespace only. “Readable state recovered” is a visual label, not a claim that OCR recovered its exact text.

Exploratory, unscored captures also covered Qr3VsZYQy4s 115–118/118–122 seconds (210 frames) and Python69–73 (120 frames). They were not added to scored recall or used to claim diagram/motion qualification.
