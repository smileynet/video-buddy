---
id: "25"
title: "Find complete readable subject states by seeking within video windows"
status: in_progress
blocked_by: []
spec: "apply-build"
priority: high
tags: ["workflow-spikes"]
validation_criteria:
  - "docs/architecture/spikes/subject-frame-seeking-results.md exists and records evidence, limitations and a disposition for each scoped question"
  - "tkt validate exits 0"
---

# Find complete readable subject states by seeking within video windows

## Context and intent

Intent source: user request on 2026-10-25 to capture every remaining spike, put open research next, then review integration, features and architecture. Read docs/architecture/spike-plan.md, docs/architecture/workflow-proposal.md and docs/architecture/spikes/image-model-results.md. Primary job: apply a technique/build something and verify the result. Preserve unrelated working-tree changes. Prototype code stays on isolated spike branches; no production integration in a spike.

## What to build

Evidence that seeking across all decoded frames inside a subject window recovers complete readable states better than the existing sparse strategy.

Compare sparse/time-selected baseline, dense box/crop scoring, and optional masks/tracking on the SAME short frozen windows. Detect a subject once, associate it over the window, seek optimal frame(s), preserve distinct revisions and action order. Include typing, scrolling, blur, occlusion, slide/diagram updates and brief UI states. Use CLI/source capture mechanics rather than reinventing acquisition. Exhaustively annotate essential readable states within bounded windows; split tuning and held-out windows. Use provisional ticket 14/23 candidates, disclose partial qualification; their final completion is not required to start this joint experiment. Record deciding question, total active budget, modality/settings/hardware and all failures before comparing.

## Acceptance criteria

- [ ] Report complete-state recall against exhaustive window labels.
- [ ] Report missed revisions, duplicate evidence and wrong subject associations.
- [ ] Report exact settings/command recovery and human correction effort where observed.
- [ ] Compare frame count, decode/detection/recognition/tracking cost and memory separately.
- [ ] Show whether boxes suffice and where masks/tracking add measurable benefit; retain explicit gaps.

## Out of scope

Automatic production integration, unsupported winners, and invented user/quality measurements.

## Ticket 24 research execution contract (2026-10-25)

**Budget:** One active day after corpus preparation.

Freeze short labeled windows for typing, scrolling, blur/occlusion, diagrams and transient UI. Enumerate all essential distinct readable states across decoded frames before scoring. Compare sparse baseline, box/crop seeking and optional masks/tracking. Report complete-state recall, missed revisions, association errors, exact-text recovery, redundancy and stage costs. Tune thresholds on separate windows; preserve revisions rather than selecting one frame per entire subject.

Record raw outputs, exact versions/configuration, failures and a per-job disposition. Report metrics even if they do not favor a candidate; no invented quality threshold. Research register: `docs/agents/research/open-questions.md`.

## Provider coverage expansion

Current-provider comparison is now explicit in29–34. Coordinate shared fixtures/metrics and consume those results rather than duplicating provider installs. Original tested shortlist is not comprehensive market coverage. Final integration28 depends on all coverage dispositions.

## Comparison follow-up

Same-query providers chose browsersearch vsOSsearch on a screenshot containing both. Require task-scoped intended-region annotations (active app/window and desired action); generic subject names alone cannot define a valid accuracy comparison. Include strict geometry completeness checks before subject association. Evidence commit ce811ed8, provider reports under docs/architecture/spikes/.

## Completed local probe evidence

Consume DINO3/SAM31/specialist findings from local-model-followup.md. Stable ID can retain wrong pixels; first-time pointing is not trajectory coverage; initial seeded mask can disappear duringpropagation. Score complete intended states and expected times, not only setup success or nominaltracking labels. Raw evidence: `codex/spike-provider-coverage` commit `fc7caee6184942d39ca4cc5cc2c4d36a36498d44`.

## First matched-window execution — 2026-10-25

Report: `docs/architecture/spikes/subject-frame-seeking-results.md`. Raw branch `codex/spike-subject-frame-seeking`, commit `63082cff1f7f74e99d38dd4a955fa74364b30803`; all270 decoded subject crops, timestamps/hashes, frozen settings, annotation corrections, OCR outputs and measured costs retained.

