"""THROWAWAY: waveform-only ASR agreement, not a listening-quality judge."""

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import time
import wave

import numpy as np
import sherpa_onnx


def tokens(text):
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())


def distance(reference, hypothesis):
    previous = list(range(len(hypothesis) + 1))
    for i, word in enumerate(reference):
        row = [i + 1]
        for j, other in enumerate(hypothesis):
            row.append(
                min(row[-1] + 1, previous[j + 1] + 1, previous[j] + (word != other))
            )
        previous = row
    return previous[-1]


parser = argparse.ArgumentParser()
parser.add_argument("--audio", type=Path, required=True)
parser.add_argument("--model", type=Path, required=True)
parser.add_argument("--protocol", type=Path, required=True)
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
    model=str(args.model / "model.int8.onnx"),
    tokens=str(args.model / "tokens.txt"),
    num_threads=8,
    language="en",
    use_itn=False,
    provider="cpu",
)
records = []
for path in sorted(args.audio.glob("*.wav")):
    if not path.name.startswith(("qwen-", "chatterbox-")):
        continue
    with wave.open(str(path), "rb") as reader:
        assert reader.getnchannels() == 1 and reader.getsampwidth() == 2
        sr = reader.getframerate()
        pcm = reader.readframes(reader.getnframes())
    samples = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
    # Keep the conservative previous SenseVoice <30s condition explicit.
    assert len(samples) / sr < 30, (
        "Long output requires a declared segmentation protocol"
    )
    stream = recognizer.create_stream()
    stream.accept_waveform(sr, samples)
    started = time.perf_counter()
    recognizer.decode_stream(stream)
    records.append(
        {
            "file": path.name,
            "audio_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "pcm_sha256": hashlib.sha256(pcm).hexdigest(),
            "text": stream.result.text,
            "decode_s": time.perf_counter() - started,
        }
    )
# Expected words are used only after all waveform-only decoding, never as prompts.
protocol = json.loads(args.protocol.read_text(encoding="utf-8"))
for row in records:
    case = next(c for c in protocol["cases"] if row["file"].endswith(c["id"] + ".wav"))
    intended = protocol["texts"][case["text"]]
    a, b = tokens(intended), tokens(row["text"])
    row.update(
        intended=intended,
        reference_words=len(a),
        edits=distance(a, b),
        normalized_edit_rate=distance(a, b) / len(a),
        exact_normalized_agreement=a == b,
    )
result = {
    "reviewer": "SenseVoiceSmall int8 2024-07-17; waveform-only English, CPU8threads, greedy, no ITN",
    "runtime": importlib.metadata.version("sherpa-onnx"),
    "model_sha256": hashlib.sha256(
        (args.model / "model.int8.onnx").read_bytes()
    ).hexdigest(),
    "tokens_sha256": hashlib.sha256(
        (args.model / "tokens.txt").read_bytes()
    ).hexdigest(),
    "human_listening": False,
    "naturalness_or_speaker_similarity_judged": False,
    "limits": "Agreement with intended text is a machine diagnostic; ASR mistakes and TTS errors are not independently adjudicated. No voice preference, fidelity or accent quality inferred.",
    "records": records,
}
args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
for row in records:
    print(row["file"], row["edits"], "/", row["reference_words"], row["text"])
