---
id: "08"
title: "Make CrisperWhisper the default engine in workspace config"
status: open
blocked_by: ["06"]
priority: high
---

# Make CrisperWhisper the default engine in workspace config

## Context

With auto-selection (ticket 06) working, update the workspace config and documentation to
reflect CrisperWhisper as the recommended default. This is a config/docs change, not code.

## What to build

1. Update `vb-workspace/.video-buddy.toml` to uncomment `engine = "auto"`
2. Update AGENTS.md to document the new engine preference
3. Update README.md quick start to mention GPU backend
4. Document the monolith setup in a new `docs/gpu-backend-setup.md`

## Acceptance criteria

- [ ] Workspace config has `engine = "auto"` uncommented
- [ ] AGENTS.md mentions CrisperWhisper as default when monolith available
- [ ] README mentions GPU backend for faster transcription
- [ ] `docs/gpu-backend-setup.md` documents monolith setup for new users
- [ ] `docs/transcript-schema.md` updated to note CrisperWhisper as primary producer of v2

## Validation criteria

- Fresh clone + `uv sync` + workspace init → `transcribe` auto-selects CrisperWhisper
- Documentation is accurate and complete enough for someone else to set up a GPU backend
