# Agent Integration Contract

Use `video-buddy` as a mechanical CLI.

Rules:
- Run CLI verbs; do not reimplement fetch/transcribe/frames/correlate/render/finalize in prompts.
- Prefer `--json` for machine parsing.
- Treat draft notes in `intermediates/note_<id>.md` as the writable surface for prose.
- Read companion prompts from `intermediates/agent-prompts/` when filling note sections.
- Do not invent paths; use workspace conventions.

Current end-to-end YouTube flow:
1. `video-buddy --json fetch <url>`
2. `video-buddy --json transcribe <video-id>`
3. `video-buddy --json frames <video-id>`
4. `video-buddy --json correlate <video-id>`
5. `video-buddy --json render <video-id>`
6. Fill note sections in `intermediates/note_<id>.md`
7. `video-buddy --json finalize <video-id>`
