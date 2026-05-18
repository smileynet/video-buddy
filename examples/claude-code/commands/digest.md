# /digest

Argument: a URL list file path.

Workflow:
1. Run `video-buddy --json digest fetch <urls.txt>`.
2. If the manifest reports captionless videos, run `video-buddy --json digest transcribe <manifest.json>`.
3. For each fetched video, read the source artifacts and write `vb-workspace/intermediates/summaries/video_<id>.md`.
4. Run `video-buddy --json digest compile <manifest.json> --date <YYYY-MM-DD>`.
5. Return the final digest path.
