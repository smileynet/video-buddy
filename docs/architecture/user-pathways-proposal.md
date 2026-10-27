# Proposed user pathways

Status: design rationale, 27 October 2026. The active [reader experience contract](../agents/video-guide-user-pathways.md) adopts the relevant requirements; the narration prototype demonstrates bounded navigation behavior, with human outcomes still open. These are proposed experiences, not claims of implemented navigation or saved progress. Agent procedures live in the separate [agent workflow proposal](agent-workflow-proposal.md).

## Start with a useful result

The user supplies a video and a goal in ordinary language: “Help me choose a voice workflow” or “Help me try the technique in my project.” Infer the likely path from that request and offer a useful first result. Users should not need to select a document type, source classification, skill or processing pipeline.

When the goal is ambiguous, show a short source-based overview and one suggested next action. Ask a focused question only when the answer changes the result materially. Keep changing direction easy.

## A small set of pathways

| User's job | What they receive first | Clear next action | Useful stopping point |
| --- | --- | --- | --- |
| Understand or decide | Main idea, reasoning, key tradeoff and relevant source evidence | “Apply this to my situation” | A reasoned explanation or decision, with uncertainty visible |
| Try what the creator demonstrates | Target result, essential requirements, first step and expected checkpoint | “Try the first step” | An observed checkpoint or a clear recovery action |
| Find an answer later | Compact reference and source moment for their question | “Show the source” or the relevant action | The answer without rereading the lesson |
| Extend beyond the video | A separately labeled example proposal with scope, effort and cost | “Read the example” or “Build this example” | A useful plan, or the explicitly requested working result |

These are contextual actions, not four mandatory onboarding choices. Keep one primary next action on the current view. Additional routes should explain when they help before asking the user to choose them.

## What the guide should show

The opening answers: what this helps you do, whether it fits your situation, and what to try first. For a conceptual video, the first action may be a small decision using the framework. For a source walkthrough, it may be the first executable step. Required costs, unavailable dependencies and constraints that affect that action stay visible.

Each topic or step gives the explanation/action, expected check and relevant timestamp or frame. Evidence is accessible nearby without forcing users to inspect it before continuing. Preserve the current topic and user work when opening evidence or an alternative, and provide a clear return action. Persistence or cross-device resume must be described according to what is actually implemented.

Use collapsed sections for optional explanations, deeper comparisons, setup detail for unselected routes and full provenance. Keep a short recovery action visible beside a failed check; detailed troubleshooting can expand there. “Get unstuck” should not require finding a distant evidence appendix.

## Handle missing pieces constructively

Example: “The creator's automation program is unavailable. You can still learn the paragraph-revision pattern here. To try it, start with one paragraph in the recommended editor; the separate example explains how to assemble the pipeline.” Name the editor, explain relevant costs and identify what the suggested route can actually produce.

Show a concise “Added starting point” label for external help, with its citation available nearby. Keep the distinction from the creator's method clear without making the user learn the internal evidence vocabulary. A recommended workaround must not imply the original custom program was recovered or a complete pipeline was tested.

## Keep optional building optional

Place “Try a worked example” after the relevant teaching, with the outcome, requirements, likely effort/cost and current status. For an already requested build, carry out the agreed work and report progress rather than repeatedly asking for permission. For a newly proposed build, let the user choose it explicitly.

An example should link back to the idea it illustrates. A model comparison can support a tool choice inside that example, but its measurements and listening review belong in a separate drill-in. The main learning path should remain useful without completing either.

## Validate the pathways

Test comprehension and navigation separately from implementation success. Observe whether a reader can:

- Identify what they will learn or produce, and the first useful action.
- Recognize a missing dependency and choose a viable next step before investing effort.
- Distinguish source teaching from our added example and its actual validation status.
- Open evidence and return to the same topic without losing work.
- Find a previously needed setting or decision rule without rereading the guide.
- Decline the extra build and still complete the intended learning task.

Record observed failures and revise the pathway. A rendered page or a self-reported preference alone does not establish these outcomes.
