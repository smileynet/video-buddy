# Local TTS runtime eligibility for the narration spike

Checked **27 October 2026** against official current source and checkpoint configuration. Documentary preparation for Windows / RTX5070 / Python3.11, not an installed or inferred runtime result. No packages or models installed and no inference performed by this research task.

## Load-bearing dependency conflicts

**High confidence, declared metadata.** Current Qwen source identifies `qwen-tts`0.1.1 and pins Transformers4.57.3 and Accelerate1.12.0, while listing torchaudio without a version. Supporting snippets: `transformers==4.57.3`, `accelerate==1.12.0`. [Qwen pyproject](https://github.com/QwenLM/Qwen3-TTS/blob/main/pyproject.toml).

Current Chatterbox source identifies0.1.7 and, on Python3.11, requires NumPy1.x, torch/torchaudio2.6.0, Transformers5.2.0, Librosa0.11.0, Diffusers0.29.0, Safetensors0.5.3 and Perth from its moving git master. Supporting snippets: `torch==2.6.0; python_version < '3.14'`, `transformers==5.2.0`, `resemble-perth @ git+https://github.com/resemble-ai/Perth.git@master`. [Chatterbox pyproject](https://github.com/resemble-ai/chatterbox/blob/master/pyproject.toml).

**Recommendation/inference:** separate model environments. One resolver environment cannot satisfy both exact Transformers pins. Inspect the installed release metadata too: the PyPI wheel may differ from these current repository files. Freeze actual package, source and checkpoint revisions with the run.

## Blackwell / CUDA choice

**High confidence in official release support; actual wheel execution still required.** PyTorch2.7 introduced Blackwell support: “support for the NVIDIA Blackwell GPU architecture”. Its release post mentions CUDA12.8 wheels. [PyTorch2.7 release](https://pytorch.org/blog/pytorch-2-7/).

The official previous-version page lists a Linux/Windows CUDA12.8 installation route for matching torch/torchaudio2.7.1 and2.8.0. Supporting snippet: `torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0`. [Official previous versions](https://pytorch.org/get-started/previous-versions/),2.8.0 / Linux and Windows / CUDA12.8.

**Experimental starting point, not a verified compatibility promise:** matching torch/torchaudio2.8.0 cu128 in each environment is a plausible common backend for the RTX5070. This overrides Chatterbox's Python3.11 torch2.6 declaration and must be reported as a deviation, with a CUDA smoke test and actual synthesis. Do not let a later dependency install silently downgrade torch or torchaudio. Qwen's optional FlashAttention build is not required by its source interface: `_supports_sdpa = True`. Try `attn_implementation="sdpa"` when avoiding a Windows FlashAttention build, and record this departure from the README example. [Qwen model implementation](https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/core/models/modeling_qwen3_tts.py).

No minimum VRAM, Windows success, CPU performance or quality is established by these sources or by parameter counts. Available GPU memory and competing processes must be measured during the actual run.

## Shared official English reference

The [Qwen README Voice Clone example](https://github.com/QwenLM/Qwen3-TTS#voice-clone) supplies [clone.wav](https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-TTS-Repo/clone.wav) and the associated English transcript in its `ref_text` variable. It is an upstream demonstration reference, not the creator's video voice or the user's recording. Use the same downloaded bytes for both options; preserve the hash and this provenance. The source example's transcript is not an independent listening annotation.

**Measured header probe only:** a read-only HTTP request and RIFF header inspection found mono24000Hz IEEE-float WAV,775680 audio-data bytes, duration8.08seconds. Python's stdlib `wave` initially rejected WAV format3; this is a parser limitation, not a corrupt-file finding. Use SoundFile/Librosa for decoding. No persistent audio copy was made by this research task.

Chatterbox's current code requires the prompt to exceed5seconds, so that header duration satisfies the stated condition. Supporting snippet: `Audio prompt must be longer than 5 seconds!` Its internal reference preprocessing retains at most10seconds for the decoder and15seconds for encoder conditioning. [Turbo implementation](https://github.com/resemble-ai/chatterbox/blob/master/src/chatterbox/tts_turbo.py).

This checks a documented demo entry point, not a blanket license or rights determination for unrelated voices/recordings. It is suitable to identify the proposed common reference; the experiment owner should preserve the actual downloaded fixture and status.

## Freeze effective generation settings

**Qwen0.6B Base:** [checkpoint generation_config.json](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base/blob/main/generation_config.json) currently declares sampling enabled, repetition penalty1.05, temperature0.9, top-p1.0, top-k50; subtalker sampling uses temperature0.9/top-p1.0/top-k50; output cap8192new tokens. Supporting snippet: `"max_new_tokens": 8192`. The [wrapper merge function](https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/inference/qwen3_tts_model.py) prioritizes explicit arguments, then loaded checkpoint defaults, then fallback defaults; its fallback output cap is2048. Log effective values rather than assuming the fallback. Set English explicitly, use the supplied reference transcript and `x_vector_only_mode=False` for the documented ICL cloning route. Reusable `create_voice_clone_prompt` avoids repeated reference-feature work; report whether prompt preparation is inside generation timing.

**Chatterbox-Turbo:** public `generate` defaults are temperature0.8, top-p0.95, top-k1000, repetition penalty1.2, reference loudness normalization enabled. CFG/exaggeration/min-p are ignored by Turbo when requested; do not report them as active controls. Its [T3 turbo sampler](https://github.com/resemble-ai/chatterbox/blob/master/src/chatterbox/models/t3/t3.py) has `max_gen_len=1000`, while the public wrapper does not expose that argument. The [GPT2 medium configuration](https://github.com/resemble-ai/chatterbox/blob/master/src/chatterbox/models/t3/llama_configs.py) lists context/positions8196; input tokenization requests truncation. Neither number is an endorsed safe paragraph length. Keep the initial paragraphs short and inspect all requested words for truncation/omissions.

Neither public default fixes an experiment seed. Set and record Python/NumPy/torch seeds (for example42) before the compared take; this is a protocol choice, not proof of cross-model or cross-hardware determinism. Different default samplers mean a same-script/reference comparison is an application-route comparison, not an isolated architecture experiment.

## Watermark and measurement boundary

Current [Perth metadata](https://github.com/resemble-ai/Perth/blob/master/pyproject.toml) is1.1.0 with NumPy>=1.24 and torch/torchaudio>=2.1; it does not itself impose Chatterbox's torch2.6 exact pin. Supporting snippet: `version = "1.1.0"`. The [Perth initializer](https://github.com/resemble-ai/Perth/blob/master/src/perth/__init__.py) catches an import failure and sets `PerthImplicitWatermarker` to None, which is not a working fallback for Turbo's unconditional constructor. Investigate a failing installation rather than silently removing watermarking.

Turbo creates the real Perth implicit watermarker and applies it before returning audio. The [watermarker constructor](https://github.com/resemble-ai/Perth/blob/master/src/perth/perth_net/perth_net_implicit/perth_watermarker.py) defaults to CPU. Supporting snippet: `device="cpu"`. Keep that behavior in the application-route measurement and include it in generation wall time; do not call the result pure GPU inference time. The default [Perth model directory](https://github.com/resemble-ai/Perth/blob/master/src/perth/config.py) is packaged `perth_net/pretrained`, so include required watermark assets in offline-readiness checks. No watermark detection/effect test was performed here.

## Outstanding before a comparative claim

Actual resolver/installation outcomes, GPU compatibility, package/checkpoint revisions, reference fixture hash, memory peaks, generation times and output quality remain experiment observations. Separate setup/download/import/model-load/reference-preparation and warm synthesis costs. Preserve failed attempts and any source/dependency overrides. A source read and an8.08-second header do not establish model quality or successful local synthesis.
