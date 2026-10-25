# Ticket36 revision boundaries — throwaway comparison

Question: retain completed commands and checkpoint context without spending the cap on typing prefixes. Prototype branch `codex/spike-revision-boundaries`; no production integration.

## Frozen split and policies

Protocol/source windows reserved at af29e5a; reference labels locked at7b77096 before policy development. Development is the already observed round3 940–946s window from Traversy's Git crash course. Validation is a previously unscored856–864s window from that source plus33–42s from Fireship's Git Explained in100Seconds (`hwP7WQkmECE`). The second source contains edited command illustrations and recorded UI, not proof of command execution. The three windows total689 frames:180 development and509 validation. Full frame hashes and uncertain labels are in reference.json.

The preferred packet policy, collector and references were frozen in55aeb15 before validation OCR. validation-guard.json verifies their normalized Git contents remain identical to that commit; selection-freeze.json also preserves original working-file byte hashes. Line-ending normalization is disclosed, not a source-code change.

- Legacy: byte-identical original two-frame/first-string selector, invoked from the prior spike's candidate_frozen.py. Its event times now retain full-frame context for an explicit context ablation, rather than comparing crop payload with full-frame payload silently.
- Settled: exact whole-viewport OCR runs lasting at least0.2s, ranked by duration, sharpest representative. Repeated OCR variants remain distinct.
- Packets: new command occurrences acknowledged by a later prompt; response lines become context features. Initial-history counts and a15%-of-viewport downward-position test identify new occurrences. Greedy novelty selection; no response is interpreted as success. If no packet exists, use the frozen settled fallback, marked unverified.
- Grid: offsets0,.25,.5,.75 at caps1,2,3,4,6,8, full-frame payload, actual source seeks verified.

These are composed alternatives: PSM6, viewport/context retention and boundary rules change together relative to the legacy selector. This is not a boundary-only causal ablation or a general OCR-engine benchmark. No command-name vocabulary or reference label enters policies.py. All validation policies stayed unchanged; the preferred policy was not swapped after its weaker terminal result.

## Run

Use this branch's repo environment, FFmpeg, Tesseract5.4.0 and psutil. Exact source SHA-256 and package versions are in artifact-manifest.json / protocol.json. Capture stays in the repo experimental CLI; folders must be absent:

```powershell
uv run --no-sync python -m video_buddy.frames.spike_seek .scratch/seek-retained-source/SWYqp7iY_Tc.mp4 .scratch/revision-val-terminal 856 864
uv run --no-sync python -m video_buddy.frames.spike_seek .scratch/seek-retained-source/hwP7WQkmECE.mp4 .scratch/revision-val-ui 33 42
uv run --no-sync python docs/architecture/spikes/revision-boundaries/collect.py development
uv run --no-sync python docs/architecture/spikes/revision-boundaries/collect.py validation
uv run --no-sync python docs/architecture/spikes/revision-boundaries/legacy.py
uv run --no-sync python docs/architecture/spikes/revision-boundaries/audit_grid.py
uv run --no-sync python docs/architecture/spikes/revision-boundaries/compare.py development
uv run --no-sync python docs/architecture/spikes/revision-boundaries/compare.py validation
uv run --no-sync python docs/architecture/spikes/revision-boundaries/publish.py
```

The development capture is the previous `seek-real-scroll3` folder (940–946s); recreate with the same capture CLI when needed. Source retrieval uses that CLI's `--download-source`; validate hash before comparing exact bytes. Public URLs can change or become inaccessible. This run retained exact originals locally and claims no independent remote source backup. Do not overwrite frozen result files to represent a new run; copy the experiment directory or write new output names.

Initial development TSV parsing used CSV quote handling, causing Tesseract quotes to merge rows. The failure is preserved as dev-parser-failure.json.gz. collect.py was corrected to QUOTE_NONE before the policy/validation freeze; complete raw TSV is retained inside the compressed successful observations. No validation parse repair/tuning occurred. Every parsed word/line was checked to contain no leaked TSV separators.

## Evidence and limits

- *-ocr.json.gz: every viewport OCR output, raw TSV, line positions/confidence, frame time, sharpness and OCR time.
- development-results.json / validation-results.json: all selectors, caps, offsets, min/max state coverage, missed states, redundant state occurrences and literal audits. Prefix-only counts are manually scoped to the development window; validation prefix-only is null, not measured zero.
- grid-audit.json:144 actual seek requests, all matched decoded neighborhoods;12 nominal indices corrected in the new terminal window. Final scoring uses verified indices.
- reference.json / label-notes.json: single-agent visually reviewed reference, transition/character uncertainty retained; not independent human ground truth.
- selection-freeze.json / validation-guard.json: locked preference and unchanged implementation evidence.
- validation-memory.json / stage-costs.json: nominal20ms sampled summed collector-plus-child RSS and separate stage timings. Shared pages may double count, short peaks may be missed. Decode, annotation, legacy and monitor are excluded from that peak.
- *-selected.jpg: only three small representative comparison sheets in ordinary Git. Exhaustive inspection sheets/captured frames remain ignored under .scratch and are regenerable from pinned inputs; source files are not committed.

Within each window every method returns whole source images at the same output cap. Caps are not pixel/byte budgets; source resolutions and window lengths differ. Grid OCR literal checks reuse the common PSM6 audit and are not a cost of grid acquisition. New policies share the same OCR foundation. A full-frame image retaining a UI count does not mean the OCR viewport read that count or that execution was verified.

No user task-completion or correction-time study. Filename/punctuation/emoji errors remain in OCR. The preferred policy's repeated-command identity heuristic failed in locked terminal validation; no threshold was changed to rescue it. The settled policy's good validation result is bounded by these two windows and does not automatically replace the preferred policy or production default.

## Storage / recovery decision

Source code is changing original; protocol/reference/freeze files are a small explicit frozen reference set; compressed OCR/results and three JPEGs are useful generated evidence. Keep these in ordinary Git through review28. Keep large captured media and regenerable exhaustive sheets local/ignored with source/frame hashes and CLI reproduction. No LFS conversion, external upload, deletion, history rewrite or billing claim. Artifact inspection covers only the newly staged index candidates in this worktree, not prior experiment growth, ignored media backup or remote availability.
