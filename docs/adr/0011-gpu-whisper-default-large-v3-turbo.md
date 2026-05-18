# 0011 — Default to `large-v3-turbo` on GPU

**Context.** CPU and GPU machines should not share the same Whisper default. CPU has already been pinned to `base` from local benchmark evidence. The unresolved question was which model video-buddy should prefer when a CUDA-capable backend is selected automatically.

Three alternatives existed:
1. **`large-v3-turbo`** — GPU-oriented default; keep the highest-throughput large model as the preferred accelerated path.
2. **`distil-large-v3`** — also GPU-oriented, but with less user familiarity in the current workflow.
3. **`base` everywhere** — one default across CPU and GPU until dedicated GPU benchmarks exist.

**Decision.** Option 1. Use `large-v3-turbo` as the GPU-preferred default.

**Why.**
- The existing workflow historically chose `large-v3-turbo` from GPU-oriented benchmarks; the user explicitly wants to preserve that preference on GPU.
- CPU and GPU have materially different operating envelopes. A conservative CPU default does not imply the same choice on accelerated hardware.
- `large-v3-turbo` is already a known model name in the current workflow, so the public tool stays aligned with operator expectations.
- Users can still force another model explicitly; this only governs the auto-selected default on GPU-capable backends.

**Implications.**
- Auto model selection becomes hardware-aware: CPU defaults to `base`, GPU defaults to `large-v3-turbo`.
- Docs must say `--whisper-model` default is backend-dependent, not globally `base`.
- The public bundle names should distinguish CPU and GPU intent: `recommended-cpu` and `recommended-gpu`, not a single ambiguous `recommended`.
- If future GPU benchmarks contradict this choice, the model can change without altering the selector surface.
