# A small teaching format for video-derived guides

2026-10-27. Proposal only; no guide, prototype or production behavior changed.

## Recommendation

Adopt **one practical outcome, a short explanation, an action and a check**. Keep one canonical guide with an optional quick-reference view and per-step evidence. The goal is to help someone apply a technique in their project, recover when blocked, and later look up how it works.

Teach Me supplies useful authoring patterns. Its full learning system serves a broader job than Video Buddy needs today. This review inspects local guidance, scaffolds and an actual lesson; it does not establish that those patterns improve task completion in our app.

## What to take

| Teach Me pattern | Small Video Buddy adaptation |
|---|---|
| Concrete mission and observable win | Start with the result, target environment and prerequisites. Reuse known intent; ask only when a missing detail changes the procedure. |
| End-state preview, context, then explanation | Show what finished looks like and explain the mechanism in a short paragraph. Use a diagram only when it clarifies a relationship or sequence. |
| Code framed by purpose and observable result | Before a command/configuration, name its purpose and where it goes. After it, show the expected result. Mark incomplete snippets and missing dependencies. |
| Exercises tied to the win, with hints and answer criteria | One optional transfer task after the main procedure. Reveal a hint, then criteria to check the result. Avoid gates and definition quizzes. |
| Reference as a work-time lookup artifact | Offer a compact settings/decision/recovery table derived from the same guide. It should answer a question quickly, not retell the lesson. |
| Optional depth in details; explanation beside relevant visuals | Keep required instructions visible. Reveal rationale, alternatives, evidence and troubleshooting near the current step. |
| Private learner records separate from shareable material | Keep user results/notes out of committed guide fixtures. Self-report, observed task completion and machine execution remain distinct. |

Retain Video Buddy's stronger evidence distinctions: **shown in video**, **adapted for the target**, **tested under stated conditions**, and explicit gaps. Documentation support and a working code block do not establish learner understanding or successful completion.

## Proposed guide shape

1. **Your result:** one sentence and a concrete done condition. Add a preview only if useful.
2. **Before you start:** essential tools, versions, inputs and missing prerequisites.
3. **How it works:** a brief explanation that makes the procedure understandable.
4. **Steps:** each has “Do”, a short “Why” where needed, and “Check”. Attach the source moment and origin/status; reveal deeper evidence on request.
5. **Try one change:** optional application to the reader's actual goal, with a collapsed hint and observable success criteria.
6. **Keep handy:** a compact reference plus next action if blocked.

No fixed step count. A source's chapter structure need not become the guide structure. If the source cannot support the promised result, narrow the outcome or show the missing work before the reader begins.

## Applied to the narration sample

**Result:** produce narration that can be revised one paragraph at a time while keeping captions aligned. The current sample describes this outcome; it has not executed it.

**How it works:** each paragraph is a replaceable audio unit. Joining fixes their order; timing is derived from the final joined narration, so duration changes affect downstream cues.

**Example step — replace a paragraph**

- **Do:** regenerate the changed paragraph, keep the other accepted takes, then rebuild the final narration.
- **Why:** limit regeneration while preserving a coherent final timeline.
- **Check:** unchanged takes are retained, the replacement joins cleanly, and captions still match the revised audio.
- **Evidence:** the video describes paragraph-level generation and downstream timing at6:44–7:05. The revision/check procedure is our adaptation, not a demonstrated production run.

**Optional transfer question:** “Your replacement paragraph is longer. Which work can you keep, and which needs another check?”

**Hint:** separate the accepted audio units from the timeline built from them.

**Criteria:** keep unchanged paragraph takes; rebuild the final audio; refresh or inspect affected caption/visual timing; listen at joins. A plausible explanation is not proof of a correct final export.

**Reference:** voice/model/settings, paragraph naming/order, regeneration rule, caption check, missing custom automation dependency. Keep the creator's application configuration separate from provider API fields.

## What to defer

Do not import Teach Me's Preact shell, learner-profile machinery, topic DAGs, quizzes, spaced repetition, Anki exports or separate lesson/reference publishing pipeline. A shared Markdown-first guide can support the present linked and adjacent-evidence views. Consider additional machinery only after a real task demonstrates the need.

Also omit universal quotas such as a diagram for every concept, three glossary terms or three citations per page. Match explanation and evidence to the claim. Keep important gaps plainly visible; useful next actions must not hide unverified execution behind reassuring prose.

## Small adoption experiment

After the current layout review, revise the sample's authoring structure once and apply it identically to A and B. Do not improve only B's content. Ask the reader to explain the revision rule, identify the missing automation dependency, and perform one revision if an authorized working environment exists. Observe lookup effort, corrections and actual result separately. Keep ticket18 focused on review layout,21 on fresh task performance, and28 on integration scope. No new learning-platform dependency is proposed.

## Inspected sources

Local Teach Me checkout at HEAD `fc5335a57aab98fd08355202dbad1f82ce04c5d1`; these links refer to its working files, which may change. Teach Me was read only.

- [Teaching workflow and lesson shape](D:/code/teach-me/.kiro/skills/teach/SKILL.md): mission, one win, references, private learner state and publishing requirements.
- [Informal learning decision](D:/code/teach-me/.memory/adr/0001-informal-learning-posture.md): delivery-oriented learning; rejects prediction-quiz/scaffold-withdrawal course patterns. Some broader visual guidance still lists prediction as an exercise example; prefer this explicit decision for our lightweight proposal.
- [Lesson components](D:/code/teach-me/.kiro/skills/teach/references/lesson-components.md): optional depth, hints, visuals and plain-language self-assessment.
- [Lesson scaffold](D:/code/teach-me/assets/scaffolds/lesson.html) and [reference scaffold](D:/code/teach-me/assets/scaffolds/reference.html): observable win, hint/criteria and work-time lookup structure.
- [Visual teaching guidance](D:/code/teach-me/.kiro/steering/visual-teaching.md): purposeful visuals, colocated labels, contextual code and complete/fragment metadata. Its research effect-size figures were not independently audited or adopted here.
- [Actual Ink lesson](D:/code/teach-me/library/ink-godot/lessons/0001-ink-flow-and-knots.html): win, explanation and exercise patterns in an authored artifact.
- [Code checker](D:/code/teach-me/tools/check-lesson-code.py): toolchain checks and explicit skips. A successful syntax check or skipped runtime is not demonstrated end-user behavior.
