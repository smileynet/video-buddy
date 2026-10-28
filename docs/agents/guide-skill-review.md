# Skills after the single-source guide iteration

28 October 2026. The initial proposal below is retained as its decision record. The user subsequently authorized building and installing the skill; see the installation and adversarial trial record at the end. Project behavior remains routed through AGENTS.md and the active authoring documents.

## One skill worth creating

The [video-guide candidate](skill-candidates/video-guide/SKILL.md) packages the recurring task: teach/apply a video's content, revise a guide, or preserve a source walkthrough. It routes to existing workspace contracts and the project's authoritative guidance/template. It is useful across future videos without binding a personal skill to one checkout or embedding current model/provider recommendations.

The candidate is intentionally not installed in the user's global skills directory. The user asked which skills to create/update; keeping the actual entry point reviewable avoids activating a new global trigger as an incidental repository edit. Structural validation is not a behavioral trial of an installed skill.

## What stays where

| Concern | Home / disposition |
| --- | --- |
| Source recovery, private credentials, compute and finalization | Existing repository AGENTS.md and CLI; do not duplicate them in a provider-specific skill |
| Teaching, whole-source overview, bounded researched context | Existing video-guide-authoring.md, reached by the candidate |
| Reader hierarchy, colors, optional comparisons, evidence and return navigation | Existing reader-experience contract and template; labels and semantics precede decorative styling |
| Primary-source investigation and citation checks | Reuse research and research-audit when applicable; no new category-research skill |
| A/B experience or design uncertainty | Reuse prototype/spike-options; keep Video Buddy's fixture/return/privacy checks in project guidance |
| Tool qualification | Separate bounded spikes; no skill for each model or audio provider |
| Dashboard and task state | Existing delivery-dashboard and ticket workflows |
| Multi-source knowledge collection and ongoing related-topic research | Follow-up44, unstarted until the current guide iteration is finished |

## Changes already retained from the session

The active guidance/template now specify a complete-method overview before detail, a distinct researched context block, meaningful visuals, labeled reading levels, optional related-approach comparisons, visible action/check/recovery, and separate worked examples. Keep these in those documents rather than grow multiple overlapping skills for each feedback item.

A further practical need is a shared guide-presentation helper: repeated scratch transformations can lose dark theme, contextual labels or provenance updates. That is a tool/design question for the existing integration review, not another authoring skill or an authorization to replace the production rendering contract now.

## Candidate acceptance before activation

- Check routing on a conceptual comparison, a demonstrated tutorial with a missing dependency, an ordinary intake/digest and an existing A/B revision.
- Confirm that source teaching stays primary, examples remain separate, and targeted context research stops at a useful answer.
- Confirm the candidate finds project-local instructions without hardcoded checkout paths and does not broaden unrelated requests.
- Activate normal discovery only after deciding the intended installation location and verifying those realistic cases. The current direct project guidance already supplies the behavior during this review.

## Validation in this pass

The candidate passed the skill-creator structural validator and repository pre-commit checks. The revised narration/browser guides passed A/B parity, source/evidence/return navigation, expanded comparison and mobile checks, but those are artifact checks under current guidance—not a behavioral qualification of an installed skill. Independent source auditing supported the context blocks; a request-stitching clarification was incorporated. No global skill was installed or modified.

## Installation and adversarial trial — 28 October 2026

Installed `video-guide` at `C:/Users/uosmi/.codex/skills/video-guide` at the user’s explicit request. The tracked package remains [here](skill-candidates/video-guide/SKILL.md). Normal automatic discovery is enabled by default; explicit invocation is `$video-guide`. The entrypoint selects current project guidance when present, otherwise its bundled authoring, reader-pathway and template references. Bundled files are generated portable snapshots from the project documents: when behavior changes, refresh them and reinstall the package together; project copies remain authoritative in this repo. No private media, credentials or reader responses are packaged.

Structural validation passed for the installed package. An independent adversarial critic is evaluating the actual browser guide and a bounded conceptual-source fixture using the installed skill. This is an agent behavioral trial and artifact review, not human learning validation.

### Critic results and corrections

The independent critic identified a confirmed P2 navigation defect: Resume focused the response form instead of the selected topic. Restored focus/scroll to the topic. Its alleged broken opening example link was rejected after inspecting the parsed fixture: the review already links to `guide.html#worked-example` in another tab; the critic confused the canonical Markdown fragment with the review URL. The unnecessary proposed anchor was removed. The critic also flagged unconditional Video Buddy wording in the bundled fallback; it now uses workspace tools and makes CLI publishing conditional.

The bounded behavioral trial used only a supplied conceptual-video summary (rough shape → early pose → silhouette feedback → revision). It produced an overview and expandable Try/Check/If stuck instructions, marked application guidance and unavailable exact timestamps/commands, offered a sketch-based reasoning route, and avoided unsupported execution claims or an unrequested build. The critic found the actual browser guide’s expanded help topic-specific and useful, and the optional order-board example clearly separate. This establishes a limited agent trial, not broad skill qualification or observed reader success.
