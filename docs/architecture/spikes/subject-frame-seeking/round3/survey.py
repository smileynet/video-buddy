"""Exploratory source survey through existing capture mechanics, not scored data."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

from video_buddy.frames.capture import capture_video_frames

parser = argparse.ArgumentParser()
parser.add_argument("source", type=Path)
parser.add_argument("folder", type=Path)
parser.add_argument("times", nargs="+", type=float)
args = parser.parse_args()
meta = capture_video_frames(
    args.source.stem,
    media_dir=args.folder,
    media_path=args.source,
    timestamps_s=args.times,
)
(args.folder / "survey.json").write_text(json.dumps(meta, indent=2) + "\n")
sheet = Image.new("RGB", (1280, ((len(meta["frames"]) + 3) // 4) * 205), "white")
d = ImageDraw.Draw(sheet)
for i, frame in enumerate(meta["frames"]):
    im = Image.open(args.folder / frame["filename"])
    im.thumbnail((320, 180))
    x, y = i % 4 * 320, i // 4 * 205
    sheet.paste(im, (x, y + 20))
    d.text((x, y), str(frame["timestamp_ms"] / 1000), fill="black")
sheet.save(args.folder / "survey.jpg")
