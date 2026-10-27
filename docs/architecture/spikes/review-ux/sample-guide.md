## Sample guide: build a repeatable narration workflow

### Your result

Produce narration you can revise one paragraph at a time, with captions that still match the final audio. **Done means:** one paragraph has been replaced, the other accepted takes are retained, the rebuilt narration plays correctly, and caption timing has been checked.

### Before you start

Use this guide for prerecorded narration, such as a product demo or training lesson. Have a short script, a voice you have permission to use, access to a suitable voice service or local workflow, and an audio/video editor. Establish whether source audio may leave your machine before selecting the route.

**Missing dependency:** the creator's custom automation program is not supplied. You can try a manual paragraph-by-paragraph workflow; automated generation and joining require a separate implementation. This sample has not enrolled a voice, generated audio or verified an export. Live dialogue and performance conversion need separate workflows.

### How it works

Each paragraph is a replaceable audio unit. You assemble accepted units in script order, then derive caption and visual timing from that final narration. Replacing one unit preserves the others, but a duration change can shift the timing of everything after it.

**Evidence labels:** Source identifies what the creator describes or shows. Adaptation identifies our added procedure. Docs checked identifies provider guidance checked27October2026. A citation, a successful API request and a listener-approved result are different kinds of evidence.

### 1. Choose the job before the model

**Do — adaptation:** choose one real script, its audience, whether audio may leave your machine, and your monthly production volume. Use your own voice or one you have permission to use.

| Need | Starting route | What to establish |
|---|---|---|
| Prerecorded narration with little setup | Try hosted TTS | Listening fit and actual cost for your script |
| Audio must stay on your machine | Evaluate a local workflow | Local handling in practice, hardware and applicable terms |
| Change the sound of an acted/sung performance | Evaluate voice conversion | Conversion preserves the performance you need |
| Live spoken replies | Test a low-latency system separately | End-to-end delay and interruption handling |

**Why:** The required result and handling constraints determine which voice workflow is suitable; a voice-similarity score cannot choose that for you.

**Check:** write one sentence explaining your route. The creator's hosted preference is a candidate to test, not a universal winner. **Source:** [5:44 decision questions](https://www.youtube.com/watch?v=ABeo1kKueRs&t=344s).

### 2. Create one voice from clean speech

**Do:** record the delivery you intend to use. For this hosted example, open Voices, the plus control and Instant Voice Clone; upload/record your sample, name the voice, complete the rights/consent confirmation and save its voice ID.

**Docs checked:** the provider recommends roughly 1–2 minutes of clear, consistent audio and at least one minute. Use that guidance here. The video's successful 30-second example is the creator's result, not this guide's recording target. [Cloning instructions and recording guidance](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning).

**Why:** Consistent recording and delivery give the cloning system a clearer example of the voice you intend to use.

**Check:** the voice is available in your account and you know its ID. No voice was enrolled while preparing this sample.

### 3. Approve one paragraph before a whole script

**Do — adaptation:** choose a paragraph containing a product name, a number and the intended delivery. Compare eligible candidates on the same text. Hide provider labels if someone can prepare the samples for you.

Listen for word accuracy, pronunciation, pacing, pauses and audience fit. Record the correction you would make. If delivery is exaggerated, simplify the direction and change one factor at a time.

**Why:** A short real passage exposes pronunciation and delivery problems before you spend effort on a full script.

