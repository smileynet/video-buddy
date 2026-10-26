# Guide adaptation source checks audit

Audited: 2026-10-26, independently using the research-audit skill. Scope: citation accuracy and interpretation of `guide-adaptation-source-checks.md`; no workflow execution or runtime verification.

**Overall trust: 7/10 — substantive primary-source evidence, but one material New-Item wildcard claim overstates an internally conflicting cited source. Revise before relying on the note.** This is not an empty-stub failure.

## Per-claim verdicts

| Claim | Verdict | Re-fetched evidence and limits |
| --- | --- | --- |
| Normal touch creates missing files empty and updates timestamps | supported for v9.7; weak for host application | [Pinned GNU manual source](https://raw.githubusercontent.com/coreutils/coreutils/v9.7/doc/coreutils.texi), touch invocation, states creation unless `-c`/`-h` and current-time defaults. Primary and correctly scoped; host Coreutils 8.32 is a different version. |
| touch preserves existing file contents | supported for v9.7 implementation | [Pinned touch.c](https://raw.githubusercontent.com/coreutils/coreutils/v9.7/src/touch.c), lines 119–123, opens with the quoted flags and no truncation flag; timestamp update follows. Correctly labeled an implementation inference, not proof of unchanged timestamps or host behavior. |
| New-Item creates files; File with Force can empty an existing file | supported for documented 7.5; weak for exact host version | [Microsoft New-Item 7.5](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-item?view=powershell-7.5), Example 9, explicitly describes overwrite and shows 24 bytes becoming zero. Host PowerShell 7.6.9 is not the cited version; caveat is present. |
| New-Item Path supports/interprets wildcards | **unsupported** | The same Microsoft page, Path description, says: “Wildcard characters are not interpreted.” It explicitly compares Path to other cmdlets' LiteralPath. However, re-fetched Example 6 (lines 170–194) uses `New-Item -Path C:\Temp\* -Name temp.txt` and demonstrates wildcard expansion across directories. The page is internally inconsistent; neither blanket wildcard-support nor blanket no-wildcard claims are established. The note asserts the blanket support claim twice. |
| Test-Path LiteralPath provides exact-name guarding, unlike Path | supported for documented 7.5; weak for exact host version | [Microsoft Test-Path 7.5](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/test-path?view=powershell-7.5), LiteralPath description, directly supports the quoted claim; quoting alone does not select this parameter. Its Path behavior must not be transferred to New-Item. |
| Fixed-name existence guard avoids replacing existing content | supported as scoped inference | The branch skips creation when the path exists; the directory, race, and timestamp limitations are acknowledged. No atomicity or arbitrary-name runtime guarantee follows. |
| Git global/system configuration can be redirected | supported as documentation; weak as host validation | [Git environment manual](https://git-scm.com/docs/git), GIT_CONFIG_GLOBAL/SYSTEM, matches the quoted substitution claim. Empty-file guidance is a reasonable inference with correctly listed isolation gaps. Manual 2.56 differs from host 2.53.0.windows.2. |
| Porcelain v1 supports stable state comparison | supported as documentation | [git-status](https://git-scm.com/docs/git-status), Porcelain Format Version 1, matches the stability quote; manual last changed in 2.53.0. This is not evidence that comparisons were run. |
| Index revision syntax and cat-file verify staged size/content | supported as documentation; weak as host validation | [gitrevisions](https://git-scm.com/docs/gitrevisions) documents the index blob spelling; [git-cat-file](https://git-scm.com/docs/git-cat-file) documents size and content output. Both retrieved pages last changed in 2.56.0; the note correctly requests host exercise later. |

## Required correction and interpretation boundaries

1. Remove both blanket statements that New-Item Path interprets wildcards, including the cross-reference in the LiteralPath section. Record the conflict between Example 6 and the Path paragraph rather than choosing either as a universal rule. Keep the adaptation bounded to fixed filenames, using an existing directory as Path and the fixed filename as Name if desired; no generic-path qualification follows. Test-Path still needs LiteralPath for exact-name guarding.
2. Keep version confidence separate from source accuracy. GNU v9.7 and Microsoft 7.5 establish their documented semantics; they do not establish exact behavior of Coreutils 8.32 or PowerShell 7.6.9. The existing caveats substantially handle this, but section-wide “high confidence” labels should not be read as exact-host qualification.
3. Git isolation, status, and staged-blob sections are background research proposals, not performed validation. The bounded main experiment covered two files only, using fixed `-Path .` and `-Name` values; it did not exercise wildcards. Do not report full-guide execution, Git state validation, arbitrary filenames, directory rejection, or races as experimentally tested from this note.

All cited sources were re-fetched from primary upstream/Microsoft sources. No installs, uv commands, environment/configuration changes, or host behavior tests were performed for this audit. Only this companion file was written.

## Resolution check — 2026-10-26

Re-read the corrected producer note after the initial audit; the **7/10 above remains the initial snapshot**, not a current unresolved failure score. Both blanket wildcard assertions have been withdrawn, the conflicting Microsoft sections are explicitly recorded, and the note avoids claiming general-path or concurrent-creation qualification. The required source-interpretation correction is resolved.

**Usable for the bounded fixed `-Path '.'` / fixed `-Name` experiment.** The corrected note distinguishes v9.7/v7.5 background sources from the separately measured Coreutils 8.32 / PowerShell 7.6.9 behavior, and says the Git suggestions were not exercised. The parent reports unchanged implementation/guide hashes and two-file runtime evidence; this resolution check does not independently repeat or broaden those tests. General wildcard paths, races, full-guide execution, and Git state validation remain outside the qualified result. No additional source fetches, runtime probes, installs, or environment changes were performed for this resolution check.
