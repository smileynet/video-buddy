# Author a practical video guide

Use this workflow when a user wants to learn from a video and apply its ideas or procedure. Use [the guide template](../templates/video-guide.md); adapt its shape to the source and the user's goal. Learning from a guide and executing an implementation are distinct activities.

## Teaching and worked examples

Classify the source before authoring: concept explanation, decision/comparison, demonstration, or worked walkthrough. Keep what the video teaches as the main guide. For a conceptual/decision video, explain its ideas, evidence and tradeoffs, then help the reader apply the reasoning. Do not turn it into a new engineering project simply because the source mentions tools or shows a pipeline.

If the video itself is a worked example, its demonstrated steps and checkpoints can be the main guide. Preserve its actual scope and distinguish additions needed for another target environment.

For a worked example we propose, use a separate optional companion with its own purpose, prerequisites, fit/cost choices and validation status. Link it from the lesson after the main teaching. Identify whether it is proposed, written, partly executed or validated; a component spike does not establish a complete worked example. Offer to propose or build an example, and execute it only when the user's request authorizes that work. Do not quietly expand guide authoring into installations, model comparisons, purchases or implementation.

Keep three outcomes distinct: **understanding** (explain/apply the idea), **example execution** (the artifact behaves as intended), and **tool qualification** (a model/runtime comparison). Publish each result in its proper place. A useful experiment must not crowd out the lesson it was meant to support.

## Workflow

1. **Recover the source through the CLI.** Follow AGENTS.md intake/enrichment contracts. Read the transcript, relevant frames and companion prompts before writing. Seek exact visual evidence when settings, commands, ordering or brief states matter. Keep timestamps and provenance.
2. **Name the learning outcome and source type.** State what the reader can explain, decide or apply, and how to check that understanding. For a source walkthrough, also state its demonstrated artifact/result. Reuse known goals; ask only for missing context that changes the teaching. Scope any additional implementation separately.
3. **Recommend a route where the job requires a choice.** Name the provider/product or local model, explain what it does, and give the first action. Evaluate meaningful alternatives, including local execution when privacy, ownership, offline use, existing hardware or source context makes it relevant. Do not restrict discovery to one provider or silently omit an important class because it needs more setup. Put implementation-specific choices in the optional companion when they are not what the video teaches.
4. **Weigh the choices.** Apply hard fit constraints first (required task, data handling, platform, language and permitted use), then compare setup/upkeep and total cost. Include subscriptions/usage, retakes, hardware/compute/storage and engineering time where applicable. Distinguish a free client from paid generation, free exploration from paid features, code licenses from checkpoint terms, headline rates from account quotes and promotions from renewal. Use qualitative judgments with reasons; numerical rankings require measured criteria. Identify unqualified candidates instead of claiming a winner.
5. **Fill consequential gaps with research.** For a missing explanation or prerequisite, consult primary sources and add the minimum useful clarification. For an implementation dependency, provide prior art and next actions in the relevant walkthrough or optional example. Date/version unstable claims. An official example is not the creator's recovered program or proof that an assembled workflow works. Offer other end-use branches only when helpful.
6. **Teach the mechanism in the appropriate form.** For concepts/decisions, explain the idea, show its evidence or illustration, and give a way to apply/check the reasoning. For source walkthroughs, use Do / Why / Check steps. Add rationale where it changes understanding. Name files/environment for executable material; distinguish complete code from configuration/illustration. Keep unsupported additions separate from the source.
7. **Disclose optional depth.** Follow the hierarchy below. Add an optional transfer task with a hint and observable criteria, then a compact work-time reference. Keep the task tied to the promised result; no compulsory quiz or course machinery.
8. **Verify and publish.** Check sources, links, code provenance, prerequisites, dates, prices and observable checks. Actual runtime/quality evidence must name the environment and result; syntax or documentary checks do not imply task completion. For interactive views, check desktop/mobile, source links, keyboard behavior and consistent content. Follow CLI finalize/enrichment rules for the canonical note and pre-commit requirements for changed files. Preserve notes/fixtures separately from private reader responses.

## Wording and information hierarchy

Write as a knowledgeable colleague helping the reader try something. Lead with the useful action: “Start with one paragraph”, “Try this adjustment”, “Check the export”. Use plain words, readable dates and short paragraphs. Explain a product on first mention. Keep status truthful in a brief relevant note; do not repeatedly open sections with lists of work that was not performed.

**Keep visible:** the outcome; recommendation and why it fits; essential prerequisites; a short cost/paid-feature explanation; constraints that rule out a route; required actions; expected results; blockers that affect the next action. Never hide a required paid plan, missing program or local-handling incompatibility in a collapsed callout.

**Collapse when useful:** Alternative starting points and full comparison; optional route setup; deeper mechanism/background; API versus application mapping; model/hardware/license detail beyond the decisive summary; version/pricing nuances; full research status; troubleshooting for other symptoms; glossary; practice hint and answer criteria. Use specific labels that tell the reader what they will find. Keep each callout near the relevant step, avoid nested callout trees, and do not require opening every panel to follow the recommended route.

For a local candidate, show the model/checkpoint name, task/language fit and a concise resource/setup/terms summary. Put download commands and detailed hardware guidance behind its callout. “Local” is a route to qualify, not a guarantee of privacy, offline readiness, zero cost or commercial eligibility.

## Evidence vocabulary

- **Source:** the video describes/shows it; attach a source moment or frame.
- **Researched starting point / Docs:** external material supporting an extension; cite the relevant primary page and check date/version.
- **Adaptation:** our procedure for the stated target; explain material changes from the source.
- **Tested:** an executed check with environment, inputs and observed result. Distinguish machine checks, model review, human self-report and directly observed task performance.

Keep important uncertainty next to the affected instruction; consolidate general validation status into one short note. Avoid “verified” without saying what was verified.

## Authoring check

- The main guide teaches the video's ideas or demonstrated walkthrough; additional examples and tool experiments are clearly optional and separate.
- Where a choice is needed, the reader can identify the recommended route, provider/model, first action and likely costs without opening optional details.
- Alternatives are real routes; tools that belong to one route are grouped as components.
- Relevant local choices are named or their actual research/access blocker is recorded.
- Every essential source gap leads to a researched next action or a specific unresolved question.
- Learning checks assess understanding/application. Implementation checks belong to the relevant walkthrough or optional example; optional depth supports rather than interrupts the teaching.
- Source, researched additions, target adaptations and actual execution remain distinct.
- Comparison views use identical canonical content; copy improvements are not attributed to one layout.
