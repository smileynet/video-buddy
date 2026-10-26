# Tutorial speech reference provenance audit

Audited 2026-10-25 against fresh retrievals of the cited primary publisher pages, transcript assets, and institutional documentation. No audio listening or video-frame inspection was performed.

**Overall trust: 9/10 — pass with one currency correction and one wording caution.** The file correctly distinguishes publisher text, historical workflow evidence, file-specific human review, and human word-boundary truth.

| Claim group | Verdict | Independent check |
| --- | --- | --- |
| MIT human editing workflow | supported, historical scope | [MIT News](https://news.mit.edu/2015/3play-media-more-efficient-video-captioning-0408), dated April 8, 2015, contains both quoted editing/final-review snippets and describes ASR drafts plus word-associated time data. It supplies no review record for these candidate files. |
| OCW Studio vendor relationship | supported; date weak | [Current system context](https://engineering.ol.mit.edu/system_architecture/ocw-studio/system-context/) retains the quoted 3Play role, but the freshly retrieved page says generated **2026-10-14 15:05 UTC**, not 2026-06-24. This documents the integration rather than certifying historical file provenance. |
| MIT 2017 candidate identity and assets | supported | The [resource page](https://ocw.mit.edu/courses/res-3-002-collaborative-design-and-creative-expression-with-arduino-microcontrollers-january-iap-2017/resources/introduction-to-git-github/) identifies Andrew Ringler, January IAP 2017, and the stated video/caption/PDF assets. The PDF responds successfully. Fresh raw VTT retrieval confirms all three listed cue spans and their described content. |
| CS50 candidate identity and historical asset distinction | supported | The [2026 course page](https://cs50.harvard.edu/x/shorts/command_line/) links the stated video and 2017-path subtitle/transcript assets. Both text assets were retrieved; SRT cues 46–47, 158, 176, and 188 match the stated times/content, including the self-correction. A 2017 asset path is not itself proof of the recording date; the findings appropriately avoid that claim. |
| MIT 2013 terminal candidate | supported for publisher text | The [resource page](https://ocw.mit.edu/courses/6-370-the-battlecode-programming-competition-january-iap-2013/resources/lecture-4-git-repository/) establishes January IAP 2013 and the stated video/caption linkage. Fresh raw VTT retrieval confirms 21:07.860–21:37.040, the three-times cue, and 07:22.770–07:28.280. Exact executable path spelling remains unverified as stated. |
| No specific-file human-review or human word-timing certification | supported as a bounded evidence limit | None of the inspected cited sources supplies either certification. Caption spans and word-associated playback data do not establish manually checked acoustic word boundaries. This is a finding about these sources, not proof that such records cannot exist elsewhere. |

Findings for the producer:

1. **Currency correction:** replace the OCW Studio generated date with the fresh date above, or describe it as the generation date observed on retrieval. The vendor-role claim remains intact.
2. **Wording caution:** “Use the MIT candidate when workflow-level evidence of human transcript editing is required” is defensible only as institutional historical context. Prefer “Use MIT as a candidate backed by institutional workflow context; these specific files still have no verified human-review trail.” In particular, the 2013 lecture predates the 2015 workflow account, and the 2017 lecture postdates it; neither date bridges the file-level gap.

No unsupported factual cue claims were found. Comparative usefulness and the humorous interpretation are reasonable analyst judgments, not independently audio-verified facts. Strict human-verified spoken-command accuracy and word-boundary timing remain open acceptance criteria.
