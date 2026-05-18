# 0008 — Migration: lift-then-strip, direct to main

**Context.** The knowledge-vault private project contains ~3,500 LoC of generic engine code that needs to land in video-buddy. Three carry strategies were considered:
- (a) **Manual port file by file.** Highest fidelity, slowest, by-eye review.
- (b) **Mechanical lift then strip.** Two commits per file: verbatim copy, then personal-data strip + rewire to new abstractions.
- (c) **`git filter-repo`** to preserve knowledge-vault commit history with path rewrites and personal-data scrubbing.

Branch / PR strategy was a separate choice: PR-per-group vs direct-to-main.

**Decision.**
- Carry strategy: option (b), mechanical lift then strip.
- Branch strategy: **direct to main** for initial deployment.
- Commit granularity: one logical group per pair of (lift, strip) commits within each phase.

**Why lift-then-strip.**
- knowledge-vault's commit history is full of personal references (channel names, usernames, manifest paths). Carrying it via filter-repo means auditing every commit message and every historical diff for leakage — multi-day work with zero functional payoff.
- Two-phase commits give reviewable diffs: the "lift" commit is `git mv` with zero content change; the "strip" commit shows the exact personal-data removal and Workspace/ComputeBackend wiring. Either can be reverted independently.
- Manual port (a) over-allocates careful-redesign effort to mechanical work. The careful effort is reserved for genuinely-reshaped components (`monolith.py` → `compute/ssh.py`, `init_vault.py` → `init.py`).

**Why direct-to-main.**
- Solo author. Self-review via PR adds friction without catching anything the lift-then-strip diff pair doesn't already isolate.
- `git show <lift>` and `git show <strip>` provide the same reviewability as the PR diff view, with zero overhead.
- CI gates can run on push to main once they exist; nothing about direct-to-main blocks adding pre-merge checks later.
- Reversible: switching to PR-per-group later is additive (rule change, no history rewrite needed).

**Implications.**
- Every carried file has at least two commits: lift and strip. Some files (e.g. `monolith.py`) have a third: lift, strip-personal-data, reshape-to-ComputeBackend.
- Commit messages follow a pattern: `lift(fetch): copy fetch_video.py from knowledge-vault verbatim` / `strip(fetch): rewire to Workspace, drop hardcoded paths`.
- Verification gates per phase (SPEC § 8) act as ad-hoc CI: a phase isn't done until its named tests pass.
- knowledge-vault remains untouched throughout. No upstream patches, no provenance markers in video-buddy's commits.
