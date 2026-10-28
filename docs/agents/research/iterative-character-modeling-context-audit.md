# Audit: iterative character-modeling context

Independent audit, 28 October 2026. Reviewed the findings and the separate context proposal; active guides were not changed.

**Overall trust: 8.5/10 — pass with bounded limitations.** Current Blender 5.2 source supports the technical distinctions. Practitioner sources support useful prior art; they do not establish a universal method name, prevalence or a new trend.

## Claim verdicts

| Finding | Verdict | Independent check |
| --- | --- | --- |
| 1. Blockout/refinement and polygon versus brush editing | Supported | Both quoted fragments match the official 5.2 mesh-introduction source. The descriptive coarse-to-fine mapping is appropriately marked as interpretation. |
| 2. Non-destructive operations versus iteration | Supported | All three fragments match the official modifier introduction. Applying changes and editing original data support the stated limitation. |
| 3. Linked mesh data is not a backup | Supported | Both fragments match Duplicate Linked. The inference is sound, with the shared-Action limitation already recorded. |
| 4. Early pose-test precedent | Supported, course-specific | Live Studio outline independently shows the quoted pose test between expression tests and face/head retopology. It supports that course sequence, not prevalence or current UI behavior. |
| 5. Hard-surface/organic overlap | Weak as general guidance; supported as dated prior art | Studio page matches the modifiers/feedback excerpts. Its organic deformation-test text also matches after inline whitespace normalization. The page explicitly remains WIP with a 2023 notice. |
| 6. Animation blocking adjacency | Weak as general guidance; supported as historical prior art | Both excerpts match the first-party 2021 animator article. The findings correctly avoid naming Noggi's modeling method “animation blocking.” |
| 7. NPR definition and Guilty Gear context | Supported definition; weak publisher refetch | Official 5.2 Freestyle source independently defines NPR as a rendering approach. Arc System Works publisher URLs returned HTTP 403 on this audit, so its exact quotation/date could not be independently confirmed. Retain that material as historical context with an access limitation, not technical lineage evidence. |

The official release-branch API independently confirms commit `4a3be8f9ed3b66b24913e0a0d491d3429a70ea08`, dated 17 August 2026. Finding links currently target the mutable release branch; commit-qualified source links would make the recorded pin reproducible. Quoted snippets remain within 25 words per cited source. No member-only transcript or image was reproduced in the findings.

## Corrections and refinements

1. **Publisher access limitation:** disclose that the independent auditor could not refetch the Arc page. The technical recommendation does not depend on it; do not upgrade it to verified detailed production history.
2. **Editing terminology:** in the research's adjacent-route table, replace “Another representation/production route” for sculpting with “Another editing/production route.” The cited introduction describes brush deformation of the same mesh; it does not establish a distinct underlying representation.
3. **Pinned links:** prefer raw commit-qualified URLs for the four 5.2 manual files, while retaining readable documentation links. This is a reproducibility improvement, not a mismatch in the inspected branch content.
4. **Learner hierarchy:** the proposed context block repeats part of the existing whole-source overview. Keep context responsible for category and relationships; let the existing overview own the blockout–pose–refine recipe. The map and adjacent paths should remain optional, as proposed.

The suggested labels are explicitly descriptive, not claimed standards. The proposal appropriately separates feedback strategy, editing/reversibility, asset type and visual target, and makes no unsupported prevalence, regional or emerging-trend claim. No reader-comprehension or UX result is established by this document audit.
