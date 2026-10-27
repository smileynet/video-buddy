# Adversarial review of agent guidance and user pathways

27 October 2026. Independent critic reviewed the workflow proposal, authoring guidance, reusable template and teaching-format rationale against learning/application JTBD. This is a design review, not observed user research.

## Finding

The original proposal described agent artifact production more clearly than the user's path to a useful result. Adopt distinct contracts: internal agent execution, authoring rules/template, user experience, and internal research/progress. They should connect through pointers and useful actions rather than become one visible workflow.

## Findings and disposition

| Priority | Failure case | Required revision | Disposition |
| --- | --- | --- | --- |
| P1 | “Help me apply this” becomes a choice among document/source types | Infer format internally; present the useful result and one next action | Added audience boundary to agent proposal and separate user pathways proposal |
| P1 | Reader opens a companion and loses their topic or work | Show purpose, requirements, effort/cost, readiness, exact return target and continuity | Proposed navigation contract added; prototype implementation still needs validation |
| P1 | Historical narration-build example overrides source-first teaching | Mark history and identify authoritative active authoring rules | Historical example labeled; full rationale cleanup remains adoption work |
| P1 | Faithful source advice is outdated or incompatible with the user's task | Distinguish “In the video” and “For your setup”; recommend suitable current action | Agent proposal amended; Active authoring rules and template now distinguish source/setup advice |
| P2 | Conceptual video becomes a setup tutorial | Keep one entry template with distinct idea/example/application and walkthrough/checkpoint bodies; remove visible internal “Guide type” | Active template now selects distinct concept/walkthrough bodies and omits the reader-facing type label |
| P2 | A prepared check or tested component becomes an overall validation claim | Separate ready to read, ready to try and executed result; human outcomes require observation | Agent proposal amended; Active guidance/template use exact component and remaining-work wording |
| P2 | Required recovery or a fitting alternative is hidden in optional details | Put immediate recovery beside a check; promote the fitting route when constraints exclude the default | User pathways proposal amended; Active template now keeps immediate recovery visible |
| P2 | Research expands into all-model comparisons | Name the next action research unblocks; stop at a credible route and known limits | Agent proposal amended with explicit research bound |

## User pathway acceptance cases

- **Ten minutes to understand:** reach an explanation and small application without setup or tool shopping.
- **Try one paragraph:** get a bounded attempt and check without being pulled into a full production pipeline.
- **A step failed:** see the relevant immediate recovery action without searching an appendix.
- **Audio must stay local:** get a fitting main recommendation; a hidden local alternative is insufficient.
- **Find the command again:** jump directly to the relevant instruction and source evidence.
- **Creator's program is missing:** understand the gap, take a useful next step and return to the lesson; proposed prior art must not look like a tested replacement.

Before adoption, run these against representative guides and observe navigation and task behavior. Document review and link checks cannot establish that users succeed.

## Adoption update

The user authorized adoption. Active authoring guidance and template now address format inference, source/setup differences, bounded research, distinct readiness gates and visible recovery. The separate reader experience contract governs navigation and user wording. Both narration views apply the changes, with exact-topic companion return and memory-only notes. Browser verification establishes behavior; the acceptance cases still require observed reader/task review. CLI prompt routing and production integration remain separate future work.

## Original proposed next change

Revise the active authoring guidance and template together, then validate the source-first narration guide and a real source walkthrough against the cases above. Keep companion-prompt routing changes separate from UX validation. Production integration remains subject to the existing integration review.
