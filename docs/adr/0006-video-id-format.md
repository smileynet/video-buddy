# 0006 — Video-id format as public stable identifier

**Context.** Every CLI verb after `fetch` takes a video-id as its primary argument. Every artifact in the workspace is named by it (`video_<id>.json`, `frames_<id>/`, `note_<id>.md`, etc.). The format of this id is a public contract — changing it later breaks every persisted workspace.

Three formats were considered:
- (a) Source-shaped (yt-dlp ID for YouTube, sha256-prefix hash for others). Matches knowledge-vault convention.
- (b) UUIDs. Universal, but opaque — users can't grep their workspace meaningfully.
- (c) Slugs of the title. Human-readable but unstable (title can be edited, leading to id drift).

**Decision.** Option (a). The schema:

| Source | Format | Example |
|---|---|---|
| YouTube | yt-dlp's 11-char ID, `[a-zA-Z0-9_-]{11}` | `dQw4w9WgXcQ` |
| Web article | `web-<sha256(url)[:12]>` | `web-3f2a8b1c4d5e` |
| Local file | `file-<sha256(resolved_path)[:12]>` | `file-7c9e2a4f5b6d` |
| Paper with DOI | `doi-<slugified-doi>` | `doi-10-1234-foo-bar` |

**Why.**
- Direct compatibility with knowledge-vault's existing 1500+ video JSONs — dogfooding works without migration.
- YouTube IDs are already public, stable, and well-known. Using them directly avoids invention.
- Hash-based IDs for non-YouTube content are stable across re-fetches of the same URL/path; titles are not.
- 12-char hash prefix has ~10⁻¹⁴ collision probability across realistic workspace sizes (millions of items would still be safe).
- Pattern-matchable: an agent can validate a string is a video-id by checking it against four regexes.

**Implications.**
- Changing the hash length, hash algorithm, or DOI slug rules in the future is a breaking change. Workspace migration tools would be required.
- The id is **not** a permalink to the source — re-fetching a YouTube video years later still maps to the same id; re-running an article URL through `fetch` is idempotent only as long as the URL hasn't been canonicalized differently.
- Tests can construct synthetic ids of any of the four shapes.
