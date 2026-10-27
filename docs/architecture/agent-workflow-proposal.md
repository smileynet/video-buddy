# Proposed agent guidance and workflow

Status: authoring guidance/template and reader pathway contract adopted on 27 October 2026. CLI prompt routing, skill packaging and production integration remain proposed; this document does not add commands or activate a new skill.

Audience: agents and maintainers. The separate [user pathways proposal](user-pathways-proposal.md) describes what people see and do. Artifact classes, CLI stages, skills and evidence bookkeeping are internal decisions; users express their goals in ordinary language. Infer the route and present one useful next action rather than exposing this document's routing table as onboarding.

Adversarial review: [findings and disposition](agent-workflow-critique.md). The active template and authoring rules now incorporate the critic’s recommendations; reader outcomes and production changes remain open.

## Recommendation

Keep one small agent entry point and one authoritative guide-authoring workflow. Route by the user's desired artifact before choosing tools. Teach the video's content first, offer useful researched starting points, and give additional worked examples and tool evaluations their own scope and evidence.

The narration exercise demonstrated why this matters: comparing local TTS models produced useful component evidence, but that evidence answers a different question from what the source video teaches or whether a reader learned it.

## Current foundation and gaps

| Area | Exists today | Proposed change |
| --- | --- | --- |
| Mechanical processing | AGENTS.md intake/digest contracts and CLI | Preserve ownership; reuse existing artifacts and enrich only where evidence is needed. |
| Teaching | [Authoring guidance](../agents/video-guide-authoring.md) and [template](../templates/video-guide.md) | Make source type and learning outcome explicit before drafting. |
| Agent handoff | CLI companion prompts for summary, concepts, detailed notes and timestamps | Add conditional routing to teaching guidance when a guide is requested; retain source-only note instructions for ordinary intake. |
| Research | Existing research and research-audit skills | Use for consequential gaps and current claims; attach additions to their own sources. |
| Experiments | Existing spike/prototype skills and evidence reports | Require a decision question, bounded comparison and disposition before a spike starts. |
| Review | A/B guide views, optional example and listening comparison | Keep learning, layout preference, model preference and executed task results separate. |
| Progress | Tickets, plan and dashboard | Show the requested outcome first, evidence and unresolved gaps next, experiments behind drill-in. |

Inspection basis: AGENTS.md, the authoring guidance/template, and `src/video_buddy/cli.py::_write_companion_prompts`. The latter currently generates four source-based prose prompts; it does not select a teaching format.

## Proposed routing

| User wants to… | Primary artifact | Completion criterion |
| --- | --- | --- |
| Remember or find information | Source note or digest | Useful summary, concepts and traceable source moments; CLI finalization/compilation completes. |
| Understand, decide or apply an idea | Teaching guide | The main idea, reasoning and an observable application check are present, with source evidence. |
| Follow the video's demonstrated build | Source walkthrough | Demonstrated steps, prerequisites, checkpoints and missing dependencies are explicit. |
| Try an additional implementation | Separate worked-example companion | A bounded plan or authorized execution delivers its stated result and records its actual validation status. |
| Choose a tool or implementation | Research or comparison report | Fit, complexity and total cost support a recommendation, with measured claims separated from documentary claims. |

Reuse the user's stated goal. Ask only when missing context would materially change the result. A guide may link to an optional companion without starting its execution. A request to build an example authorizes its necessary work within the requested scope; avoid a redundant confirmation gate.

## Proposed workflow

1. **Set the outcome.** Record the requested artifact, intended reader, end use and source type: explanation, comparison, demonstration or worked walkthrough. Finish when the scope and success check are concrete enough to choose evidence.
2. **Recover evidence.** Use the CLI and inspect its returned paths and steps. Read existing transcripts and metadata before repeating work. Seek frames for exact commands, visual states and settings; inspect the image when OCR alone leaves ambiguity. Finish with traceable evidence for the guide's consequential claims and explicit remaining gaps.
3. **Draft the teaching.** Explain the source's ideas and reasoning, or its demonstrated steps and checkpoints. Add a small transfer task where useful. Finish when a reader can identify what to learn, why it works and how to check their application.
4. **Resolve consequential gaps.** Research primary sources for missing explanations, prerequisites or usable starting points. Name what each route supplies and what remains to do. Finish with a practical next action or a specific unresolved dependency beside the affected instruction.
5. **Recommend only where a choice matters.** Apply task and data-handling constraints first, then setup/upkeep and total cost. Consider relevant local and hosted routes. Explain the recommended product/model on first mention. Finish with a defensible recommendation and meaningful alternatives; components of one route stay grouped together.
6. **Scope additional work separately.** Put an invented build or tool trial in a companion/ticket with inputs, expected result, effort boundary and validation criteria. Execute when authorized. Finish at the requested scope, with a proposed, written, partly executed or validated status supported by evidence.
7. **Publish and verify.** Finalize through the CLI, check source links and required instructions, and verify interactive views when changed. Keep required costs/blockers visible; collapse optional depth. Update tickets, plan and dashboard for work worth surfacing. Report what is ready and the specific remaining uncertainty.

