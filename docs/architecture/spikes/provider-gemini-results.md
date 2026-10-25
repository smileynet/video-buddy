# Google Gemini: comparison pending configured access

Date2026-10-25. Ticket30. **Status: documented, not inference-tested.**

Representative: `gemini-3.8-flash`. [Current-provider research](../agents/research/open-questions.md#current-provider-coverage-expansion-2026-10-25) records the dated primary-source contract and eligibility limits.

No matching Gemini/Google API credential is exposed in the probed current process environment; account/model access, quota and other private configuration remain unverified. Configuration location was requested from the user; no key was requested in chat, printed or saved. No provider request or paid call was made. This is not an observed authentication rejection or a model-quality failure. Probe evidence: `access-and-runtime.json` on `codex/spike-provider-coverage`.

Once configured, validate actual model availability, pin response identity/API/SDK, and run the same frozen public object/UI/diagram/negative queries as local baselines. Preserve geometry conversion, raw labels/masks, costs and latency; assess input/video sampling separately from source action coverage. Do not infer service rights from client-code licensing. Ticket remains open. Final review28 must explicitly review the result or defer the provider; it cannot claim comprehensive coverage.

## Expanded credential lookup (user-directed)

Checked existing HF CLI authentication, user mise TOML and standard alternate locations, plus project/worktree.env.local. Found HF_TOKEN, authenticated it, and saved it to Git-ignored project-local files as requested. No matching Gemini/DINO-X key was present in those checked sources. HF model-download authentication is valid; separate hosted API authentication remains unverified. Agent guidance now records the project-local lookup and worktree fallback to prevent repeated rediscovery. No key value is in this report.

## Reproducible evidence

[Raw inputs/pointers, scripts, outputs, failures and environment](https://github.com/smileynet/video-buddy/tree/ce811ed8cd1864d347953ed4a08f0b141955ca95/docs/architecture/spikes/provider-coverage), branch `codex/spike-provider-coverage`, commit `ce811ed8cd1864d347953ed4a08f0b141955ca95`. Hosted/runtime reports preserve limited readiness probes only, not inference.
