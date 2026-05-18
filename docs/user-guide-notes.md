# User Guide Notes

Running capture of user-facing decisions from the design interview. The source of truth for the eventual public `README.md` and `docs/`. Anything in here is something the end user needs to know — internal architecture lives in `SPEC.md` / `docs/adr/`.

Organized roughly as a quickstart-shaped README. Updated after every interview question with user-facing implications.

---

## Install

video-buddy is distributed as a git clone, **not** as a PyPI package. The agent integration files (Claude Code skill, slash commands, prompt templates, worker scripts) live in the repo alongside the Python code, so a pip-only install would only give you half the tool.

```bash
git clone https://github.com/<owner>/video-buddy.git
cd video-buddy
uv sync --extra gpu-ocr
uv run video-buddy --help                 # verify
```

Optional extras:
- `[gpu-ocr]` — easyocr for GPU-accelerated OCR
- `[ocr-cpu]` — pytesseract (system `tesseract` binary required at runtime)

Whisper is part of the base install. GPU OCR is genuinely optional: without `[gpu-ocr]`, video-buddy falls back to remote EasyOCR (if configured) or local Tesseract, which is slower and usually lower quality on code-heavy frames.

If no OCR engine is available at all, `frames` fails with an actionable error and tells you how to disable OCR intentionally via `[frames].ocr = "off"` or `--ocr off`.

When OCR is off, frame capture still runs and the rendered note still embeds frame images. The tool omits OCR text, skips OCR-based code matching, and still preserves repo links explicitly mentioned in the video description.

If you want the leanest possible install and are intentionally opting out of the strong-default model flow, omit `[gpu-ocr]` and use `video-buddy init --no-models`.

For PATH-global access without venv activation:

```bash
uv tool install --from . video-buddy
```

To upgrade: `git pull && uv sync --extra gpu-ocr`.

## What video-buddy is

- A CLI that fetches YouTube videos (and web articles / PDFs / papers), transcribes audio with Whisper, captures + OCRs frames, correlates on-screen code against GitHub repos, renders draft Markdown notes, and finalizes them into a notes workspace.
- Designed to pair with an **agent harness** (Claude Code is the reference target). Agents use prompts plus CLI scripts to drive `/intake` / `/digest` style workflows, then fill the judgment-heavy note sections from the generated artifacts.
- The Python package owns the repeatable pipeline steps; the agent owns summary writing, key concepts, detailed notes, and other cognitive outputs.

## Input types supported in v1

- YouTube video URLs (primary use case; all features apply)
- Web article URLs (text extraction via trafilatura; no frames, no repo correlation)
- PDF files and arxiv/DOI URLs (academic paper handling; same note shape as articles, optional Semantic Scholar metadata enrichment)

Articles and papers share one note template — no separate paper notes.

## What ships in v1

| Capability | Notes |
|---|---|
| Single-URL `ingest` | YouTube + articles + papers |
| Batch `digest` | YouTube-only triage flow (per-video summaries + grouped report) |
| Frame capture + OCR | Local GPU EasyOCR if available, automatic Tesseract fallback, SSH backend for offload, explicit `ocr=off` bypass |
| Repo correlation | Auto-extracts GitHub URLs from video descriptions; matches OCR'd filenames and identifiers against cloned repo files |
| Concept extraction | Cross-linked concept notes from agent-produced concept JSON |
| Claude Code integration | Reference skill + `/intake` and `/digest` commands |
| Optional Obsidian template | Opt-in for `[[wiki-link]]` users |
| SSH compute backends | Declare GPU hosts in TOML to offload Whisper/EasyOCR |

## CLI verbs

```
video-buddy fetch <url>             # YouTube/article URL → intermediate JSON
video-buddy transcribe <video-id>   # captionless video → transcript
video-buddy frames <video-id>       # scene capture + OCR
video-buddy correlate <video-id>    # match OCR against GitHub repo files
video-buddy render <video-id>       # JSON → draft Markdown note
video-buddy extract-concepts <id>   # agent-produced concepts JSON → concept notes
video-buddy finalize <video-id>     # commit draft → final notes location

video-buddy ingest <url>            # convenience: fetch+transcribe+frames+correlate+render
video-buddy digest <urls.txt>       # batch fetch+manifest, agent fills summaries, compile
video-buddy audit <manifest>        # health-check a batch run

video-buddy init [dir]              # create workspace + pre-install models
video-buddy models {list,install,remove}
video-buddy backends [test|deploy]  # list/probe/deploy SSH worker hosts
```

