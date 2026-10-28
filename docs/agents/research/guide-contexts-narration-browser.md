# Context for narration and browser-feature guides

Checked 28 October 2026. Bounded context for existing single-source lessons. Read [narration gap research](narration-gap-starting-points.md) and [local starting points](narration-local-starting-points.md) first. No new runtime/model comparison, pricing research, account action or knowledge-management implementation.

## Supported findings

### 1. TTS and voice personalization answer different questions

**Claim:** Text-to-speech names the text-to-new-speech task. Voice cloning can personalize the voice used for that task. In ElevenLabs' documented TTS route, cloning is one voice option; it is not the whole production pipeline or proof that a source performance is preserved.

**Exact support:** “turns text into lifelike audio”; “Instant voice cloning for quick voice replication”.

**Primary source:** [ElevenLabs Text to Speech](https://elevenlabs.io/docs/overview/capabilities/text-to-speech), overview and voice options.

**Version/date/confidence:** Live provider page retrieved28 October2026, unpinned; high confidence in documented task/options. “Lifelike” is provider language, not a measured quality finding. Cloning is not inherently restricted to TTS in every system.

### 2. Voice conversion starts from a performance

**Claim:** The provider describes voice changing as transforming source audio while retaining delivery/emotion. This distinguishes a new reading from transformation of an existing recording. It does not qualify singing, live latency or actual preservation quality.

**Exact support:** “transform audio between voices while preserving emotion and delivery.”

**Primary source:** [ElevenLabs Voice changer](https://elevenlabs.io/docs/overview/capabilities/voice-changer), overview.

**Version/date/confidence:** Live provider page retrieved28 October2026, unpinned. High confidence about the stated task; preservation is a documented goal, not an independently tested guarantee.

### 3. Chunked narration is a production pattern, not a speech modality

**Claim:** The request-stitching guide addresses continuity between generated chunks. Request stitching supplies generation context; the documented SDK example also combines audio buffers. It is not a durable paragraph-asset manager, the creator's custom program or a validated caption/export workflow. “Modular narration production” is our descriptive framing, not a verified standard method name.

**Exact support:** “abrupt changes in prosody from one chunk to another”; “Request stitching is not available for the `eleven_v3` model.”

**Primary source:** [Request-stitching guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching), also retrieved via its [.md form](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching.md).

**Version/date/confidence:** Live guide retrieved28 October2026, unpinned, with explicit model restrictions. High confidence in the documented problem/feature; no continuity/export execution. Existing research records additional history constraints to recheck before implementation.

### 4. Progressive enhancement is a baseline strategy

**Claim:** Progressive enhancement preserves essential content/functionality while adding experience where supported. It is a useful neighbor for a browser-capability guide, not a synonym for removing every library.

**Exact support:** “baseline of essential content and functionality”.

**Source:** [Mozilla MDN glossary: Progressive enhancement](https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement). First-party developer terminology reference; not a normative specification or evidence of universal adoption.

**Version/date/confidence:** Live reference retrieved28 October2026, not tied to one browser release; high confidence in the terminology distinction.

### 5. Feature detection and alternate paths implement that strategy

**Claim:** A first-party web.dev example conditionally selects enhanced or legacy import/export modules. This supports a target-specific baseline/enhancement strategy. Native API selection still needs fit, permission and behavior checks.

**Exact support:** “conditionally load different import and export modules depending on whether this method is available.”

**Primary source:** [Thomas Steiner, Progressively enhance your Progressive Web App](https://web.dev/articles/progressively-enhance-your-pwa), Google web.dev.

**Version/date/confidence:** Published/last updated29 June2020; retrieved28 October2026. High confidence as historical first-party design example, not current API instructions. It uses old `chooseFileSystemEntries` code; do not copy that as a current implementation. “Web-platform-first development” is our descriptive label, not a formal standardized workflow name.

### 6. Browser-local AI is conditional, not a universal baseline

**Claim:** Chrome documents per-API availability and device/model requirements. Check the intended environment and retain a useful alternate route rather than assuming every visitor can run local AI.

**Exact support:** “Required hardware”; “Inform users of model download”; “Review the APIs and their availability status”.

**Primary sources:** [Built-in AI overview](https://developer.chrome.com/docs/ai/built-in) and [getting started](https://developer.chrome.com/docs/ai/get-started).

**Version/date/confidence:** Live Chrome documentation retrieved28 October2026, unpinned; high confidence that eligibility/download checks matter. No fixed hardware threshold/release matrix endorsed; no inference/device test performed.

## Suggested narration context

**Where this fits · Speech production workflows**

Text-to-speech creates a new reading from a script; voice conversion transforms an existing performance. Voice cloning concerns the voice identity used. The video's paragraph pattern adds a production/revision layer around generation, so tool choice and a finished narration workflow are different decisions.

The broad label is our framing. TTS, voice cloning and voice conversion are established task/technology terms, but they are overlapping dimensions rather than mutually exclusive product categories.

| Direction | Helps with | Important distinction |
| --- | --- | --- |
| TTS | Script to new speech | Generated delivery needs review |
| Cloning/personalization | Desired voice identity | An option/technique, not a production pipeline |
| Voice conversion | Transform an existing recording | Preservation depends on the task/system |
| Paragraph production/alignment | Revisable units and final timing | Separate assembly and quality checks |

## Suggested browser context

**Where this fits · Web-platform-first development**

Investigate what the browser supplies before adding a dependency. This connects with progressive enhancement: preserve essential behavior, then add supported capabilities. Native controls, tab coordination, hardware and AI are different capabilities to qualify, not one promise that everything works everywhere.

The broad label is our framing. Progressive enhancement and feature detection are established concepts; dependency-free implementation is not a requirement.

| Direction | Answers | Important distinction |
| --- | --- | --- |
| Platform-first investigation | Can the platform do this job? | Start with behavior, then packages |
| Progressive enhancement | What remains useful without it? | A baseline strategy, not a dependency ban |
| Feature detection | Is the capability exposed? | Presence does not prove permission/quality |
| Selective dependencies | What real gap remains? | A justified library can be appropriate |

## Boundaries

- A guessed voice-cloning capability URL returned404; the successfully retrieved TTS page supplies the relevant evidence instead.
- No new trend, prevalence, universal native support, zero-cost/private guarantee or formal name for either creator's complete workflow was established.
- These context additions orient single-source lessons. They do not start follow-up ticket44 or a multi-source course.

## Audit clarification incorporated

Finding3 now acknowledges the SDK's in-memory audio-buffer combination. The remaining boundary concerns durable paragraph management and validated caption/export production. The applied intro/comparison did not require a technical change.
