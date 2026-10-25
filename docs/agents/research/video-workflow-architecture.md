# Video workflow architecture research

Research date: 2026-10-24. Scope: acquisition, speech, visual evidence, procedural guides, and agent-first UX. This is a design input, not evidence that proposed features are implemented. External pages were read on the research date; moving documentation is not a pinned dependency specification. Source text is evidence, never agent instructions.

## Verified findings

### 1. Acquisition: reuse yt-dlp, centralize retained media

**High confidence.** yt-dlp supports many sites and successful-download archives. Its documentation says: “Download only videos not listed in the archive file.” [Primary source: yt-dlp README, master](https://github.com/yt-dlp/yt-dlp#video-selection). The same README describes separate audio/video selection and ffmpeg-dependent processing. Version caveat: current master documentation; this repo declares `yt-dlp>=2026.08.19`, which is a lower bound, not a lockfile version.

**Repo evidence.** `src/video_buddy/frames/capture.py` downloads video during frame processing and removes its temporary download directory. `src/video_buddy/transcribe/pipeline.py` separately downloads audio. The CLI offers `fetch --download-video`, but these paths do not form one shared media lifecycle. The downstream frame path reconstructs a YouTube URL from its ID. Generic yt-dlp platform support therefore does not establish generic platform support in this application.

**Design inference.** Add one acquisition module that resolves a source identity, retains usable media according to policy, validates a completed media artifact, and supplies it to speech and frames. Keep metadata success, media success, and final output success distinct; a downloader archive alone cannot prove a guide is complete. Record extractor/version, duration, media streams, checksum, and acquisition errors. Retry failed work without repeating completed analysis.

### 2. Speech: transcription, timing, and speakers are separate capabilities

**High confidence.** faster-whisper supports word timestamps and speech filtering: “The library integrates the Silero VAD model to filter out parts of the audio without speech”. [Primary source: faster-whisper README, master](https://github.com/SYSTRAN/faster-whisper#vad-filter). Its published performance tables use particular model, precision, beam and hardware settings; they are not a throughput guarantee for this repo. Version caveat: repo declares `faster-whisper>=1.0.0`; documentation describes current master.

**High confidence.** WhisperX explicitly reports: “Overlapping speech is not handled particularly well by whisper nor whisperx” and “Diarization is far from perfect”. It also documents alignment failures for words outside the alignment model dictionary. [Primary source: WhisperX README, master](https://github.com/m-bain/whisperX#limitations-). The repo declares optional `whisperx>=3.8.4`; verify the installed version before choosing features.

**High confidence.** sherpa-onnx provides distinct pretrained segmentation and embedding models and APIs for speaker diarization. Supporting snippet: “Pre-trained models for speaker segmentation”. [Primary source: sherpa speaker diarization documentation, documentation label 1.3](https://k2-fsa.github.io/sherpa/onnx/speaker-diarization/index.html). This documentation label is not the Python package version; this repo declares `sherpa-onnx>=1.12.14`.

**Repo evidence.** `transcribe/pipeline.py` already reuses captions and offers WhisperX alignment. Current working-tree `transcribe/diarization.py` independently computes speaker turns and labels mixed segments; `cli.py` offers `diarize` and `transcribe --diarize`. These are implementation observations, not model quality evaluations.

**Design inference.** Preserve transcript text, optional aligned words, and acoustic turns as separately versioned artifacts on one media timeline. Keep stable anonymous speaker IDs; allow user-supplied names without implying biometric identity. Do not display one speaker as certain when turns overlap. Default to captions for fast notes, permit forced ASR for poor captions, and request alignment/diarization when the user's output needs them. Expose missing timing and unknown speakers as inspectable quality issues.

### 3. Visuals: change detection, text recognition, and interpretation solve different problems

**High confidence.** PySceneDetect ContentDetector “Detects shot changes using weighted average of pixel changes in the HSV colorspace.” [Primary source: PySceneDetect detector documentation, 0.7.1](https://www.scenedetect.com/docs/latest/api/detectors.html). Version mismatch: this repo allows `scenedetect>=0.6`; evaluate against the locked runtime before relying on 0.7.1 interfaces. Pixel-change detection does not establish importance to a particular task.

**High confidence.** FFmpeg supplies timestamped scene-change metadata: “Detect video scene change.” [Primary source: FFmpeg filter documentation, moving development documentation](https://ffmpeg.org/ffmpeg-filters.html#scdet). This offers another deterministic candidate-generation mechanism, not proof that a frame contains useful instructional information. The installed ffmpeg version is not established by this research.

**High confidence.** EasyOCR separates detection from recognition. Supporting snippets: “Detect text boxes only.” and “Recognize characters from text boxes.” [Primary source: EasyOCR API documentation, unversioned](https://www.jaided.ai/easyocr/documentation/). It also exposes language, contrast, rotation, and box settings. This repo declares `easyocr>=1.7`; tune settings against actual tutorial frames.

**Repo evidence.** `frames/capture.py` ranks brightness/edges, deduplicates hashes, and limits frames to a configurable count (default 15). `should_ocr` tests brightness. `frames/ocr.py` joins EasyOCR detections into a string, losing spatial structure in the stored result. `face_area_ratio` is a constant placeholder in scoring. Scene analysis defaults to bypassing full scene detection beyond 600 seconds.

**Design inference.** Build a visual evidence module with bounded candidate sampling, real text-box detection, spatial OCR results, and agent visual observations. Combine time coverage, chapters, changes, and transcript cues; let the agent request additional frames around a step. Store original frame time, crop coordinates, OCR confidence, and interpretation separately. Treat absence from a sparse sample as unknown, not proof that a visual event never occurred. Evaluate command text, diagrams, UI transitions, and quiet demonstrations independently.

### 4. Guides: procedure structure and citation quality need explicit checks

**High confidence.** Microsoft advises: “Use a separate step for each instruction.” It also recommends specifying where an action occurs and including actions that complete a procedure. [Primary source: Microsoft Style Guide, updated 2026-04-02](https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions). This is writing guidance, not a video extraction algorithm.

**High confidence.** ALCE evaluates evidence-grounded generation along “fluency, correctness, and citation quality”. [Primary source: Gao et al., Enabling Large Language Models to Generate Text with Citations, v2, 2023-10-31](https://arxiv.org/abs/2305.14627). It supports assessing citation support separately from fluent writing; it does not validate this product's proposed guide workflow.

**Design inference.** Add a guide artifact containing outcome, prerequisites, versions/environment, ordered steps, exact observed commands/settings, expected results, troubleshooting, and unresolved gaps. Each substantive step references transcript intervals and/or frame evidence. Distinguish source-demonstrated facts from inferred connective instructions. Require an explicit gap marker when the video skips a prerequisite; do not silently invent executable commands. A guide can be complete as an extraction while still marked untested as a procedure.

### 5. UX: reveal capability and recover from mistakes

**High confidence.** Microsoft's validated human-AI guidance addresses behavior “upon initial interaction, during regular interaction, when they’re inevitably wrong, and over time.” [Primary source: Microsoft Research, project established 2019-06-04](https://www.microsoft.com/en-us/research/project/guidelines-for-human-ai-interaction/). This is general human-AI prior art, not evidence of the particular users' preferences.

**Design inference.** Begin with the outcome: understand a video, reproduce a task, compare a batch, or inspect what was shown. Present progress in user terms (source saved, speech ready, visuals checked, draft ready). Include useful partial results, a specific recovery action, evidence inspection, speaker correction, and local reruns of affected stages. Preserve the repo's agent-first experience; a durable local review page can complement chat without requiring a hosted product.

## Proposed module architecture

1. **Source acquisition:** `resolve(source)` and `acquire(source, media_policy)` hide URL normalization, provider adapters, authentication integration, retries and media validation.
2. **Run orchestration:** `plan(intent, source, quality_budget)` and `resume(run_id)` own dependencies, stage state, cancellation, cache fingerprints, warnings and output lineage. Start with a file-backed run manifest and atomic writes; add a database only when concurrency/query requirements justify it.
3. **Evidence production:** speech and visual modules produce versioned artifacts on a common timeline. Existing local/SSH compute adapters remain config driven.
4. **Agent synthesis:** a task packet names evidence paths, requested output schema, gaps, and acceptance criteria. The external agent writes notes, guides, or digest entries; no LLM SDK needs to enter the mechanical package.
5. **Validation and publishing:** validate evidence references, placeholders, output structure and media links before finalization. Publishing is distinct from mechanical pipeline success. Preserve human edits through revisions or explicit merge targets.

Canonical evidence records should contain `evidence_id`, `source_id`, `media_revision`, `start`, `end`, `kind`, artifact reference, producer/version, quality signals, and optional crop/region. A guide step references evidence IDs rather than copying untraceable prose.

## User jobs and acceptance measures — hypotheses to test

| Job | Experience | Proposed acceptance measure |
|---|---|---|
| Understand without rewatching | Concise notes with timestamped supporting moments | Readers answer source questions and locate support |
| Reproduce a demonstrated task | Ordered guide, exact observed inputs, expected outcomes | Independent walkthrough; unsupported steps counted |
| Recover visual information | Timeline and frame inspection beside speech | Relevant slide/UI/diagram recall on a labeled set |
| Follow multiple speakers | Editable anonymous speaker labels | Speaker error and overlap cases on representative talks |
| Process a backlog | Batch progress, usable partial output, resume | Failed-item retry avoids repeating completed work |
| Trust and reuse output | Evidence links and visible gaps | Citation support and coverage evaluated independently |

These measures have no baseline yet. Avoid numerical quality promises until a small representative benchmark is labeled and run.

## Could not verify / decisions requiring experiments

- Best default ASR engine for this user's hardware, terminology, and languages. Existing benchmark artifacts can inform selection but do not establish universal quality.
- Best diarization model, threshold, and handling of simultaneous speakers for real inputs. A comparative evaluation is needed.
- Frame budget that reliably captures tutorial steps. Fifteen frames may be sufficient for slides and insufficient for detailed UI demonstrations; evaluate recall and time/cost.
- Best semantic vision provider. No provider was benchmarked, and local versus remote privacy/cost constraints are not established. Keep the first semantic workflow in the existing agent harness, with explicit evidence outputs.
- User preference for a standalone GUI. Agent-first chat plus Markdown is an established repo intent; a new full product UI is a design option, not a validated requirement.
- Acquisition durability under restricted sources and future site changes. Official tool capability does not establish access to any specific URL.

## Suggested order

First reconcile agent contracts and define note/guide/digest acceptance. Next add retained media plus resumable run manifests and evidence IDs. Then add a bounded visual-review workflow and guide validation. Finally compare models and build a richer review interface when actual correction tasks justify it. Keep the existing CLI verbs as compatibility wrappers throughout migration.

## Follow-up: hire tools for the downstream job

Reviewed again on 2026-10-24. This section supersedes any interpretation that existing dependencies were endorsed as universally best. **Keep** means suitable infrastructure to retain; **conditional** means invoke only for a relevant output; **evaluate** means a candidate has documented capability but has not won a local comparison; **defer** means no demonstrated need justifies the added complexity. None of these choices establishes model quality without representative evaluation.

### End needs, artifacts and processing policy — product hypotheses

The user's subsequent clarification makes **apply a technique / build something** the primary job. Treat the implementation guide as an execution packet: target outcome, environment and source versions, prerequisite checks, ordered actions, exact inputs, expected checkpoints, recovery, evidence and unresolved gaps. Keep three independent statuses: extraction coverage, evidence support and real execution verification. A fully extracted guide can remain untested; a successful walkthrough on one environment is not universal compatibility. Other uses below are secondary hypotheses.

| End need | Artifact the person will use | What makes it useful | Processing hired for that use |
|---|---|---|---|
| Decide what deserves attention or whether to adopt an approach | Decision brief: relevance, alternatives, tradeoffs, assumptions, follow-up questions | Helps make a specific decision; distinguishes a speaker's assertions from corroborated facts | Captions/ASR and targeted evidence; compare sources when requested; diarization only when provenance or disagreement affects the decision |
| Implement or reproduce something | Runnable guide/checklist: prerequisites, versions, steps, commands, checkpoints, gaps | A different person can complete the task and recognize success/failure | Targeted visual sequences, exact OCR, linked repository revision and independent walkthrough; fluent summary is insufficient |
| Learn a skill and remember it later | Worked example, explanation, exercises and retrieval questions with answer evidence | Learner can explain and apply the idea later, including a new case | Concept synthesis plus active practice; no need for exact speaker identity in most lessons |
| Brief a teammate or teach someone else | Shareable explanation with selected figures, examples, source links and scope | Recipient understands without the original video; can inspect disputed statements | Evidence-backed synthesis and accessible text for visual material; verbatim quotes only where the wording matters |
| Compare opinions or support a recommendation | Claim/evidence matrix with source, speaker role, conditions, disagreement and unknowns | Preserves differences instead of flattening them into one summary | Multi-source synthesis; conditional diarization; verify quote text against audio where consequential |
| Find and reuse something months later | Searchable reference with source/time links, stable IDs, tags and preserved assets | User retrieves the right fact or example quickly and checks its original context | Index transcript, OCR and curated claims; stable links and source freshness; embeddings only after lexical search misses are measured |

Speaker turns, transcripts and frames are intermediate evidence. They become user value through one of these downstream uses. Ask for or infer a purpose and audience; do not ask users to select engines. A single source can support multiple artifacts without rerunning extraction. These jobs need interviews and observed tasks before defaults are fixed.

### Comparative selection record

| Job for the tool | Recommendation | Alternatives and rejection/selection trigger |
|---|---|---|
| Obtain media reliably | **Keep yt-dlp + FFmpeg; add ffprobe inspection.** Centralize acquisition and retained media. | Custom browser download automation is a fallback for an actually unsupported source, not the first implementation. Provider support needs real application fixtures, not just yt-dlp's site list. |
| Produce understandable speech text | **Keep faster-whisper as an available CPU/GPU baseline; use available captions for low-cost orientation.** Escalate uncertain key passages for guides/quotes. | **Conditional CrisperWhisper** for verbatim detail or timing, subject to exact model/version/license and local quality comparison. No automatic winner follows from the existing benchmark. |
| Tie a known transcript to precise audio locations | **Conditional alignment.** Retain WhisperX as a candidate when timings affect quote playback, speaker assignment or frame targeting. | Native word timestamps may suffice for coarse references. Compare boundary errors and missing/alignment-failed words before adding another model pass. |
| Preserve attribution/disagreement | **Conditional sherpa-onnx** as the existing local implementation; **evaluate pyannote Community-1** on target discussions. | Skip diarization when it does not change the final artifact. Community-1 adds gated model access/token setup; its exclusive display turns must not erase original overlapping turns. |
| Generate visual candidates | **Keep FFmpeg/PySceneDetect**, combined with chapter/time coverage and step-directed capture. | Pixel cuts miss static-screen UI changes; sparse stills miss order/motion. Compare bounded clips or denser timestamped sequences for action-heavy tasks. No scene detector alone proves coverage. |
| Recover exact text from a screen | **Keep EasyOCR baseline, evaluate PaddleOCR, retain tuned Tesseract CPU fallback.** Preserve boxes and confidence. | Evaluate on small terminal text, punctuation, dark themes, diagrams and multilingual UI. OCR character error and exact command match matter more than document-wide average accuracy. |
| Understand a diagram or demonstrated action | **Conditional vision-capable harness**, using timestamped images/sequences and structured evidence. **Evaluate Qwen3-VL** only if local inference is a real need. | Do not select a provider on benchmark marketing or assume a still-image model understands motion. Compare critical-step recall, order, unsupported claims, latency and hardware memory. |
| Turn evidence into an artifact | **Keep external agent synthesis; add purpose-specific schema and validation.** | A schema validator proves shape/references, not correctness. A second model is a critic candidate, not independent ground truth; human walkthroughs are essential for guides. |
| Retrieve saved knowledge | **Keep Markdown/JSON as canonical; evaluate a rebuildable SQLite FTS5 index when retrieval is required.** | Defer vector database and embeddings until a labeled query set shows lexical search misses paraphrases that matter. Keep source IDs through chunking and search. |

### Newly verified tool facts and caveats

**High confidence — acquisition inspection.** ffprobe describes its purpose as “gathers information from multimedia streams” and supports machine-readable output. [FFmpeg ffprobe documentation](https://ffmpeg.org/ffprobe.html), moving documentation, accessed 2026-10-24. **Inference:** inspect streams/duration and use a decode/error check where needed; a successful metadata probe alone does not establish that every frame decodes or a download is complete.

**High confidence — faster-whisper word timings are real.** Its official example sets `word_timestamps=True`. [faster-whisper README, Word-level timestamps](https://github.com/SYSTRAN/faster-whisper#word-level-timestamps), master, accessed 2026-10-24. This is upstream capability, regardless of whether this repo's baseline invocation requested or serialized those words. The same source documents GPU execution; CPU-only is a local comparison configuration, not a product limitation.

**High confidence — CrisperWhisper is a specialized and separately licensed choice.** Its current reference documents “verbatim + intended modes” and states standard weights have a “non-commercial research license”; the inference code is MIT. [CrisperWhisper DOCS.md](https://github.com/nyrahealth/CrisperWhisper/blob/main/DOCS.md), main, accessed 2026-10-24. It documents a custom CTranslate2 backend and a Transformers backend, with separate install extras. Current main documents model shorthands including `turbo`; standard and Pro weights have distinct licensing. **Version caveat:** local benchmark reports package 2.0.2; upstream releases show 2.0.3. Do not infer the installed worker's model revision or license from the package/code license. Verify those exact artifacts before selecting a default. This is a tooling eligibility observation, not legal advice.

**Repo evidence:** `workers/crisperwhisper_worker.py` imports `crisperwhisper.CrisperWhisperModel`, requests `word_timestamps=True` and defaults to `turbo` plus verbatim mode. It converts non-WAV/FLAC audio to 16 kHz mono WAV. `compute/ssh.py` probes a separate configured Python environment. This supports retaining the adapter, not claiming that its environment is installed, pinned or suitable for every user's deployment.

**High confidence — pyannote is a genuine comparison candidate with onboarding cost.** Community-1 lists “exclusive speaker diarization” and setup requires “Accept user conditions”. [Community-1 model card](https://huggingface.co/pyannote/speaker-diarization-community-1), model `community-1`, benchmarks labeled 2025-09, accessed 2026-10-24. The card supports local/offline execution after acquiring files, known speaker counts, GPU use and separate ordinary/exclusive outputs. Its benchmark comparisons do not include this repo's exact sherpa setup, so they cannot establish the winner here. Preserve overlap evidence even when rendering an exclusive turn view.

**High confidence — PaddleOCR is an OCR candidate, not a reason to adopt its whole document stack.** Its general pipeline separates “Text Detection Module” and “Text Recognition Module”. [PaddleOCR general OCR documentation](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/OCR.en.md), moving main documentation currently describing 3.7/PP-OCRv6, accessed 2026-10-24. It also permits optional orientation/unwarping stages. **Inference:** benchmark only detection/recognition relevant to video screens; do not pay document-layout costs without a use case. Pin the evaluated model/engine because moving defaults and runtimes change.

**High confidence — Tesseract fallback needs task-specific tuning.** Its docs say “By default Tesseract expects a page of text” and recommend different segmentation for regions. [Tesseract quality guidance](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html), moving docs covering multiple major versions, accessed 2026-10-24. It documents rescaling, binarization, segmentation and dictionary controls for codes. **Inference:** raw full-frame OCR is an unfair baseline for terminal/UI crops; evaluate crop/scale/segmentation settings without assuming preprocessing always helps.

**High confidence of capability claim, unverified local quality — local temporal vision.** Qwen3-VL documents “Text–Timestamp Alignment” and video inference examples. [Qwen3-VL official repository](https://github.com/QwenLM/Qwen3-VL), main, accessed 2026-10-24. This makes it a concrete candidate for local video interpretation. No local model size, quantization, memory use or task accuracy was measured. Retain time-indexed evidence and compare it with the current harness on the same tasks before adoption; upstream capability claims do not guarantee tutorial-step recall.

**High confidence — lexical retrieval does not need a vector database.** SQLite describes FTS5 as providing “full-text search” and documents ranking, highlighting and snippets. [SQLite FTS5 documentation](https://www.sqlite.org/fts5.html), moving documentation, accessed 2026-10-24. **Inference:** a rebuildable lexical index is a proportionate first addition when finding saved artifacts becomes a real job. Validate build support in the packaged SQLite; ranking is not factual verification.

**High confidence in general learning prior art; product effect unverified.** The authors' review states “Tests enhance later retention more than additional study”. [Roediger and Karpicke, The Power of Testing Memory](https://www.psychologicalscience.org/journals/perspectives/j.1745-6916.2006.00012.x/), September 2006. **Inference:** if the goal is learning, add practice/retrieval artifacts rather than optimizing only note length. This does not prove generated quizzes are accurate, that a particular review schedule is optimal, or that this product improves learning. The original 2006 experiment publisher/PubMed/Purdue links were attempted but not reliably accessible in this run; no experimental effect size is claimed.

### Correct the interpretation of the local ASR benchmark

The following are evidence-assessment findings about [benchmark/results.md](../../../benchmark/results.md), dated 2026-08-23; this review does not rewrite the original experiment or fabricate new runs.

1. **The speed result compares deployments.** CPU/base/int8 versus GPU/turbo/float16 changes hardware, model and precision together. The reported elapsed times can describe those recorded configurations; they do not isolate an engine advantage. Include decoding/batch settings, model load/warmup, transfer and preprocessing when repeating it.
2. **No words in an output is not no word-timestamp capability.** The claim that faster-whisper only has segment timings conflicts with its official interface. Re-run with requested/serialized word timings before comparing accuracy or timing cost.
3. **Agreement is not accuracy.** Two transcripts can agree on the same wrong name or omit the same sentence. Score WER/CER against a deduplicated human reference, and separately score entities, commands, omissions and additions. Engine-to-engine distance is a disagreement indicator, not a correctness measure.
4. **Zero counted repeats is not zero hallucinations.** Repetition detection catches one failure class. Audit speech in silence, wrong content, omissions and unsupported words, including enough silence/music cases to estimate reliability. Four videos do not establish elimination.
5. **Word timestamps do not establish quote accuracy.** Verify both the words and boundary alignment. Preserve verbatim originals for quotations; keep intended/readability edits in a separate field.
6. **The benchmark cannot retire alignment or choose a universal default.** Its reported ~30 ms precision is not a local annotated boundary evaluation. Compare native timestamps and alignment on the same known text/audio where exact timing matters. Re-evaluate current package/model versions, license eligibility and target hardware.

### Evaluation gates before changing tool defaults

Build a small labeled set around intended reuse: implement a command tutorial, compare a two-speaker disagreement, learn a technical concept, recover a brief UI action, interpret a non-text demonstration, and find an old example. Preserve versions and ground truth. Compare current pipeline against candidate changes with identical inputs and budgets.

- **Speech:** human-reference errors; names/commands; silence additions; word boundary error where needed; total latency/memory.
- **Speakers:** speaker confusion and missed/false speech, with explicit overlap policy; does attribution alter the downstream decision?
- **OCR:** region recall, character error and exact command/settings match, including punctuation and case.
- **Vision:** critical-step/diagram recall and temporal order; missing-evidence admission; unsupported observations; compute cost.
- **Artifacts:** independent task completion, supported essential claims, delayed learner recall/application, decision usefulness and evidence retrieval success. Fluency and a valid schema are insufficient acceptance measures.

**Unverified:** no fair engine shootout, OCR comparison, vision comparison, user study or delayed-learning test was performed in this research pass. The recommendation is a shortlist and a decision policy, not a claim that each incumbent is best.

## Ticket 24 currency update (2026-10-25)

[Open-question register](open-questions.md) rechecks source identity, checkpoint terms, runtime contracts and the remaining spike observations. In particular, CrisperWhisper v1 and its current successor must be distinguished from the worker model alias and historical package benchmark. Installed code, alias resolution, weights revision and deployment eligibility remain ticket 15 work; the current worker adapter alone does not establish them. No historical benchmark result selects a universal default.