Two usage tiers:

1. **Direct CLI** for users who want to fill prose by hand or pipe transcripts into their own tooling.
2. **Agent-driven** for the full "URL in, finished note out" experience: install one of the shipped agent integrations and run `/intake <url>` or `/digest <urls.txt>` inside the agent harness.

## Note format

Default output is **plain Markdown**. Concept references render as `[Concept Name](concepts/concept-name.md)` links. Opens cleanly in any markdown editor.

**Obsidian users:** set `[notes].template = "obsidian"` in `.video-buddy.toml`, or pass `--template obsidian`, to get `[[Wiki-Style]]` links and Obsidian-flavored concept-note frontmatter. Both templates produce the same `concepts/` directory structure — only the link style and concept-note frontmatter differ.

video-buddy does **not** maintain a global `Home.md` index even in Obsidian mode. If you want one, you maintain it.

## Where files live (workspace layout)

video-buddy operates inside a **workspace** — a directory you choose. Default is `./vb-workspace/` relative to where you invoke the CLI. Inside it:

```
vb-workspace/
├── intermediates/      # JSON, transcripts, frame captures, draft notes, prompts
├── notes/              # final rendered .md notes (point Obsidian here if you use it)
│   ├── concepts/       # cross-linked concept notes
│   ├── media/          # frame .jpg files referenced by notes
│   └── digests/        # compiled digest reports
├── .video-buddy.toml   # workspace-local config (annotated; every key commented at its default)
└── .gitignore          # written speculatively; inert until you `git init`
```

**Heavy regenerable caches live outside the workspace** in `$XDG_CACHE_HOME/video-buddy/` (`~/.cache/video-buddy/` on Linux):
- `models/` — Whisper + EasyOCR models (shared across all workspaces on this machine)
- `repos/` — GitHub clones for repo correlation

This keeps the workspace small and portable. To get a fully self-contained workspace, override `model_cache` and `repo_clone_root` in `.video-buddy.toml`.

`video-buddy init` creates the layout above. It:
- Refuses to clobber a non-empty target dir unless `--force`
- Does **not** run `git init` — pick your own VCS
- Pre-installs models by default (see § Models)
- Writes `.video-buddy.toml` with every key commented at its default (discoverable by reading the file)
- Accepts a positional dir name: `video-buddy init my-research` creates `./my-research/`

Every path is configurable. `--workspace <path>` is the universal flag; per-directory overrides: `--notes-dir`, `--intermediates`, `--media-dir`, `--model-cache`, `--repo-clone-root`.

## Models

`video-buddy init` pre-downloads the curated recommended sets so first-use ingest is never blocked on a multi-minute download:

- `recommended-cpu` — `base` and `small`
- `recommended-gpu` — `base`, `small`, and `large-v3-turbo`; selected when the GPU OCR path is in play
- With no explicit bundle, `init` and `models install` pick `recommended-gpu` when a GPU-capable backend is detected and the GPU path is available; otherwise they pick `recommended-cpu`.
- Whisper remains part of the core install because transcription is core.
- **EasyOCR:** English language pack (~64 MB). This installs when `[gpu-ocr]` is present; otherwise init tells you OCR will fall back to remote EasyOCR (if configured) or local Tesseract.
Default model selection is hardware-aware: CPU defaults to `base`; GPU defaults to `large-v3-turbo`.

Named bundles shipped in v1:
- `recommended-cpu` — `base` and `small`
- `recommended-gpu` — `base`, `small`, and `large-v3-turbo`
- `whisper-core` — `base` and `small`
- `whisper-all` — `base`, `small`, and `large-v3-turbo`
- `easyocr-en` — EasyOCR English language pack
- `cpu-only` — `whisper-core` plus the local Tesseract path (`[ocr-cpu]`)

These live in `$XDG_CACHE_HOME/video-buddy/models/`, shared across all workspaces.

**Opt-out paths:**
- `video-buddy init --no-models` — skip the install; rely on auto-download at first use of each model
- `video-buddy init --models recommended-cpu,easyocr-en` — install a named bundle plus an explicit model, or `--models base,small` for raw names. Non-bundled models like `large-v3-turbo` stay available by raw name
- `video-buddy models remove medium large-v3` — reclaim disk later
- `video-buddy models install recommended-gpu` — add a named bundle post-init

