# Starting points for the missing narration automation

Checked 2026-10-27 against first-party documentation and upstream source. Scope: fill the sample guide's missing `anim.py` dependency with practical alternatives, not reconstruct the creator's private implementation. No account, credential, package, generation, join, export or listening test was performed. Findings are documented starting points; the assembled workflow remains untested.

## Verified findings

### 1. Studio is a low-code route to paragraph narration and export

**Confidence: high for documented features; user workflow untested.** Studio documents audio projects, selected-text generation, per-paragraph generation history, paragraph locking, timeline editing and audio export. An audio project can start with the reader's script rather than the creator's custom program. The quickest proposed trial is: create/upload a short script, select the intended voice/model, generate a paragraph, listen, change that paragraph, regenerate, then export. Inspect credits before generating; unchanged text/voice regeneration allowances are conditional, not unlimited free revisions. Studio's timeline/project model is an alternative to the custom file-per-paragraph wrapper, not proof of identical behavior.

Supporting snippets: “Select Generate to generate audio for the selected text.” and “Select Export to export the project as audio or video.” [Official Studio guide](https://elevenlabs.io/docs/eleven-creative/products/studio), Generate/Regenerate, Generation history, Lock paragraph, Exporting and sharing sections.

**Version/date:** the page currently describes ElevenCreative Studio4.0 and multiple project types, including the previous video editor. Most new projects default to Multilingualv2; select the intended model explicitly. UI/plan-dependent quality may change. Do not transfer the sample API output-format entitlement to Studio; their documented quality rules differ.

### 2. The official Python SDK supplies the generation primitive

**Confidence: high for SDK example; installed-version compatibility untested.** The upstream README demonstrates importing `ElevenLabs`, creating a client, and calling `text_to_speech.convert` with text, voice ID, model ID and output format. This is useful prior art for a small replacement client. It does not provide the creator's `anim.py`, a complete resumable paragraph runner, safe revision handling or an independently verified final export.

Supporting snippet: “The official Python SDK for the ElevenLabs API.” [Upstream elevenlabs-python README](https://github.com/elevenlabs/elevenlabs-python), Text to Speech example.

**Version/date:** current `main` README, not a pinned installed release. Its basic TTS example uses `eleven_v3`, while the stitching cookbook below uses `eleven_v4`; do not combine these examples without checking model-specific support. Choose an account-available model and record the SDK version when implementing. SDK licensing is separate from provider generation terms and model/voice permissions.

### 3. API context can help continuity between paragraph requests

**Confidence: high for documented inputs; improvement unmeasured.** The speech endpoint accepts previous/next text and previous/next request IDs for continuity conditioning. Previous request IDs take precedence over previous text, with a documented maximum of three previous IDs. The same-model recommendation matters when retaining accepted takes. Zero-retention requests disable history-dependent request stitching; privacy configuration and continuity strategy must be chosen together.

Supporting snippet: “A maximum of 3 request_ids can be send.” [Official Create speech endpoint](https://elevenlabs.io/docs/api-reference/text-to-speech/convert), `previous_text`, `next_text`, `previous_request_ids`, `enable_logging` fields.

**Version/date:** live API reference checked2026-10-27; no account request made. Context inputs do not physically join audio files and are not a guarantee of seamless delivery.

### 4. The stitching cookbook is especially close prior art, with restrictions

**Confidence: high for example and documented restrictions; runtime untested.** The official recipe loops over paragraphs, finishes reading each response and captures its request ID before conditioning a following request. It currently shows `eleven_v4`. The FAQ requires fully processed previous audio before reuse, and says IDs should be no older than two hours. It excludes `eleven_v3`. The cookbook's in-memory combined playback is an example, not a durable export/revision pipeline.

Supporting snippets: “Request stitching is not available for the `eleven_v3` model.” and “The request IDs should be no older than two hours.” [Official request-stitching cookbook](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching).

**Version/date:** current cookbook, checked2026-10-27, unpinned. Old accepted takes may remain useful audio even when their conditioning IDs have expired. Changing a paragraph/context may affect neighboring prosody: listen at both adjoining boundaries rather than assuming a perfect local replacement. This last sentence is an engineering recommendation, not an observed result.

### 5. FFmpeg supplies joining, but compatibility is a real precondition

**Confidence: high for upstream contract; files not joined here.** FFmpeg's concat demuxer reads an ordered file list and adjusts successive timestamps. Its contract requires compatible streams; incorrect durations can cause artifacts. A small automation should standardize generated output format and validate codec/sample-rate/channel/time-base compatibility, or normalize/re-encode before joining. File extension equality is insufficient. The resulting file must still be listened to and checked; concatenation success cannot establish narration quality.

Supporting snippet: “All files must have the same streams (same codecs, same time base, etc.).” [FFmpeg upstream demuxer documentation, concat section](https://github.com/FFmpeg/FFmpeg/blob/master/doc/demuxers.texi).

**Version/date:** upstream `master` text fetched2026-10-27 via its raw source after the HTML manual timed out. No installed FFmpeg build or produced-file compatibility was qualified. This is a component choice, not a tested joining command for the reader's files.

### 6. With a matching script, forced alignment is another timing starting point

**Confidence: high for endpoint purpose; timing accuracy untested.** Forced alignment takes audio plus a supplied transcript and returns character/word times. If the final narration actually matches the approved script, this offers a documented alternative to first recovering the words with ASR. Feed the final joined audio and its corresponding spoken transcript; review omissions, substitutions, names and boundaries. Alignment locates supplied text, so it does not independently prove that the synthesis spoke every intended word. If text differs, correct/establish the spoken transcript before relying on alignment.

Supporting snippet: “Force align an audio file to text.” [Official forced-alignment endpoint](https://elevenlabs.io/docs/api-reference/forced-alignment/create).

**Version/date:** live endpoint checked2026-10-27. No timing test. Avoid asserting a file cap here: the API reference says less than1GB, while the [capability page](https://elevenlabs.io/docs/overview/capabilities/forced-alignment) currently says3GB. That disagreement needs resolution before processing a large file. These are hosted services, not a local-only alternative.

### 7. Live conversations and performance conversion have separate official entry points

**Confidence: high for documented product separation; suitability untested.** For live dialogue, [ElevenAgents overview](https://elevenlabs.io/docs/eleven-agents/overview) links conversation-flow controls including turn-taking, interruptions and timeouts. Supporting snippet: “Configure turn-taking, interruptions, and timeout settings”. For an existing performance, [Voice changer documentation](https://elevenlabs.io/docs/overview/capabilities/voice-changer) describes transforming source audio; supporting snippet: “transform audio between voices while preserving emotion and delivery.” These are pointers for a new scoped trial, not instructions that make the prerecorded paragraph loop suitable for either job. The voice changer is hosted and does not satisfy a local-only requirement by itself.

**Version/date:** current product documentation checked2026-10-27; no live system or performance-conversion test. Provider outcome claims have not been independently confirmed.

## Proposed starting routes, not tested implementations

**Fastest UI route:** use a Studio audio project for a short script; choose the voice/model explicitly, generate and inspect one paragraph, revise it, listen at joins, export, and inspect timing. This avoids implementing the absent wrapper for the first user trial. It does not establish file-level caching or reproduce the creator's exact automation.

**Smallest custom automation:** use the official SDK for one approved paragraph, save the returned audio, and retain a local manifest of paragraph ID/text, voice/model/settings, output path and request ID/time. Then add ordered generation and an accept/revise state; add context conditioning only for a model/privacy setup supporting it. Join compatible accepted files using FFmpeg, derive/check timing from final audio and matching transcript, and run the one-paragraph revision test. Preserve good takes; do not treat stale request IDs or hashes as proof of audio quality. This sequence is our synthesis of prior art, not a supplied production program.

## Still missing or not verified

- The creator's exact custom program, configuration mapping and retry/accept/revision behavior were not found or reconstructed.
- SDK installation/version pin, paid account/model/voice availability, commercial eligibility and actual credit spend are not qualified here.
- Continuity, export correctness, alignment accuracy and real user completion require the described small trial; documentary support alone does not resolve them.
- Forced-alignment file-size documentation conflicts; no single limit is endorsed.

## Reusable gap-help pattern

For a missing prerequisite, show: **what is absent → simplest documented alternative → relevant prior-art implementation → conditions/gotchas → smallest completion check → status and source date**. Keep “shown in video”, “researched starting point”, “adapted procedure” and “tested here” distinct. A gap should lead to a practical next action without being silently upgraded into a verified solution.
