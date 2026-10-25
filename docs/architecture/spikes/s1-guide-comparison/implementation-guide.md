# Sine-wave techniques: implementation packet variant B

Throwaway comparison artifact for ticket 12. Not a production guide. Uses exactly the same evidence and mathematical adaptations as variant A. Evidence: `evidence.json`, historical machine transcript; no screen commands are verified.

## Desired result and prerequisites

Task 1: generate 360 samples of circular motion and verify constant unit radius. Task 2: decide whether this packet specifies the exact square-wave procedure shown by the source. Use Python 3.10+ standard library and an empty disposable output directory. Python, sampling, output format and numeric tolerance are experiment choices, not observed video instructions.

## Task 1: unit circle

1. Use 360 evenly spaced phase values theta = 2*pi*i/360 for i = 0…359. Choose unit amplitude and equal frequency for both coordinates. **Adapted experiment setup.**
2. Calculate x = sin(theta) and y = sin(theta + pi/2). **Derived adaptation** of the quarter-turn relationship in E015–E016 (95.92–112.04 seconds); this exact code/formula was not recovered from a frame.
3. Save theta, x and y as CSV columns. **Adapted output format.**
4. Check every point satisfies abs(x*x + y*y - 1) <= 1e-12 and the first point is approximately (0, 1). **Adapted verification.**

Expected outcome: a constant-radius circle. If the phase offset is accidentally zero, the coordinates lie on a line; do not mark that result successful just because a CSV exists. This failure prediction is mathematical reasoning, not quoted troubleshooting from the video.

## Task 2: reproduce the demonstrated square wave

**Blocked by missing evidence.** E010–E012 (71.70–85.14 seconds) name the waveform but do not specify harmonic indices, coefficient magnitudes, signs or phase conventions. This packet cannot determine the exact source procedure. Do not invent these parameters or present a generic Fourier recipe as an observed implementation.

Next evidence request: inspect the frames/clip around this passage, or add separately attributed mathematical documentation as an adaptation. The missing information may exist in the video; it is absent from this packet.

## Review state

| Dimension | Status |
|---|---|
| Extraction coverage | Partial: transcript only |
| Evidence support | Circle relationship supported; formula/setup adapted; square procedure unresolved |
| Execution validation | Not run at draft time; numeric probe recorded separately in observations.json |

This guide is not evidence that a fresh reader completed either task.
