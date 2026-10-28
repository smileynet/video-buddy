---
id: "44"
title: "Explore concept-linked research and multi-source learning guides"
status: open
blocked_by: []
priority: medium
validation_criteria:
  - "A cited exploration proposal defines learner jobs, low-complexity user pathways and agent responsibilities separately"
  - "A worked example models concepts, tags, relationships and claim-level provenance across at least two sources"
  - "Supplemental research and related-topic offers include scope, evidence quality, freshness and user control"
  - "Architecture options, evaluation criteria, project boundaries and an explicit next-step disposition are recorded"
tags: ["knowledge-management"]
---

# Explore concept-linked research and multi-source learning guides

## Intent source

On 28 October 2026 the user requested a follow-up exploration of a robust knowledge-management project: track concepts/tags, conduct supplemental research, offer related-topic research and supporting/reference/guide documentation, and compose guides from multiple sources. This follows the agreed modeling-context proposal, not a request to implement a knowledge platform immediately.

## Starting context

- [Context proposal](../docs/architecture/guide-context-proposal.md)
- [Modeling research](../docs/agents/research/iterative-character-modeling-context.md) and [independent audit](../docs/agents/research/iterative-character-modeling-context-audit.md)
- [Guide authoring](../docs/agents/video-guide-authoring.md), [reader pathways](../docs/agents/video-guide-user-pathways.md) and [template](../docs/templates/video-guide.md)
- Existing CLI concept extraction and source artifacts are prior art to inspect before adding another storage or authoring pipeline.

## What to explore

Develop a cited product/architecture proposal and a small illustrative knowledge collection. Decide whether this should be a separate project, a companion knowledge layer or a bounded Video Buddy feature. Reuse existing evidence and tooling where useful; do not assume a graph database, embeddings or a new application framework is necessary.

### Learner jobs and user pathways

Help people place a technique in a wider knowledge space, recall it later, follow an adjacent learning need and apply information gathered from several sources. Explore:

- One concise “Where this fits” category/context block, followed by the whole-approach overview; optional related topics explain why they matter.
- Contextual offers such as “Explore non-destructive workflows” or “Learn deformation testing”, with the question, expected artifact, depth/scope and likely effort made clear. Users can accept, narrow or decline; do not silently expand every guide into an open-ended research project.
- Distinct outputs for supporting explanations, compact reference pages, practical guides and separate worked examples. Readers should not need to understand the internal taxonomy or research pipeline.
- Navigation back to the originating guide/topic and reuse of existing research instead of generating duplicate pages.

### Knowledge model and research lifecycle

Explore stable concept IDs, aliases, tags and typed relationships such as broader/narrower, related, prerequisite and contrasting approach. Distinguish established terms from our descriptive labels; avoid treating every tag as a formal category.

Preserve claim-level evidence: original source and exact passage/frame where available, author, date/version, source versus inference, confidence, disagreements and verification method. Keep machine transcription/model review distinct from human verification. Track research questions, findings, gaps and freshness/recheck triggers; show when an answer remains unverified. Evaluate how changed sources mark dependent references/guides for review rather than silently rewriting them. Respect source access boundaries; member/private evidence and reader responses must not leak into shared artifacts.

### Multi-source guide composition

Start from a learner outcome, select relevant sources and explain their combined approach up front. Distinguish shared conclusions, complementary material, conflicting advice and different environments/versions. Every consequential instruction should trace to its supporting source(s) or be labeled as our adaptation. Several sources repeating one claim are not automatically independent confirmation. Preserve individual-source context and separate optional implementation work from the teaching.

### Bounded exploration and options

Use iterative character modeling, non-destructive operations and deformation testing as an example cluster. Reuse the existing source analysis plus at least two independently authored primary sources where available. Demonstrate one related-topic research offer, a supporting/reference page, and a short guide synthesized from multiple sources. This is an illustrative content/provenance experiment, not a finished knowledge platform or a complete character-modeling course.

Compare a lightweight file/link collection, a structured concept/claim index and richer retrieval/graph options. Evaluate evidence traceability, terminology ambiguity, contradiction handling, update cost, portability, privacy/access control and reader cognitive load. Recommend the smallest useful scope, project boundary, initial spikes and explicit defer/adopt/reject decisions. Record unknowns without treating polished mockups as validated usability.

## Acceptance criteria

- [ ] A cited proposal separates learner jobs and low-complexity reader pathways from agent research/curation/composition responsibilities.
- [ ] An illustrative cluster models stable concepts/tags, aliases and meaningful relationships, with provenance across at least two sources and explicit handling of disagreements/uncertainty.
- [ ] A related-topic research offer and resulting supporting/reference material show scope, evidence quality, freshness, reuse and user control.
- [ ] A multi-source guide explains the combined approach while retaining source attribution, version differences, adaptations and a separate worked-example boundary.
- [ ] Architecture options, evaluation criteria, separate-project versus integration boundary, initial spikes and a concrete next-step disposition are documented.

## Sequencing and boundaries

Open follow-up in the knowledge-management workstream. It can be researched independently and is not added as a mandatory blocker to integration review28. Coordinate any proposed production integration with28; implementation should follow the exploration's disposition and separately scoped tickets. No new project, provider subscription, background research automation or production schema change is authorized by creating this ticket alone.

## Separate-project handoff — 28 October 2026

The user authorized initialization of the separate **Learning Library** exploration at `D:/code/learning-library`. Its committed `docs/project-brief.md` preserves the outcome/boundary, `docs/context/video-buddy-44.md` snapshots this intent, and `docs/plan.md` orders local tickets 01–04: learner path, concept/claim provenance, research reuse and multi-source composition, then architecture disposition. Repository setup and tracker checks passed; no exploration ticket is claimed or completed.

Detailed execution is tracked in Learning Library. Keep this originating ticket open as the cross-project disposition checkpoint until the exploration returns its findings; initialization alone does not satisfy its research acceptance criteria. No production integration dependency is added to review28. The new repo is local-only, with no remote configured.
