# Optional worked example: paragraph-based narration

Use this companion when you want to practice or implement the production pattern. The main guide explains the video; this is our additional implementation plan.

**Status:** written plan, with the local text-to-speech component measured. The complete joining/captioned-export workflow has not been implemented or validated. Choose a route and scope before requesting a build.

## Sample guide: build a repeatable narration workflow

### Your result

Make a short narration, replace one paragraph, and keep its captions aligned. You are done when the revised audio plays in order, the unchanged takes are retained, and the captions match what you hear.

### Before you start

Bring a short script and a voice you have permission to use. This guide focuses on prerecorded narration, such as a product demo or training lesson.

**Recommended for a quick hosted trial: an ElevenLabs Studio audio project.** Studio is ElevenLabs' browser-based editor for generating, editing and exporting narration. Start here if you want to finish your first passage with little setup. It keeps the work in one interface, so you can learn the paragraph-revision workflow before writing automation. [Studio guide](https://elevenlabs.io/docs/eleven-creative/products/studio).

**What it costs:**

- **Explore:** the $0 plan includes 10,000 credits per month and three Studio projects. Try an available stock voice to learn the workflow.
- **Use your own voice or publish commercially:** those features are listed under paid Starter. Its pricing card displays $6 per month alongside introductory offers; confirm the recurring charge at checkout.
- **Budget for retakes:** generation uses credits. Compare the cost of an accepted passage, including revisions, before scaling up.

<p class="subtle">Prices checked 27 October 2026. Confirm features and current offers on the <a href="https://elevenlabs.io/pricing">ElevenLabs pricing page</a>.</p>

**Your first action:** create an audio project, add one paragraph, select a voice/model and generate it. Listen, change one sentence, then export the revision. If your own voice is essential, choose a plan with cloning before step 2.

**Prefer local execution?** For a short English trial with the model kept loaded, try **Chatterbox-Turbo** first if its listening samples suit your project. It generated speech much faster in our local run, while **Qwen3-TTS 0.6B Base** used less measured process RAM. Qwen remains a documented multilingual candidate; this spike tested English only. Choose a local trial when audio handling, offline use after setup, control or existing hardware makes local execution a better fit. Expect model downloads, runtime setup and local compute costs. Use the measured comparison and listening samples below, then the setup notes for your chosen route.

<details id="gap-starting-points">
<summary>Alternative starting points</summary>

**How to choose:** first match the workflow to your goal and audio-handling requirements. Then weigh setup effort and the cost of producing and revising your actual script. These are qualitative recommendations, not benchmark scores.

