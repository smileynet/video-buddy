# video-buddy — Specification

A publicly shareable, Obsidian-agnostic toolkit for turning YouTube videos
(plus articles/papers) into structured Markdown notes with timestamped
transcripts, scene-captured frames + OCR, and code-matched repository
correlation.

This spec proposes the extraction of the generic, reusable engine from the
private `knowledge-vault` project. It is prescriptive: every section calls
out what is **copied verbatim**, what is **stripped/rewritten**, and what is
**dropped**.

---

## 1. Vision & Non-Goals

### What it is

A CLI that, given a YouTube URL, produces:

1. `video_<id>.json` — metadata + captions/transcript
2. `transcript_<id>.json` — Whisper transcription when captions missing
3. `frames_<id>/` — selected frames + `frames_meta.json` (OCR + repo matches)
4. `note_<id>.md` — rendered Markdown note (plain Markdown, no Obsidian wiki-links)
5. Optional: same flow for web articles, PDFs, and papers

Two usage tiers:

- **Mechanical CLI** — Run the pipeline. Get JSON, OCR'd frames, repo-matched code blocks, full transcripts, and a Markdown note scaffold with HTML-commented `<!-- agent: fill ... -->` markers where prose belongs. Useful as-is for technically-fluent users who want to fill the prose by hand.
- **Agent-driven** — Drop the shipped skill / slash commands / prompts (under `examples/`) into your agent harness (Claude Code is the reference target). The agent calls the CLI for every mechanical step, reads the JSON and transcripts the CLI produces, fills the prose-shaped sections of the note in place, then calls the CLI again for finalization. **The agent is the brain; the CLI is the hands.** No LLM SDK ever ships inside the Python package.

### What it is not

- **Not** an Obsidian vault. No `Home.md`, no `[[wiki-links]]`, no `.obsidian/` config,
  no concept-graph cross-linking. Output is plain Markdown that opens fine in
  Obsidian/Logseq/VSCode/anything, but the tool does not own a vault directory.
- **Not** a Claude Code plugin. No slash commands. The current `/intake`, `/digest`,
  `/batch-intake` Markdown commands are private orchestration — they ship as
  optional `examples/claude-code/` and `examples/scripts/` recipes, not core.
- **Not** opinionated about hosting. There is no built-in remote host. The
  `ComputeBackend` abstraction (§ 5.2) lets users declare any SSH-accessible
  GPU box (or sibling Python venv) in their config and have whisper/easyocr
  jobs dispatched to it; the tool ships with built-in `local`, `ssh`, and `subprocess` backend types.

### Out of scope for v1

- Concept extraction / cross-linking across notes (Obsidian-flavored, LLM-heavy,
  drove most of the personal-config surface area).
- Multi-channel digests with grouped triage tables.
- Batch ingest orchestration (`batch_intake.md` ~190 lines of Claude-driven
  glue). The underlying scripts (`batch_fetch.py`, `batch_transcribe.py`) survive
  and are invokable; the Claude orchestration on top does not ship.
- Article/paper PDF support **is** retained but flagged secondary — most of the
  novel value is the YouTube pipeline.

---

## 2. Scope: copy / strip / drop

The current `~/code/knowledge-vault/scripts/` directory has 22 Python files
(~3,500 LoC). Decision per file:

### 2.1 Copy verbatim (or near-verbatim)

These are clean, generic, no personal data:

