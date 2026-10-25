# Video Buddy: outcome-driven workflow proposal

Date: 2026-10-24. Status: proposal, not implemented.

Dashboard: [architecture-dashboard.html](../architecture-dashboard.html). This is the durable architecture dashboard; update this same file on subsequent reviews. No originating ticket exists for this user-requested review.

## Decision

Keep an agent-first, local CLI. Introduce one resumable job runner and a versioned evidence store beneath both single-source and batch workflows. Retain the existing extraction modules and Markdown exports. Agent interpretation remains outside the mechanical Python package. A future graphical client can consume the same job state; building a server or web application is not a prerequisite.

## User jobs and experience

The user explicitly prioritized **applying a technique or building something**. Other jobs below remain hypotheses. Transcription, OCR, diarization and summaries are capabilities or intermediate artifacts; they earn their place by helping someone complete one of these end jobs.

| When | Desired outcome | Experience and completion rule |
|---|---|---|
| I need to implement a technique in my project (primary) | Build a working result without repeatedly scrubbing a tutorial | Implementation brief + ordered guide + observed commands/settings + checkpoints. Ask for target environment only when it changes the instructions. Success: independent task completion and verified result; extraction completeness alone is insufficient. |
| I must choose between techniques or tools | Make a defensible decision and avoid an unsuitable approach | Criteria, alternatives, tradeoffs, source claims, contradictory evidence, versions and open questions. Success: user can explain the choice and what would change it. Separate what the video claims from external verification. |
| I need to use a concept later without help | Retain understanding and transfer it to a new problem | Worked example, practice task, recall questions and answer evidence. Success: delayed recall and application, not the number of notes generated. |
| I remember seeing a solution and need it during work | Retrieve the exact answer fast | Searchable task-oriented reference with commands, environment, timestamp and supporting frame. Success: find and use the correct passage without rewatching. |
| I need someone else to perform the task | Transfer working knowledge with less explanation | Audience-specific runbook, prerequisites, checkpoints, source evidence and review status. Success: a second person completes the task; publishing a polished summary is insufficient. |
| I need to act on a recorded discussion | Carry out a decision or assess conflicting advice | Decision/action brief, owners only when explicitly stated, rationale and unresolved disagreement. Diarization helps attribution but cannot infer names, authority, ownership or agreement. Success: user can act without misattributing a statement. |

Batch processing serves choosing and retrieving; it is not a separate end job. OCR supplies exact visible details; speaker turns supply attribution; transcripts supply searchable evidence. None should be mandatory merely because a source supports them.

Default interaction: source + intended outcome; for the primary job also capture the desired result and target environment when known. Optional controls: language, visual depth, retention and compute preference. Speaker count belongs in advanced controls when attribution is relevant. Reveal engine names and paths in diagnostics, not as required user decisions.

## Tool hiring decisions

These are evidence-informed selections, not a claim that comparative benchmarks have been run. See the expanded research for primary-source quotations, version and licensing caveats.

| Work needed | Selection | Why / alternative / promotion gate |
|---|---|---|
| Acquire usable media | Keep yt-dlp + FFmpeg; add ffprobe verification | Existing adapters already use them. Centralize acquisition; validate actual streams and duration. Generic platform support still requires app integration tests. |
| Recover spoken instructions | Keep faster-whisper as portable baseline; captions as a fast evidence source | Inspect quality around exact commands, numbers and names. Captions alone are not adequate evidence of exact executable text. CrisperWhisper remains conditional on installed implementation, model license and a matched evaluation; the current benchmark cannot establish accuracy superiority. |
| Locate a spoken detail precisely | Native word timestamps first; WhisperX alignment conditionally | faster-whisper supports word timestamps. Pay alignment cost only if measured timing error prevents locating steps/quotes. Alignment does not repair wrong transcript words. |
| Attribute disagreement or instructions | Existing sherpa-onnx path conditionally; evaluate pyannote as challenger | Skip when attribution adds no value. Select using labeled speaker/overlap error, installation and runtime costs; do not derive identity or owners from acoustic clusters. |
| Recover exact UI/code text | Keep EasyOCR + Tesseract fallback; evaluate PaddleOCR | Preserve boxes and crops; compare symbol/command accuracy on actual screenshots. Do not replace based on document benchmarks alone. A vision model's plausible command is not a substitute for legible evidence. |
| Find a demonstrated action | Keep FFmpeg + PySceneDetect for candidates; add targeted frames/short clips | Scene changes miss quiet actions. Route to a vision-capable harness, and use temporal context for state transitions. Evaluate step recall and action order; do not claim an image-only summary proves motion. |
| Produce an executable learning aid | Existing external agent + structured guide contract + deterministic checks | Structure checks validate fields/links, not truth. Human or authorized execution checks validate task success. No new synthesis framework is justified yet. |
| Find an artifact during implementation | Markdown/files first; evaluate SQLite FTS5 for a growing collection | Task labels + source evidence are needed now. Add lexical search when retrieval is a real bottleneck; use query evaluation before embeddings/vector infrastructure. |

