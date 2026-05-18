# 0010 — Whisper in base install; GPU OCR remains optional

**Context.** `video-buddy init` pre-installs models by default. That makes install shape matter: if the package is missing the libraries needed to use those models, the default workflow breaks or becomes confusing. The question was whether `faster-whisper` and `easyocr` should both remain optional extras, or whether one belongs in the base dependency set.

Three alternatives existed:
1. **Both optional.** Users add `--extra whisper --extra gpu-ocr` for the full local path.
2. **Whisper core, GPU OCR optional.** Transcription works everywhere out of the box; local GPU OCR is opt-in.
3. **Both core.** One install path includes every local heavy dependency.

**Decision.** Option 2. `faster-whisper` moves into the base dependency set. `easyocr` stays behind `[gpu-ocr]`.

**Why.**
- Transcription is a core capability, not an acceleration tier. A clone that cannot transcribe locally by default is missing essential functionality.
- GPU OCR is genuinely optional because the system already has two fallback paths: remote EasyOCR on an SSH backend and local Tesseract.
- The optionality boundary now matches user-visible behavior: omitting `[gpu-ocr]` degrades OCR speed/quality, but does not remove a whole pipeline stage.
- Making both core would force every install to pay the EasyOCR dependency cost even on machines that will never run local OCR.

**Implications.**
- `pyproject.toml` lists `faster-whisper` in base `dependencies`.
- Install docs lead with `uv sync --extra gpu-ocr`, not `--extra whisper`.
- `init` may assume Whisper is importable; missing Whisper is an environment breakage, not an expected optional path.
- If `[gpu-ocr]` is absent, docs and runtime messaging must say what changes: OCR falls back to remote EasyOCR (if configured) or local Tesseract, with lower speed and usually lower quality on code-heavy frames.
