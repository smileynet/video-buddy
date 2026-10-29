---
name: video-guide
description: Create or revise a rich HTML learning guide from a video, including source walkthroughs, researched context and optional worked examples. Use for teaching or applying the source, rather than ordinary transcript notes or digest summaries.
---

# Video guide

Produce a useful learning path from the source as a rich, responsive HTML guide by default. Use the reader's goal to choose the teaching approach and navigation; guide types, skills and pipeline stages are internal decisions. Honor an explicitly requested alternative output format.

## Project entry

Read the workspace's agent instructions and use its source-processing tools. In Video Buddy, follow the intake/enrichment and finalization contracts; mechanical extraction remains CLI-owned. Reuse existing artifacts before repeating acquisition. Preserve configured compute and private credential handling.

When the project has `docs/agents/video-guide-authoring.md`, read it before drafting. Use `docs/templates/video-guide.md` for structure and `docs/agents/video-guide-user-pathways.md` for the reader experience. Those documents own the project-specific rules. If they are absent, use the bundled [authoring reference](references/authoring.md), [reader pathways](references/user-pathways.md) and [template](references/guide-template.md). Bundled references are a portable baseline; project guidance takes precedence. Use available source tools outside Video Buddy rather than assuming its CLI exists. A general note prompt does not authorize attributing outside research to the source.

## HTML deliverable

Before drafting, inspect representative existing HTML guides and their companion files in the workspace. Reuse established reader-facing conventions where they fit; distinguish the teaching guide from review harnesses and runnable examples. A Markdown template supplies the content outline, not the final presentation format.

Deliver a rich HTML lesson with readable typography, responsive layout, clear topic navigation, meaningful visuals or captioned source evidence where useful, and keyboard-operable disclosures for deeper explanation and Try / Check / If stuck help. Keep the outcome, required actions, constraints and immediate recovery visible in the skim path. Use semantic labels with restrained color. Richness should help the reader understand and act; A/B layouts, video players, note-taking and runnable companions remain optional.

In Video Buddy, complete CLI intake/enrichment and Markdown finalization, then author the HTML guide alongside its required local assets in the project's established guide location. Link the finalized source note as supporting material. Reuse one authored lesson across HTML, optional Markdown companions and comparison views. Return the HTML guide as the primary deliverable. Completion requires the HTML artifact and its presentation checks; a finalized Markdown note alone completes only the source-note pipeline.

## Author and revise

1. Recover enough of the whole source to understand its complete argument or procedure. Use relevant frames for settings, commands, brief states and visual decisions. A chapter list alone is not a teaching reference.
2. Name the learner’s real-world job and useful result. Organize practical teaching around that workflow; use source comparisons to explain choices along it. Checks inspect the result and recovery offers an adjustment; written answers and scoring are optional unless assessment is requested. State what the reader can understand, decide or apply. Teach the source's worked example when it demonstrates one; otherwise explain the ideas and their application. Keep an additional proposed build or tool comparison in a separate, explicitly scoped companion.
3. Give the complete approach before section details. When broader context helps, research a short “Where this fits” explanation and a misconception-preventing distinction; put adjacent approaches behind an optional comparison. Mark descriptive labels as our framing. Research only what unblocks the current learning path.
4. Establish the reading hierarchy: takeaway, useful visual, action, observable check and immediate recovery. Keep concise Try / Check / If stuck summaries visible and expandable into topic-specific instructions, success/failure examples and recovery. Disclose expanded rationale and provenance. Keep essential constraints and experimental status visible. Use semantic labels and restrained color together; source captures and explanatory diagrams have different evidence roles.
5. Where a route choice matters, recommend a named starting point and weigh relevant alternatives by fit, setup/upkeep and total cost. Respect hard constraints such as local handling. A conceptual lesson need not become tool shopping.
6. Label source content, researched additions, adaptations and actual execution distinctly. A model transcript/review is not human verification; a tested component is not a completed workflow; browser checks are not observed learning success.

## Publish and verify

Keep one canonical teaching fixture across comparison views. Preserve topic/evidence mapping, optional playback, separate example navigation, actual notes/persistence behavior and private responses. Follow the project's publishing contract for source artifacts and the HTML deliverable above. Keep core teaching readable without a network dependency; disclose any online playback or external service requirements.

Open the actual HTML in a browser and inspect desktop/mobile layout, keyboard navigation and disclosures, source links, local assets, visual readability and the skim path with optional panels closed. If browser inspection is blocked, report that limitation and distinguish authored HTML from browser-checked presentation. Check that required instructions and recovery remain usable. Report exactly what was executed and what the reader can review. Stop at the requested scope; unrelated research, a multi-source course or a knowledge platform is separate work.

## Adversarial review when requested

Use this skill and the applicable references as review criteria. Inspect the actual guide and evidence, then attempt the reader’s tasks: understand the whole idea, try a bounded step, recognize success, recover, and return from optional branches. Report concrete blockers with location, affected task, evidence and smallest useful correction. Separate source fidelity, instruction readiness, interface behavior and observed learner outcomes. Apply this to the requested artifact; review does not authorize new builds or unrelated research.
