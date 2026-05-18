# 0005 — Lazy ComputeBackend probe with declared capabilities

**Context.** Whisper and EasyOCR jobs can dispatch to local or SSH-attached compute backends. Each backend declares its capabilities (`whisper`, `easyocr`, `gpu`) in TOML. The question: how and when does the CLI verify those capabilities are actually present?

Four alternatives existed:
1. **Pure declared.** Trust TOML; never probe. Silent failures at job time.
2. **Eager probe at startup.** Run a probe against every backend on every invocation. Always accurate; adds 200ms–2s startup latency per backend.
3. **Lazy probe on selection.** Declared capabilities advertised; probe runs only when the dispatcher selects that backend for a real job. `backends` verb forces a fresh probe across all.
4. **Probe with TTL cache.** Like (3) plus a cached probe result for N minutes.

**Decision.** Option 3, plus failure-model split: auto-fallthrough when no `--backend` is given; fail-fast when `--backend X` is explicit.

**Why.**
- Persona #1 won't tolerate startup latency on a daily-use CLI; (2) is out.
- Silent failures (1) violate the "errors must be diagnosable" expectation.
- Cached probes (4) over-engineer the realistic case: probes are cheap compared to the SSH file-transfer + GPU inference job that follows. The cache adds invalidation complexity ("is my homelab back up?" → `--no-cache`) for no real win.
- Auto-fallthrough on default dispatch matches user mental model: "I just want the job to run." Fail-fast on explicit `--backend X` matches the inverse: "I picked it for a reason, don't second-guess me."
- Failure reporting is informative: "tried backend 'homelab' for capability 'whisper': SSH connection refused. Falling back to 'local'."

**Implications.**
- The dispatcher emits a one-line stderr note when it falls through on auto-dispatch, so the user knows.
- The `backends` verb is the only place that forces a synchronous probe across all configured hosts — used for diagnostics ("which of my hosts are reachable right now?").
- Tests can construct a `ComputeBackend` with `available()` returning a fixed boolean; no mocking of network calls.
