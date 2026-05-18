# /intake

Argument: a single URL.

Workflow:
1. Run `video-buddy --json fetch <url>`.
2. Inspect the JSON output to determine whether the result is a YouTube video (`video_<id>.json`) or an article/paper (`article_<source_id>.json`).
3. For YouTube:
   - run `video-buddy --json transcribe <id>`
   - run `video-buddy --json frames <id>`
   - run `video-buddy --json correlate <id>`
   - run `video-buddy --json render <id>`
4. For article/paper:
   - run `video-buddy --json render <source-id>`
5. Read the draft note in `vb-workspace/intermediates/note_<id>.md`.
6. Read the companion prompts in `vb-workspace/intermediates/agent-prompts/`.
7. Fill these sections in the draft note:
   - Quick Summary
   - Key Concepts
   - Detailed Notes
   - Timestamps (YouTube only)
8. Run `video-buddy --json finalize <id>`.
9. Return the final note path.

Constraints:
- Use the CLI for mechanical steps.
- Ground prose in the fetched source material only.
- If OCR is unavailable, keep going if frame capture succeeded and note that OCR was skipped.
