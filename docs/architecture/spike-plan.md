# Spikes before integration

Status: proposed, not run. Date: 2026-10-24.

Primary job: apply a technique or build something and verify the result. A spike earns its place when an observation can change a design decision. These are throwaway experiments, not implementation commitments or a claim that any candidate wins.

## Recommended order

Start with S1: does an implementation packet improve task completion? Then S2: which visual evidence is necessary? Run S3/S4 against the failure cases those reveal. S5 qualifies shared state before orchestration integration. S6/S7 qualify adaptation and review UX. Attribution and collection search remain conditional S8/S9.

Timeboxes below are proposed active investigation budgets per spike, covering all options. Record model-download, setup and compute time separately. If an option cannot be evaluated inside the budget, record it as unresolved, not inferior. Do not integrate spike code automatically.

## Shared experiment contract

- Use four bounded, public or user-provided tasks: command/code tutorial, UI configuration, diagram-led technique and non-text demonstration. Select a representative task segment with enough context to perform it. Add discussion and retrieval fixtures only for the conditional spikes.
- Freeze media, intended result, reference commands/settings, essential actions, checkpoints and environment before comparing. A reviewer labels ground truth from the source; model-generated answers are not ground truth.
- Keep prompts, versions, model revisions, settings, hardware, latency, memory, downloads and failures with results. Match budgets within each comparison and disclose unavoidable differences.
- Record extraction coverage, evidence support and execution result separately. Never run extracted commands simply because a model produced them; inspect the task and execute only within an authorized disposable environment.
- Prefer a fresh task performer. If one person sees multiple variants, counterbalance order/use equivalent tasks and disclose learning effects. If no walkthrough is possible, report source correctness only and leave usability unanswered.
- Proposed absolute gate: no unsupported essential executable instruction may be presented as source-demonstrated. Gaps may remain explicit. Relative improvements must exceed observed run-to-run variation; do not invent a numerical quality target before measuring baseline.
- Each result includes deciding question, option, observed outcome, evidence paths, cost, limits, failed attempts and verdict: adopt / retain baseline / reject / unresolved. Repeat only comparisons where variability could reverse the decision.

## S1 — Does a guide help someone finish the task?

**Deciding question:** does an implementation packet improve successful task completion enough to justify a new output contract?

**Options:** A: current detailed note; B: ordered implementation packet with prerequisites, versions, observed commands/settings, checkpoints and gaps. Give both the same evidence and generation budget so richer extraction does not confound format.

**Throwaway:** generate both artifacts for two tasks; have a reader perform the task in a disposable environment. Stop after the deciding tasks, rather than building a guide engine.

**Observe:** verified result, interventions, time to first successful checkpoint, time searching the source, missing prerequisites, unsupported instructions and evidence lookup effort.

**Decision:** promote a guide contract only if it improves completion or materially reduces help/source searching without introducing unsupported actions. If both fail because evidence is missing, route that failure to S2 rather than declaring the format ineffective.

**Budget:** one day plus task-performer time. **Unlocks:** output contract and highest-value missing evidence. No dependency on a new runner.

## S2 — What visual depth recovers the essential actions?

**Deciding question:** what is the least costly visual pass that recovers the actions needed to execute the task?

**Options:** A: current sparse selected frames; B: chapter/time coverage plus agent-requested nearby frames; C: targeted short clips or dense timestamped sequences. Use a harness that genuinely supports the supplied modality; an unsupported video input is not an evaluated option.

**Throwaway:** use the same transcript and two source segments containing a brief UI action and a non-text/state-change demonstration. Compare both equal-budget first passes and incremental cost to close each gap.

**Observe:** essential-action recall, action order, exact settings recovered, unsupported observations, unresolved gaps, frame/clip volume and latency.

**Decision:** keep sparse frames where adequate; add targeted follow-up if it closes gaps; add temporal input only where order/motion failures persist. A new vision model is justified only after the current harness's failure is demonstrated. Local Qwen3-VL is a conditional additional comparison, not a prerequisite.

**Budget:** one day. **Unlocks:** frame-request interface, temporal evidence needs and capability checks.

## S3 — Which OCR produces usable commands and settings?

**Deciding question:** can a better OCR path reduce manual correction of exact screen text?

**Options:** A: existing EasyOCR; B: tuned Tesseract with region/scale/segmentation settings; C: pinned PaddleOCR detection/recognition. Give each the same fixed full-frame and cropped inputs; report preprocessing and detection costs separately.

**Throwaway:** label a small reusable set of approximately 30 regions from S1/S2: terminal punctuation, code, numbers, small UI labels, dark themes and low contrast. Tune on a subset; score on held-out regions.

**Observe:** exact command/setting match, character errors, region misses, correction time, box retention, CPU/GPU memory and installation friction.

**Decision:** replace or route OCR only if held-out exact-text/correction outcomes improve at acceptable measured cost. Retain originals/crops and explicit uncertainty. No general document benchmark can win this comparison.

**Budget:** half to one day excluding downloads. **Unlocks:** OCR engine choice and result schema.

## S4 — Which speech path preserves implementation-critical details?

**Deciding question:** which eligible configuration recovers the instructions and timings needed for these tasks?

**Options:** A: available captions; B: faster-whisper with word timestamps; C: exact installed CrisperWhisper distribution/model if eligible and available. Compare native timing against WhisperX alignment only on passages where native timing fails the evidence-location task.