| File | LoC | Notes |
|---|---|---|
| `fetch_video.py` | 467 | YouTube metadata + caption fetching. Already parameterised on `cookies_from_browser`. The leaked `HF_TOKEN` is **not** here. |
| `fetch_article.py` | 365 | trafilatura + pymupdf4llm + Semantic Scholar. No personal config. |
| `capture_frames.py` | 725 | PySceneDetect + ffmpeg + OpenCV + imagehash. **One change needed:** strip the hardcoded `FFMPEG_PATH = Path("/home/linuxbrew/.linuxbrew/bin/ffmpeg")` — fall back to `shutil.which("ffmpeg")`. |
| `correlate_repo.py` | 876 | GitHub repo cloning + OCR-to-source matching. Generic. |
| `correlate_repo_pool.py` | 448 | Org-wide pool correlation. Generic. |
| `extract_concepts.py` | 368 | Concept-note writer. **Mark as LLM-tier** — the JSON it consumes only comes from an LLM. Keep as opt-in. |
| `generate_note.py` | 307 | Template renderer. Generic. |
| `vault_utils.py` | 70 | Duration/date formatting + dedup. Rename to `note_utils.py`; drop the vault-specific `filter_vault_duplicates` function (or generalize to "filter notes already in `<output-dir>`"). |
| `yt_dlp_opts.py` | 48 | Cookie auth + JS runtime check. Generic. |
| `detect_cuda.py` | 78 | GPU detection. Generic. |
| `import_onetab.py` | 170 | OneTab → URL list. Generic. |
| `import_takeout.py` | 220 | Google Takeout → URL list. Generic. |
| `audit_fetch.py` | ~40 | Legacy manifest auditor. Generic, but consider dropping (it's marked "legacy"). |

### 2.2 Copy with personal data stripped

| File | What changes |
|---|---|
| `monolith.py` (107 LoC) | **Delete.** Replaced by `compute/ssh.py` — a generic `SshBackend` that knows nothing about `sam@monolith.lan` or `~/kv-ocr-worker`. The host, user, worker root, and capability set are all per-backend TOML (§ 5.3). |
| `ocr.py` (648 LoC) | The three-tier dispatch (local GPU → remote monolith → local Tesseract) becomes a single dispatcher over `ComputeBackend.run_easyocr` / `run_tesseract`. The "remote tier" is just "a non-local backend in the registry advertises `easyocr`." Drop `monolith_available()`. |
| `transcribe.py` (505 LoC) | Drop hardcoded monolith assumptions. Calls become `backend.run_whisper(audio, ...)`. The Windows NVIDIA-DLL injection block (lines 26-32) moves into `compute/local.py`'s startup, gated on `sys.platform == "win32"`. The `--worker local\|monolith` flag becomes `--backend <name>`. |
| `digest.py` (306 LoC) | The vault-dedup pass (`--vault knowledge-vault/`) becomes `Workspace.notes`-aware: scan `workspace.notes/**/*.md` for `video_id:` frontmatter. No vault-specific knowledge. |
| `batch_fetch.py` (84 LoC) | Manifest format hardcodes a `{"channel": ..., "videos": [...]}` shape. Generalize — manifests accept a flat URL list **or** the channel-grouped shape. Outputs land in `workspace.intermediates`. |
| `batch_transcribe.py` (173 LoC) | Same generalization. `--worker` flag → `--backend`. |
| `audit_channel.py` (630 LoC) | Useful but heavy. Drop personal manifest path references in docstrings; switch defaults to `Workspace` resolution. |
| `init_vault.py` (131 LoC) | Heavily Obsidian-flavored (writes `.obsidian/app.json`, `Home.md`, `concepts/`, `videos/YYYY-MM/`, etc.). **Replace** with `init.py` that creates `Workspace` dirs (`intermediates/`, `notes/`, `notes/media/`, `.cache/`) and a starter `.video-buddy.toml`. No `.obsidian/`, no `Home.md`. |
| `build_export_bundle.py` (524 LoC) | Useful generic feature (self-contained zip of notes + media + cloned repos for sharing). Replace hardcoded `knowledge-vault/` references with `Workspace` paths. |
| `finalize_video_ingest.py` (296 LoC) | Currently writes to `knowledge-vault/videos/YYYY-MM/<slug>.md`, copies media to `knowledge-vault/media/<id>/`, updates `Home.md`. Rewrite to use `workspace.note(slug, month=...)` and `workspace.media_for(video_id)`, with month-grouping gated on `[notes].group_by`. Drop the `Home.md` update entirely (no global index in v1). |
| `backfill_vault_notes.py` (326 LoC) | One-shot fix script for the original author's existing notes. Drop from public release. |
| `cleanup_output.py` (114 LoC) | Generic intermediate-file janitor. Keep; drop the stationeers-flavored preserve patterns; operate on `workspace.intermediates` rather than `output/`. |
### 2.3 Drop entirely

| Path | Why |
|---|---|
| `knowledge-vault/` (the directory) | The user's personal notes, 770+ concept files, Home.md (47KB), digests, media (LFS). Never ships. |
| `.env` | Contains `HF_TOKEN=...` (see Security § below). |
| `.claude/commands/intake.md`, `digest.md`, `batch-intake.md` | Claude-Code-specific orchestration with leaked personal references. Reborn as **examples** under `examples/claude-code/` after a full rewrite — they reference monolith.lan, knowledge-vault paths, etc. throughout. |
| `kits/` | Personal Cavekit specs (stationeers, godotneers). |
| `docs/planning/` | Brainstorms naming specific YouTubers/channels. |
| `docs/features/` | Acceptance criteria for kv-da3/VS-ff1 — internal milestone tracking. |
| `output/` (its contents) | 1500+ personal video JSONs, transcripts, frame dirs. Ship empty `output/.gitkeep`. |
| `templates/article_extraction_prompt.md`, `concept_extraction_prompt.md` | Generic enough to ship, but they should be rewritten as agent-facing prompt templates under `examples/prompts/` and packaged prompt fragments under `src/video_buddy/prompts/`. |
| `compare_models.py` | Benchmarking against the user's specific videos. Replace with a generic benchmark harness or drop. |
| `output/agent_video_review_list.md`, `indydevdan_agent_review_list.md`, `stationeers_*.md` | Personal triage notes. |
| Git LFS exemptions for `output/export/{stationeers,godotneers,mattpocock,indydevdan}/**` | Personal exports. Drop from `.gitignore` and `.gitattributes`. |

### 2.4 The hidden surface area: Claude orchestration

The current pipeline **depends on Claude Code** to be useful end-to-end. Specifically:

- `/intake` Step 7 (fill note sections): Claude reads transcript + template, writes Quick Summary, Key Concepts, Detailed Notes, Timestamps. Without it the rendered note is mostly empty placeholders.
- `/intake` Step 9 (concept extraction): Claude produces the `concepts_<id>.json` that `extract_concepts.py` consumes. The script does not generate it — only consumes it.
- `/intake` Step 4b/6c (repo correlation reasoning): mostly tooling, but Claude picks which repos to clone when `--auto` is ambiguous.
- `/digest` Step 3 (summarization): Claude generates every per-video summary. The Python only orchestrates fetching/manifest-writing.

video-buddy must **make this LLM dependency optional and explicit**, not implicit-via-Claude-Code. See § 4.

---

## 3. Repository layout (proposed)

```
video-buddy/
├── README.md                  # Public-facing: install, quickstart, agent integration
├── LICENSE                    # MIT
├── pyproject.toml             # name = "video-buddy"; trim deps; no .[gpu-ocr] alias name change
├── uv.lock
├── .gitignore                 # strip personal export exemptions
├── .gitattributes             # drop LFS rules tied to personal export dirs; keep generic media/**/*.jpg rules
├── CHANGELOG.md
├── docs/
│   ├── architecture.md        # pipeline stages, data flow diagram
│   ├── cli.md                 # full flag reference
│   ├── output-schemas.md      # video_<id>.json, frames_meta.json, etc.
│   ├── ocr-engines.md         # local GPU vs Tesseract vs SSH remote worker
│   ├── agent-integration.md   # contract for agents/subagents driving the CLI
│   ├── whisper-models.md      # the existing benchmark, anonymized
│   └── compute-backends.md    # local / ssh / subprocess; how to declare a GPU host
├── examples/
│   ├── claude-code/           # the (rewritten) /intake-like slash commands
│   ├── prompts/               # standalone prompts agents can reuse
│   └── workflows/             # bash recipes: "batch a channel", "render an article"
├── src/video_buddy/           # importable package (replaces flat scripts/)
│   ├── __init__.py
│   ├── cli.py                 # single entry point: `video-buddy <verb>`
│   ├── workspace.py           # Workspace dataclass + path helpers (§ 5.1)
│   ├── config/
│   │   ├── __init__.py
│   │   ├── defaults.py        # built-in defaults; never reads user files
│   │   ├── loader.py          # XDG + workspace + env + CLI layering (§ 5.4)
│   │   └── schema.py          # TOML → typed Config dataclasses (pydantic-free)
│   ├── compute/               # ComputeBackend registry & implementations (§ 5.2)
│   │   ├── __init__.py
│   │   ├── base.py            # ComputeBackend Protocol, Capability enum
│   │   ├── registry.py        # pick(needs=...) dispatcher
│   │   ├── local.py           # in-process backend; owns CUDA detection + win32 DLL init
│   │   ├── ssh.py             # generic SSH+venv backend (replaces monolith.py)
│   │   └── subprocess.py      # sibling-Python backend
│   ├── fetch/
│   │   ├── youtube.py         # from fetch_video.py
│   │   ├── article.py         # from fetch_article.py
│   │   └── yt_dlp_opts.py     # cookie/JS runtime helpers
│   ├── transcribe/
│   │   └── pipeline.py        # orchestrates: download audio → backend.run_whisper(...)
│   ├── frames/
│   │   ├── capture.py         # PySceneDetect + ffmpeg + scoring/dedup
│   │   └── ocr.py             # orchestrates: backend.run_easyocr(...) / run_tesseract(...)
│   ├── correlate/
│   │   ├── repo.py            # from correlate_repo.py
│   │   └── pool.py            # from correlate_repo_pool.py
│   ├── render/
│   │   ├── note.py            # from generate_note.py
│   │   ├── templates/         # from templates/*.md, Obsidian-stripped
│   │   └── finalize.py        # from finalize_video_ingest.py, vault-stripped
│   ├── batch/
│   │   ├── fetch.py
│   │   ├── transcribe.py
│   │   └── digest.py
│   ├── prompts/               # packaged prompt-template fragments the CLI interpolates
│   │   ├── concept_extraction.md       # from templates/concept_extraction_prompt.md
│   │   ├── article_concept_extraction.md
│   │   ├── digest_summary.md           # lifted from .claude/commands/digest.md Step 3b
│   │   └── note_sections.md            # Quick Summary / Key Concepts / Detailed Notes fill prompts
│   ├── utils/
│   │   ├── duration.py
│   │   ├── dates.py
│   │   └── slugify.py
│   └── audit.py               # from audit_channel.py, generalised
├── workers/                   # deployable to a remote host by SshBackend
│   ├── ocr_worker.py          # from kv-ocr-worker/remote_worker.py
│   └── transcribe_worker.py   # from kv-ocr-worker/transcribe_worker.py
├── tests/
│   └── ...                    # pytest, mirrored from existing tests/, vault-stripped
└── vb-workspace/.gitkeep      # default workspace skeleton (intermediates/, notes/, .cache/)
```

### Packaging

- Repo-distributed project named `video-buddy` (clone-first; no PyPI publish).
- Console script `video-buddy` registered via `[project.scripts]`.
- All current `scripts/foo.py` are reachable as `python -m video_buddy.<subpackage>` for advanced users.
- Optional install extras:
  - `uv sync --extra gpu-ocr` → easyocr
  - `uv sync --extra ocr-cpu` → pytesseract (system `tesseract` binary required at runtime)
  - Whisper ships in the base install via `faster-whisper`; local transcription is a core capability.
  - No LLM SDK extras. The Python never imports `anthropic`, `openai`, or `ollama`.

---

## 4. CLI surface

Replaces every slash command with a real CLI. One verb per pipeline stage, plus
two convenience verbs:

```
video-buddy fetch <url>                 # URL → fetch metadata + captions
video-buddy transcribe <video-id>...    # captionless video(s) → transcript
video-buddy frames <video-id>           # scene-capture + OCR
video-buddy correlate <video-id>        # match OCR against GitHub repos
video-buddy render <video-id>           # JSON → draft Markdown note + companion prompts
video-buddy extract-concepts <video-id> # agent-produced concepts JSON → concept notes
video-buddy finalize <video-id>         # commit draft → final notes location
video-buddy ingest <url>                # convenience: fetch+transcribe+frames+render
video-buddy digest <urls.txt>           # batch fetch → per-video JSON, no summary by default
video-buddy audit <manifest.json>       # health-check a batch run
video-buddy init [dir]                  # create workspace skeleton + pre-install models
video-buddy models                      # list / install / remove cached models
video-buddy backends                    # list configured ComputeBackends and their probe results
```

### 4.1 Universal flags

Every verb accepts:

- `--workspace <path>` — `Workspace.root` (§ 5.1). Falls back to `VIDEO_BUDDY_WORKSPACE`, then CWD's `.video-buddy.toml`, then `./vb-workspace`.
- `--notes-dir <path>`, `--intermediates <path>`, `--media-dir <path>`, `--model-cache <path>`, `--repo-clone-root <path>` — power-user overrides for individual `Workspace` paths.
- `--config <path>` — explicit config file; bypasses the layered loader.
- `--backend <name>` — force a specific `ComputeBackend` (§ 5.2). Default: registry dispatcher picks the highest-priority available backend that satisfies the job's capabilities. `--backend local` is the canonical "do everything here" override.
- `--verbose` / `-v` — structured log to stderr; `-vv` for debug.

### 4.2 Verb-specific flags

- `fetch` — `--cookies-from-browser <name>` for members-only/age-gated YouTube content (preserves existing `yt_dlp_opts.py` logic).
- `transcribe` — `--whisper-model <name>` (default: auto-selected by backend: `base` on CPU, `large-v3-turbo` on GPU; see `docs/whisper-models.md`), `--device auto|cpu|cuda`, `--compute-type auto|float16|float32|int8|int8_float16`.
- `frames` — `--no-frames`, `--max-frames N`, `--engine easyocr|tesseract` (forces an OCR engine; otherwise the backend dispatcher picks), `--ocr auto|off`.
- `render` — `--template default|obsidian|<path>` (default template emits plain Markdown; `obsidian` keeps `[[wiki-links]]` for existing users).
- `ingest` — `--no-frames`, `--no-whisper`, plus inheriting `fetch`/`transcribe`/`frames`/`render` flags including `--ocr auto|off`.
- `init` — `--force` (clobber existing non-empty workspace); `--no-models` (skip the pre-install step); `--models <comma-list>` (subset, e.g. `--models recommended-cpu,easyocr-en` or `--models base,small`). Default is to pre-install a recommended bundle plus EasyOCR English (see § 4.4). Positional dir arg overrides the default `vb-workspace` name.
- `models` — subverbs `list` (show cached models + sizes), `install [<names...>]` (idempotent download; with no args, installs a recommended bundle), `remove <names...>` (free disk).

### 4.3 The `ingest` shortcut

`video-buddy ingest <url>` replaces `/intake`:

1. Fetch metadata + captions → `workspace.video_json(id)`.
2. Transcribe if needed → `workspace.transcript_json(id)`.
3. Capture frames + OCR → `workspace.frames_dir(id)` (via `ComputeBackend` dispatch). With `--ocr off`, frames are still captured but OCR text is omitted.
4. Run repo correlation if the description contains GitHub URLs → clones under `workspace.repo_clone_root`. With OCR off, description-linked repos still participate, but OCR-based code matching is skipped.
5. Render `workspace.intermediates/note_<id>.md` (DRAFT) + companion prompts at `workspace.agent_prompt(id, kind)` for the agent.

Step 5 is the handoff point — the agent fills the in-note markers using the companion prompts (see § 7 Agent integration model) and then invokes `extract-concepts` and `finalize` to commit the result.

### 4.4 Model install: strong default

`video-buddy init` pre-downloads models to `$XDG_CACHE_HOME/video-buddy/models/` by default. This trades disk space for the promise that no `ingest` is blocked mid-flow on a model download.

The curated recommended sets:
- `recommended-cpu` — `base` and `small`
- `recommended-gpu` — `base`, `small`, and `large-v3-turbo`; selected when the GPU OCR path is in play
- With no explicit bundle, `init` and `models install` pick `recommended-gpu` when a GPU-capable backend is detected and the GPU path is available; otherwise they pick `recommended-cpu`.
- Whisper models remain core because transcription is core.
- EasyOCR: English (~64 MB) — installed when `[gpu-ocr]` is present. If it is not, `init` continues and emits an explicit note that OCR will fall back to remote EasyOCR (if configured) or local Tesseract.
Default model selection is backend-aware: CPU defaults to `base`; GPU defaults to `large-v3-turbo`.

Named bundles shipped in v1:
- `recommended-cpu` — `base` and `small`
- `recommended-gpu` — `base`, `small`, and `large-v3-turbo`
- `whisper-core` — `base` and `small`
- `whisper-all` — `base`, `small`, and `large-v3-turbo`
- `easyocr-en` — EasyOCR English language pack
- `cpu-only` — `whisper-core` plus the local Tesseract path (`[ocr-cpu]`), with no EasyOCR dependency implied

Opt-out paths:
- `video-buddy init --no-models` — skip entirely; rely on auto-download at first use.
- `video-buddy init --models recommended-cpu,easyocr-en` — install a named bundle plus an explicit model, or `--models base,small` for raw names. Non-bundled models like `large-v3-turbo` stay available by raw name.
- `video-buddy models remove medium large-v3` — reclaim disk later.

Behavior is idempotent: `init` after the cache is already populated is a no-op for the model step. Models can be added/removed later via `video-buddy models`.

PyTorch CUDA is **not** managed by `init` — that's the user's Python env decision. `init` detects and reports what it sees (GPU presence, CUDA version, current torch install) but does not modify the Python environment.

### 4.5 Argument conventions and `--json` output

**Primary argument shape per verb:**

- `fetch` and `ingest` take URLs (no choice — that's the whole input).
- Post-fetch verbs (`transcribe`, `frames`, `correlate`, `render`, `extract-concepts`, `finalize`) take **video-ids** as primary arguments. The CLI resolves to `workspace.video_json(id)` and friends internally. See ADR 0006 for the id format spec.
- Batch flows accept multiple ids: `video-buddy transcribe ABC123 def456 ghi789`.
- `--video-json <path>` is an escape hatch on every post-fetch verb for workspace-external JSONs (testing, ad-hoc inspection).
- `digest` takes a urls.txt path; `audit` takes a manifest.json path.

**Stream conventions:**

- Without `--json`: human-readable summary on stdout, progress on stderr.
- With `--json`: stable structured object on stdout, progress on stderr.
- Errors **always** go to stderr (human-readable). With `--json`, an additional structured error object goes to stdout so the agent can react programmatically.
- Non-zero exit code always means failure.
- `--verbose` / `-v` adds structured detail to stderr; never changes stdout.
- No `--quiet` flag. Redirect stderr if you want silence.

**`--json` payload guarantees:**

- Every payload has a `schema_version` field. Schema changes follow semver.
- Every payload has `verb`, the video-id (or relevant scope id), the paths it wrote, and a `warnings: []` array.
- Full schemas live at `docs/output-schemas.md`.
- The agent recipes always pass `--json`. Humans never bother.

---

## 5. Core abstractions

Personal config leaks across the current pipeline because two concepts live nowhere as types and everywhere as ad-hoc string defaults:

1. **Where do files live?** — `knowledge-vault/`, `output/`, `knowledge-vault/videos/YYYY-MM/`, `knowledge-vault/media/<id>/`, `~/kv-ocr-worker` all appear as literal strings sprinkled across scripts, slash commands, tests, and `.gitignore`.
2. **Which machine runs the expensive job?** — Whisper inference and EasyOCR run either "here" or "on `sam@monolith.lan` via SSH" via a binary `--worker local|monolith` switch hardcoded across three scripts (`transcribe.py`, `ocr.py`, `batch_transcribe.py`).

Both deserve to be real types, not stripped strings.

### 5.1 `Workspace` — owns every path

A single object resolved once at CLI entry. Every script accepts a `Workspace`; no script ever takes raw path strings.

```python
@dataclass(frozen=True, slots=True)
class Workspace:
    root: Path              # the user-chosen workspace dir; content paths derive from it
    intermediates: Path     # JSON, transcripts, frame dirs, agent prompts   (default: root / "intermediates")
    notes: Path             # final .md output                                (default: root / "notes")
    media: Path             # frame .jpg files referenced by notes            (default: root / "notes/media")
    model_cache: Path       # Whisper / EasyOCR models                        (default: $XDG_CACHE_HOME / "video-buddy/models")
    repo_clone_root: Path   # cloned GitHub repos for correlation             (default: $XDG_CACHE_HOME / "video-buddy/repos")
    templates: Path | None  # user template overrides; falls back to pkg      (default: None)

    @classmethod
    def resolve(cls, root: Path | None, overrides: WorkspaceOverrides) -> Workspace: ...

    def video_json(self, video_id: str) -> Path:      return self.intermediates / f"video_{video_id}.json"
    def transcript_json(self, video_id: str) -> Path: return self.intermediates / f"transcript_{video_id}.json"
    def frames_dir(self, video_id: str) -> Path:      return self.intermediates / f"frames_{video_id}"
    def frames_meta(self, video_id: str) -> Path:     return self.frames_dir(video_id) / "frames_meta.json"
    def note(self, slug: str, *, month: str | None = None) -> Path:
        return (self.notes / month / f"{slug}.md") if month else (self.notes / f"{slug}.md")
    def media_for(self, video_id: str) -> Path:       return self.media / video_id
    def agent_prompt(self, video_id: str, kind: str) -> Path:
        return self.intermediates / "agent-prompts" / f"{video_id}_{kind}.md"
    # Audio temp during transcribe is `tempfile.TemporaryDirectory()`, not workspace-resident.
```

Defaults split intentionally between **workspace-local content** (intermediates + notes + media — small, portable, backup-worthy) and **XDG cache** (models + repo clones — large, regenerable, shareable across workspaces). Users who want a fully self-contained portable workspace override `model_cache` and `repo_clone_root` to point inside `root`.

This kills the entire class of "is the user's vault committed in-tree?" decisions: the workspace is a user-owned directory at any path, with no in-tree assumption. Existing Obsidian users point it at their vault root; everyone else uses the default. Month-bucketing (`videos/YYYY-MM/`) becomes an opt-in `[notes].group_by = "upload_month"` setting, not a hardcoded path shape.

### 5.2 `ComputeBackend` — owns every "where does this job run?" decision

The current code has a binary `--worker local|monolith` flag. The right abstraction is a named, capability-tagged backend that any stage can ask: "can you do X for me?"

```python
class Capability(StrEnum):
    WHISPER  = "whisper"
    EASYOCR  = "easyocr"
    GPU      = "gpu"
    FFMPEG   = "ffmpeg"

class ComputeBackend(Protocol):
    name: str                                # config-defined identifier, e.g. "local", "homelab", "runpod-a40"
    capabilities: frozenset[Capability]      # advertised; verified by available()
    priority: int                            # higher wins when multiple backends satisfy a job

    def available(self) -> bool: ...
        # health probe: e.g. SSH reachable + remote venv has expected imports + GPU present

    def run_whisper(self, audio: Path, *, model: str, device: str, compute_type: str) -> list[Caption]: ...
    def run_easyocr(self, frames_dir: Path, frame_names: list[str]) -> dict[str, OCRResult]: ...
    def run_tesseract(self, frames_dir: Path, frame_names: list[str]) -> dict[str, OCRResult]: ...
```

The required capabilities are declared at the call site; the dispatcher picks the highest-priority *available* backend that satisfies them. No script names a backend directly.

```python
backend = registry.pick(needs={Capability.WHISPER, Capability.GPU}) \
       or registry.pick(needs={Capability.WHISPER})
captions = backend.run_whisper(audio, model=cfg.whisper.model, device="auto", compute_type="auto")
```

Built-in backend types:

| Type | Description | Replaces |
|---|---|---|
| `local` | Runs in-process. CUDA-detected via `nvidia-smi`/`ctranslate2`; falls back to CPU. Always present (implicit, priority 0). | Today's "local" path in `transcribe.py` and the local-GPU/Tesseract tiers in `ocr.py`. |
| `ssh` | Runs via SSH against a remote host with a pre-deployed venv at a configurable `worker_root`. Capability set is *probed*, not assumed (the probe runs `nvidia-smi` + a Python `import` check against the worker venv). | Today's hardcoded `sam@monolith.lan` worker — the host, user, and path all move to user config. |
| `subprocess` | Runs a sibling Python interpreter on the same machine (e.g. a sandboxed venv where CUDA libs resolve cleanly). Useful for keeping a fragile CUDA stack out of the main env. | New — also the clean place for the Windows nvidia-DLL injection currently at `transcribe.py:26-32`, instead of polluting global `os.add_dll_directory` state. |

`runpod`, `modal`, `ollama-host`, etc. are intentionally **not** built-in for v1, but `ComputeBackend` is the entire extension surface — adding one is a single file in `src/video_buddy/compute/` that registers itself with the registry.

### 5.3 Backend registry & user config

Backends are user-declared, not auto-magic. The default config has only `local` (implicit); additional hosts are TOML entries:

```toml
[workspace]
root = "./vb-workspace"
# intermediates, notes, media, cache, templates override individually if needed

[notes]
group_by = "flat"        # "flat" | "upload_month"
template  = "default"    # "default" | "obsidian" | <path to user template>

[whisper]
model = "auto"           # auto => `base` on CPU, `large-v3-turbo` on GPU
device = "auto"
compute_type = "auto"

[frames]
max_per_video = 15
scene_detection_max_duration_s = 600
ocr = "auto"              # "auto" | "off"

[agent]
harness = "claude-code"     # descriptive only; no runtime SDK binding

[youtube]
cookies_from_browser = ""
caption_retry_max = 3

[tools]
ffmpeg    = "ffmpeg"     # binary name or absolute path; resolved via shutil.which
node      = "node"
git       = "git"
tesseract = "tesseract"

# --- Compute backends. The "local" backend is always implicit at priority 0.
# Declare additional named hosts here:

[[compute]]
name         = "homelab"
type         = "ssh"
priority     = 10
host         = "user@gpu-box.lan"
worker_root  = "~/video-buddy-worker"
capabilities = ["whisper", "easyocr", "gpu"]
ssh_opts     = ["-o", "ConnectTimeout=8", "-o", "BatchMode=yes"]

[[compute]]
name         = "isolated-cuda"
type         = "subprocess"
priority     = 5
python       = "/opt/cuda-venv/bin/python"
capabilities = ["whisper", "gpu"]
```

This is the documented path to "I have a GPU box, point video-buddy at it" — without ever naming the original author's `monolith.lan`.

### 5.4 Config resolution order

Layered (later overrides earlier):

1. Built-in defaults in `src/video_buddy/config/defaults.py`.
2. `$XDG_CONFIG_HOME/video-buddy/config.toml` — user-global.
3. `<workspace-root>/.video-buddy.toml` — workspace-local.
4. Env vars — `VIDEO_BUDDY_WORKSPACE`, `VIDEO_BUDDY_BACKEND`, `ANTHROPIC_API_KEY`, etc.
5. CLI flags — final override.

### 5.5 Hardcode-to-abstraction mapping

| Current hardcode | New home |
|---|---|
| `SSH_TARGET = "sam@monolith.lan"` (`scripts/monolith.py:7`) | User-defined `[[compute]]` entry with `type = "ssh"`. No built-in default. |
| `REMOTE_WORKER_ROOT = "~/kv-ocr-worker"` (`scripts/monolith.py:8`) | `[[compute]].worker_root`, per backend. |
| `FFMPEG_PATH = Path("/home/linuxbrew/.linuxbrew/bin/ffmpeg")` (`scripts/capture_frames.py:51`) | `[tools].ffmpeg`, resolved via `shutil.which` with absolute-path passthrough. |
| Windows nvidia-DLL injection (`scripts/transcribe.py:26-32`) | Owned by the `local` backend's startup path, gated on `sys.platform == "win32"`. Never runs in tests. |
| `--vault knowledge-vault/` default (digest, audit, finalize, ...) | `Workspace.notes`, derived from `--workspace`. |
| `--output-dir output` default (several scripts) | `Workspace.intermediates`. |
| `--worker local\|monolith` flag (transcribe.py, batch_transcribe.py) | `--backend <name>` to force; otherwise the registry dispatcher picks the best available. |
| `monolith_has_gpu_and_python(...)` probe (`scripts/monolith.py:59`) | `SshBackend.available()` runs a generic probe taking the imports the requested capability needs as input. |
| `--force-local` / `--engine tesseract` in OCR | Survive as `--backend local` / `--engine tesseract`, but dispatch through the same `ComputeBackend.run_*` methods. When no OCR engine is available at all, `frames` fails with an actionable error that points to `[frames].ocr = "off"` or `--ocr off` for users who intentionally want frame capture without OCR. |
| `knowledge-vault/media/<id>/` | `Workspace.media_for(video_id)`. |
| `knowledge-vault/videos/YYYY-MM/<slug>.md` | `Workspace.note(slug, month=...)`. Month-grouping opt-in via `[notes].group_by`. |
| `kv-ocr-worker/{remote_worker,transcribe_worker}.py` | Ship as `workers/{ocr,transcribe}_worker.py`; an `SshBackend` knows how to deploy them to `worker_root`. |
---

## 6. Output format: post-Obsidian

The current `templates/video_note.md` uses Obsidian wiki-links (`[[Concept Name]]`)
and depends on a vault-wide concept directory. video-buddy's default template:

- Plain Markdown links (`[Concept Name](concepts/concept-name.md)`) **only when**
  the agent wrote concept links into the draft AND `--cross-link` is set. Otherwise,
  key concepts render as a flat bullet list of names.
- YAML frontmatter unchanged for compatibility (`video_id`, `title`, `channel`, etc.).
- `## Visual Notes`, `## Source Code`, `## Timestamps`, `## Full Transcript`
  sections rendered by template — no agent required. With OCR disabled, `## Visual Notes` still embeds frames, OCR-derived text is omitted, and the note keeps description-linked repo references but not OCR-correlated code snippets.
- `## Quick Summary`, `## Key Concepts`, `## Detailed Notes` rendered as
  HTML-commented placeholders by default; populated later by the agent or by hand.

Vault-only sections that get dropped from the default template:

- "Personal Takeaways" prompt (the `/intake` Step 8b flow asking "what's actionable for your work?").
- `Home.md` update (no global index in v1).
- `concepts/` cross-linking (handled by the agent; the CLI's `extract-concepts` script consumes agent-produced JSON to create/update the actual files).

The Obsidian-style template is preserved under `templates/obsidian.md` as an
**opt-in template** via `--template obsidian`. So existing Obsidian users can
keep their flow; everyone else gets plain Markdown.

---

## 7. Agent integration model

The Python package contains **zero LLM client code**. No `anthropic` import, no `openai`, no `ollama`, no `LLMAdapter` protocol. The agent harness — Claude Code by default, but anything that can spawn subprocesses works — is responsible for everything cognitive. The CLI is responsible for everything mechanical.

### 7.1 Contract surface

The boundary between agent and CLI is three concrete things:

1. **The CLI itself.** Every verb is documented, idempotent (re-running on an existing artifact is a no-op unless `--force`), and emits machine-readable output where useful (stable JSON to stdout when `--json`, human-readable to stderr).
2. **Conventional file paths.** When the agent needs to write something the CLI will later consume, the path is conventional and discoverable via `Workspace` methods (e.g. `workspace.concepts_json(id) = intermediates/concepts_<id>.json`). The agent does not invent paths.
3. **In-note markers.** `render` lays down a draft note at `workspace.intermediates/note_<id>.md` containing HTML-commented markers like `<!-- agent: fill Quick Summary (2-3 sentences from transcript) -->`. The agent edits the markdown file in place, replacing the marker with prose. `finalize` later moves the draft to its final location and applies any agent-produced tags from the concepts JSON.

### 7.2 Shipped artifacts under `examples/`

- `examples/claude-code/skill.md` — a skill the agent reads on demand describing how to drive video-buddy. Replaces the implicit knowledge currently encoded in the author's brain.
- `examples/claude-code/commands/intake.md` — `/intake <url>` slash command. The public, scrubbed descendant of `~/code/knowledge-vault/.claude/commands/intake.md`.
- `examples/claude-code/commands/digest.md` — `/digest <urls.txt>` slash command.
- `examples/claude-code/commands/batch-intake.md` — channel-scale batch ingest.
- `examples/prompts/` — the standalone prompt fragments the slash commands reference (concept extraction, digest summary, note-section fill). Other agent ecosystems can adopt them directly.
- `examples/AGENTS.md` — drop-in `AGENTS.md` snippet describing the contract for any agent that supports the convention.

Other agents (Codex CLI, Aider, Cline, ...) are not shipped in v1 but are not blocked — anyone can write equivalent integrations against the same CLI surface and the same `examples/prompts/` fragments.

### 7.3 Prompts are data, not code

The shipped prompt files at `src/video_buddy/prompts/*.md` are *data* — the CLI's `render` verb interpolates the relevant transcript section + existing-concept list + video metadata into the appropriate prompt and writes the result to `workspace.agent_prompt(id, kind)` as a companion artifact for the agent. The agent reads that file, sends it to whatever model stack it owns, and writes the result wherever the contract says (in-note marker, or `workspace.concepts_json(id)`, or `workspace.summary(id)`).

The CLI never sends a prompt over the network. The agent does.

### 7.4 Why this shape

- **No vendor lock-in.** Switching agent stacks or underlying models is outside video-buddy.
- **No SDK dependency churn.** Fast-moving provider SDKs stay out of the install graph.
- **No API key handling in the public codebase.** Zero blast radius if video-buddy itself is compromised.
- **Honest about where intelligence lives.** The current knowledge-vault `/intake` flow is already 95% "agent does the thinking, scripts do the I/O" — this just names that truth instead of hiding it behind a fictitious `LLMAdapter`.
- **Trivially testable.** Every CLI verb is a subprocess invocation with deterministic file inputs and outputs. No mocking of model APIs required.

---

## 8. Migration plan

A concrete, executable extraction. Three phases.

Migration carry strategy is lift-then-strip with direct-to-main commits (no PRs), one logical group per (lift, strip) commit pair. See ADR 0008 for rationale.

### Phase 1 — Skeleton (no behavior change)

**Status: done at design-artifact level.** The current `main` already contains `SPEC.md`, `CONTEXT.md`, `docs/adr/`, `docs/architecture/`, `docs/user-guide-notes.md`, `docs/output-schemas.md`, `LICENSE`, `README.md`, `.gitignore`. Remaining Phase 1 work:

1. Initialize `pyproject.toml` with the trimmed dependency list (faster-whisper, yt-dlp, yt-dlp-ejs, requests, trafilatura, pymupdf4llm, scenedetect, imagehash, Pillow) and the optional-deps groups (`gpu-ocr`, `ocr-cpu`, `dev`).
2. Add `[project.scripts] video-buddy = "video_buddy.cli:main"` so `uv sync` installs the binary into the venv.
3. Empty package layout under `src/video_buddy/` per § 3 (just `__init__.py` files and module stubs).
4. `tests/` skeleton with `conftest.py` and one passing smoke test.

### Phase 2 — Lift & shift (mechanical)

For every "copy verbatim" file in § 2.1, the two-commit pattern:

- **lift commit**: `git mv` (or scripted copy) from knowledge-vault's layout into video-buddy's `src/video_buddy/<subpackage>/` layout. Zero content diff. Tests carried alongside.
- **strip commit**: rewire imports (`from fetch_video import …` → `from video_buddy.fetch.youtube import …`), drop `from vault_utils import …` references to the renamed `note_utils`, drop hardcoded paths (`/home/linuxbrew/...`, `knowledge-vault/`, `~/kv-ocr-worker`), replace argparse defaults that referenced `knowledge-vault` with Workspace-resolved equivalents. Update test path strings (~10 known occurrences in `test_finalize_video_ingest.py`, `test_audit_channel.py`, `test_init_vault.py`).

For every "copy with personal data stripped" file in § 2.2, the same pattern. The `monolith.py` → `compute/ssh.py` reshape is deferred to Phase 3.

### Phase 3 — Reshape (deliberate)

1. Introduce `src/video_buddy/workspace.py` and `src/video_buddy/config/` (defaults, schema, layered loader). Every script's argparse defaults that named `output/` or `knowledge-vault/` now resolve through a `Workspace` passed in by `cli.py`.
2. Introduce `src/video_buddy/cli.py` with the verbs in § 4. Each verb wires together the existing functions; old `scripts/*.py` entry points are removed. `--json` payloads (per § 4.5 and `docs/output-schemas.md`) wired through every verb.
3. Introduce `src/video_buddy/compute/` (`base.py`, `registry.py`, `local.py`, `ssh.py`, `subprocess.py`). Refactor `frames/ocr.py` and `transcribe/pipeline.py` to dispatch through `registry.pick(needs=...)`. Delete `scripts/monolith.py`. Windows nvidia-DLL injection moves into `compute/local.py`.
4. Introduce `src/video_buddy/prompts/` with the lifted-and-stripped prompt fragments. `render` interpolates them into companion prompts at `workspace.agent_prompt(id, kind)`. No LLM SDK code anywhere in the package (per ADR 0002).
5. Rewrite `render/templates/default.md` to drop Obsidian-only constructs; ship `render/templates/obsidian.md` as the opt-in (`--template obsidian`).
6. Rewrite `render/finalize.py` to use `workspace.note(slug, month=...)` and `workspace.media_for(video_id)`. Drop the `Home.md` update.
7. Port `init_vault.py` → `init.py` (creates Workspace dirs, writes annotated `.video-buddy.toml`, pre-installs models per § 4.4 unless `--no-models`, refuses non-empty target unless `--force`).
8. Write `examples/claude-code/` artifacts: `skill.md`, `commands/intake.md`, `commands/digest.md`, `commands/batch-intake.md`, plus `AGENTS.md` template. These wrap the CLI; no logic lives in them.
9. Write `workers/{ocr_worker.py,transcribe_worker.py}` (lifted from knowledge-vault's `kv-ocr-worker/`) and `backends deploy` verb that scp's them to the configured `worker_root`.

### Phase 4 — Polish

1. Replace placeholder README with a real quickstart (clone → uv sync → init → ingest).
2. Fill out `docs/` (architecture, cli reference, ocr-engines, whisper-models, compute-backends, schema reference).
3. End-to-end smoke test against a known-stable public-domain YouTube URL.
4. Real-session smoke test: open Claude Code in the cloned repo, run `/intake <url>`, verify the full agent-driven flow produces a finalized note.

---

## 9. Security checklist

**Must do before any public push:**

1. **Revoke `HF_TOKEN`** at `~/code/knowledge-vault/.env:1` (a real Hugging Face token,
   value redacted from this document). Revoke at <https://huggingface.co/settings/tokens>.
   Do **not** carry it over.
2. **No `.env` in video-buddy**. Ship only `.env.example` with placeholder names.
3. **Scrub all `monolith.lan`, `sam@…`, `/home/linuxbrew/…`, `C:/Users/uosmi/…`** references in code, comments, docs.
4. **Scrub channel/creator names** (`Cows are evil`, `Stationeers`, `Matt Pocock`,
   `IndyDevDan`, `Godotneers`, `mattpocock`, etc.) from every file we copy.
   Sample audit returned hits in: `kits/`, `docs/planning/`, `docs/features/`,
   `output/`, multiple slash command files, `knowledge-vault/Home.md`,
   `knowledge-vault/stationeers-knowledge-guide.md`. Since most of those are in
   the "drop entirely" bucket, the residual surface is small.
5. **Do not import LFS pointers** from the source repo. The new `.gitattributes`
   sets up LFS rules but the new repo starts with zero LFS objects.
6. **Run `gitleaks` (or equivalent)** on the staged commit before the first push.
7. **Confirm `.claude/`, `.idea/`, `.vscode/`, `.obsidian/` are all gitignored.**

---

## 10. Dependencies — public version

Trimmed `pyproject.toml`:

```toml
[project]
name = "video-buddy"
version = "0.1.0"
description = "Turn YouTube videos and articles into structured Markdown with transcripts, frame OCR, and code correlation."
requires-python = ">=3.10"
dependencies = [
    "faster-whisper>=1.0.0",
    "yt-dlp>=2026.02.21",
    "yt-dlp-ejs>=0.8",       # cookie-auth JS challenge solver
    "requests>=2.31.0",
    "trafilatura>=2.0.0",
    "pymupdf4llm>=0.0.17",
    "scenedetect>=0.6",
    "imagehash>=4.3",
    "Pillow>=10.0",
]

[project.optional-dependencies]
gpu-ocr = ["easyocr>=1.7"]
ocr-cpu = ["pytesseract>=0.3.10"]   # system tesseract binary required
dev = ["pytest>=8.0.0", "ruff>=0.6"]

[project.scripts]
video-buddy = "video_buddy.cli:main"
```

Runtime system dependencies (documented, not vendored):

- `ffmpeg` on PATH — frame extraction + audio download.
- `git` on PATH — repo correlation.
- `node` on PATH — only when `--cookies-from-browser` is used (yt-dlp n-challenge solver).
- `tesseract` on PATH — only when the Tesseract OCR tier is active.
- An NVIDIA GPU + CUDA — optional, accelerates Whisper and EasyOCR.

---

## 11. Resolved late decision

`ssh` ComputeBackend support ships built-in in v1. `SshBackend` is always importable; it stays inert unless the user declares a `[[compute]] type = "ssh"` entry. Rationale: the dependency cost is negligible, and "I have a GPU box" is a first-class workflow for the target user. See ADR 0009.

---

## 12. What success looks like

A user with no prior context runs:

```bash
git clone https://github.com/<owner>/video-buddy.git
cd video-buddy
uv sync --extra gpu-ocr
video-buddy init
video-buddy ingest https://www.youtube.com/watch?v=<id>
```

…and gets `notes/<slug>.md` with:

- Working YAML frontmatter
- Embedded frame images with OCR captions
- Verified code blocks linked to GitHub permalinks (when the description had a repo URL)
- A full timestamped transcript
- HTML-commented `## Quick Summary` / `## Key Concepts` / `## Detailed Notes` placeholders for them to fill, alongside prompt files at `vb-workspace/intermediates/agent-prompts/<id>_*.md` they can pass to their agent harness

…without any references to `monolith.lan`, `sam@`, `knowledge-vault`, `HF_TOKEN`, or any specific YouTube channel in the install, output, or docs.
