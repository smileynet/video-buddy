# Audit: narration gap starting points

2026-10-27. Independent re-fetch of the producer's primary sources. Scope is documentary support, not execution, account availability or audio quality.

**Trust: 9/10 — usable as researched starting points with the recorded restrictions.** All seven findings have verifiable primary support. Sources are live documentation/current upstream branches rather than pinned installed versions; no production workflow is qualified.

| Finding | Verdict | Independent check |
|---|---|---|
| 1. Studio route | Supported | [Studio guide](https://elevenlabs.io/docs/eleven-creative/products/studio), Generate/Regenerate, Generation history, Lock paragraph and Export sections support selected-text generation, per-paragraph history/download, locking and project export. Changed text loses generated status; limited unchanged regenerations do not imply free revisions. Model default and plan-dependent export quality caveats are correct. |
| 2. Official SDK | Supported | [Upstream README](https://github.com/elevenlabs/elevenlabs-python), TTS example, demonstrates client construction and conversion with text/voice/model/format. Its example currently uses eleven_v3. It is a generation primitive, not the missing resumable wrapper. |
| 3. Context inputs | Supported | [Create speech API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert) documents previous/next text and request IDs, three-ID limits, ID precedence, same-model recommendation and logging-disabled stitching restriction. These inputs condition generation; they do not export/join files. |
| 4. Stitching cookbook | Supported | [Official recipe](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching) currently uses eleven_v4, excludes eleven_v3, reads the response and retains IDs. FAQ confirms completion and two-hour constraints. Its playback example is not an acceptance/revision/export system. Neighbor-boundary listening remains clearly identified engineering advice. |
| 5. FFmpeg concat | Supported | [Raw upstream concat documentation](https://raw.githubusercontent.com/FFmpeg/FFmpeg/master/doc/demuxers.texi), concat section, confirms ordered files, timestamp adjustment, compatible streams/codecs/time bases and duration-error artifacts. Normalizing formats and checking the result are recommendations, not executed findings. |
| 6. Forced alignment | Supported, file cap unresolved | [API reference](https://elevenlabs.io/docs/api-reference/forced-alignment/create) documents audio plus transcript input and word/character timing. It says less than1GB; the [capability page](https://elevenlabs.io/docs/overview/capabilities/forced-alignment) says3GB. The producer correctly avoids endorsing a cap. Matching/correcting the actual spoken text is an appropriate stated precondition, not an independently verified accuracy guarantee. |
| 7. Separate workflows | Supported | [Agents overview](https://elevenlabs.io/docs/eleven-agents/overview) links turn-taking/interruption controls; [Voice changer](https://elevenlabs.io/docs/overview/capabilities/voice-changer) describes source-audio transformation. Pointers are kept distinct from prerecorded TTS and local-only processing. |

## Corrections and use conditions

No unsupported or secondary-only load-bearing claim found; no producer correction required. Keep the following conditions when adapting the report into the guide:

- Present Studio and SDK routes as alternatives to the absent creator program, not recovered source code or a tested complete solution.
- Preserve stitching model/privacy/time restrictions; distinguish conditioning from physical joining.
- Do not transfer API format entitlements to Studio, promise unlimited free regeneration, or select a single alignment file-size limit from contradictory docs.
- Keep installation/version pin, paid model/voice access, commercial eligibility, generation, export, alignment accuracy and listener/task results unverified until tested separately.

No provider request, credential access, installation or media operation was performed by the auditor.
