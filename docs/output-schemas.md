# `--json` output schemas

Every implemented CLI verb emits structured JSON on stdout when called with `--json`.

Current schema version: `1.0`

## Common success shape

```json
{
  "schema_version": "1.0",
  "verb": "fetch",
  "scope": "dQw4w9WgXcQ",
  "path": "/abs/path/to/artifact",
  "warnings": []
}
```

Common fields:
- `schema_version`
- `verb`
- `scope`
- `path`
- `warnings`

Optional fields used by some verbs:
- `written`
- `outputs`
- `steps`
- `counts`
- verb-specific extras

## Common error shape

When `--json` is set and the command fails, stdout receives:

```json
{
  "schema_version": "1.0",
  "error": "human-readable error message"
}
```

stderr still receives the normal `Error: ...` line.

## `init`

```json
{
  "schema_version": "1.0",
  "verb": "init",
  "scope": "/abs/path/to/workspace",
  "path": "/abs/path/to/workspace",
  "warnings": []
}
```

## `fetch`

```json
{
  "schema_version": "1.0",
  "verb": "fetch",
  "scope": "dQw4w9WgXcQ",
  "path": "/abs/path/to/vb-workspace/intermediates/video_dQw4w9WgXcQ.json",
  "warnings": [],
  "written": ["/abs/path/to/vb-workspace/intermediates/video_dQw4w9WgXcQ.json"]
}
```

Article/paper fetch uses `scope = <source_id>` and `article_<source_id>.json`.

## `transcribe`

Single target:

```json
{
  "schema_version": "1.0",
  "verb": "transcribe",
  "scope": "dQw4w9WgXcQ",
  "path": "/abs/path/to/vb-workspace/intermediates/transcript_dQw4w9WgXcQ.json",
  "warnings": [],
  "written": ["/abs/path/to/vb-workspace/intermediates/transcript_dQw4w9WgXcQ.json"]
}
```

Batch form adds:

```json
{
  "outputs": [
    {"scope": "id1", "path": "..."},
    {"scope": "id2", "path": "..."}
  ],
  "written": ["...", "..."]
}
```

## `frames`

```json
{
  "schema_version": "1.0",
  "verb": "frames",
  "scope": "dQw4w9WgXcQ",
  "path": "/abs/path/to/vb-workspace/intermediates/frames_dQw4w9WgXcQ/frames_meta.json",
  "warnings": [],
  "written": ["/abs/path/to/vb-workspace/intermediates/frames_dQw4w9WgXcQ/frames_meta.json"]
}
```

## `correlate`

```json
{
  "schema_version": "1.0",
  "verb": "correlate",
  "scope": "dQw4w9WgXcQ",
  "path": "/abs/path/to/vb-workspace/intermediates/frames_dQw4w9WgXcQ/frames_meta.json",
  "warnings": [],
  "written": ["/abs/path/to/vb-workspace/intermediates/frames_dQw4w9WgXcQ/frames_meta.json"]
}
```

## `render`

```json
{
  "schema_version": "1.0",
  "verb": "render",
  "scope": "dQw4w9WgXcQ",
  "path": "/abs/path/to/vb-workspace/intermediates/note_dQw4w9WgXcQ.md",
  "warnings": [],
  "written": ["/abs/path/to/vb-workspace/intermediates/note_dQw4w9WgXcQ.md"]
}
```

Companion prompt files are written under `intermediates/agent-prompts/`.

## `extract-concepts`

```json
{
  "schema_version": "1.0",
  "verb": "extract-concepts",
  "scope": "dQw4w9WgXcQ",
  "path": "/abs/path/to/vb-workspace/intermediates/concept_result_dQw4w9WgXcQ.json",
  "warnings": [],
  "written": ["/abs/path/to/vb-workspace/intermediates/concept_result_dQw4w9WgXcQ.json"]
}
```

## `finalize`

