# 0009 — Ship SSH ComputeBackend support built-in

**Context.** `video-buddy` has three backend types in the design: `local`, `ssh`, and `subprocess`. The unresolved question was whether `ssh` support should live in the core install or behind an optional extra. The target user often has a second GPU-capable machine available over SSH, but many users will run everything locally.

Two alternatives existed:
1. **Built-in.** `SshBackend` ships in the core codebase and is always importable. It does nothing unless a user declares `[[compute]] type = "ssh"` in config.
2. **Optional extra.** `SshBackend` is unavailable unless the user installs an extra dedicated to SSH support.

**Decision.** Option 1. Ship `ssh` support built-in.

**Why.**
- SSH support has near-zero dependency cost because the design uses standard `ssh`/`scp` subprocesses and user-managed SSH config, not a heavyweight Python SSH stack.
- The target workflow includes "I have a GPU box" often enough that making SSH a plugin would hide a first-class path behind avoidable install friction.
- Optional extras are justified for heavy libraries whose functionality is genuinely optional (`easyocr`), not for a thin transport shim.
- Keeping `ssh` in the core surface simplifies docs and examples: one install shape, one backend model, no branching quickstart.
- Inert-unless-configured preserves the local-only experience; users who never add a `[[compute]]` entry pay essentially nothing.

**Implications.**
- `src/video_buddy/compute/ssh.py` is part of the default package.
- `video-buddy backends` always understands `type = "ssh"` entries.
- README/spec/user docs describe SSH as a built-in backend type, not an add-on.
- Any future remote backend that pulls in real external dependencies (`runpod`, `modal`, etc.) can still be treated differently; this decision is specific to plain SSH.
