# NVIDIA Cosmos3-Edge: runtime prerequisite remains open

Date2026-10-25. Ticket34. **Status: current family researched and runtime availability probed; no inference.**

Current representative is `nvidia/Cosmos3-Edge`, revision `344d602b128d1bbdacb43b08d0a3626f46343e29`, reasoner path. Cosmos-Reason2 is a predecessor. Metadata reports3,858,999,728 BF16 parameters; that is neither total deployment memory nor a12GB fit guarantee. The repo also includes generation assets, which are not needed for source-evidence analysis.

The pinned card documents `vllm/vllm-openai:cosmos3` for reasoning, separately from `vllm/vllm-omni:cosmos3` generation. Docker CLI is installed locally, but a read-only server check failed because the dockerDesktopLinuxEngine pipe is absent. No supported running reasoner endpoint or local12GB recipe was verified. Probe evidence is in `access-and-runtime.json` on `codex/spike-provider-coverage`. No model inference or hardware-quality verdict follows from an inactive serving runtime.

Next: establish an eligible configured Linux/GPU reasoner endpoint and bound context/frames/resolution against measured memory; then use a manually referenced physical/non-text action sequence against Qwen/Molmo/ordered-frame baselines. Current image fixtures are insufficient to claim physical task causality. Record exact runtime, OpenMDW1.1 and third-party notices, input/output identity, action-order recovery and unsupported explanations. Do not generate footage as evidence. Ticket remains open; review28 must explicitly accept a measured role or defer it.

## Reproducible evidence

[Raw inputs/pointers, scripts, outputs, failures and environment](https://github.com/smileynet/video-buddy/tree/ce811ed8cd1864d347953ed4a08f0b141955ca95/docs/architecture/spikes/provider-coverage), branch `codex/spike-provider-coverage`, commit `ce811ed8cd1864d347953ed4a08f0b141955ca95`. Hosted/runtime reports preserve limited readiness probes only, not inference.
