# Ticket 18 review pack — prepared, not a usability result

Question: does evidence adjacent to a blocked guide step reduce lookup and correction work compared with a linear linked document?

Throwaway prototype: open prototype.html. A is linear linked-document rendering, B is adjacent evidence; use ?variant=A or ?variant=B. Exactly two variants implement the ticket-defined comparison. Same task, source frame, source commands, guarded adaptation, checkpoint text, documentation and raw execution links. The baseline is an HTML rendering of a Markdown-style document, not a test of an actual editor/chat application. Both have the same note/pause controls, so the comparison isolates layout imperfectly rather than adding controls only to B.

No command runs, files change, network requests are made automatically, or notes persist. Source frame and raw results are offline; optional publisher/docs links require internet. Record/export are memory-only; copy JSON before closing. Pause hides the guide and restores notes; it does not qualify crash/reload recovery.

## Frozen task / procedure

Fixture: ticket17 source at 10:38, same retained frame and provenance/results under ../guide-adaptation. Existing index.html contains useful work; target profile is native-only PowerShell without GNU touch. Flawed draft Force command is explicitly unexecuted and deliberately wrong for preservation. Reader locates exact source commands, missing prerequisite, safe correction/checkpoint, support vs tested status, and next action after interruption. Do not execute the flawed draft or ask the reader to run any commands.

Current user has seen ticket17 findings: formative review, not fresh performance. Begin A, record answer/help/friction, pause/return, record, then optionally inspect B and explain what changed. Same-task learning makes quantitative A/B attribution invalid. Next fresh participant should begin B; equivalent unseen tasks and counterbalanced orders are needed before comparative claims. Ticket21 retains fresh-performer execution qualification.

Collect actual reader answers separately from machine QA. Local events measure page interactions and wall timestamps only; they miss external evidence reading and unreported help. Do not infer completion, confidence or success from buttons, timestamps, elapsed time or model agreement. Mark reader self-report, directly observed behavior and machine checks separately. Ask about behavior, not visual preference. No automatic scoring or pass threshold.

## Preparation checks, 2026-10-26

Playwright Chromium: identical guide/evidence text (layout headings/link affordance excluded), A linear/B columns, real evidence links, mobile390px without overflow, pause/resume, note retention across switches, export, arrow-key input exclusion, no page errors. Browser automation filled synthetic notes; these are QA, not participant responses, and were discarded. Screenshots ignored under .scratch/review-ux. No reader has been observed; format winner unresolved. Prototype only; no app integration.

Reproduce: open the file in a current browser. No dependencies or server needed. Source artifacts are pinned by parent branch commit f305c9fe9f3f87f5c04bf6c27e92d600a67b4f01. No new media copies or package changes. Cost: one static HTML page and this protocol; reader time not measured. Ticket18 remains in_progress pending the invited review.
