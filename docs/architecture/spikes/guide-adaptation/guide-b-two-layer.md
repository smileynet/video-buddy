# B — Observed source plus a labeled native adaptation

Goal and source scope are identical to A: prepare index.html and app.js before editing HTML. This is an experimental guide, not a shipped translator.

## Layer1 — observed, unchanged

S1/S2: source frame10:38 shows these completed Git Bash commands on Windows:

```bash
touch index.html
touch app.js
```

The full frame/source packet is retained. No exact historical Git/Coreutils version was established.

## Layer2 — adaptation for a declared target

Target: Windows PowerShell7, writable ordinary local folder, fixed filenames, GNU touch unavailable on PATH. If touch is already available, A remains a valid simpler route; do not rewrite a working procedure automatically.

A1: replace creation with New-Item File (Microsoft New-Item reference). A2: guard existing paths with Test-Path LiteralPath (Microsoft Test-Path reference). A3: reject a directory occupying either required filename using PathType Leaf. A4: omit Force to preserve existing contents. A5: stop on creation errors. These are analyst-authored adaptations supported by the cited docs, not observed tutorial commands.

```powershell
foreach ($name in @('index.html', 'app.js')) {
    if (Test-Path -LiteralPath $name) {
        if (-not (Test-Path -LiteralPath $name -PathType Leaf)) {
            throw "$name exists but is not a file. Stop and resolve the conflict."
        }
        continue
    }
    New-Item -ItemType File -Path . -Name $name -ErrorAction Stop | Out-Null
}
```

## Changed semantics and verification status

This adaptation ensures missing files exist and preserves existing contents. It does NOT reproduce touch timestamp updates: existing files are left alone. The test/create sequence is not atomic; no arbitrary paths, symlinks, concurrent writers or permission scenarios are qualified. Fixed names and a known writable ordinary directory are assumptions.

Docs: Microsoft New-Item/Test-Path7.5 views; target host reports7.6.9. GNU v9.7 source supports semantics but may differ from the installed executable. Actual execution evidence is pending in the frozen protocol and will be published separately; do not mark this source-demonstrated or generally verified just because it reads plausibly.

## Checkpoint

Fresh folder: exactly two ordinary empty files. Existing-file case: original bytes remain. Directory conflict: stop explicitly, preserve its sentinel and do not claim success. Check the files; process exit status alone is insufficient.

Reader ability to distinguish the layers is unmeasured. These labels are a reviewable contract proposal, not usability evidence. Current validation is an experimenter walkthrough only.

## Adaptation provenance map

- A1/A4, file creation and no Force: [Microsoft New-Item7.5](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-item?view=powershell-7.5), especially nameSet syntax and the existing-file Force example.
- A2/A3, exact existence and file-type guard: [Microsoft Test-Path7.5](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/test-path?view=powershell-7.5), LiteralPath/PathType.
- A5, creation failure terminates this operation: [Microsoft common parameters7.5](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_commonparameters?view=powershell-7.5), ErrorAction Stop. Host execution still must be checked against7.6.9.
- Timestamp difference: [GNU v9.7 touch](https://github.com/coreutils/coreutils/blob/v9.7/doc/coreutils.texi), separate source semantics. This is not a timestamp emulator.

Frozen pre-execution guide; consult the separate result ledger/report for actual tested status. No human reader outcome is implied.
