# A — Source-faithful project-file preparation

Goal: create the tutorial's index.html and app.js placeholders. Scope ends before editing HTML or later Git steps.

## Source observations

At10:38, the source shows a Windows MINGW64/Git Bash terminal with these completed commands and two files in Explorer. Source installed Git/Coreutils versions are not verified; the adjacent download webpage is not runtime-version evidence.

```bash
touch index.html
touch app.js
```

Source evidence: S1/S2 in source-packet.json and the retained full frame. Zero-byte creation is supported by GNU documentation and will be independently checked in the current replay; Explorer's0KB display alone is not byte-exact proof.

## Preconditions and target gap

Use a writable ordinary project directory and Git Bash/GNU touch. The host already has touch, so native PowerShell can also invoke it there. A native-only profile without GNU utilities cannot run these lines. If touch is absent, stop or use Git Bash; this source-faithful variant does not supply a native substitute.

Do not infer a missing command merely from the shell name. Check command availability. These steps are not a complete project/tutorial guide.

## Checkpoint

Two ordinary files named index.html and app.js exist; fresh placeholders are empty. Existing contents should survive normal touch operation, although timestamps change according to GNU semantics. No reader-completion or exact historical runtime claim.

Support for the touch semantics, separate from the video: [GNU Coreutils v9.7 manual source](https://github.com/coreutils/coreutils/blob/v9.7/doc/coreutils.texi), touch invocation, and [implementation](https://github.com/coreutils/coreutils/blob/v9.7/src/touch.c). Current installed touch version is recorded separately; no exact historical runtime claim.
