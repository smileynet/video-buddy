"""THROWAWAY ticket 25 capture CLI. No sampling, ranking or OCR at capture."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import time

from .capture import _ffmpeg_bin, download_video


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("start", type=float)
    parser.add_argument("end", type=float)
    parser.add_argument("--download-source", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    if args.download_source:
        args.source = download_video(
            f"https://www.youtube.com/watch?v={args.source}",
            args.output.parent / "seek-retained-source",
        )
    started = time.perf_counter()
    result = subprocess.run(
        [
            _ffmpeg_bin(),
            "-hide_banner",
            "-copyts",
            "-ss",
            str(args.start),
            "-i",
            str(args.source),
            "-vf",
            f"trim=start={args.start}:end={args.end},showinfo",
            "-an",
            "-fps_mode",
            "passthrough",
            "-q:v",
            "2",
            str(args.output / "decoded_%06d.jpg"),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    elapsed = time.perf_counter() - started
    times = [
        float(t) for t in re.findall(r"\bn:\s*\d+.*?pts_time:([\d.]+)", result.stderr)
    ]
    files = sorted(args.output.glob("decoded_*.jpg"))
    assert len(files) == len(times) and files
    frames = []
    for path, pts in zip(files, times, strict=True):
        name = f"frame_{round(pts * 1000):08d}.jpg"
        path.rename(args.output / name)
        frames.append({"filename": name, "pts_s": pts})
    payload = {
        "source": str(args.source),
        "start": args.start,
        "end": args.end,
        "decode_write_s": elapsed,
        "frames": frames,
    }
    (args.output / "capture.json").write_text(json.dumps(payload, indent=2))
    print(json.dumps({"frames": len(frames), "decode_write_s": elapsed}))


if __name__ == "__main__":
    main()