| Starting point | Fit | Setup and upkeep | Cost to consider | Recommendation |
|---|---|---|---|---|
| **ElevenLabs Studio** | First narration, occasional projects, hands-on editing | Low: browser, account and project settings | Free exploration; paid features for own-voice cloning/commercial use; generation credits and retakes | **Start here** for this sample |
| **ElevenLabs Python SDK + audio-joining tools** | Repeated jobs, automated batches, explicit file/revision tracking | Higher: Python, API credentials, ordered files, retries and exports | API usage plus development and maintenance time; a free SDK does not make generation free | Choose when a working manual process needs automation |
| [Qwen3-TTS 0.6B Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) · local candidate | Reference-voice narration in ten documented languages | Higher: Python/device setup, model downloads and output checks | Your compute, storage and setup time; selected code/checkpoint declare Apache 2.0 | Try for multilingual needs; only English and lower process RAM measured here |
| [Chatterbox-Turbo](https://huggingface.co/ResembleAI/chatterbox-turbo) · local candidate | English reference-voice narration | Higher: Python/device setup, checkpoint download and output checks | Your compute, storage and setup time; selected code/checkpoint declare MIT | Next English local trial for warm speed; check listening quality and setup override |

**Use constraints to choose:** when audio must stay local, rule out both hosted routes and qualify one of the named local candidates. If cloud handling is acceptable and setup time matters most, start with Studio. Compare accepted output and total effort before scaling. The local trial below measures speed/resources on one machine; listening preference remains open.

</details>

<details id="local-measured-findings">
<summary>Measured local comparison and listening samples</summary>

**Same sample, same reference:** both models generated the guide's outcome and mechanism paragraphs, using one official demo reference and two seeds. Four cases each ran on Windows with an RTX 5070 / 12 GB. This is a short English trial, not a full narration/caption export.

| Measured here | Qwen3-TTS 0.6B Base | Chatterbox-Turbo |
|---|---|---|
| Warm generation, 3 calls | 19.3–26.4 seconds | 3.2–3.4 seconds |
| Speech produced in those calls | 10.2–12.0 seconds | 12.4–13.2 seconds |
| Seconds of work per second of speech | 1.79–2.30 | 0.254–0.264 |
| Peak sampled process RAM | 2.35 GiB | 4.66 GiB |
| Peak Torch-allocated GPU memory during generation | 2.64 GiB | 3.13 GiB |
| Model load / reference preparation | 13.4 / 3.0 seconds | 61.4 / 15.0 seconds |
| Recognizer disagreements with intended words | 0 / 136 word presentations | 1 / 136 word presentations |

**Choose by the job:** Chatterbox is the stronger next warm English trial for speed; Qwen used less process RAM here and supports a documented multilingual path. Chatterbox required a PyTorch compatibility override on this GPU. A one-off passage also pays model/startup costs. Other GPU activity remained present, so these are observed runs rather than an isolated benchmark or minimum-hardware claim.

**Listen before choosing quality.** Both samples below read the same outcome paragraph. The voice comes from an official model demo, not the video creator or the user. Listen for clarity, pacing, the joins between phrases and whether the intended words were spoken.

Qwen3-TTS — first take:

<audio controls preload="none" src="../local-narration/audio/qwen-cold-outcome.flac" aria-label="Qwen3-TTS reading the outcome paragraph"></audio>

Chatterbox-Turbo — first take:

<audio controls preload="none" src="../local-narration/audio/chatterbox-cold-outcome.flac" aria-label="Chatterbox-Turbo reading the same outcome paragraph"></audio>

**What to inspect:** the recognizer heard “attained” instead of the intended “retained” in Chatterbox's first take; its other takes matched after normalization. All Qwen takes matched the script in this machine check. This does not establish which model sounds better or prove the word was spoken incorrectly. No human naturalness, speaker-similarity or preference score has been collected. All eight outputs were finite and unclipped.

[All eight listening samples, raw measurements, setup details and replay instructions](../local-narration/README.md). Generation timings include each model's normal returned audio path; saving is separate. Qwen used SDPA/bfloat16, Chatterbox its normal generation/watermark path; native defaults differ. Longer scripts, other languages, CPU use and full export need their own trials.

</details>

<details id="local-model-setup">
<summary>Local model setup: quickstarts, downloads and terms</summary>

**Qwen3-TTS:** use the exact cloning checkpoint `Qwen/Qwen3-TTS-12Hz-0.6B-Base`. Follow the [official voice-cloning quickstart](https://github.com/QwenLM/Qwen3-TTS#quickstart) in an isolated environment, provide a permitted local reference recording and its matching text, generate one paragraph and save the WAV. The documented languages are Chinese, English, Japanese, Korean, German, French, Russian, Portuguese, Spanish and Italian. VoiceDesign and CustomVoice are different tasks/checkpoints.

The example uses CUDA, bfloat16 and FlashAttention 2; check compatibility before installing optional acceleration. Load a downloaded model directory when testing offline use. The [code license](https://github.com/QwenLM/Qwen3-TTS/blob/main/LICENSE) and [selected checkpoint metadata](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) declare Apache 2.0.

**Chatterbox-Turbo:** follow the [official Turbo example](https://github.com/resemble-ai/chatterbox#usage), load `ChatterboxTurboTTS`, provide a permitted local reference and save one generated paragraph. The selected `ResembleAI/chatterbox-turbo` checkpoint is English TTS. Its [code license](https://github.com/resemble-ai/chatterbox/blob/master/LICENSE) and [checkpoint metadata](https://huggingface.co/ResembleAI/chatterbox-turbo) declare MIT. Other Chatterbox variants serve different needs; this is a bounded starting shortlist.

**Plan the setup:** download the required model/tokenizer files before an offline trial. The tested CUDA paths ran on this Windows machine. Use the replay record for exact versions and the Chatterbox Torch override; minimum hardware, CPU performance and other platforms still need qualification. Model parameter counts do not establish those results. Inspect the complete runtime's file/network behavior when local handling is required, and check dependencies and recording permissions for your use.

**Plan the cost:** running downloaded weights on your own machine avoids a hosted TTS per-request bill for that route. Include compute/electricity, storage, retries and your setup time; rented GPUs or hosted inference add their own charges. Use the same short script/reference for your first comparison, then record setup effort, generation time, resource use and listening corrections.

**First local win:** save one paragraph, revise one sentence, then carry the accepted audio into joining and caption checks. Use the measured English samples as a starting point, then try your own permitted reference and paragraph. These runs do not select a production default.

</details>

<details id="automation-depth">
<summary>Automation details: generation, joining and timing</summary>

#### Build automation from documented examples

Start with the [official ElevenLabs Python SDK](https://github.com/elevenlabs/elevenlabs-python): generate and save one paragraph. Then inspect the [paragraph-stitching example](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching) for continuity between requests. It is a component of the SDK route, rather than another competing product.

Add features in this order: save an accepted take → record its text/settings and position → generate the remaining takes → join them → check timing → revise one passage. Keep a manifest so you can find the right file when something changes.

**Budget the API route:** the public API page currently advertises Eleven v4 at $0.08 per 1,000 characters. Use that as a starting estimate, then check the applicable account rate, retakes, extra timing calls and taxes. Engineering time is additional. [API pricing](https://elevenlabs.io/pricing/api). There is no measured cost advantage for automation in this sample.

#### Add joining and timing

- **Join accepted files:** [FFmpeg's concat demuxer](https://github.com/FFmpeg/FFmpeg/blob/master/doc/demuxers.texi#L70) reads an ordered list. Standardize and check codecs, sample rates, channels and time bases, or normalize the files before joining. Listen across every boundary.
- **Keep delivery consistent:** the stitching example shows `eleven_v4`, excludes `eleven_v3`, and calls for completed requests with IDs no older than two hours. Check the chosen model/privacy setup. Accepted audio can remain useful after its request ID expires; listen on both sides of a replacement.
- **Create timing:** use transcription, or [forced alignment](https://elevenlabs.io/docs/api-reference/forced-alignment/create) when you have a transcript that matches the final audio. Check names, numbers and joins. Resolve the provider's conflicting large-file limits before a large upload.

Studio handles projects differently from a file-per-paragraph program. Select export quality from your Studio plan; its limits differ from API format options.

#### Explore a different end result

For live replies, begin with [turn-taking and conversation guidance](https://elevenlabs.io/docs/eleven-agents/overview). To change the voice of an existing performance, inspect [voice conversion](https://elevenlabs.io/docs/overview/capabilities/voice-changer). Pick these branches when the end result calls for them; prerecorded narration can stay with the simpler path above.

<p class="subtle">Documentation reviewed 27 October 2026. These researched routes provide alternatives to the creator's custom program. Try one exported passage to establish fit; end-to-end generation, quality and cost have not been measured for this sample.</p>

</details>

### How it works

Each paragraph is a replaceable audio unit. Arrange accepted units in script order, then derive caption and visual timing from the final narration. A longer replacement can shift the timing of everything after it.

**Reading the evidence:** “Source” points to the creator's description or a retained frame. “Adaptation” identifies the practical procedure added for this guide. “Docs” links to current provider guidance. The proposed checks describe what to verify in your own trial.

### 1. Choose the route for your first project

**Do — adaptation:** choose one real script, its audience, and whether its audio may leave your machine. For a short hosted narration with little setup, use ElevenLabs Studio. For local control or a local-handling requirement, use the Qwen3-TTS/Chatterbox trial above. Move to SDK automation when repeated jobs justify coding and maintenance.

**Why:** a route that fits your work is more useful than a voice chosen only for its similarity score.

**Check:** write down your route, why it fits, and your trial budget. If local handling is required, plan that trial before uploading audio.

**Source:** [5:44 — choosing a workflow](https://www.youtube.com/watch?v=ABeo1kKueRs&t=344s). The route ranking is our recommendation for this sample.

### 2. Choose a voice or create your own

**Do:** for a low-cost first trial, select an available stock voice. If your own voice is the goal, use an account plan with Instant Voice Cloning. In ElevenLabs, open Voices, choose the plus control and Instant Voice Clone, then follow the recording, naming and consent steps.

Record about 1–2 minutes of clear, consistent speech in the delivery you want. The current docs recommend at least one minute; use that guidance as your starting point. The creator reports a successful 30-second example. [Cloning and recording guidance](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning).

**Why:** consistent speech gives the system a clearer example of your intended voice and delivery.

**Check:** the selected voice works for a short preview. For your own clone, save its voice ID for the project.

### 3. Approve a paragraph before the whole script

**Do — adaptation:** choose a paragraph with a product name, a number and the intended delivery. Generate it and listen for accuracy, pronunciation, pacing and pauses. If comparing candidates, use the same passage and hide labels when practical.

If delivery is exaggerated, simplify the direction and change one factor at a time. Keep a note of the adjustment that helped.

**Why:** a small, realistic passage reveals problems while revisions are still cheap.

**Check:** you or another listener can accept the words and delivery. Revise this passage before generating the rest.

**Source:** [1:13 — listening versus similarity](https://www.youtube.com/watch?v=ABeo1kKueRs&t=73s), [2:34 — delivery direction](https://www.youtube.com/watch?v=ABeo1kKueRs&t=154s).

### 4. Save settings you can reuse

**Do — adaptation:** save the selected voice, model, delivery settings and output format. In Studio, keep them with the project. In a custom client, record the voice ID and API settings with the script.

**Source frame — 6:42:** the creator's `voice.md` shows:

```yaml
voice_id: YOUR_OWN_VOICE_ID
model: eleven_v4
stability: natural
format: mp3_44100_192
```

Use your own voice ID. The remaining values show the creator's application settings. To automate them, translate the fields through the current API schema; look up how the chosen model expresses stability before mapping `natural`.

<details>
<summary>Map these settings to the API and export format</summary>

**Docs:** speech requests use `text`, `model_id` and optional `voice_settings`, with output format as a request option. The documented 192 kbps MP3 API option requires Creator tier or above. Studio export quality follows its own plan settings. [Speech API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert), [models](https://elevenlabs.io/docs/overview/models), [Studio export options](https://elevenlabs.io/docs/eleven-creative/products/studio).

</details>

**Why:** reusable settings keep the voice choice consistent across the script and make revisions easier to trace.

**Check:** you can find the project's voice/model and explain how saved application labels map to the generation tool you use.

### 5. Generate and keep accepted paragraphs

**Do:** write as you speak and split the script into natural paragraphs. In Studio, generate and review project paragraphs, using generation history or paragraph locking to retain accepted work. For an SDK or local-model route, save numbered files such as `001`, `002` and `003`, with text/settings recorded in a manifest.

**Why:** accepted paragraph units let you revise a passage while keeping the rest of the narration.

**Check:** every paragraph has an accepted take in the right order. Keep the original while comparing a replacement.

**Source:** [6:44 — paragraph generation](https://www.youtube.com/watch?v=ABeo1kKueRs&t=404s). Studio project handling is the researched alternative to the creator's files. His displayed `python anim.py speak <slug>` belongs to a custom program; use the SDK examples under Alternative starting points to build your own automation.

### 6. Export, listen and check timing

**Do:** export your Studio narration, or join accepted files in order in your editor/custom workflow. Listen across boundaries for missing words, repeats, volume changes and awkward pauses.

Create captions/timing from the final audio. Use transcription, or align a matching spoken transcript. Check names, numbers and transitions, then position captions and visual cues with the corrected times.

**Why:** captions and visuals follow the assembled timeline. A duration change can move later cues.

**Check:** the narration plays in order and the captions match what you hear. Recheck affected timing whenever a passage changes.

**Source:** [6:54 — assembly and timing](https://www.youtube.com/watch?v=ABeo1kKueRs&t=414s). The creator uses Whisper; Studio export and alignment are researched options. Validate timing in your output.

### 7. Try a one-paragraph revision

**Do — adaptation:** change one paragraph. Regenerate that passage, retain the other accepted takes, then export/rebuild the narration and refresh affected timing.

**Why:** a small revision lets you see whether the workflow delivers its main benefit.

**Check:** you can update one passage, hear a clean result and keep captions aligned. Record what needed extra work so your next project starts with better settings.

**Source use case:** [7:15 — reusable narration](https://www.youtube.com/watch?v=ABeo1kKueRs&t=435s).

### Try one change — optional

Your replacement paragraph is longer. Which accepted work can you keep, and what needs another check? Write your plan, then try it if you have a working project.

<details>
<summary>Hint</summary>
<p>Separate the accepted takes from the timeline built by assembling them.</p>
</details>

<details>
<summary>What a successful result includes</summary>
<ul><li>Keep unchanged accepted takes and replace the changed passage.</li><li>Export or rebuild the final narration in order.</li><li>Refresh or check affected caption and visual timing.</li><li>Listen at the joins and verify names, numbers and alignment.</li></ul>
<p>Record your explanation and hands-on result separately so you know what still needs practice.</p>
</details>

### Keep handy

| When you want to… | Next action |
|---|---|
| Finish a first passage with little setup | Use an ElevenLabs Studio audio project |
| Explore before paying for cloning | Try an available stock voice within Free-plan credits |
| Use your own voice | Check a plan with Instant Voice Cloning, then record clean speech |
| Repeat the approved voice choice | Reuse project settings or your saved voice/model/API settings |
| Revise one passage | Keep accepted takes; regenerate the changed passage |
| Keep captions in sync | Recheck timing against the revised final audio |
| Try local voice cloning | Use the Qwen3-TTS Base or Chatterbox-Turbo quickstart and test one paragraph |
| Automate repeated jobs | Start with the official SDK or local-model client, then add file tracking, joining and retries |

<details>
<summary>Get unstuck and check the evidence</summary>

| What you notice | Try next |
|---|---|
| Similar voice, wrong delivery | Simplify direction and compare the same short passage |
| Missing or mispronounced words | Correct that paragraph before accepting it |
| More retakes than expected | Record the useful settings and include retakes in the trial budget |
| Local setup exceeds your budget | Revisit hardware/model requirements before investing more time |
| Captions drift after an edit | Check affected timing against the new final audio |
| Unclear client handling or permitted use | Confirm the exact plan/model terms and handling requirements |

**Evidence status:** the settings frame was visually inspected, and linked documentation was reviewed on 27 October 2026. The workflow and cost rankings are recommendations based on fit and setup effort; local generation and resource use were measured in the linked spike; full captioned export, human listening quality and user completion remain to be checked. The creator's exact wrapper and settings mapping remain unavailable.

Use the dated price examples to plan a small trial, then confirm [current plan](https://elevenlabs.io/pricing) and [API pricing](https://elevenlabs.io/pricing/api) in your account. Compare the cost of your accepted output, including retakes and your time.

</details>
