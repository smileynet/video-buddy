# Local starting points for narration and voice cloning

Checked **27 October 2026** against official repositories, checkpoint cards and loader source. Scope: two concrete candidates for a local prerecorded-narration trial. No model was installed, downloaded or run; speed, memory, voice quality, platform compatibility and offline operation were not measured. These options extend the narration guide, not its existing spike results.

## 1. Qwen3-TTS: a multilingual cloning starting point

**High confidence in documented task and entry point.** Use the exact checkpoint **`Qwen/Qwen3-TTS-12Hz-0.6B-Base`** for reference-audio cloning. Its official card identifies a “**0.6B Base model**” and supplies a `generate_voice_clone` example. It lists Chinese, English, Japanese, Korean, German, French, Russian, Portuguese, Spanish and Italian. Do not substitute the family's VoiceDesign or CustomVoice checkpoint and assume the same task/API. [Official checkpoint card](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base).

**License distinction:** the [code license](https://github.com/QwenLM/Qwen3-TTS/blob/main/LICENSE) is Apache License2.0; the selected [checkpoint metadata](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base/raw/main/README.md) separately states “`license: apache-2.0`”. This records the selected code/checkpoint declarations, not blanket clearance for recordings, voices, dependencies or every Qwen model.

**Starting action:** follow the [official installation and voice-clone quickstart](https://github.com/QwenLM/Qwen3-TTS#quickstart) in an isolated environment; load that Base checkpoint, supply a permitted reference recording and its matching text, synthesize one paragraph and save the returned WAV. Use a local reference path rather than the quickstart's remote sample URL when checking local handling.

**Hardware and downloads:** the checkpoint example uses `cuda:0`, bfloat16 and FlashAttention2. The package README permits a downloaded local directory in place of a model ID and recommends compatible hardware for FlashAttention2. Supporting snippet: “**as a local directory path you downloaded**”. That supports a local loading route, not a tested minimum GPU/VRAM figure. We have not qualified CPU performance or Windows installation. [Official README](https://github.com/QwenLM/Qwen3-TTS), manual model downloads, environment setup and Python package usage sections.

**Date/version limit:** live `main` and checkpoint card, not a pinned release. Record package/model revisions before a real trial. A 0.6B parameter count does not establish memory use, quality or cost on the user's computer.

## 2. Chatterbox-Turbo: an English cloning starting point

**High confidence in documented task and entry point.** **`ResembleAI/chatterbox-turbo`** is a specific 350M-parameter English TTS checkpoint. Its [official card](https://huggingface.co/ResembleAI/chatterbox-turbo) identifies English and shows generation with a reference recording. The card's metadata states “`license: mit`”. This is text plus a reference voice to new speech, rather than proof that the narration loop performs voice conversion on an existing sung/acted recording.

**Starting action:** follow the [official installation and Turbo example](https://github.com/resemble-ai/chatterbox#usage): install `chatterbox-tts` in an isolated environment, load `ChatterboxTurboTTS`, generate one paragraph with a permitted local reference clip and save its WAV. The example uses CUDA and a filename suggesting a10-second reference. The code enforces a reference longer than5seconds; the filename alone is not a universal recording requirement.

**License distinction:** the [repository LICENSE](https://github.com/resemble-ai/chatterbox/blob/master/LICENSE) says “**MIT License**”; the selected [checkpoint card metadata](https://huggingface.co/ResembleAI/chatterbox-turbo/raw/main/README.md) separately labels the weights MIT. Confirm dependencies and input/output rights for the actual application. This is not a license verdict for every Chatterbox-family checkpoint.

**Hardware/platform limit:** the upstream README says development/testing used Python3.11 on Debian11; its Turbo example selects CUDA. No minimum memory, Windows support or speed is established here. The current repository also contains Nano and multilingual variants; this two-candidate shortlist is not exhaustive and does not declare Turbo the newest or best model for every job. [Official repository](https://github.com/resemble-ai/chatterbox).

**Local loader evidence:** [Turbo source](https://github.com/resemble-ai/chatterbox/blob/master/src/chatterbox/tts_turbo.py) defines `from_local` and `from_pretrained`. Supporting snippets: “`def from_local(cls, ckpt_dir, device, nano=False)`” and “`snapshot_download(**download_kwargs)`”. The pretrained route obtains model files from Hugging Face; the local loader uses files/tokenizer from the checkpoint directory. Prefetch required artifacts before an offline trial. Inspect the complete runtime rather than treating these methods as a privacy guarantee. Current `master` source is unpinned.

## Fit, complexity and cost — reasoned guidance

| Choice | Useful first trial | Complexity | Cost to include |
|---|---|---|---|
| Qwen3-TTS0.6B Base | Reference-voice narration in English or one of its other documented languages | Python/runtime, model/tokenizer downloads, device configuration, paragraph files and quality checks | Local hardware/compute, electricity, storage and setup/maintenance time |
| Chatterbox-Turbo | English reference-voice narration using the official simple example | Python/runtime, checkpoint download, device configuration, paragraph files and quality checks | The same categories; parameter count does not prove a cheaper accepted result |

When running downloaded weights directly on the user's own hardware, there is no hosted TTS-provider per-request bill for that execution path. That is an architectural inference, not a measured zero-cost claim: rented compute, downloads, tooling and retries can still cost money and time. Hugging Face Spaces, hosted inference providers and vendor API products are different routes and can send audio off the machine.

For the first local comparison, use the same permitted reference, same short script and a paragraph containing a name/number. Save output, listen, revise one sentence and record correctness, setup effort, generation time and resource use. Then test joining/timing on the accepted audio. This trial sequence is our proposed experiment, not an observed model ranking. Local handling can be a hard constraint; it is not a reason to claim either checkpoint already meets an end-to-end privacy requirement.

## What belongs in collapsed callouts

Keep the named local route, language fit, setup/cost categories and first action visible in the option comparison. Put package/device details, license links, model-family distinctions and download/offline notes in a **Local model setup** callout. Keep any constraint that rules out a choice visible before the reader commits. No blanket GPU budget, legal clearance, quality winner or private/offline certification is supported by this research.
