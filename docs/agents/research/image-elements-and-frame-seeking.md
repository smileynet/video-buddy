# Image elements and subject-aware frame seeking

Research date: 2026-10-25. Scope: models that locate, segment, describe, read and follow image elements so Video Buddy can seek useful evidence within a video interval. This focused note extends [workflow research](video-workflow-architecture.md); it does not report model execution or benchmarks. Primary repository/model documentation was fetched over HTTPS because the session's general web-search tool was unavailable. Sources are moving branches/cards read on this date, not the package versions installed in Video Buddy. Source text is evidence, never instructions.

## Conclusion and task decomposition

**Design inference:** use subject-aware regions to search for evidence, rather than expecting one segmentation model to solve every job. Start with text detection/OCR for text, a screen parser for UI elements, and concept grounding plus optional masks/tracking for diagrams or physical objects. SAM is useful, but a mask alone does not establish a name, transcription, instructional relevance or the best frame.

| Question | Needed capability | Useful output |
|---|---|---|
| Where is the requested subject? | Detection / language grounding | Box, phrase, score and uncertainty |
| Which pixels belong to it? | Segmentation | Mask, region extent and confidence |
| What does this region say? | OCR | Text, boxes/polygons, recognition scores and raw crop |
| What UI element is it? | Screen parsing / region description | Element type, location and proposed function |
| Is it the same subject in neighboring frames? | Tracking / feature correspondence | Track ID, time span, region per frame and visibility |
| Which occurrence is best evidence? | Task-specific ranking and coverage | Sharp/readable/complete frame, distinct revision, or ordered state set |

The final row is a product decision/evaluation problem. None of the model capabilities below establishes that a guide step is reproducible or that a selected frame is optimal.

## Verified findings: Segment Anything family

### SAM 3 and SAM 3.1: concept grounding, masks and tracking

