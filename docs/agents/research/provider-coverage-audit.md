# Independent audit: current-provider coverage expansion

Audit date: 2026-10-25. Target: the “Current-provider coverage expansion” section of [open-questions.md](open-questions.md), not the earlier register. **Pass, 95/100 for bounded experiment planning.** No blocking source/snippet or current-version mismatch found. This is not deployment clearance, measured model quality or exhaustive market coverage.

## Method

Independently re-fetched all 20 unique cited external URLs. GitHub/Hugging Face blob links were read through their raw equivalents; rendered Google/Ultralytics pages were decoded to check content beyond navigation. Also checked four current PyPI JSON manifests and both IDEA API repositories' LICENSE files at the cited source revisions. All fetched successfully. No credential, checkpoint download or inference was performed by the auditor.

## Per-claim verdicts

| Claim group | Verdict | Independent evidence |
|---|---|---|
| Gemini current catalog distinguishes flagship Argon and stable Flash3.8 | Supported | Official models page lists Gemini4Argon as flagship with endpoint gemini-4-argon and Gemini3.8Flash as stable. This does not establish account availability. |
| Gemini segmentation geometry uses normalized coordinates and specified box ordering | Supported | Official image guide describes polygon masks and box_2d as [ymin,xmin,ymax,xmax] normalized0–1000; do not substitute an older raster-mask contract. |
| Gemini static video defaults to1FPS and has a separate opt-in agentic mode | Supported | Official video guide explicitly distinguishes both modes and warns rapid content can be missed; last-updated date2026-10-13 matches the register. |
| Gemini unpaid/paid data handling differs | Supported | Official terms have separate Unpaid Services/Paid Services sections; the register correctly leaves deployment policy and budget unresolved. |
| Molmo2 general model differs from video-point and GUI-point specialists | Supported | Pinned source/cards match IDs/revisions. Vid4B says only trained for video pointing; GUI8B says single-image input and single-point output. GUI example's Img8B naming inconsistency is real. |
| Molmo cards request Transformers4.57.1 and remote implementation | Supported | Pinned setup/examples use the stated version and trust_remote_code. Latest package metadata does not override a tested recipe. |
| Molmo Apache notices do not erase third-party dataset restrictions | Supported | Pinned code/card metadata identify Apache2.0; each selected card includes the academic/noncommercial third-party-dataset warning. No legal clearance is inferred. |
| 4B/8B local memory fit and offload remain unmeasured | Supported as explicitly qualified inference | The register labels estimates as resource inference, not a verified minimum or completed runtime. Quantization/offload must be separate configurations. |
| YOLOE26s is a current practical text-prompt representative | Supported | Official guide uses yoloe-26s-seg.pt and set_classes. Prompt-free checkpoints reject language prompts; visual prompts use temporary numbered labels. |
| YOLOE text encoding requires auxiliary assets | Supported | Official guide identifies mobileclip2_b.ts and ultralytics/CLIP installation; asset hashes remain execution work. |
| YOLO27 is unavailable as a comparison arm | Supported | Current official FAQ explicitly says no release/set launch date and labels it coming soon. Preview navigation alone would not prove availability. |
| Ultralytics source uses AGPL3.0 | Supported | Pinned raw LICENSE is GNU AGPL3.0. This does not settle all model/dependency/intended-use obligations. |
| DINO-X and GroundingDINO1.6 are hosted models distinct from local tiny | Supported | Pinned official API READMEs describe DINO-XPro,1.6Pro, API V2 transition and token application/quota. Local GroundingDINO smoke evidence does not test them. |
| IDEA API/demo client code is Apache2.0 | Supported | Independently fetched both pinned LICENSE files; both Apache2.0. Client license is not hosted-service terms or weight access. |
| NVIDIA current family is Cosmos3 with Edge4B, not Reason2 | Supported | Pinned NVIDIA source calls Cosmos3 the current family and dates Edge toJuly2026; pinned Edge card describes4B and the vllm/vllm-openai:cosmos3 reasoner container. |
| NVIDIA selected source/model notice is OpenMDW1.1 | Supported | Pinned root notice and model card identify OpenMDW1.1 and separate third-party notices. No12GB/Windows deployment claim follows. |
| Package versions are current metadata, not a tested integration | Supported | PyPI manifests returned google-genai2.33.0, ultralytics8.4.189, dds-cloudapi-sdk0.5.3 and transformers5.20.2. |
| Hosted availability, runtime quality and task benefit remain unknown | Supported as bounded scope | The report explicitly distinguishes documented, attempted, observed, qualified and selected. Missing access is not a negative quality result. |

## Non-blocking traceability improvements

1. Link package-version claims to the actual PyPI manifests: [google-genai](https://pypi.org/pypi/google-genai/json), [ultralytics](https://pypi.org/pypi/ultralytics/json), [dds-cloudapi-sdk](https://pypi.org/pypi/dds-cloudapi-sdk/json), [transformers](https://pypi.org/pypi/transformers/json). These values were independently verified but the register currently states them without explicit metadata links.
2. Link the code-license claim to the pinned [DINO-X LICENSE](https://github.com/IDEA-Research/DINO-X-API/blob/813c629437e5c34c3008669944b4b36ac16a6454/LICENSE) and [GroundingDINO API LICENSE](https://github.com/IDEA-Research/Grounding-DINO-1.5-API/blob/2be80fe64ab3ca7f105821c31840ef303fbc14b9/LICENSE), rather than relying only on README links.
3. Preserve actual package/environment and asset hashes when executing. A current source-tree pin is not independently proof that an installed package was built from that exact commit.

No finding requires blocking the planned local experiments. Catalogs and hosted aliases remain moving sources and must be rechecked at actual execution time. The audit's pass applies to the researched selection boundaries, not a claim that the provider comparisons are complete.
