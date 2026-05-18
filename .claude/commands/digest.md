# /digest

Argument: a URL list file path.

Goal: produce a grouped digest note for a batch of YouTube videos.

Workflow:
1. If the workspace does not exist yet, run `uv run video-buddy init`.
2. Run `uv run video-buddy --json digest fetch <urls.txt>`.
3. Read the manifest path from the JSON `path` field.
4. Run `uv run video-buddy --json digest transcribe <manifest.json>`.
5. For each manifest item, read the fetched source artifacts and write `vb-workspace/intermediates/summaries/video_<id>.md` using the item's `video_id`.
6. Run `uv run video-buddy --json digest compile <manifest.json> --date <YYYY-MM-DD>`.
7. Return the final digest path from the compile payload.

Constraints:
- Digest is a triage workflow, not a full per-video note workflow.
- Use the CLI for mechanical steps.
- Ground every summary in the fetched source material only.
- Do not skip per-video summary files; compile is only the final assembly step.
