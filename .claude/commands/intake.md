# /intake

Argument: a single source URL.

Goal: produce a finalized note with the agent-written sections filled in.

Workflow:
1. If the workspace does not exist yet, run `uv run video-buddy init`.
2. Run `uv run video-buddy --json ingest <url>`.
3. Inspect the JSON result.
   - `scope` is the source id you will reuse for later commands.
   - `path` is the draft note path.
   - `steps` shows which mechanical CLI steps already ran.
   - `needs_agent_fill = true` means the draft still needs prose.
4. Read the draft note named by `path`.
5. Read the companion prompts in `vb-workspace/intermediates/agent-prompts/`.
6. Fill these sections directly in the draft note:
   - Quick Summary
   - Key Concepts
   - Detailed Notes
   - Timestamps refinement if useful
7. If you also produce `vb-workspace/intermediates/concepts_<scope>.json`, run `uv run video-buddy --json extract-concepts <scope>`.
8. Run `uv run video-buddy --json finalize <scope>`.
9. Return the final note path from the finalize payload.

Constraints:
- Use the CLI for all mechanical steps.
- Ground prose in the fetched source material only.
- If OCR is unavailable, continue when frame capture succeeded and note that OCR was skipped.