```json
{
  "schema_version": "1.0",
  "verb": "finalize",
  "scope": "dQw4w9WgXcQ",
  "path": "/abs/path/to/vb-workspace/notes/my-note.md",
  "warnings": [],
  "written": ["/abs/path/to/vb-workspace/notes/my-note.md"]
}
```

## `ingest`

```json
{
  "schema_version": "1.0",
  "verb": "ingest",
  "scope": "dQw4w9WgXcQ",
  "path": "/abs/path/to/vb-workspace/intermediates/note_dQw4w9WgXcQ.md",
  "warnings": [],
  "needs_agent_fill": true,
  "steps": [
    {"verb": "fetch", "scope": "dQw4w9WgXcQ", "path": "..."},
    {"verb": "transcribe", "scope": "dQw4w9WgXcQ", "path": "..."},
    {"verb": "frames", "scope": "dQw4w9WgXcQ", "path": "..."},
    {"verb": "correlate", "scope": "dQw4w9WgXcQ", "path": "..."},
    {"verb": "render", "scope": "dQw4w9WgXcQ", "path": "..."}
  ]
}
```

Article/paper ingest omits the video-only inner steps.

## `digest fetch`

```json
{
  "schema_version": "1.0",
  "verb": "digest.fetch",
  "scope": "/abs/path/to/manifest.json",
  "path": "/abs/path/to/manifest.json",
  "warnings": [],
  "counts": {
    "total": 1,
    "succeeded": 1,
    "failed": 0,
    "no_captions": 0,
    "already_in_notes": 0
  }
}
```

## `digest transcribe`

```json
{
  "schema_version": "1.0",
  "verb": "digest.transcribe",
  "scope": "/abs/path/to/manifest.json",
  "path": "/abs/path/to/manifest.json",
  "warnings": [],
  "counts": {
    "transcribed": 3
  }
}
```

## `digest compile`

```json
{
  "schema_version": "1.0",
  "verb": "digest.compile",
  "scope": "2026-05-17",
  "path": "/abs/path/to/vb-workspace/notes/digests/digest-2026-05-17.md",
  "warnings": [],
  "digest_path": "/abs/path/to/vb-workspace/notes/digests/digest-2026-05-17.md",
  "groups": ["AI Engineer"],
  "missing_summaries": []
}
```

## `digest`

Convenience command (`digest run`) emits:

```json
{
  "schema_version": "1.0",
  "verb": "digest",
  "scope": "2026-05-17",
  "path": "/abs/path/to/vb-workspace/notes/digests/digest-2026-05-17.md",
  "warnings": [],
  "manifest": "/abs/path/to/manifest.json",
  "digest_path": "/abs/path/to/vb-workspace/notes/digests/digest-2026-05-17.md",
  "counts": {"...": "..."},
  "groups": ["AI Engineer"],
  "missing_summaries": []
}
```

## `models list`

```json
{
  "schema_version": "1.0",
  "verb": "models.list",
  "scope": "/abs/path/to/model/cache",
  "path": "/abs/path/to/model/cache",
  "warnings": [],
  "whisper_models": ["base", "small"],
  "easyocr_en_cached": true
}
```

## `models install` / `models remove`

```json
{
  "schema_version": "1.0",
  "verb": "models.install",
  "scope": "/abs/path/to/model/cache",
  "path": "/abs/path/to/model/cache",
  "warnings": []
}
```

`models.remove` has the same shape with `verb = "models.remove"`.

## `backends list`

```json
{
  "schema_version": "1.0",
  "verb": "backends.list",
  "scope": "backends",
  "path": "backends",
  "warnings": [],
  "backends": [
    {"name": "local", "available": true, "reason": "ready"}
  ]
}
```

## `backends deploy`

```json
{
  "schema_version": "1.0",
  "verb": "backends.deploy",
  "scope": "homelab",
  "path": "homelab",
  "warnings": [],
  "available": true,
  "reason": "ready"
}
```

This document reflects the implemented contract, not the full design intent in `SPEC.md`.