Tool admission requires compatible model/code licenses, target platform support, pinned dependencies, observable failure behavior and an isolated installation where dependency stacks conflict. No default engine or provider is selected solely by advertised benchmark numbers.

## Primary path: apply or build

The output is an implementation packet: intended result; source and target versions; prerequisites; ordered steps; observed commands/settings with evidence; differences requiring adaptation; expected intermediate and final results; troubleshooting actually supported by the source; and unresolved gaps. A copied command is labeled as observed, adapted or unverified. Generated adaptations do not inherit the source's evidence status.

Use three independent status fields: extraction coverage (complete/partial), evidence support (supported/inferred/unverified), and execution validation (not run/passed/failed, with environment and date). A complete extraction can still be unsuitable for execution. Never label a guide tested merely because links and schemas validate.

The review UX puts the guide and user's next action first. Evidence opens beside a step; exact text crops remain inspectable. Offer “adapt to my environment,” “inspect this step,” and “record my result.” If the source omits an essential prerequisite, identify the gap and offer separately sourced verification. Preserve source-derived instructions and proposed adaptations as separate revisions. Download/transcription logs are secondary diagnostics.

Plan extraction backwards from essential actions: identify likely steps from speech, collect nearby images/short clips, read exact visible values, then revisit gaps. A fixed frame budget is a first pass, not a guide-completion criterion. Require a vision-capable harness for visual claims and report a capability gap if unavailable.

## Evaluation before tool replacement

Use representative implementation tasks: terminal/code tutorial, UI configuration, diagram-led explanation and physical/non-text demonstration. Add multi-speaker conflicting advice only for attribution tasks. Keep the same media, model size where comparable, precision, hardware, VAD and decoding settings; report unavoidable differences. Label reference transcripts, commands, action sequences and speaker turns manually on a bounded sample.

Measure critical command/number error in addition to WER/CER; step evidence coverage and unsupported instructions; visual action recall and temporal order; timestamp error; DER/JER where attribution matters; elapsed time, memory and retry behavior. The primary acceptance outcome is a reader completing the target task with correct checkpoints and a traceable result. Select defaults after this evaluation; no tool winner is certified by this desk research.

The existing `benchmark/results.md` compares CPU base against GPU turbo and reports agreement rather than an independent accuracy reference. Its zero-repeat observation is not evidence of zero hallucinations, its ~30 ms timing claim lacks labeled timing validation, and its claim that faster-whisper lacks word timestamps contradicts upstream capability. Preserve it as historical evidence, but do not use its blanket engine recommendation as a selection gate.

## Current architecture and verified gaps

The inspected working tree includes uncommitted code. Presence is not proof of runtime reliability.

