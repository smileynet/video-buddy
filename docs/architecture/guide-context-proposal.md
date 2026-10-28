# Proposal: place a guide in its wider learning context

28 October 2026. Adopted in the local Noggi single-source guide and both A/B views, with a visible category/distinction and an optional related-approach comparison. Supporting research: [modeling context findings](../agents/research/iterative-character-modeling-context.md), independently [audited with limitations](../agents/research/iterative-character-modeling-context-audit.md).

## Recommendation for Noggi

Use **Iterative character modeling** as the broad learner-facing category. Describe this example more specifically as **pose-aware polygon modeling**. These are descriptive labels chosen for orientation, not a verified formal name for a single standardized method.

Keep “non-destructive modeling” as a related editing strategy. It answers a different question: how much remains adjustable, rather than when the artist seeks feedback. Noggi's source combines direct geometry edits with shared mesh data and live deformation. Calling the entire method non-destructive would imply a guarantee it does not establish.

## Proposed opening block

**Where this fits · Iterative character modeling**

> Noggi connects polygon modeling with early pose and silhouette testing. Useful neighboring approaches include sculpting with retopology where needed, and deformation testing. Non-destructive tools can keep parts adjustable, but describe how edits are managed rather than the feedback strategy. Hard-surface workflows can share these tools; here they serve stylized character design.

Show one category label and this brief context immediately before the existing “whole approach at a glance”. Keep the latter responsible for explaining this video's complete method and section map. The context block explains where that method belongs; it should not repeat the whole lesson.

## A small knowledge map

This is an author-facing editorial map, not a formal taxonomy or an extra onboarding step. Its dimensions overlap. Use it to select one useful category for the visible opening; show a map only inside the optional related-approaches callout when it helps.

| Question | How to orient this example |
| --- | --- |
| What is being made? | A stylized character |
| How is the shape authored? | Primarily direct polygon modeling in this source |
| How is it evaluated? | Coarse-to-fine iteration with early pose and camera feedback |
| How editable is the setup? | A mix of direct edits and adjustable/shared-data techniques |
| What should the image feel like? | Stylized, with silhouette and line-art decisions; related to NPR production |

“NPR” means non-photorealistic rendering: a related visual target, not another name for polygon modeling. The linked-data exercise already demonstrates why a shared mesh is also not a backup: geometry edits propagate to its linked users.

## Optional “Related approaches” callout

Show only adjacent paths that help the reader choose what to learn next:

| If you want to… | Related direction | What transfers / what changes |
| --- | --- | --- |
| Keep operations adjustable | Non-destructive or modifier-based modeling | Adjustable operations can support iteration; applying/baking or direct edits can commit changes |
| Explore forms through brushwork | Sculpting, then retopology when needed | Keep the feedback loop; change the shape-authoring and topology workflow |
| Build a prop or mechanism | Hard-surface blockout and refinement | Reuse early shape/movement checks; the asset constraints differ |
| Make a 3D character read like an illustration | Stylized/NPR character production | Study view, silhouette, shading and line decisions together |

Use these as learning links, not product recommendations or invitations to install several tools. The main next action remains the existing rough-pose exercise.

## Evidence and boundaries

- Blender's modifier documentation distinguishes adjustable operations from applying permanent geometry changes. The research record pins the inspected source and flags its version relative to local Blender 5.2.
- Blender Studio's [artist modeling guide](https://studio.blender.org/tools/artist-guide/asset-creation/modeling) documents a hard-surface blockout/refinement route and an organic sculpt/retopology route with deformation material. It is explicitly a work in progress, not a universal production standard.
- The developer-published [Guilty Gear Xrd art talk](https://www.arcsystemworks.com/guilty-gear-xrds-art-style-the-x-factor-between-2d-and-3d-talk-from-gdc-2015-is-now-available-online/) supplies historical 2D/3D art context. It does not establish that Noggi's exact technique is the game's complete pipeline.
- The reviewed sources support useful relationships, not a measured new trend, regional generalization, or uniquely recognized name. Avoid calling this a Japanese standard, box modeling, procedural modeling or corrective sculpting without the source-specific evidence those terms need.

## Reusable authoring addition to consider

Before writing the introduction, ask: **What larger idea does this instantiate, what distinction would prevent a misconception, and what adjacent direction serves the learner's next need?** Research only those claims using primary sources. Prefer an established broad category; mark any more specific descriptive label as our framing. Sometimes the answer is that no useful larger category was verified.

Reader presentation: one short “Where this fits” block, then the whole-source overview; put a compact relationship map and a few purposeful learning links under “Related approaches”. Keep category research, quotations and uncertainty bookkeeping in the maintainer research file. Do not turn every introduction into a history lesson or a mandatory taxonomy.

Before adoption, check whether the reader can distinguish the feedback strategy from the editing tools, explain how this source relates to prior knowledge, and identify one relevant next learning direction. No reader validation has been performed for this proposal.

## Review disposition

Independent audit supported the bounded technical distinctions. Historical/WIP practitioner guidance remains labeled as prior art; the Arc publisher page could not be independently re-fetched by the auditor, so it supports an optional historical pointer rather than technical lineage. The proposed opening was shortened to avoid repeating the existing whole-approach overview. Sculpting is called an editing route rather than a different representation. The official release-branch references retain the inspected commit hash/date; a later attempt to use commit-qualified raw URLs returned403 in this environment, so no successful re-fetch is claimed for those alternative URLs. The current single-source guide and reusable authoring guidance now apply the bounded context block and comparison; the broader knowledge-management exploration remains follow-up ticket44.
