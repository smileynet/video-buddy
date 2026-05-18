# Glossary

**video-buddy**:
The public OSS project under design at `~/code/video-buddy`. A clean greenfield extraction, not a fork.
_Avoid_: "the public version", "the rewrite".

**knowledge-vault**:
The author's private Obsidian-flavored notes project at `~/code/knowledge-vault`. Unchanged by this work; remains the personal daily-driver.
_Avoid_: "the original", "the old codebase" — it is the *current* codebase, just private.

**parallel extract**:
The relationship pattern between video-buddy and knowledge-vault: a clean greenfield extraction of the generic engine into a new public repo, with the private repo left running as-is. Not a fork, not a rename, not a replacement.
_Avoid_: "fork", "port".

**agent**:
An LLM-driven orchestrator (Claude Code is the reference target; any subprocess-spawning harness works) that drives the video-buddy CLI. The agent owns every cognitive step: parsing user intent, choosing which verbs to call, reading JSON artifacts the CLI produces, writing prose into note files, generating concept/summary JSON the CLI later consumes.
_Avoid_: "LLM", "model" — those are the agent's underlying components, not the orchestrator itself.

**mechanical verb**:
A video-buddy CLI subcommand. Deterministic, idempotent, side-effects-on-filesystem only. Examples: `fetch`, `transcribe`, `frames`, `correlate`, `render`, `extract-concepts`, `finalize`. No LLM calls.
_Avoid_: "script", "command" — too generic.

**cognitive task**:
A step in the end-to-end flow that requires intelligence: writing prose, choosing concepts, deciding what to summarize, picking which of N matched repos is the canonical one. **Always** performed by the agent, never by the CLI.
_Avoid_: "LLM step".

**Workspace**:
The dataclass at `src/video_buddy/workspace.py` (§ 5.1 of SPEC.md) that owns every path the tool touches. One root directory (`workspace.root`), all other paths derive from it. No script ever takes raw path strings.
_Avoid_: "vault" — that's an Obsidian-flavored term; the Workspace is plain.

**ComputeBackend**:
The Protocol at `src/video_buddy/compute/base.py` (§ 5.2 of SPEC.md) that owns every "where does this expensive job run?" decision. Named, capability-tagged, priority-ordered. Local is always implicit; SSH backends are user-declared in TOML.
_Avoid_: "worker" — that word is overloaded with the deployed Python script that runs on the remote host. A ComputeBackend may *use* a worker, but they are not the same thing.

**worker**:
A standalone Python script at `workers/{ocr,transcribe}_worker.py` that an `SshBackend` deploys to a remote host's `worker_root` and invokes via SSH. It is not a long-running daemon; it is invoked per-job.
_Avoid_: "remote worker", "server" — the host is not a server, just a machine with a Python interpreter.

**draft note**:
A markdown note at `workspace.intermediates/note_<id>.md`, written by the `render` verb. Contains the full frontmatter + transcript + frame embeds + repo-matched code, plus HTML-commented markers (`<!-- agent: fill ... -->`) where prose is expected. The agent edits this file in place. `finalize` later moves it to its final path in `workspace.notes/`.
_Avoid_: "scratch note", "WIP note".

**in-note marker**:
An HTML comment of the form `<!-- agent: fill Quick Summary (2-3 sentences from transcript) -->`. The agent locates these in the draft note and replaces each with prose. This is one of three surfaces in the agent-CLI contract; the others are CLI verbs and conventional file paths.

**companion prompt**:
A markdown file at `workspace.intermediates/agent-prompts/<id>_<kind>.md`, written by the `render` verb. Contains an instruction-ready prompt (interpolated from `src/video_buddy/prompts/*.md`) plus the relevant transcript or metadata context. The agent reads it, sends it to whatever model stack it owns, and writes the response back into the draft note or a conventional JSON file.
_Avoid_: "prompt file" — too generic; "companion" emphasizes its pairing with a specific draft.

**primary agent**:
The agent instance that received the user's invocation and orchestrates the full flow. Owns CLI invocation, branch decisions, and final reporting. Spawns subagents for cognitive-heavy work in batch flows.
_Avoid_: "main agent", "root agent" — "primary" emphasizes its orchestration role.

**subagent**:
An agent instance spawned by the primary with a fresh, isolated context window, given file-path inputs and file-path outputs only. Does not invoke CLI verbs that mutate vault state. Reports a small textual summary to the primary on completion.
_Avoid_: "child agent", "worker" — worker is already taken by the deployed Python script on a remote host (see entry).

**CognitiveFill / DigestSummary / BatchIngestFill / CorrelationReview**:
The four subagent classes the shipped recipes spawn. See `docs/architecture/task-graph.md` § Subagent boundaries for inputs/outputs of each.