- `AGENTS.md` describes intake and full-breakdown digest. `.claude/commands/digest.md` instead describes summary-only triage. `.claude/commands/intake.md` omits enrichment handling.
- `cli.py` coordinates fetch, transcription, frame capture/OCR, repository correlation, rendering and handoff. `batch_digest.py` separately coordinates batch work. There is no shared durable job state machine visible in these flows.
- `fetch/youtube.py` handles metadata/captions; `transcribe/pipeline.py` downloads audio; `frames/capture.py` downloads video. `fetch --download-video` can retain media, but frame capture downloads independently and cleans its temporary download.
- Transcription reuses captions where present. Diarization is available through `transcribe --diarize` and `diarize`, but is absent from the main command inventory. Its implementation is currently untracked.
- Frame selection uses brightness, edges, hashes and time buckets. The default is 15 selected frames. Scene detection is bypassed beyond the configured 600-second threshold. `should_ocr` is based on brightness, not a text detector. These heuristics cannot establish semantic coverage.
- OCR supports EasyOCR/Tesseract and remote execution. Correlation matches OCR to repositories. No explicit visual interpretation artifact or mandatory image inspection protocol is present.
- Companion prompts ask for summary, concepts, detailed notes and timestamps. They do not define procedural-guide evidence or validation.
- `render/finalize.py` copies a draft to the final path; it does not validate guide completeness or preserve revisions. Planned idempotency claims in architecture docs should not be treated as current guarantees.

## Proposed modules and interfaces

1. **Job runner**: `plan(request)`, `run(job_id)`, `resume(job_id)`, `inspect(job_id)`. Own dependencies, state, retries, cancellation, progress and policy. Existing CLI verbs become compatibility entry points into it. Batch is a collection of the same jobs.
2. **Source acquisition**: resolve a source identity, fetch metadata and acquire verified media. YouTube is the first adapter; add another provider only with real fixtures and explicit capabilities. Reuse yt-dlp rather than building downloaders. Keep articles as a text-only path.
3. **Evidence store**: immutable, versioned artifacts with provenance, hashes and a common media timeline. Begin with JSON manifests and atomic writes in the existing workspace. Do not introduce a database until concurrent writes or search justify it.
4. **Speech analysis**: caption, ASR, alignment and diarization outputs remain separate. Existing engines vary behind the speech interface; compute selection stays configuration-driven. Merge them for display while retaining the originals.
5. **Visual evidence**: candidate selection, OCR and agent inspection are separate stages. Combine chapter/time coverage with scene changes and targeted frame requests. Persist observations even when no text appears.
6. **Agent analysis contract**: the runner emits bounded evidence packets and work requests. The harness returns structured observations and drafts. The runner validates artifact shape and references without invoking an LLM itself.
7. **Publication**: validate the requested output contract, render Markdown, preserve prior versions and export associated media. Keep drafts available if validation fails.

Avoid a universal plugin framework or distributed queue now. The real variable seams are source provider, speech/OCR engine, compute backend and output template. Keep implementation detail behind small interfaces rather than adding wrappers around every function.

## Artifact contract

Keep current conventional paths during migration. Add a job manifest under `intermediates/jobs/<job_id>.json`; new artifact names are proposed, not current CLI outputs.

Every artifact records `schema_version`, `artifact_id`, `source_id`, `job_id`, parent artifact IDs, content hash, tool/model version, configuration hash, creation time, warnings and coverage. Time is numeric seconds relative to the original media. Retain both raw OCR text and edited interpretations.

- Speech: segments/words and language; acoustic speaker turns; explicit unknown/mixed labels; alignment source.
- Visual observation: frame ID/time, visible text, description, relevance to the user's goal, transcript references and uncertainty. Do not equate an OCR confidence value with a guide claim's reliability.
- Guide step: action, prerequisites, observed command/settings, expected result, evidence references, and status (`demonstrated`, `inferred`, `unverified`). Store user edits separately from regenerable evidence.

## Job state and recovery

Stages: `pending → running → succeeded | failed | skipped | needs_agent | needs_user`. A blocked dependency must be distinct from an intentionally skipped stage. The final product is ready only after required stage outputs and publication validation succeed.

