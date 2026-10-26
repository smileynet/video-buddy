"""THROWAWAY: create independent controlled speech diagnostics before ASR."""

import hashlib
import json
from pathlib import Path
import subprocess
import time
import urllib.request
import wave

import numpy as np

HERE = Path(__file__).resolve().parent
MEDIA = Path(".scratch/speech-details")
MEDIA.mkdir(parents=True, exist_ok=True)
RATE = 16000


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_wave(path, values):
    with wave.open(str(path), "wb") as out:
        out.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        out.writeframes(np.asarray(values, dtype="<i2").tobytes())


groups = [
    (
        "development",
        "Microsoft David Desktop",
        [
            ("Run git status.", ["run git status"]),
        ],
    ),
    (
        "commands",
        "Microsoft Zira Desktop",
        [
            ("Run git status.", ["run git status"]),
            (
                "Then run git add index dot h t m l.",
                [
                    "then run git add index dot h t m l",
                    "then run git add index html",
                    "then run git add index h t m l",
                ],
            ),
            ("Finally run git status again.", ["finally run git status again"]),
        ],
    ),
    (
        "numbers",
        "Microsoft Zira Desktop",
        [
            (
                "Set the port to eight thousand and eighty.",
                [
                    "set the port to eight thousand and eighty",
                    "set the port to 8080",
                    "set the port to 8 080",
                ],
            ),
            (
                "Set the timeout to thirty seconds.",
                ["set the timeout to thirty seconds", "set the timeout to 30 seconds"],
            ),
            (
                "Use Python three point twelve.",
                ["use python three point twelve", "use python 3 12"],
            ),
            (
                "Do not set retries to zero.",
                ["do not set retries to zero", "do not set retries to 0"],
            ),
        ],
    ),
]
start = time.perf_counter()
fixtures = []
for name, voice, phrases in groups:
    combined = list(np.zeros(RATE // 2, dtype=np.int16))
    spans = []
    for index, (text, aliases) in enumerate(phrases):
        wav = (MEDIA / f"{name}-{index}.wav").resolve()
        # No shell interpolation: saved script and data are separate arguments.
        ps = MEDIA / "synthesize.ps1"
        ps.write_text(
            "param($Voice,$Output,$Text)\nAdd-Type -AssemblyName System.Speech\n$s = New-Object System.Speech.Synthesis.SpeechSynthesizer\n$s.SelectVoice($Voice)\n$s.Rate=0\n$s.SetOutputToWaveFile($Output)\n$s.Speak($Text)\n$s.Dispose()\n"
        )
        subprocess.run(
            ["powershell.exe", "-NoProfile", "-File", str(ps), voice, str(wav), text],
            check=True,
            capture_output=True,
        )
        pcm = MEDIA / f"{name}-{index}-16k.wav"
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-i",
                str(wav),
                "-ar",
                str(RATE),
                "-ac",
                "1",
                str(pcm),
            ],
            check=True,
        )
        with wave.open(str(pcm), "rb") as reader:
            values = np.frombuffer(reader.readframes(reader.getnframes()), dtype="<i2")
        active = np.flatnonzero(np.abs(values.astype(np.int32)) > 100)
        assert len(active)
        offset = len(combined) / RATE
        spans.append(
            {
                "text": text,
                "aliases": aliases,
                "start": offset + int(active[0]) / RATE,
                "end": offset + (int(active[-1]) + 1) / RATE,
                "timing_reference": "amplitude >100 of 32768; phrase envelope, not phonetic word boundaries",
            }
        )
        combined.extend(values)
        combined.extend(np.zeros(int(RATE * 0.8), dtype=np.int16))
    path = MEDIA / f"{name}.wav"
    write_wave(path, combined)
    fixtures.append(
        {
            "id": name,
            "kind": "synthetic-authored",
            "split": "development" if name == "development" else "validation",
            "path": path.as_posix(),
            "voice": voice,
            "sha256": digest(path),
            "duration": len(combined) / RATE,
            "text": " ".join(x[0] for x in phrases),
            "phrases": spans,
        }
    )
for name, values in [
    ("silence", np.zeros(RATE * 8)),
    (
        "tones",
        np.sin(
            2
            * np.pi
            * np.arange(RATE * 8)
            / RATE
            * (220 + 110 * (np.arange(RATE * 8) // (RATE // 2) % 5))
        )
        * 3000,
    ),
]:
    path = MEDIA / f"{name}.wav"
    write_wave(path, values)
    fixtures.append(
        {
            "id": name,
            "kind": "authored-negative",
            "split": "validation",
            "path": path.as_posix(),
            "sha256": digest(path),
            "duration": 8,
            "text": "",
            "phrases": [],
        }
    )
# Pin upstream source revision; do not infer a corpus WER reference from an ASR output.
with urllib.request.urlopen(
    "https://api.github.com/repos/openai/whisper/commits/main"
) as response:
    revision = json.load(response)["sha"]
url = f"https://raw.githubusercontent.com/openai/whisper/{revision}/tests/jfk.flac"
path = MEDIA / "jfk.flac"
urllib.request.urlretrieve(url, path)
test_url = f"https://raw.githubusercontent.com/openai/whisper/{revision}/tests/test_transcribe.py"
with urllib.request.urlopen(test_url) as response:
    test = response.read()
assert b"1.8" in test and b"Americans" in test
fixtures.append(
    {
        "id": "jfk",
        "kind": "natural-upstream-integration",
        "split": "validation",
        "path": path.as_posix(),
        "sha256": digest(path),
        "source": url,
        "test_source": test_url,
        "test_sha256": hashlib.sha256(test).hexdigest(),
        "text": None,
        "phrases": [],
        "target": {"word": "americans", "contains_time": 1.8},
        "limitation": "A known model test, likely contaminated/familiar; no independent tutorial command/number or WER reference.",
    }
)
(HERE / "references.json").write_text(
    json.dumps(
        {"preparation_seconds": time.perf_counter() - start, "fixtures": fixtures},
        indent=2,
    )
    + "\n"
)
print(
    json.dumps(
        {"fixtures": len(fixtures), "preparation_seconds": time.perf_counter() - start}
    )
)
