# Throwaway state-store comparison

Ticket 16 / S5. This is an experimental harness, not product code.

Run `python docs/architecture/spikes/s5-state-comparison/probe.py` on Windows with Python 3.10+ (only the standard library is required). Optional first argument supplies a different media fixture. The included JPEG comes from the CLI capture of public video Qr3VsZYQy4s at selected timestamp 174.148 seconds. Its byte hash is recorded in the observation report. Stores are created in a fresh `video-buddy-THROWAWAY-state-*` temporary directory; the report is written beside the script. The script does not delete prior runs.

Both options use a **global single-writer lock**, not concurrent execution of separate sources. File manifests use a Windows byte-range lock, fsync and atomic replace. SQLite uses `BEGIN IMMEDIATE` and transaction commit/rollback. Both write external artifacts atomically and validate their known expected bytes, including the media fixture hash and configuration key. This is not a general stage validator, downloader, durable media decoder or real job graph.

Ten scenarios per option: death after artifact promotion; partial artifact write; death during state update; corrupt output; missing output; changed config; duplicate same-source processes; authentication requiring explicit recovery; optional failure with visible warning; user sidecar preservation.

The two-process crash/concurrency probes inspect exit codes and output states. They do not simulate power loss, guarantee network filesystem behavior, establish high throughput or merge user edits. The saved result shows 20/20 scenario observations passing. Interpret that as bounded feasibility for both options, not a universal storage winner.
