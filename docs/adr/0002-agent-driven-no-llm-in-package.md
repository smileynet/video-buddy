# 0002 — Agent-driven, no LLM SDK in the package

**Context.** The current `knowledge-vault` pipeline depends on Claude Code orchestration for everything cognitive (note summary, concept extraction, digest summarization). An earlier draft of SPEC.md proposed an `LLMAdapter` Protocol inside the Python package, with `noop`, `anthropic`, `openai`, and `ollama` adapters as opt-in extras. Three alternatives were on the table: (a) ship the adapter plumbing + one real provider; (b) ship `noop` only; (c) punt entirely.

**Decision.** None of (a)-(c). The Python package contains zero LLM client code. The agent harness (Claude Code by default) drives the mechanical CLI from the outside, owns all cognitive steps, and reads/writes conventional files the CLI consumes or produces.

**Why.**
- The current `/intake` flow is already 95% "agent does the thinking, scripts do the I/O". Encoding that truth as the architecture matches reality.
- Zero vendor lock-in. Switching LLMs is a user config change in the agent harness, not a code change in video-buddy.
- Zero SDK churn pressure on the public package — `anthropic`, `openai`, `ollama` all move fast and break.
- Zero API key handling means zero blast radius if video-buddy is ever compromised.
- The agent-CLI contract is three concrete things: mechanical CLI verbs, conventional file paths, and HTML-commented in-note markers. Every one of those is trivially testable.
- Other agent ecosystems (Codex CLI, Aider, Cline, ...) can integrate against the same surface without any code in video-buddy.
