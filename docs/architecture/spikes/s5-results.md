# S5 state-store spike results

Date: 2026-10-24. Ticket: [16](../../../.tickets/16-spike-resumable-state.md).

## Deciding question

Can atomic JSON manifests safely support the intended bounded recovery/concurrency cases, or is transactional state already necessary? Options: Windows file manifest with OS byte-range lock and atomic replace; SQLite transaction with external artifact files. Neither implementation is production code.

## Evidence

Throwaway branch `codex/spike-state-comparison`, commit `82ce90eaa04c98ce0a41d4f884d4adea75069c0a`. Reproduction: on Windows/Python 3.10+, run `python docs/architecture/spikes/s5-state-comparison/probe.py` from that branch. Inputs, script, README and machine-readable observations are committed there; no prototype was merged into the product.

Observed environment: Windows 11 build 26300; Python 3.13.14; SQLite 3.53.1. Fixture: a 283,710-byte JPEG produced by the real frame CLI from Qr3VsZYQy4s, selected timestamp 174.148s; SHA-256 `ad4513b01f0bbe1883f5ecf668685c1695093ed8a6412f881c89b720f1fee383`. The fixture is included on the spike branch so results do not depend on a private workspace cache.

The full comparative run took 11.83 seconds on this machine, including child-process startup and intentional short delays. This is not a storage performance benchmark or a representative video-processing latency.

| Injected scenario | Manifest | SQLite | Observed outcome |
|---|---|---|---|
| Process death after artifact promotion | Pass | Pass | Resume completes state with one total generation |
| Partial artifact write | Pass | Pass | Unpromoted partial file is not reused; restart regenerates |
| Process death during state update | Pass | Pass | Restart obtains writer ownership and produces valid completion state |
| Corrupt output | Pass | Pass | Output regenerated rather than trusted from completion state |
| Missing output | Pass | Pass | Output regenerated |
| Changed configuration key | Pass | Pass | Previous output invalidated |
| Two same-source processes | Pass | Pass | Both exit successfully; one generation |
| Authentication failure | Pass | Pass | No generation on blind resume; explicit recovery enables generation |
| Optional stage failure | Pass | Pass | Warning and failed optional-stage state remain visible |
| Human edit sidecar | Pass | Pass | Sidecar retained across rerun/configuration change |

20/20 scenario observations passed. The scripted controls inspect exit codes, generation counts, completion state and output hash; raw checks are in `observations.json` on the branch.

## Verdict and implications

**Retain the file-based design as viable for a bounded single-writer implementation; do not select a universal winner or integrate either prototype.** These cases did not reveal a transactional requirement forcing SQLite. Both approaches needed external artifact validation and atomic file promotion; database transactions alone do not make media files trustworthy.

The evidence supports a narrow design requirement: use OS-released ownership rather than an existence-only lockfile, validate disk artifacts on resume, and distinguish explicit user-action recovery from automatic retry. These are experimental design inputs pending production review, not a claim that the current runner already does this.

## Limits and remaining work

- Both options hold one global writer lock, including the dummy stage. This is intentionally bounded and cannot establish acceptable multi-source throughput. A real runner would need short state transactions and per-source ownership; that design has not been qualified here.
- The stage wraps real image bytes with configuration metadata; it does not download, transcribe or decode media. Known expected fixture bytes substitute for a general artifact-validation interface.
- Failure injection uses immediate process exit, not machine power loss, disk failure or a network filesystem. File locking is Windows-specific; Linux behavior is unmeasured.
- “No blind retry” is a scripted state policy, not evidence about real authentication services. “Edits preserved” covers a sidecar file, not a merge algorithm.
- A single run with two competing processes is feasibility evidence, not a stress test or reliability rate.

Close the comparison ticket with this bounded verdict and keep prototype code out of production. Reopen the storage decision if required multi-source concurrency or platform behavior invalidates the constraints. Implementation remains subject to the relevant spike results and review; no new storage dependency is approved by this report.