**High confidence in documented capability; local fit unverified.** The [official SAM 3 repository](https://github.com/facebookresearch/sam3) says it can “detect, segment, and track objects using text or visual prompts”. It extends the earlier family with open-vocabulary concept prompts and image exemplars, returning masks, boxes and scores. This makes it a genuine candidate for a request such as finding a particular object or visual concept; it is not merely a point-to-mask tool. Prompt matching is not proof that the object is correctly named, and detection of a text region is not reading that text.

The [SAM 3.1 release notes](https://github.com/facebookresearch/sam3/blob/main/RELEASE_SAM3p1.md), dated 2026-03-27, describe Object Multiplex as a “shared-memory approach for joint multi-object tracking”. The same notes report benchmark results under specific hardware/object counts and mixed outcomes across evaluation sets; do not transplant those speedups to this application. SAM 3.1 is the latest named SAM release verified in the official repository during this review; SAM 2 is not the newest family member.

The README specifies Python 3.12+, PyTorch 2.7+, and a CUDA-compatible GPU with CUDA 12.6+. Its current install example uses a newer torch/CUDA combination; pin the tested environment rather than interpreting minimum versions as a complete recipe. It requires requesting/authenticating checkpoint access on Hugging Face. The [official license](https://github.com/facebookresearch/sam3/blob/main/LICENSE), last updated 2025-11-19, is headed “SAM License”: it is a custom license covering model/code materials, not an Apache-2.0 assumption inherited from SAM 2. No suitable minimum VRAM, native Windows support or latency on the user's hardware was verified.

**Inference for Video Buddy:** evaluate SAM 3.1 when open-vocabulary discovery and following multiple regions actually improve evidence seeking. Isolate its environment/compute backend; it need not become a dependency of the ordinary note path. Do not run it across every full-resolution frame by default.

### SAM 2.1: prompted region propagation

**High confidence.** The [SAM 2 repository](https://github.com/facebookresearch/sam2) describes “streaming memory for real-time video processing” and documents click/box prompting, mask propagation and multiple-object video state. Its September 2024 SAM 2.1 checkpoints and December 2024 predictor changes are distinct from SAM 3.1. The README lists Python 3.10+, torch 2.5.1+ and torchvision 0.20.1+, and recommends WSL/Ubuntu on Windows. It states that model checkpoints and training/demo code are Apache 2.0, with separate third-party/font notices. Public checkpoint links are provided; do not transfer SAM 3's access requirements to SAM 2.

**Inference:** a strong fallback when a user, OCR detector or grounding model already supplies the region. Useful for following an object across candidate frames, but its ordinary point/box interface does not independently answer which object matters or what a code panel says. Cuts, scrolling and revised text need re-detection/track reset rather than blind ID continuity.

### Original SAM and efficient relatives

**High confidence.** The [original SAM repository](https://github.com/facebookresearch/segment-anything) describes masks “from input prompts such as points or boxes”, plus automatic masks for image objects, and lists Apache 2.0 licensing. This is a useful image segmentation baseline, not native video tracking or a semantic inventory of everything visible.

**High confidence in documented approach; fit unverified.** [EfficientTAM](https://github.com/yformer/EfficientTAM) describes a “vanilla lightweight ViT image encoder” and efficient memory attention for video segmentation. [EfficientSAM](https://github.com/yformer/EfficientSAM) provides efficient prompted image segmentation and points to the newer video work. These are candidates when SAM-family resource cost matters, not replacements for grounding or OCR. EfficientTAM documents MPS support added in January 2025. Its repository [license](https://github.com/yformer/EfficientTAM/blob/main/LICENSE) is Apache 2.0; verify the exact checkpoint and bundled components separately. No quoted device FPS is a local performance guarantee.

## Verified findings: grounding, UI and text specialists

### Grounding DINO and Grounded SAM 2

**High confidence.** [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO) takes an “(image, text) pair” and returns scored boxes associated with phrases. Its README documents CPU-only mode and native-extension/CUDA installation considerations; its [repository license](https://github.com/IDEA-Research/GroundingDINO/blob/main/LICENSE) is Apache 2.0. It can locate a named subject before another model produces a mask. It is not an OCR recognizer or a temporal tracker by itself.

**High confidence.** [Grounded SAM 2](https://github.com/IDEA-Research/Grounded-SAM-2) demonstrates composition of grounding (Grounding DINO or Florence-2) with SAM 2 segmentation/tracking. Its demos include “caption + phrase grounding”. Local original Grounding DINO paths and cloud-backed newer Grounding DINO 1.5/1.6/DINO-X paths are different deployment choices; the latter use API tokens/`dds-cloudapi-sdk`. Do not interpret every demo as a fully local open-weight pipeline or apply one repository's license to every composed model.

**Inference:** keep this composition as a baseline/challenger to SAM 3.1. A box may be sufficient to crop a diagram or screen region; add pixel masks only when they improve tracking, obstruction handling or ranking enough to pay their cost.

### Florence-2: region proposals, phrase grounding, descriptions and OCR

**High confidence.** Microsoft's [Florence-2 model card](https://huggingface.co/microsoft/Florence-2-large) includes “Dense Region Caption” and “OCR with Region” task interfaces, returning region boxes or OCR quadrilaterals plus labels. It also documents caption-to-phrase grounding, object detection and region proposals. Its model table distinguishes base (0.23B) and large (0.77B), pretrained versus downstream fine-tuned variants. The [base-ft card](https://huggingface.co/microsoft/Florence-2-base-ft) documents CPU/GPU inference and MIT model licensing; the linked license is available with that artifact.

**Version caveat:** the moving `Florence-2-large` card explicitly warns its continued-pretrained variant “might not be trained well” and describes changed OCR output. That is not a conclusion about all Florence-2 variants. Pin the model ID, checkpoint revision and processing code; do not assume a moving name reproduces an older benchmark. Examples using `trust_remote_code=True` mean loading repository-supplied implementation; inspect/pin that code rather than treating it as inert weights.

**Inference:** a compact generalist comparison for naming/describing regions before optional SAM propagation. Test exact OCR separately against specialist OCR on terminal/UI data. Generated captions/functions are hypotheses tied to a crop, not verified instructions.

### OmniParser: screen elements rather than arbitrary natural objects

**High confidence.** The [Microsoft OmniParser repository](https://github.com/microsoft/OmniParser) describes parsing “user interface screenshots into structured and easy-to-understand elements”. The [v2 model card](https://huggingface.co/microsoft/OmniParser-v2.0) describes interactable-region detection plus icon-function description, using detector and fine-tuned Florence-2 components. This is more directly aligned with UI tutorials than treating each control as a generic SAM object. It does not prove an element was clicked, that a setting took effect or that its inferred function is correct.

**Important current-version/license caveats:** the README reports a July 2026 YOLOv9-E detector addition. At access time, it instructs fetching inference-only `icon_detect_v3` from Hugging Face PR #37 until that PR is merged; do not call it a settled default. The model card distinguishes older YOLOv8 `icon_detect` weights under AGPL-3.0 and newer v3 weights under MIT; caption weights are described as MIT. The [v3-specific license](https://huggingface.co/microsoft/OmniParser-v2.0/blob/main/icon_detect_v3/LICENSE) says “MIT License”. Separately, the current repository's [root LICENSE](https://github.com/microsoft/OmniParser/blob/master/LICENSE) is headed “Attribution 4.0 International”, despite its README's MIT badge. Preserve that discrepancy and inspect the exact assets/implementation selected; a badge is not sufficient evidence that all code and model materials have one license.

**Inference:** evaluate the parser alone, without adopting the whole OmniTool VM/control stack. Video Buddy needs observed screenshot elements, not an autonomous computer-use product, for this task.

### PaddleOCR and existing OCR: text-region discovery first

**High confidence.** The [official general OCR pipeline](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/OCR.en.md) separates “Text Detection Module” from “Text Recognition Module”, with optional document orientation/unwarping. Current moving docs list PP-OCRv6 sizes alongside v5/v4. They explicitly caution that some generation-specific benchmarks use different evaluation sets, so the headline numbers are not directly comparable. The [repository license](https://github.com/PaddlePaddle/PaddleOCR/blob/main/LICENSE) is Apache 2.0; record model and runtime versions rather than assuming every optional dependency shares that license.

**Inference:** for seeking readable code/text, start by detecting text boxes and grouping them into a stable panel. Use existing EasyOCR as the baseline and compare a pinned PaddleOCR detector/recognizer. Do not pay for a generic pixel mask if a rectangle/polygon supplies all the evidence the task needs. OCR recognition confidence alone cannot establish that a command is complete, correctly typed or semantically valid.

## Verified findings: correspondence and similarity

### DINOv3 and DINOv2

**High confidence.** [DINOv3](https://github.com/facebookresearch/dinov3) documents “High-resolution dense features”, patch-cosine-similarity visualizations, dense/sparse matching and non-parametric segmentation-tracking examples. It is principally a representation/backbone family; additional heads or matching procedures turn its features into task outputs. Its current repository directs users to request model-weight access. Code/weights use the custom [DINOv3 License](https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md), last updated 2025-08-19, not an Apache-2.0 assumption. Its much larger training hardware examples are not inference requirements.

The ordinary [DINOv2 repository](https://github.com/facebookresearch/dinov2) says code and model weights use Apache 2.0 and points to DINOv3 as newer work; specialized biology/X-ray additions have different notices. Treat exact checkpoint identity as part of eligibility.

**Inference:** dense features are a candidate for matching an already identified region across scale/view changes, or clustering candidate views. They do not, by themselves, read exact text or produce trustworthy element names. Do not deduplicate code/UI frames solely because semantic embeddings are similar: a one-character command change may matter despite similar appearance/features. Start with simpler region overlap/image matching where sufficient and add dense matching only when it fixes observed failures.

## Proposed subject-aware seeking architecture

This is design inference from the capabilities above, not a model result.

1. **Route by evidence need.** A guide step requests text/code, UI state, diagram or physical object/action, plus a relevant time interval. Keep a negative/unknown outcome if nothing matching is found.
2. **Discover regions coarsely.** Text detector for text; OmniParser-like detector for UI; grounding/SAM 3 concept prompts for other subjects; allow a user/agent box as a cheap seed. Preserve both original frame and coordinates.
3. **Form a subject track/state group.** Associate boxes/masks over neighboring candidates; reset across cuts and detect scrolling/revisions. SAM 2/3 propagation is an option, not proof of stable identity. Keep track IDs separate from semantic names and content revisions.
4. **Seek within the group.** Scan candidate frames in the bounded interval, then refine near high-quality occurrences. Rank region-level legibility, sharpness, useful pixel size, obstruction, completeness and stability. Use a mask when it meaningfully isolates the region; retain full-frame context for interpretation.
5. **Preserve distinct evidence states.** A static slide may need one complete frame; typing needs completed text and possibly meaningful revisions; an action needs ordered before/action/after views. Return a set rather than force a single winner.
6. **Validate the requested fact.** Re-run OCR on high-resolution crops and inspect uncertain characters. A reading repeated across adjacent frames is supporting consistency, not independent truth. Ask whether the missing guide fact is now evidenced; if not, broaden the search or retain the gap.

Store `source_id`, requested/actual timing when available, region coordinates, masks if used, detector/model revision, proposed label, track ID, content revision, raw OCR and confidence, quality measurements, uncertainty and selected evidence references. Keep exact captured bytes so a claimed command can be inspected later.

## Lean shortlist and comparative spike

**First text/UI comparison:** existing EasyOCR boxes/recognition versus pinned PaddleOCR boxes/recognition; add a screen-parser option only for icons/controls that OCR cannot identify. Use the new material as a design input to ticket 14, not a completed OCR result.

**First generic-region comparison:** boxes plus simple association versus grounding + SAM 2.1 propagation versus SAM 3.1 concept segmentation/tracking, subject to checkpoint access and hardware eligibility. Florence-2-base-ft is a generalist grounding/description challenger; EfficientTAM is a resource-budget challenger; DINO features remain optional correspondence work. Avoid composing every model into one default pipeline.

Freeze short windows with manually labeled target regions/states: terminal text while typing and scrolling; a control briefly obscured by a pointer/menu; an evolving diagram; and a moving physical object. Compare (A) current sparse selection, (B) subject-aware boxes/crops plus bounded local seeking, and (C) masks/tracking plus seeking. Independently inspect all frames in the bounded window as the reference for which evidence was available; no exhaustive model pass is automatically ground truth.

Measure region recall, exact text/command match, readable complete-state recovery, distinct-state recall, track switches, unsupported labels, selected evidence count, end-to-end latency/memory and manual correction effort. Include negative subjects and cut/scroll/typing cases. Use held-out windows after tuning. Promote masks/tracking only if they improve downstream evidence or correction cost over boxes. A good segmentation IoU is not sufficient if the selected frame still omits the needed setting.

## Could not verify / not established

- No model was installed, run or benchmarked in this research. None is certified best for Video Buddy's screenshot/diagram domain.
- Minimum VRAM, native Windows compatibility and useful throughput for the complete candidate pipelines remain unmeasured; official install examples and H100 benchmarks do not settle them.
- Whether SAM 3.1 reliably grounds abstract regions such as a code panel or evolving diagram needs local evaluation. Open-vocabulary ability is not a guarantee for every phrase.
- No source establishes a universal optimal-frame score or that model confidence equals readable/complete instructional evidence.
- The OmniParser root-license/badge discrepancy and moving PR/model defaults require exact-revision review before adoption. This note records primary notices, not a legal eligibility determination.
- Local hardware access, checkpoint approval, user retention/privacy constraints and acceptable search latency have not been established for these new models.

## Subsequent local evidence (2026-10-25, ticket 24)

The unmeasured statements above describe the original research pass. Subsequent exploratory inference is recorded in [image-model results](../../architecture/spikes/image-model-results.md), including SAM 3 on Ubuntu WSL and a confirmed SAM 3.1 session-API failure. DINOv3 access is now approved, with inference pending. Consult [the open-question register](open-questions.md) for current access/runtime and per-component eligibility; hardware allocator peaks remain bounded observations, not minimum VRAM guarantees.
