# Ticket17 — throwaway guide adaptation comparison

Question: can a small observed procedure be adapted to a declared target without hiding unsupported changes? This is not a translator implementation or a complete Git guide.

## Frozen evidence and artifacts

Freeze `b442b1b` contains the source packet/frame, shared two commands, both guide variants, adapted script, protocol and runner before target execution. The source frame at638s was captured using the repository CLI; earlier624s partial typing is not completed-command evidence. The source video is https://www.youtube.com/watch?v=SWYqp7iY_Tc , Traversy Media, Git & GitHub Crash Course For Beginners. One unchanged selected frame is retained for comparative analysis; full original media/capture intermediates remain ignored, with no separate backup claim. Recover the frame via the capture recipe/source hash and compare the frozen JPEG hash; future source transcodes can differ, so the retained JPEG is the exact visual reference.

Guide A retains source commands and a target gap. Guide B preserves the same source block plus labeled documentation-supported native changes. Frozen guides retain their pre-execution status; actual tested status is in results/verification/provenance-ledger, not silently written back into source observations.

## Replay

Windows with Python3.10+, Git for Windows providing Bash/touch, and PowerShell7 on PATH:

```powershell
python docs/architecture/spikes/guide-adaptation/run.py
python docs/architecture/spikes/guide-adaptation/verify.py
```

Before replay, restore the five exact text inputs from frozen-inputs.zip into this guide-adaptation directory. The original Windows working files use CRLF while Git stores normalized text; the ZIP preserves the pre-execution bytes recorded in the frozen hashes. Restore them deliberately before running; do not guess an LF/CRLF conversion. The source JPEG is retained separately as an unchanged binary. The runner discovers pwsh and Git; the Bash/touch lookup assumes the Git for Windows usr/bin layout. It creates a new uniquely owned `.scratch/guide-adaptation/run-*` directory each run. It never deletes prior directories or writes to the primary checkout/user config. Source and native scripts run with those child working directories. Only the native child PATH is constrained; no parent PATH rewrite, global Git config, installation or network execution occurs. OS-wide side effects are not audited.

The Force negative control intentionally truncates only its newly created16-byte canary, not user files. Direct filesystem byte/type/mtime checks determine outcomes; an exit0 native source copy created nothing. Verification rechecks persisted files separately from runner booleans and confirms source/adapted Markdown blocks match executed scripts.

## Scope and interpretation

The actual host has touch, so the source lines work from its normal PowerShell. The native-only profile is an explicit controlled target, not a claim every PowerShell lacks touch. Current replay versions are not the exact historical tutorial environment. Coreutils9.7/PowerShell7.5 docs are cited background; actualtouch8.32/PowerShell7.6.9 observations establish only these cases.

Eight cases include expected failures/negative controls; do not call them eight successful reader tasks. One experimenter authored both guides and ran all cases. No human format preference, reading time or ability to distinguish layers was measured. Existing-file timestamps deliberately differ, and general names/permissions/concurrency are unqualified. No package/module or prototype code is promoted to main.

The initial source audit caught an overbroad New-Item wildcard claim. The note now records the documentation's internal conflict and withdraws generalization. Fixed Path dot/Name execution did not depend on that claim. Exact source/adaptation guides and protocol remained unchanged after results.
