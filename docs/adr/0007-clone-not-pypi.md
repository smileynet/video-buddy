# 0007 — Distribution as cloned repo, not PyPI package

**Context.** Standard Python tool distribution is PyPI publish + `pip install`. Earlier in the design interview, that was the proposed model. Three alternatives existed:
- (a) Publish to PyPI; user runs `pip install video-buddy`.
- (b) Distribute as git clone only; user runs `git clone && uv sync`.
- (c) Both — PyPI for the binary, encourage clone for agent integration files.

**Decision.** Option (b). The repo is cloned, not pip-installed. No PyPI publish.

**Why.**
- The product is not just the Python package. The Claude Code skill, slash commands (`examples/claude-code/commands/{intake,digest,batch-intake}.md`), prompt templates, `AGENTS.md` snippet, and worker scripts (`workers/{ocr,transcribe}_worker.py`) are all repo artifacts.
- A pip-installed package gives you the `video-buddy` binary but not the agent integration files. Users would have to clone the repo *anyway* to use the tool the way it was designed.
- Removing PyPI from the install path collapses two install styles into one supported flow: "clone, sync, you have everything." Simpler docs, simpler support.
- Users who explicitly want to install without cloning (uncommon for this tool's use case) can still `uv pip install git+https://github.com/<owner>/video-buddy.git` — it works because `pyproject.toml` still defines the package — they just don't get the `examples/` content.
- Option (c) would be the most flexible but at the cost of doubled docs and the risk of split-brain installs ("which version of the skill matches which version of the package?").

**Implications.**
- `pyproject.toml` still defines `[project.scripts] video-buddy = "video_buddy.cli:main"` so the binary lands in the venv after `uv sync`. Users run `uv run video-buddy <verb>` or activate the venv.
- For PATH-global access without venv activation, users can `uv tool install --from . video-buddy` (or the equivalent pipx command) inside their clone.
- No PyPI account, no Trusted Publishers, no `twine upload`. GitHub Releases mirror tags but ship source tarballs, not wheels.
- The README's quickstart leads with `git clone`, not `pip install`.
- Updating means `git pull && uv sync`, not `pip install -U`.

**Reversibility.** This is reversible if usage patterns shift — adding PyPI publish later is additive. The reverse (yanking from PyPI after publishing) is harder and confuses dependency graphs.