**Check:** a listener accepts the passage, including names and numbers. If not, revise before batching. **Source:** [1:13 listening versus similarity](https://www.youtube.com/watch?v=ABeo1kKueRs&t=73s), [2:34 delivery direction](https://www.youtube.com/watch?v=ABeo1kKueRs&t=154s). This proposed procedure is not a rerun of his experiment.

### 4. Save the approved settings

**Source frame — 6:42:** his `voice.md` shows:

```yaml
voice_id: YOUR_OWN_VOICE_ID
model: eleven_v4
stability: natural
format: mp3_44100_192
```

The ID above is a replacement placeholder. Other values are visually observed, but this is **his application's configuration**, not an API payload. Do not copy his personal voice ID.

**Do — adaptation:** save your voice ID, selected model, approved delivery settings and output format together. Start with provider defaults where you have not approved a value. If automating, translate the configuration through the current API schema; do not assume `natural` is a numeric API setting.

**Docs checked:** the API accepts `text`, `model_id` and optional `voice_settings`; audio format is a request option. Query supported models rather than guessing IDs. Its documented 192 kbps MP3 option requires Creator tier or above. [Speech endpoint](https://elevenlabs.io/docs/api-reference/text-to-speech/convert), [model documentation](https://elevenlabs.io/docs/overview/models).

**Why:** Shared settings let you reproduce a voice choice across paragraphs; application labels still need translation into provider request fields.

**Check:** you can distinguish saved application settings from the request sent to the provider.

### 5. Generate numbered paragraphs

**Do:** write as you speak, split the script into natural paragraphs and generate one audio file per paragraph. For your first pass, generate/download them individually in the provider interface.

**Adaptation:** name outputs `001`, `002`, `003`; retain a manifest mapping each file to its text and approved settings. Listen before accepting each file. Keep the original take when comparing a replacement.

**Why:** Separate accepted files let you replace a changed passage while keeping the other takes.

**Check:** every paragraph has an accepted file, in script order. **Source:** [6:44 paragraph-to-file workflow](https://www.youtube.com/watch?v=ABeo1kKueRs&t=404s).

**Automation gap:** the frame shows `python anim.py speak <slug>`, a custom program not supplied by this video or guide. It is not a generic ElevenLabs command. A working client, retries and join implementation must be supplied separately.

### 6. Join, listen, then derive timing

**Do:** join accepted files in order in your audio/video editor. Listen across joins for missing or repeated words, level changes and awkward pauses.

Run transcription/timing on the **joined final audio**, then compare captions with what you hear. Inspect names, numbers and transitions. Use corrected timing for captions and visual cues. The creator uses Whisper; his claim of exact word timing is not independently validated here.

**Why:** Captions and visual cues depend on the final assembled timeline, so a changed duration can move downstream cues.

**Check:** narration plays in order and captions match it. If an edit changes duration, refresh/recheck downstream timing. **Source:** [6:54 joining and timing](https://www.youtube.com/watch?v=ABeo1kKueRs&t=414s). Join checks and revision rules are adaptations.

### 7. Test a one-paragraph revision

**Do — adaptation:** change one paragraph, regenerate only its file, rebuild the narration and refresh affected timing. Keep the other approved takes.

**Why:** One controlled revision checks whether the workflow actually delivers its promised benefit.

**Check:** you can update one passage without rerecording the whole script and the final captions still align. This is the working-result test, not an observed outcome of this sample. **Source use case:** [7:15 reusable narration](https://www.youtube.com/watch?v=ABeo1kKueRs&t=435s).

### Try one change — optional

Your replacement paragraph is longer than the original. Which work can you keep, and what must you check again? Explain your plan before looking at the hint. If you have a working environment, try the revision and record the actual result separately from your explanation.

<details>
<summary>Hint</summary>
<p>Separate the accepted paragraph files from the timeline made by joining them.</p>
</details>

<details>
<summary>What a successful result includes</summary>
<ul><li>Keep unchanged accepted takes and replace the changed paragraph.</li><li>Rebuild the final narration in the intended order.</li><li>Refresh or inspect affected caption and visual timing against the new final audio.</li><li>Listen at the joins and check names, numbers and caption alignment.</li></ul>
<p>A correct explanation is not proof of a successful export. Record execution and listening checks only if you performed them.</p>
</details>

### Keep handy

| When you need to… | Look up or do this |
|---|---|
| Reproduce a voice choice | Keep your voice ID, model, approved settings and audio format together |
| Interpret the source settings | The frame shows app configuration; it is not an API request body |
| Track a take | Map numbered paragraph files to their text and settings |
| Revise a passage | Replace that take; keep the other accepted takes |
| Restore synchronization | Rebuild/recheck final audio and affected caption/visual timing |
| Automate the manual workflow | Supply a client and joining implementation; the custom anim.py is absent |

<details>
<summary>If you get stuck: recovery steps and remaining gaps</summary>

### If you get stuck

| Symptom | Next action |
|---|---|
| Similar voice, wrong delivery | Simplify direction; compare the same short passage again |
| Missing/mispronounced words | Correct before accepting that paragraph |
| Local setup exceeds your budget | Revisit the route; his hardware does not establish every model's requirements |
| Captions drift after an edit | Recheck timing against the revised final audio |
| Client handling or permitted use unclear | Establish the exact provider/model terms and handling requirements before choosing |

### What remains unverified

No enrollment, paid generation, joining, listening assessment or timing-quality test was performed here. The wrapper source and mapping of `natural` are absent. Individual local-model licenses and installation requirements were not checked, so no specific local model is endorsed for commercial work.

Treat hardware costs, rankings and included-hour estimates in the video as dated claims. Current [pricing](https://elevenlabs.io/pricing) distinguishes plans, credits and promotions; calculate cost for your chosen model and usage instead of assuming fixed finished hours. This is a starting workflow, not a demonstrated best purchase for this user.

</details>
