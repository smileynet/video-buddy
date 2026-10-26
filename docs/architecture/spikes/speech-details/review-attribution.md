# Real speech reference review — ticket 15

Three source excerpts / 55 seconds are prepared for independent listening, with no new model predictions. Open `reference-review.html` in this directory. The page uses the exact audio files under `.scratch/speech-details/provenance/review/`; save the review JSON before closing. Do not copy model predictions into the reference. The optional publisher draft is not marked verified.

## Sources and attribution

- MIT OpenCourseWare, **Lecture 4: Git Repository**, The Battlecode Programming Competition, January IAP 2013, Maxwell Mann and Aaron Epstein: https://ocw.mit.edu/courses/6-370-the-battlecode-programming-competition-january-iap-2013/resources/lecture-4-git-repository/ . Excerpt1267–1298s, discussing git status and three occasions. Official VTT URL/hash retained in `review-manifest.json`.
- Harvard CS50, Doug Lloyd, **Command Line**, 2017 asset linked by current course page: https://cs50.harvard.edu/x/shorts/command_line/ . Excerpts506–518s (mkdir / pset2 / spoken correction) and546–558s (cp / two arguments). Official SRT URL/hash retained in the manifest.

Publisher excerpts retain **CC BY-NC-SA4.0**, https://creativecommons.org/licenses/by-nc-sa/4.0/ ; Harvard course license: https://cs50.harvard.edu/x/license/ ; MIT resource footer links the same license. Changes: bounded audio cuts and mono16k PCM conversion; publisher cue text is unchanged. These notices cover the source-derived audio/text, not a relicensing of the application. These are research/reference artifacts, not a validated production feature.

## Recovery

Extract `review-inputs-*.zip` into `.scratch/speech-details/provenance/review/` from repo root. Verify each restored WAV SHA256 against `review-manifest.json`. Then open the review page. The embedded packet checksum must match that manifest. Source media and full caption metadata remain ignored; compact clips and selected draft cues are retained on this spike branch. No independent backup claim covers ignored originals.

The exact clips can be recreated with yt-dlp bestaudio for the two source IDs recorded in the manifest, then FFmpeg `-i <source.webm> -ss <start> -t <duration> -vn -ar16000 -ac1 <clip.wav>` using the manifest spans. Different future source encodes may change hashes; the frozen ZIP is the exact replay source. Start offsets are nominal container source times; human timings are relative to the frozen clip.

## Reference lock

Listen independently, record literal spoken text including self-corrections and uncertainty, and mark actual target starts/ends with an uncertainty margin. A not-spoken/uncertain target is legitimate; never force an expected command into the reference. Save an anonymous review JSON. A ready export attests a review; software cannot prove that listening occurred. Lock the corrected reference and scoring policy in Git **before** any new inference.

Numeric scope is counts and filename digits, not unseen port/version/configuration values. Publisher cue boundaries are word groups, not word-boundary truth. Specific-file human review remains unverified despite MIT's documented institutional workflow. MIT's official and YouTube cue objects are identical; CS50's full decoded word sequences are identical despite formatting differences. Do not use either pair as two independent references.

User clarification2026-10-25: designated empty tracks are music-only. Exclude those from speech-reference scoring and retain separately as music-only controls. The earlier authored digital silence and tone fixtures remain distinct synthetic negative controls. No missing-caption heuristic is implemented.
