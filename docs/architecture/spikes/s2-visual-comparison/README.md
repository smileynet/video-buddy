# S2 throwaway targeted-frame comparison

Not approved for production. Source: Qr3VsZYQy4s. The exact retained media SHA-256, byte size, requested timestamps and measured capture durations are in `observations.json`. The baseline metadata came from the preceding real CLI run. All image inspection was performed by the same agent; there is no independent annotation/reader study or provider comparison.

## Reproduction

Use the experimental branch's CLI after installing dependencies. The primary checkout's existing `fetch --download-video` was used to retain the source; committed main lacks that flag. Alternatively obtain the source using the repo's download CLI once that prerequisite is available. Do not assume this spike made acquisition portable.

Initialize a disposable workspace with `uv run video-buddy init --no-models`. Supply the fetched source JSON and retained media through `frames --video-json <source-json> --media-file <video.mp4> --at <seconds...> --ocr off`. The exact requested seconds for both runs are recorded in observations.json. `--at` and `--media-file` are throwaway spike flags. Both reuse the existing download/extraction/scoring implementation; explicit timestamps bypass rank selection and perceptual deduplication. The dense option is a time-indexed still sequence, not native video understanding.

`exploratory-targeted-meta.json` records the first 8 captures; `dense-meta.json` records 36. After inspecting the dense set, a post-hoc 15-frame follow-up covering the same windows was run; `targeted-meta.json` and its contact sheet record that final set. Contact sheets display all final targeted/dense frames with requested timestamps. Five full-resolution representative frames are preserved for inspecting details. Raw images not individually committed can be recreated with the command. Metadata times are requested seek times, not independently verified presentation timestamps.

## Inspection notes

- At 73 and 76 seconds, multiple component waves and a sawtooth-like result are visible. By 79/82 seconds, the lower result changes toward a square waveform. No harmonic coefficient table or executable formula is visible in these waveform frames. Do not infer exact coefficients from raster amplitudes.
- At 98 seconds the square drawing panel is empty; 102 seconds shows a vertical coordinate relationship; 106/110 seconds show two wave/coordinate links and an evolving trace. This first targeted set ends before the clear circular trace appears.
- In the dense set, 112–114 seconds show a circular trace and dot at different positions. This supports the demonstrated relationship in context, not a recovered exact implementation.
- At 116 seconds the top row visibly reads `harmonic=1 amplitude=1.0000 phase=0.0000`. A faint second row is present; do not promote its low-contrast values as verified settings. This is later shape synthesis, not evidence for the earlier square-wave coefficients.

## Limitations

The fixed sparse baseline selected no frame in the two target passages. Targeted sets were deliberately chosen after reading their transcript times; this is an adaptive follow-up comparison, not equal-budget source-wide recall. The exploratory 8-frame set ends at 110 seconds, whereas dense/final targeted sets extend to 116; the added circle findings cannot be attributed to density alone. The final 15-frame follow-up used inspection of the dense set, so it is not held-out. One conceptual animation does not represent a UI/terminal tutorial or physical task. No minimum universal frame budget, exact settings recall rate, optimal vision provider or reader task completion is established.

Clean main initially failed CLI import due to `_find_breakdown` being absent from committed `batch_digest.py`; this branch copies the already existing primary-checkout helper solely to run the experiment (ticket 22). All startup prerequisites and resolution differences must remain visible when interpreting results.
