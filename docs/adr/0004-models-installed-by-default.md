# 0004 — Strong-default model pre-install at `init`

**Context.** Whisper and EasyOCR models are downloaded on demand at first use in the source `knowledge-vault` pipeline. For a 20-minute video this means a 1-5 minute delay mid-`ingest` while a ~150 MB to ~3 GB model downloads. The first-use experience is "I ran the command, why is it stuck?"

Three alternatives existed:
- (a) **Lazy-download** (today's behavior). No setup overhead; mid-flow waits.
- (b) **Lazy with progress bar.** Same delay, better UX during it.
- (c) **Eager pre-install by default with explicit opt-out.**

**Decision.** Option (c). `video-buddy init` pre-installs curated recommended model bundles to `$XDG_CACHE_HOME/video-buddy/models/` by default. Opt-out is explicit: `init --no-models` or `init --models <subset>`. A separate `video-buddy models` verb handles post-init list/install/remove.

**Why.**
- Persona #1 expects setup overhead at install time, not mid-task. Lazy-download violates that expectation.
- Modern disks make multi-GB model caches negligible; bandwidth is usually the limit and only matters once.
- Models live in shared XDG cache, so the download cost is paid once per machine across all workspaces (ADR 0008 territory — workspace cache split).
- Opt-out is preserved for users on constrained connections or who want minimal install footprint.
- The CLI auto-downloads any requested model not already cached (e.g. `--whisper-model large-v3-turbo` when only `base` was installed), so opting out doesn't break anything — it just shifts the cost back to first-use.

**Curated bundles (subject to revision as benchmark evolves):**
- `recommended-cpu` = `base`, `small`
- `recommended-gpu` = `base`, `small`, `large-v3-turbo`
- `whisper-core` = `base`, `small`
- `whisper-all` = `base`, `small`, `large-v3-turbo`
- `easyocr-en`
- `cpu-only`

When no explicit bundle is provided, the tool selects `recommended-gpu` on GPU-capable backends when the GPU path is available and `recommended-cpu` otherwise.

**Out of scope.** PyTorch CUDA install. That's a Python environment decision the user owns; `init` reports what it sees but does not run `pip install`.
