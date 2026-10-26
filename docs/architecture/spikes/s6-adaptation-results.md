# Guide adaptation: preserve the source, qualify the target

**Ticket 17 · 26 October 2026 · bounded walkthrough complete, no production integration.** A separately labeled native PowerShell adaptation created the tutorial's two placeholder files and preserved existing contents in the declared target profile. The source-faithful guide remains valid where its GNU utility is available. This supports a conditional two-layer artifact contract, not a general command translator or a reader-usability winner.

## Question and frozen evidence

Can a tutorial procedure be adapted to a different environment without hiding unsupported changes? Both variants use the same [Traversy Git tutorial](https://www.youtube.com/watch?v=SWYqp7iY_Tc) evidence. At nominal10:38, a retained full frame shows completed `touch index.html` and `touch app.js` commands in a Windows MINGW64/Git Bash context, followed by two files in Explorer. An earlier10:24 frame contains partial typing and was not used as completed-command evidence.

The scope is **file preparation before editing HTML or later Git operations**, not completion of the entire Git tutorial. Source installed Git/Coreutils versions were not verified; a download webpage advertising a version is not runtime evidence. Explorer's0KB display is not byte-exact proof. The replay independently checks bytes.

Freeze `b442b1b` committed the source packet/frame, both guides, executable adaptation, eight-case protocol and runner before execution. A retains literal source commands and an explicit target gap. B retains that identical source block plus separately labeled native changes, primary documentation, target conditions and pending verification labels. The frozen guides were not rewritten after seeing outcomes; tested status lives in a separate result/provenance ledger.

## A real, explicitly constrained mismatch

The actual host has GNU touch on PATH. Its normal PowerShell can run the original lines; the host-control case demonstrates that. The test target is a **child-only native profile**: PowerShell7 `-NoProfile`, with pwsh, Git's cmd directory and System32 on PATH, excluding GNU usr/bin. It represents a declared no-GNU target capability, not a claim that all PowerShell environments lack touch.

Observed replay versions: PowerShell7.6.9, Git2.53.0.windows.2, Bash5.2.37 and GNU Coreutils touch8.32. Documentation support uses Microsoft7.5 views and GNU9.7 source, with those version differences explicit. The current replay is not execution in the exact historical2017 environment. No packages were installed, no repositories initialized, and no user/global Git configuration or parent PATH was edited.

## Compared artifacts

| Option | Behavior | Honest limit |
| --- | --- | --- |
| A — source-faithful with gaps | Shows the two original lines, requires touch/Git Bash, warns or stops when unavailable | Provides no native substitute; this is a valid gap, not a fabricated solution |
| B — source plus adaptation | Uses guarded New-Item for fixed filenames; leaves existing file contents intact; rejects a directory conflict | Analyst-authored, documentation-backed changes, not source-demonstrated commands; ordinary fixed-name scope only |

Essential changes remain traceable: New-Item File and omission of Force cite [Microsoft New-Item](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-item?view=powershell-7.5); literal existence/file-type checks cite [Test-Path](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/test-path?view=powershell-7.5); ErrorAction Stop cites [common parameters](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_commonparameters?view=powershell-7.5). The generic creation-error path is documentation-supported but not exercised as a permissions/error-recovery test. The observed directory-conflict failure is a separate explicit guard.

The content-preserving goal comes with a deliberate semantic change: GNU touch updates existing modification time; B leaves it unchanged. Modification time was checked, not every timestamp field. Neither guide presents B as a complete touch emulator. The target requirement to preserve existing work is an explicit experiment constraint; the video demonstrates fresh file creation, not the existing-file test.

## Actual walkthrough

Every command was inspected before execution. Each case ran in a newly owned scratch folder; the Force control touched only a generated16-byte canary. Python inspected filesystem types, byte lengths, hashes and modification times independently of subprocess exit status. A second verifier re-read the persisted files and checked frozen guide/source hashes and code-block equality.

| Case | Process exit | Observed target outcome |
| --- | ---: | --- |
| Original lines, current Git Bash, fresh folder | 0 | Two empty ordinary files |
| Original lines, host PowerShell with touch | 0 | Same two empty files; no adaptation needed there |
| Original lines, native-only PowerShell | **0** | **No files**, command-not-found errors; exit0 was not task success |
| Adapted native procedure, fresh folder | 0 | Two empty ordinary files |
| Original Bash procedure, existing canary | 0 |16bytes preserved, missing file created, modification time updated |
| Adapted native procedure, existing canary | 0 |16bytes preserved, missing file created, modification time unchanged |
| Naive New-Item Force negative control | **0** | Existing16bytes became0; unacceptable preservation result |
| Adapted native procedure, directory conflict | 1 | Explicit failure, directory/sentinel preserved, no false completion |

All eight frozen experimental expectations matched. **These are not eight successful reader tasks**: the table deliberately includes failures and a destructive negative control within disposable data. A's raw native-command execution diagnoses its declared gap; it is not a recommendation to ignore the guide's precondition.

## Provenance, audit and what remains unverified

The result ledger distinguishes source observations, documentation-supported changes, tested-here cases and unsupported generalization. It does not turn an executed adaptation into something demonstrated by the video. Source and adapted Markdown code blocks exactly match their corresponding execution inputs. Static labels/link coverage were checked, but **no fresh reader was observed distinguishing the layers**. Same-agent authoring and execution cannot establish usability, human completion improvement or a preferred format.

[Primary-source checks](../../agents/research/guide-adaptation-source-checks.md) and a [separate audit](../../agents/research/guide-adaptation-source-checks-audit.md) caught an overbroad New-Item wildcard claim. The cited page conflicts internally between its parameter description and an example. The blanket claim was withdrawn before the verdict; the corrected note is usable for this fixed Path-dot/Name experiment. No frozen guide command or outcome changed. General path behavior is not qualified.

No evidence here qualifies arbitrary filenames, symlinks, concurrency, permissions/ACL failures, cross-platform PowerShell, complete Git workflows, historical source binaries or other commands. Adaptation is conditional on the declared profile and assumptions; where those cannot be established, retain A's faithful instructions and gap.

## Costs and checks

One run per case, total subprocess wall1.80seconds including startup; individual cases ranged0.05–0.43s. These are reproduction observations, not reliable performance estimates or reader times. The predeclared additional verification budget for B was60active minutes after preparation; extraction/research/guide-generation effort was not a controlled timing or token-cost comparison. Peak memory was not measured. No speed or human-effort advantage is claimed.

The corrected repository CLI capture succeeded after an initial overridden-intermediates call lacked explicit source JSON. Existing experimental frame flags/helper were used on the spike branch, not promoted; clean-checkout issue22 remains open. Eight persisted fixture checks, frozen hashes, source/adaptation block checks and parent/child profile observations passed. Pre-commit and dashboard verification are recorded with final evidence.

## Disposition

**Conditional adoption into the proposal:** preserve the observed source, separately label each target adaptation and its authority, and attach tested profile/postconditions without upgrading that into universal verification. Keep A as the correct fallback when compatibility is present or an adaptation cannot be substantiated. Reject blind syntax rewriting, Force-based “ensure file” recipes for this preservation goal, and execution-success claims based only on exit status.

Ticket17 can close with this bounded disposition. Review28 remains the feature/architecture integration gate. Reader comprehension, blocked-step correction and actual task completion remain with18/21; the prepared guides and failure cases are candidate fixtures, not substituted human results. No production implementation was made.

[Pinned raw evidence](https://github.com/smileynet/video-buddy/tree/f305c9fe9f3f87f5c04bf6c27e92d600a67b4f01/docs/architecture/spikes/guide-adaptation) includes independent verification of eight persisted cases and five exact-byte frozen text restores. The ZIP preserves original Windows line endings for replay. Pre-commit and dashboard desktop/mobile checks passed. Final staged evidence inspection covered nine files / 51,941 logical Git-blob bytes with complete metadata/content and no findings, excluding earlier freeze, history and ignored media. replay instructions, frozen guides, source frame and all failures remain on `codex/spike-guide-adaptation` under `docs/architecture/spikes/guide-adaptation/`.