Two real tutorial windows: filename preparation120frames and held-out code revision150frames. Same four-output cap: existing sparse and dense selector both saved0; crop/OCR seeking recovered2/2 filename and3/3 code states; time grid also2/2 and3/3. Both had one redundant code frame. Exact held-out OCR0/3 for both, despite visually complete evidence. Crop/OCR selection cost15.294seconds plus0.344seconds dense capture on the code window; four time-grid seeks0.431seconds before separate OCR audit. Manual fixed boxes; no detector/tracker or measured peak memory/human effort.

The global2% edge-density veto rejects these sparse editor screens. Post-hoc flag-only bypass recovers3/3 code states on sparse candidates but2/3 dense, so extra candidates alone do not establish improvement. Follow-up35 owns reviewed implementation/regression work after integration review28.

Keep this ticket in progress. Next: freeze independently checked scrolling/moving/brief-state and diagram windows, vary grid offsets/budgets, test subject association/optional masks only where boxes fail, measure memory and correction effort. Current fixed boxes do not qualify those cases. No new model or selector integrated.

## Scrolling / motion / occlusion / brief-state round — 2026-10-25

Report: `docs/architecture/spikes/subject-frame-seeking-stress-results.md`. Raw branch `codex/spike-subject-frame-seeking`, commit `39275c6072e85be74640c292310858202809a659`; complete controlled source videos, all480 decoded crops/labels, both OCR passes, selected full-frame comparisons, stage costs and sampled RSS retained.

Swept caps1,2,3,4,6,8 and grid offsets0,.25,.5,.75:96 configurations on four authored controls plus48 on earlier real windows. Real code at cap4: grid coverage2/2/3/2 of3, earlier seeker3/3. At cap8 one grid offset still missed the intermediate revision. These are correlated configurations, not independent accuracy trials.

Original PSM13/frequency seeker at cap3: scroll3/3, motion0/3, occlusion2/3, brief2/3. After an explicit post-hoc PSM7 diagnostic, static/frequency motion0/3 versus tracked/frequency3/3; short-event selection also recovered occlusion/brief3/3 versus frequency2/3. PSM7/events yielded all12 controlled states/strings with three selections per clip, no redundancy, but this is not held-out confirmation. Natural code exact OCR remains0/3. All192 distinct controlled core seeks were pixel-identical to the expected decoded frames.

Collector/children peak sampled summed RSS83.8MiB (decode/encoder excluded); tracked OCR about8.4–8.7seconds per120frame clip, template search about1second. The invariant-header fixture is deliberately easy; no wrong accepted controlled match observed, eight motion/blur abstentions. No SAM/mask benefit established.

**Next:** freeze fresh natural scrolling, movement, obstruction and brief UI windows with independent label checks, then validate the unchanged PSM7/event candidate. Also test false/repeated subjects, diagram/settings completeness, source-wide discovery and human correction/task outcomes. Current natural exploration113–125seconds was unscored; do not claim it fills those gaps. Keep ticket25 in progress and review28 gated. Existing frame tests5passed; sweep/seek/timestamp checks and pre-commit passed.

## Fresh-source frozen validation — 2026-10-25

Report: `docs/architecture/spikes/subject-frame-seeking-real-validation.md`. New Traversy Git tutorial source, four natural windows: terminal scrolling, browser zoom, installer obstruction, brief menu disappearance/reopening.456 observations/405 unique frames; browser windows overlap. Single-agent OCR-assisted reference, with explicit geometry/visibility uncertainty. Labels/inputs/candidate frozen in commit834036e before inference; exact candidate hash verified against round2. No retuning.

**Negative verdict:** frozen candidate recovered0/3 required scrolling states at every tested cap1,2,3,4,6,8. Its eight prefix/OCR-variant selections ended before the complete add command. Grid at cap4 recovered1/1/2/3 states across offsets0/.25/.5/.75. Other cases each1/1 from an early image, which does not establish tracking through later zoom/occlusion/reopened menus. Menu exact OCR was wrong. Raw branch `codex/spike-subject-frame-seeking`, commit `181e209def0389a57b0b4192b4acb2447682f6e4`.

All192 actual grid seeks matched decoded frames;8 nominal presentation-index rounding discrepancies corrected explicitly, without changing coverage results. Existing frame tests5passed; pre-commit and hash/timestamp/seek checks passed. Costs retained; fresh peak memory/human effort not measured.

Do not adopt the candidate as default. New ticket36 owns the separate revision-boundary spike; these real windows are development evidence for any revised policy, requiring new locked validation. Keep25 in progress for independent labels, broader sources/subjects, diagrams/masks and task-level qualification;35 owns the production inclusion veto and28 still gates integration.