`video-buddy models list` shows what's cached.

PyTorch CUDA is **not** managed by `init` — that's your Python environment decision. `init` detects GPU/CUDA presence and reports it, but does not run `pip install`.

## Compute backends

By default, all work runs locally. To offload Whisper / EasyOCR to a different machine you own (e.g. a homelab GPU box), declare it in `.video-buddy.toml`:

```toml
[[compute]]
name         = "homelab"
type         = "ssh"
priority     = 10
host         = "user@gpu-box.lan"
worker_root  = "~/video-buddy-worker"
capabilities = ["whisper", "easyocr", "gpu"]
ssh_opts     = ["-o", "ConnectTimeout=8"]
```

Then deploy the worker scripts:

```
$ video-buddy backends deploy homelab
```

This scp's the worker scripts, creates a venv at `worker_root/.venv`, and installs the necessary deps. Idempotent — re-running upgrades the worker in place.

The dispatcher picks the highest-priority backend that has what each job needs. No code change required to add new hosts.

**SSH authentication:** video-buddy defers entirely to standard SSH (your `~/.ssh/config`, `ssh-agent`, etc). For unusual setups, pass extra ssh args via `ssh_opts`:

```toml
ssh_opts = ["-i", "~/.ssh/homelab_ed25519", "-J", "jumphost"]
```

**Install shape:** SSH backend support ships in the core repo/package; there is no separate extra for it. If you never declare a `[[compute]] type = "ssh"` entry, it stays inert.

**Probe semantics:** declared `capabilities` are advertised; the real probe runs only when the dispatcher selects that backend for an actual job. Probe failure on an auto-selected backend transparently falls through to the next priority. Probe failure on an explicit `--backend X` fails fast (you picked it for a reason).

`video-buddy backends` lists configured backends and forces a fresh probe of each:

```
$ video-buddy backends
NAME       TYPE   CAPABILITIES         PRIORITY  STATUS
local      local  whisper,easyocr,gpu  0         ready (cuda available)
homelab    ssh    whisper,easyocr,gpu  10        unreachable (ssh: connect timeout)
```

## System dependencies you install yourself

These are binaries video-buddy expects on PATH:

- `ffmpeg` — frame extraction + audio download
- `git` — repository correlation
- `node` — only when using `--cookies-from-browser` for members-only YouTube content
- `tesseract` — only when the local OCR fallback path is active

NVIDIA GPU + CUDA is optional but accelerates Whisper and EasyOCR substantially.

## Members-only / age-gated YouTube content

Pass `--cookies-from-browser <name>` (e.g. `firefox`, `chrome`, `edge`, `brave`, `safari`). yt-dlp reads cookies directly from your installed browser's profile. Requires `node` on PATH (the YouTube n-challenge solver needs a JS runtime).

Firefox is the most reliable (unencrypted cookie DB, can be read while browser is running). Chrome/Edge 127+ require the browser to be **closed** during the call.

## Configuration model

Layered, later overrides earlier:

1. Built-in defaults
2. `$XDG_CONFIG_HOME/video-buddy/config.toml` — user-global (applies to every workspace)
3. `<workspace>/.video-buddy.toml` — workspace-local (overrides user-global)
4. Environment variables (`VIDEO_BUDDY_WORKSPACE`, `VIDEO_BUDDY_BACKEND`, etc.)
5. CLI flags

The annotated `.video-buddy.toml` shipped by `init` documents every available key with its default and a one-line explanation. `grep '^# \[' .video-buddy.toml` lists every section.

---

_Status: living document. Updated as design interview decisions land._

_Decision provenance:_
- _Q3 (agent-driven, no LLM in package) → ADR 0002_
- _Q4 (articles + papers in v1, shared template) → ADR 0003_
- _Q5 (digest in v1, YouTube-only) → § 11.5 SPEC_
- _Q7 (Obsidian opt-in template) → § 6 SPEC_
- _Q8 (workspace defaults: CWD-relative, XDG cache split, init refinements) → § 5.1 SPEC_
- _Q9 (compute backend semantics: lazy probe, explicit deploy verb, ssh defaults) → § 5.2 SPEC, ADR 0005 + ADR 0009_
- _Mid-Q9 directive (strong-default model install) → ADR 0004_
- _Follow-up packaging decision (Whisper core, GPU OCR optional with explicit tradeoff messaging) → ADR 0010_
