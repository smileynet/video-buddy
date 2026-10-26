# Tutorial speech reference provenance

Checked 2026-10-25. Scope: existing independent publisher references for real commands, numbers, and timing. No audio listening was available, and no new ASR was run. These findings identify useful prior art; they do not certify word-level ground truth.

## Verified findings

### High confidence: MIT documents a human editing workflow, with an important per-file gap

[MIT News, Captioning at scale (2015-04-08)](https://news.mit.edu/2015/3play-media-more-efficient-video-captioning-0408) describes 3Play's ASR-first process and human correction. Supporting snippets: “contracted editors can choose which transcripts to edit”; “managers give each job a final look”. It also reports word-associated time data, but does not establish that humans annotate acoustic word boundaries. The 2015 description must not silently be treated as a current service guarantee.

[MIT OCW Studio system context (generated 2026-10-14)](https://engineering.ol.mit.edu/system_architecture/ocw-studio/system-context/) still identifies 3Play: “Captioning/transcription vendor; OCW Studio orders transcripts and receives completion callbacks.” This supports a current institutional vendor relationship, not proof of which vendor or review procedure produced a particular historical transcript.

### High confidence: MIT provides a real tutorial with public video and timed publisher captions

[Introduction to Git/GitHub, January IAP 2017](https://ocw.mit.edu/courses/res-3-002-collaborative-design-and-creative-expression-with-arduino-microcontrollers-january-iap-2017/resources/introduction-to-git-github/) identifies the instructor: “Andrew Ringler provides an overview”. It supplies video, English transcript UI and transcript download.

- [Public video](https://www.youtube.com/watch?v=_3lU2LDQdUU)
- [Publisher VTT](https://ocw.mit.edu/courses/res-3-002-collaborative-design-and-creative-expression-with-arduino-microcontrollers-january-iap-2017/37c086f77ed756bfbdfa4560bd55b0aa_2039260.vtt)
- [Publisher PDF transcript](https://ocw.mit.edu/courses/res-3-002-collaborative-design-and-creative-expression-with-arduino-microcontrollers-january-iap-2017/d70b8b905f119fbad7b9abb377446076_2039260.pdf)

Direct VTT inspection yielded candidate cue spans:

| Cue span | Candidate content (paraphrase unless quoted) | Use |
| --- | --- | --- |
| 10:23.770–10:25.790 | changing three or four files | Numeric recognition |
| 14:26.300–14:31.561 (multiple cues) | Dropbox on two computers and matching folders | Numeric/context recognition |
| 16:40.700–16:47.696 | “Plus button, we say Clone.” | Actual GUI instruction |

This candidate is stronger on transcript provenance context than CS50 below, but it is a GUI Git tutorial rather than a dense terminal-command passage. The file-level human-review record remains unverified.

### High confidence: CS50 is a better command/numeral specimen, but only publisher provenance is established

[CS50 Command Line, current 2026 course page](https://cs50.harvard.edu/x/shorts/command_line/) explicitly links “Subtitles” and “Transcript”, plus MP4 and YouTube. Those links point to 2017 assets; the 2026 page does not imply a newly recorded 2026 tutorial.

- [Public video](https://www.youtube.com/watch?v=BnJ013X02b8)
- [Publisher text transcript](https://cdn.cs50.net/2017/fall/shorts/command_line/lang/en/command_line.txt)
- [Publisher SRT](https://cdn.cs50.net/2017/fall/shorts/command_line/lang/en/command_line.srt)

Direct SRT inspection yielded useful candidate spans:

| SRT cue | Span | Candidate content (paraphrase unless quoted) |
| --- | --- | --- |
| 46–47 | 02:12.360–02:20.520 | Two folders named pset0/pset1, then three files; following cue completes file list |
| 158 | 07:42.580–07:45.610 | Introduction of mkdir |
| 176 | 08:28.615–08:35.049 | “by typing mkdir, space-- I typed in n, but-- space pset2.” |
| 188 | 09:06.960–09:11.800 | cp takes two arguments, with source explanation; following cue completes destination explanation |

The self-correction in cue 176 is especially useful for a real tutorial transcription check: preserve what was said rather than replacing it with an idealized shell command. Text may verbalize punctuation, so any normalization to executable syntax needs an explicit policy.

## Could not verify / limits

- No inspected source explicitly certifies human review of either specific 2017 caption file. MIT has stronger documented workflow context, but that is not a per-file audit trail. CS50's official hosting alone cannot support a human-authored or human-reviewed label.
- Caption cue starts/ends delimit groups of words, not manually established acoustic word boundaries. Even MIT's interactive word-associated timing does not itself prove human word-boundary annotation. Do not use these files as human word-timing truth.
- No audio listening occurred. Candidate passages and numeric values are independently published text references, not freshly audio-verified speech claims. A strict independently checked spoken-command acceptance criterion still needs a human to listen and record corrections and timing.
- Agreement between a second ASR and these files, or a YouTube manual-caption flag, cannot close that provenance gap.
- Searches covered official CS50 pages and caption files, Harvard accessibility material, MIT OCW resources, MIT Open Learning engineering documentation, and MIT News descriptions of 3Play. No large media or model downloads were performed.

## Suggested use

Use the CS50 spans for a small real-tutorial lexical check against publisher text, labeled accordingly. Use the MIT candidate only as a publisher reference with workflow-level context; retain the absence of specific-file human-review records across the 2013/2015/2017 historical boundary. Neither candidate presently satisfies strict human-verified word-boundary timing. Keep that acceptance criterion open rather than reporting proxy agreement as independent truth.

## Additional stronger MIT terminal candidate

**High confidence for publisher files; workflow-level human-review inference only.** [Lecture 4: Git Repository, Battlecode January IAP 2013](https://ocw.mit.edu/courses/6-370-the-battlecode-programming-competition-january-iap-2013/resources/lecture-4-git-repository/) embeds public video ID `g2NoQCEgsCM` and links English captions. [Public video](https://www.youtube.com/watch?v=g2NoQCEgsCM); [official VTT](https://ocw.mit.edu/courses/6-370-the-battlecode-programming-competition-january-iap-2013/829d1c78b97055d9bc1377c2ad892521_g2NoQCEgsCM.vtt).

Preferred bounded command/numeric specimen: **21:07.860–21:37.040**, approximately 29 seconds, discussing running git status before/after commands. Supporting cue at 21:21.895–21:24.320: “I should have done Git status three times.” The subsequent cues enumerate the three occasions. This is real terminal instruction containing a number, although the three-times formulation is humorous advice rather than a numeric option or parameter. Another candidate is 07:22.770–07:28.280, introducing git add and a player/robot path; exact path spelling should be checked visually before syntax-level scoring. These are observed VTT cues; audio truth and word boundaries remain unverified.