### Bounds and completion

Every research detour must identify the next user action it unblocks. Stop when a credible next step and its limits are established. Expand into a benchmark only when unresolved uncertainty changes the decision and the requested scope authorizes the experiment.

Preserve source meaning while correcting consequential outdated or incompatible advice. At the affected instruction distinguish “In the video” from “For your setup”, cite the current basis and recommend the action that fits the user's situation. Source fidelity does not require recommending an unsuitable procedure.

Use separate completion gates: **ready to read** means the lesson and source distinctions pass authoring checks; **ready to try** means the selected route has usable instructions, prerequisites, checkpoints and recovery actions; **executed under stated conditions** names the exact component or end-to-end result actually observed. Human learning/task success requires its own evidence. State partial readiness in plain language rather than applying an overall “validated” badge.

## Skills and document packaging

Keep AGENTS.md focused on the CLI contract, artifact routing and conditional pointers. Keep teaching rules in the existing authoring document and structure in the template, so improvements have one home.

Initially, strengthen those pointers rather than add skills. If invocation remains unreliable, introduce **one proposed repo-local `video-guide` skill** that routes to the existing authoring guidance and template. Its triggers should cover requests to teach from a video, turn a video into an actionable guide, or revise an existing guide. Ordinary intake and digest should retain their current note workflow. The wrapper should contain the entry/exit contract, not copied teaching rules.

Reuse available skills when their actual job applies:

| Job | Existing skill/workflow |
| --- | --- |
| Recover and publish source artifacts | Repo intake/digest CLI contract |
| Investigate a consequential gap | research; research-audit for cited findings |
| Observe competing approaches | spike-options; prototype for bounded experience questions |
| Execute agreed tracked work | tkt-work |
| Keep work and progress current | tkt-reconcile; delivery-dashboard |
| Maintain agent-facing instructions | writing-for-agents; skill-creator when packaging a skill |

These development skills belong to the current agent environment; they are not all bundled repository capabilities. Repository guidance should preserve enough task-specific criteria to remain usable when a named global skill is unavailable. Avoid separate skills for every model, provider or extraction stage; the CLI and configuration own those mechanisms.

## Evidence and review contract

Use the existing Source / Researched starting point / Adaptation / Tested vocabulary. For each material claim, preserve its source moment or external citation, relevant version/date and validation method. A model's review is model-reviewed; a human's review is human-reviewed. Captions and a second model's transcript are evidence, not automatically independent ground truth.

Keep four review questions distinct:

- **Learning:** can the reader explain or apply the idea?
- **Usability:** can they find the next action and its evidence?
- **Execution:** did the worked example produce the intended result?
- **Tool choice:** what do measurements and personal preferences support?

A listening preference does not validate a complete narration pipeline. A working component does not validate a full example. A successful authoring check does not establish a human learning outcome. Store private review responses separately from tracked fixtures and reports.

## Suggested adoption order

1. Tighten the AGENTS.md routing pointer and add a short scope/outcome checklist to the existing authoring guidance. Keep this proposal separate from active instructions until adopted.
2. Update companion-prompt generation to carry the requested artifact intent without breaking the existing JSON/prose contract. Decide the smallest supported input after inspecting the current CLI changes; this proposal does not prescribe a new command or flag.
3. Validate routing on four cases: conceptual/comparison video, source worked walkthrough with a missing dependency, ordinary intake, and batch digest. Check artifact placement, provenance and scope, not just whether headings appear.
4. Re-run the narration example through the revised flow: main teaching guide, optional implementation companion and separate model report. Record review results under the appropriate question above.
5. Add the thin skill wrapper only if observed routing failures justify it. Bring production/schema changes and any tool-default recommendations to the existing final integration review (ticket 28).

Success means an agent reliably produces the requested artifact, the reader can learn and try the source's ideas, and optional engineering work remains useful, discoverable and explicitly scoped.
