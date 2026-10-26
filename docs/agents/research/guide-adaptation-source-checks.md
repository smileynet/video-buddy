# Guide adaptation source checks

Checked: 2026-10-26. Scope: ticket 17, adapting Git Bash file creation to a PowerShell 7 profile with Git's `cmd` directory available and GNU `usr/bin` absent. This is a target-profile constraint, not a claim that PowerShell cannot invoke `touch`; the working host has `touch` available.

## Verified findings

### GNU touch creates missing files and updates timestamps — high confidence

The [upstream Coreutils v9.7 manual source](https://github.com/coreutils/coreutils/blob/v9.7/doc/coreutils.texi), section `touch invocation`, says: “Any @var{file} argument that does not exist is created empty”. Its default timestamp behavior is supported by: “sets file timestamps to the current time.” These snippets retain Texinfo markup. Options such as `-c` and `-h` change creation behavior. GNU's rendered manual endpoint timed out during this check; the version-pinned upstream source was retrieved instead. Version: Coreutils v9.7, not a verified match for the host executable.

Existing contents are preserved by normal touch operation. Supporting implementation snippet from [v9.7 src/touch.c](https://github.com/coreutils/coreutils/blob/v9.7/src/touch.c): `O_WRONLY | O_CREAT | O_NONBLOCK | O_NOCTTY`. The open flags omit truncation, and the operation subsequently sets file times. Content preservation is an interpretation of this implementation, not an explicit guarantee that timestamps remain unchanged.

### New-Item File creates files; Force can destroy their contents — high confidence

[Microsoft New-Item documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-item?view=powershell-7.5), PowerShell 7.5 view, describes its filesystem behavior: “New-Item creates files and folders.” Example 9 says: “This overwrites the existing file”. That example recreates a file using `-ItemType File -Force` and shows length falling from 24 to 0. Therefore `New-Item -ItemType File -Force` is unsuitable as a content-preserving replacement for `touch`.

Prior art for adaptation, for fixed ordinary filenames in an existing directory:

```powershell
if (-not (Test-Path -LiteralPath '.gitignore')) {
    New-Item -ItemType File -Path '.gitignore' -ErrorAction Stop | Out-Null
}
```

This expresses “ensure a path exists without replacing existing contents.” It intentionally leaves existing timestamps alone and is not a complete touch emulator. Use an additional leaf check to reject an existing directory if a file is required. The test/create sequence is not atomic; omitting Force avoids requesting overwrite, but concurrency is not qualified. The earlier blanket claim that New-Item Path supports wildcards is withdrawn: the cited page's Path parameter says it works like LiteralPath and does not interpret wildcards, while Example6 demonstrates wildcard expansion across directories. Those sections conflict. This note does not resolve general path behavior; the actual adaptation uses a fixed Path of dot plus fixed Name values, so it does not rely on wildcard expansion.

Version caveat: host PowerShell reports 7.6.9; cited documentation is the explicitly selected 7.5 view. No exact 7.6 implementation comparison was performed.

### LiteralPath is the correct existence guard for exact names — high confidence

[Microsoft Test-Path documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/test-path?view=powershell-7.5), PowerShell 7.5 view: “No characters are interpreted as wildcard characters.” Its Path parameter description says: “Wildcard characters are permitted.” Quoting a string alone therefore does not provide literal-path semantics. Use `-LiteralPath` for the Test-Path guard. New-Item is a separate cmdlet whose cited page has the internal conflict described above; no blanket general-path claim is retained. The same host/documentation version mismatch applies.

### Git configuration can be isolated without editing user configuration — high confidence

[Git environment documentation](https://git-scm.com/docs/git), manual last updated for Git 2.56.0 (2026-09-28), says about `GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM`: “Take the configuration from the given files instead from global or system-level configuration files.”

Inference for reproducible fixture validation: point those variables to explicit empty temporary files in the child process environment, and set controlled per-command or repository-local settings such as identity and line-ending handling. This avoids assuming Windows understands the manual's `/dev/null` example. It does not isolate repository-local config, inherited `GIT_CONFIG_COUNT` entries, attributes, hooks, or alternate repository variables by itself; control these separately in a disposable repository. Preserve the parent environment, and never rewrite the user's global config or repurpose HOME to achieve isolation.

### Porcelain status and staged blobs validate complementary properties — high confidence

[git-status documentation](https://git-scm.com/docs/git-status), manual last updated for Git 2.53.0, says porcelain v1 “is guaranteed not to change in a backwards-incompatible way”. Use `git status --porcelain=v1` to compare staged/unstaged/untracked state; prefer `-z` when parsing arbitrary filenames. Expected state transitions matter, but status alone does not establish exact contents or timestamp preservation.

[gitrevisions documentation](https://git-scm.com/docs/gitrevisions), manual last updated for Git 2.56.0 (2026-09-28), describes `:[<n>:]<path>`: “names a blob object in the index at the given path.” [git-cat-file documentation](https://git-scm.com/docs/git-cat-file), same manual version/date, says: “Output the contents or other properties such as size, type or delta information”. Thus `git cat-file -s ':path'` verifies staged byte length and `git cat-file blob ':path'` inspects staged content; a zero-length placeholder should stage a zero-byte blob. Compare existing-file bytes separately before and after creation guards. For exact binary comparison, avoid PowerShell text decoding/re-encoding pipelines.

Version caveat: host Git reports 2.53.0.windows.2. git-status's documented version aligns with its base version; git, gitrevisions and git-cat-file pages are newer. The cited syntax should be exercised against the host during implementation validation rather than treating newer manuals as host execution evidence.

## Could not verify / boundaries

- No claim that GNU tools are absent on the actual host: the target profile intentionally excludes GNU usr/bin, while host availability differs. The parent task supplies this observation; this note did not independently resolve the host touch executable.
- No exact Coreutils build/version match or live touch behavioral run was made. v9.7 source establishes upstream semantics only.
- No full guide or fixture execution was performed here. This source check changed only this note and did not install software, run uv, alter environment variables, or edit Git configuration.
- Source text was treated as evidence, not instructions. Recommendations above are explicitly scoped inferences for the adapting guide.

## Execution/audit follow-up

The first audit caught the overbroad New-Item wildcard statement. It was corrected before the final verdict, with the page's internal conflict retained rather than selecting a convenient description. No frozen guide command or execution result changed. Actual host runs report Coreutils8.32 and PowerShell7.6.9, so v9.7/v7.5 documentation remains background support; fixed-case empirical behavior is the runtime evidence. Git environment/index suggestions were not exercised because the bounded experiment stops after file preparation, without initializing repositories.