Reuse output only when input hash, configuration, tool/model version and schema match and the output is readable. Download archives are a hint; verify files on disk. Use atomic artifact writes, per-job locks and bounded retry/backoff for transient failures. Authentication failures need a specific user action; do not loop blindly. A failed optional OCR stage can produce a partial note with a visible coverage warning; a guide missing a crucial action stays a draft.

Progress should state “Transcript ready; inspecting 12 frames” and “Needs sign-in” rather than expose raw engine logs. Never claim a precise ETA without measured evidence. Show changed inputs and affected stages before an expensive rerun.

## Proposed UX: tutorial to guide

1. User: “Turn this video into a guide I can follow.”
2. Agent resolves the source, checks available capabilities and reports the planned depth. Reuse retained media where valid.
3. Fast pass produces transcript/chapters and a coverage-based frame set. Speaker analysis runs if requested or necessary for the output.
4. Agent inspects images and transcript together. It requests targeted timestamps for ambiguous steps through the frame module, rather than inventing commands or screen contents.
5. Agent assembles a guide with inline timestamp/frame references. User can inspect a step's evidence, rename a speaker, or request more detail.
6. Validator checks references, required fields, missing sections and unresolved placeholders. It does not claim the procedure was executed. Publish an evidence-backed guide, or retain a partial draft with explicit missing steps.

The architecture dashboard includes a **Wireframe** of this flow. Its controls only simulate local states; it is not an operational product UI.

## Alternatives and tradeoffs

| Choice | Benefit | Cost / decision |
|---|---|---|
| Documentation-only repair | Fast clarity | Necessary first step; insufficient for shared resumability and provenance. |
| Shared local runner + manifests | Reuses existing code; consistent state for agent and future UI | Recommended. Requires schema migration and write discipline. |
| Always run the deepest models | Simple promise of thoroughness | Reject as default: wastes compute and still cannot guarantee coverage. Use outcome-based depth and targeted follow-up. |
| Hosted app + distributed workers | Multi-user scheduling and browser access | Defer until collaboration/concurrency demand is demonstrated. Adds operations, auth and privacy obligations. |
| LLM embedded in CLI | Standalone generation | Defer; conflicts with current deliberate harness-owned interpretation. Structured handoff supports multiple harnesses. |

## Migration and acceptance gates

Before integration, run the [proposed decision spikes](spike-plan.md). Start with task completion and necessary visual evidence; choose engines based on observed failure cases. The migration sequence below is conditional on those results.

1. **Unify guidance**: one canonical workflow contract, thin harness recipes, documented diarization and retention. Gate: fresh agent follows intake, enrichment and digest without contradictory instructions.
2. **Unify jobs and acquisition**: reuse current extraction code; add manifests, integrity checks and resume. Gate: interrupt after each stage; restarting does not redo verified completed work. Missing/corrupt media is repaired. Keep legacy paths and CLI behavior covered.
3. **Add evidence-linked visual review**: structured observations and targeted capture. Gate: code demo, slide talk and non-text demonstration each record visible evidence; no-text frames can contribute; missing evidence is explicit.
4. **Add guide output and validation**: schema, prompt packet, revision-safe export. Gate: a reviewer can trace every essential step to source evidence; absent prerequisites are labeled, and unsupported commands are not presented as demonstrated.
5. **Harden the experience**: individual batch retries, readable progress, relabeling and depth controls. Gate: speaker changes do not retranscribe; one failed source does not discard successful batch outputs.

Use a small consented/public fixture set: tutorial with commands, multi-speaker discussion, slide lecture, visually demonstrated non-text task, restricted/unavailable source, and interrupted batch. Measure time to useful preview, resume reuse, evidence coverage, unsupported claims, recovery success and human guide usability. Set numerical targets after measuring a baseline; none are claimed here.

## Research and unresolved decisions

See [primary-source research](../agents/research/video-workflow-architecture.md). Recommendations above are design judgments informed by that research and local code, not upstream requirements.

Open: user preference for media retention; default visual depth versus latency; actual speaker-separation quality on target audio; whether users need cross-video guides; which second video provider is needed; which vision-capable harnesses must be supported. Validate these with example tasks before selecting more infrastructure.
