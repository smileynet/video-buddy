# Native-browser guide and worked example

Read `guide.html` directly for the source teaching, or `guide.md` for a compact text artifact. They contain the same authored lesson. `orders.html` is our small executed adaptation; it is separate from the creator's full application.

To try it, serve this directory with a local static server. With Python 3 installed:

```text
python -m http.server 8876 --bind 127.0.0.1
```

Open http://127.0.0.1:8876/orders.html twice in the same profile. See the guide's walkthrough for updates, takeover and late joining. Use another port in both tabs if needed. The demo is intentionally memory-only; no backend or production state is present.

## Retained material

- Guide Markdown/HTML: authored teaching and reference, source-linked, no external runtime dependencies.
- Order HTML: complete reduced teaching implementation, not the creator's source code.
- Two JPG frames: selected original full source frames at 900 and 1050 seconds, CLI-captured and visually inspected. Small evidence assets retained in ordinary Git with source attribution and hashes in `provenance.json`.
- Verification JSON: executed browser checks and limits. Human usability and production qualification remain open.

Raw source video, captions and intermediate artifacts remain in the ignored workspace. Recovery commands and source links are in the provenance record; remote material can change. No model weights or whole source repositories are bundled. Browser screenshots used during QA remain ignored per-run evidence.

The related source-first note was finalized by the CLI in the active worktree's `vb-workspace/notes/`. The durable dashboard links this guide. Other talk APIs are reference coverage, not implementations qualified by the order-board checks.
