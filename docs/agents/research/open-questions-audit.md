# Independent audit: open research questions

Audit date: 2026-10-25. Target: [open-questions.md](open-questions.md). Auditor did not produce the register. **Pass; trust score 94/100 for experiment planning, not deployment clearance.** Primary-source snippets support the load-bearing claims, and missing weight/dependency eligibility is explicitly unresolved rather than inferred. No production/model-quality winner follows from this pass.

## Method and currency

Re-fetched all 32 external source URLs in the register (GitHub blob links through their raw equivalents, Hugging Face cards at the cited revisions). All returned usable content. Separately fetched raw current Qwen3-VL, yt-dlp and DINOv2 READMEs because rendered repository pages contain substantial page chrome. Checked the local S1/S2/S5 reports. Pinned sources match the tested revisions; moving sources are suitable only as dated research observations and must be pinned when their components are selected.

Authenticated checkpoint access is a parent-agent observation, now preserved in [checkpoint-access-2026-10-25.json](checkpoint-access-2026-10-25.json). The auditor did not reread credentials or independently repeat authentication. This limits independent verification of that observation, not the source/API diagnosis or the documented model notices.

## Per-claim verdicts

| Claim | Verdict | Evidence check |
|---|---|---|
| SAM 3.1 session wrapper passes an unsupported keyword | Supported | Re-fetched pinned wrapper and multiplex source; wrapper passes `offload_state_to_cpu`, callee signature omits it and has no variadic keyword argument. Prior runtime traceback corroborates this. |
| Dropping false would not implement true CPU state offload | Supported as proposed experiment boundary | Follows directly from the unsupported parameter; no repaired inference is claimed. Bucket-size mismatch is a preserved local experiment observation, not an upstream performance claim. |
| All three checkpoint accesses are now approved | Weak: directly observed, not independently repeated | Root metadata probe records approved access and DINOv3 revision/size. Correctly distinguished from inference and licensing. Earlier 403 remains historical. |
| CrisperWhisper v1 superseded, CC-BY-NC-4.0; v2 different non-commercial terms; code MIT | Supported | Both pinned cards and current code LICENSE contain the quoted notices. Installed worker identity remains explicitly unknown. |
| OmniParser original detector AGPL, v3 detector MIT, imported code root CC-BY-4.0 | Supported | Exact pinned model card, v3 license and code-root license match the snippets. Card's broad MIT-pipeline language does not erase the independently observed code-root notice. |
| Qwen3-VL has genuine video input plumbing; still-image test is not video evidence | Supported | Raw current README contains `return_video_metadata=True`, `image_patch_size=16`, `do_resize=False`, torchcodec and earlier decord guidance. Local inference claim is scoped to stills. |
| yt-dlp resume/archive mechanisms do not establish downstream completion | Supported | Raw README contains quoted resume text and archive text across wrapped lines. Broader recovery behavior is explicitly an experiment requirement. |
| Original SAM code/model Apache; dataset separate research terms | Supported | Pinned README explicitly licenses the model Apache 2.0 and names SA-1B Dataset Research License separately. |
| SAM 2.1 checkpoints/code Apache, optional components separately noticed | Supported | Pinned README explicitly names checkpoints, demo/training code, fonts and optional connected-component code. |
| EfficientSAM code Apache; separate weight coverage not established | Supported, appropriately unresolved | Pinned LICENSE is Apache; no unverified blanket weight clearance claimed. |
| EfficientTAM checkpoints and code Apache | Supported | Pinned README explicitly covers both. |
| SAM 3/3.1 custom SAM License | Supported | Pinned LICENSE headed SAM License; no Apache inheritance asserted. |
| Grounding DINO code/checkpoint Apache | Supported | Code LICENSE and exact tiny-card metadata match. Composed/cloud variants correctly remain separate assets/services. |
| Florence-2-base-ft card MIT; code/dependency inventory incomplete | Supported, appropriately unresolved | Exact tested card contains MIT metadata; no blanket dependency clearance. |
| OmniParser caption model notice MIT | Supported | Exact pinned model card's component table names the caption weights MIT. Imported code still requires its own notice inventory. |
| Ordinary DINOv2 code/weights Apache, specialized variants differ | Supported | Current raw README covers ordinary models and separately names non-commercial X-ray/Cell-DINO notices. |
| DINOv3 custom license | Supported | Official LICENSE.md headed DINOv3 License. |
| Qwen3-VL code/model Apache | Supported | Official code LICENSE and exact tested card match. Decoder/dependency notices are correctly separate. |
| EasyOCR/PaddleOCR/Tesseract code Apache; exact asset coverage incomplete | Supported, appropriately unresolved | Official repository LICENSE files match. No unsupported traineddata/recognizer blanket license assertion. |
| faster-whisper code MIT; cited converted large-v3 asset MIT | Supported | Code LICENSE and cited model card match; actual configured checkpoint remains to be pinned. |
| WhisperX BSD-2-Clause, assets independently require inventory | Supported | Official LICENSE matches; no blanket ASR/alignment/diarization clearance. |
| sherpa-onnx code Apache, exact diarization assets unresolved | Supported, appropriately unresolved | Code LICENSE matches; model asset terms not invented. |
| Community-1 anonymous fetch returned 401 | Weak: historical acquisition observation | Exact failed response is not independently reproduced here and does not establish current authenticated access. Register correctly leaves asset terms/access unresolved. |
| S1 no timed reader, S2 no native-video evaluation, S5 20/20 bounded observations | Supported | All three quoted snippets exist in the local reports; S5 limitations remain visible. |
| Procedure steps and citation quality need distinct checks | Supported as prior art/inference | Microsoft page contains the instruction-per-step quote; ALCE abstract contains fluency/correctness/citation-quality phrase. Neither proves product task-completion benefit. |
| Coverage table's model/corpus/UX/storage questions | Supported as explicit experiment requirements | Mapped to existing reports/tickets; not presented as vendor facts or completed experiments. |

## Findings and limits

1. **No blocking citation mismatch found.** The yt-dlp archive quote is whitespace-normalized across help-text line wrapping; its wording and interpretation match.
2. Root-authenticated access and the anonymous Community-1 failure are observations with limited independent auditability. Keep them dated, retain the probe artifact, and recheck at actual download time. Do not use them as evidence of quality or deployment eligibility.
3. Several eligibility rows intentionally stop at repository/model-card notices. That is adequate to identify the next observation, not sufficient for distribution or a whole-stack commercial claim. Exact downloaded asset/dependency manifests remain work for the owning tickets.
4. Moving-source URLs are date-qualified but not immutable. Pin Qwen decoder/toolkit, yt-dlp version and selected code/licenses when reproducing the spikes.

The register has verifiable primary-source content and a nonempty unresolved-work handoff. It can support closing the research-planning ticket while the owning inference, usability and integration tickets stay open.