**Throwaway:** manually reference short passages containing names, commands, numbers, silence and music. Compare ASR engines on matched hardware/model scale/settings where possible; report caption-source differences and unmatched configurations separately. Validate model/code licenses before treating an option as deployable.

**Observe:** critical-term/number errors, omissions/additions, WER/CER, timestamp boundary error, total elapsed time including transfer/preprocessing, memory and setup. Score transcript errors separately from alignment errors.

**Decision:** choose a default/fallback for the actual eligible deployment, not a universal winner. Keep captions if sufficient for orientation; do not present uncertain spoken commands as executable facts. Add forced alignment only if improved location accuracy is needed and observed.

**Budget:** one day. **Unlocks:** speech profile defaults, escalation and timing policy. Replaces conclusions, not historical measurements, from the old benchmark.

## S5 — What state model makes interrupted work safe to resume?

**Deciding question:** can atomic JSON manifests safely support intended concurrency, or is transactional state already necessary?

**Options:** A: file manifest, atomic writes and per-job locks; B: SQLite transactions with artifact files outside the database. Implement the same tiny stage interface, not the full production pipeline.

**Throwaway:** dummy acquisition/speech/analysis stages plus one small real media fixture. Inject interruption after acquisition, during artifact writing and before completion state; delete/corrupt an artifact; change configuration; start duplicate same-source jobs; simulate failed authentication and a failed optional stage.

**Observe:** stale-state detection, correct invalidation, duplicate downloads, lost edits, concurrent writer behavior, repairability, implementation complexity and stage-specific recovery messages. A readable ffprobe result alone does not establish full decode integrity.

**Decision:** prefer the simpler implementation that passes all intended failure/concurrency cases. Choose SQLite if necessary transactional guarantees cannot be achieved cleanly with file ownership and locks. Neither option justifies a distributed queue.

**Budget:** one day. **Unlocks:** durable runner/store choice. Can run independently of model spikes; integrate only after S1 defines outputs.

## S6 — Can adaptation remain useful without blurring source evidence?

**Deciding question:** can a source procedure be adapted to a different environment without hiding unsupported changes?

**Options:** A: source-faithful guide with explicit incompatibility gaps; B: two-layer guide with observed instructions and separately labeled adaptations, optionally supported by requested official documentation.

**Throwaway:** one tutorial with a known source/target version or platform mismatch. Keep evidence identical for source extraction; give the adaptation option a measured additional verification budget. Inspect proposed commands before authorized execution.

**Observe:** successful target result, mistaken version assumptions, fabricated flags, changed commands, provenance of each change and whether the reader can distinguish observed from adapted instructions.

**Decision:** promote adaptation only if the target walkthrough succeeds and all essential changes are visibly sourced or explicitly unverified. Otherwise ship the faithful guide plus gaps. A second model's agreement is not execution evidence.

**Budget:** half to one day. **Unlocks:** adaptation interface and revision/status rules. Depends on S1; use S2–S4 evidence if relevant.

## S7 — Which review experience helps at the moment of failure?

**Deciding question:** does a small review surface reduce the work needed to resolve a blocked guide step compared with Markdown/chat?

**Options:** A: Markdown/chat with timestamp and frame links; B: throwaway guide view with adjacent source evidence, visible gaps and “inspect this step / record my result” controls. Both use the same completed artifact; controls may simulate extraction requests but must be labeled.

**Throwaway:** ask a reader to locate an exact setting, identify an omitted prerequisite, correct one step and return after interruption. Observe behavior; do not ask which mockup looks nicer.

**Observe:** task completion, time/clicks to evidence, wrong interpretations, recovery success and ability to distinguish supported from tested.

**Decision:** build only the controls with demonstrated value. If linked Markdown is sufficient, retain it. A full application is not the default outcome.

**Budget:** half a day plus reader time. **Unlocks:** review UX scope. Depends on S1 artifacts; no backend integration required.

## Conditional spikes

### S8 — Does attribution change the next action?

Trigger only when conflicting instructions, decisions or named responsibilities matter. Compare no diarization, current sherpa-onnx and eligible pyannote Community-1 on the same labeled discussion. Measure correct attribution of consequential statements, overlap errors and correction effort, alongside DER/JER and runtime. Preserve raw overlap even if a display view uses exclusive turns. Acoustic clusters cannot establish names or owners. Promote diarization only if it reduces downstream misinterpretation. Budget: half to one day; independent of primary build-guide flow.

### S9 — Can the saved collection answer real implementation questions?

Trigger when finding prior solutions becomes a demonstrated bottleneck. Compare task-labeled files/current search against a rebuildable SQLite FTS5 index using approximately 20 real or representative queries, including exact commands and paraphrases. Measure correct evidence in the first results, time to usable answer, stale-version errors and source-link preservation. Only then compare embeddings/hybrid retrieval on the lexical failures. Budget: half a day for baseline/index, another half day only if a semantic comparison is justified. Unlocks retrieval, not canonical storage migration.

## Integration gate

For each spike, preserve the report and reproducible inputs separately from throwaway code. Record the branch/location actually used when experiments start; none exists yet. Review the evidence before selecting a winner. Integrate the smallest demonstrated improvement with compatibility checks and regression fixtures derived from failures. Keep unresolved options visible; installing a model or producing polished output is not a successful spike.

See [architecture proposal](workflow-proposal.md) and [tool research](../agents/research/video-workflow-architecture.md).
