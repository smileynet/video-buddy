"""Author controlled clips; capture them through the existing experimental CLI."""

import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
WORK = Path(".scratch/seek-round2")
CONFIG = json.loads((ROOT / "protocol.json").read_text())
FONT = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 25)
SMALL = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 19)
WORK.mkdir(parents=True, exist_ok=True)
truth = {}
for kind in CONFIG["clips"]:
    output = WORK / kind
    output.mkdir(exist_ok=False)
    frames = []
    for i in range(120):
        t = i / 20
        state = 0 if t < 2 else 1 if t < 4 else 2
        if kind == "brief":
            state = 0 if t < 2.05 else 1 if t < 2.25 else 2
        x, y = 120, 140
        if kind == "motion":
            x = round(160 + 130 * math.sin(t * 1.4))
            y = round(150 + 100 * math.sin(t * 1.1))
        im = Image.new("RGB", (960, 540), "#17283c")
        draw = ImageDraw.Draw(im)
        draw.text((35, 25), "Other app: idle", font=SMALL, fill="#b8d3ed")
        panel = Image.new("RGB", (580, 155), "#eef4fa")
        d = ImageDraw.Draw(panel)
        d.rectangle((0, 0, 579, 33), fill="#245f98")
        d.text((15, 5), "Build console / task evidence", font=SMALL, fill="white")
        visible = []
        if kind == "scroll":
            scroll = (
                0
                if t < 1.7
                else (t - 1.7) / 0.3 * 70
                if t < 2
                else 70
                if t < 3.7
                else 70 + (t - 3.7) / 0.3 * 70
                if t < 4
                else 140
            )
            viewport = Image.new("RGB", (540, 52), "#eef4fa")
            vd = ImageDraw.Draw(viewport)
            for j, text in enumerate(CONFIG["texts"]):
                line_y = round(7 + j * 70 - scroll)
                vd.text((8, line_y), text, font=FONT, fill="#102030")
                box = vd.textbbox((8, line_y), text, font=FONT)
                if 0 <= box[1] and box[3] <= 52:
                    visible.append(j)
            panel.paste(viewport, (20, 55))
        else:
            d.text((28, 62), CONFIG["texts"][state], font=FONT, fill="#102030")
            visible = [state]
        obscured = kind == "occlusion" and 1.75 <= t < 3.75
        if obscured:
            d.rectangle((165, 50, 410, 112), fill="#8c9aaa")
            visible = []
        blurred = kind == "motion" and (1.9 <= t < 2.1 or 3.9 <= t < 4.1)
        if blurred:
            panel = panel.filter(ImageFilter.GaussianBlur(3))
            visible = []  # Explicit severe-blur exclusion; QA checks this assumption.
        im.paste(panel, (x, y))
        im.save(output / f"authored_{i:04d}.png")
        frames.append(
            dict(
                index=i,
                pts_s=t,
                visible=visible,
                subject_box=[x + 20, y + 55, x + 560, y + 107],
                header_box=[x, y, x + 580, y + 34],
                obscured=obscured,
                blurred=blurred,
            )
        )
    source = ROOT / f"{kind}.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-framerate",
            "20",
            "-i",
            str(output / "authored_%04d.png"),
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-y",
            str(source),
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            "-m",
            "video_buddy.frames.spike_seek",
            str(source),
            str(output / "decoded"),
            "0",
            "6",
        ],
        check=True,
    )
    capture = json.loads((output / "decoded/capture.json").read_text())
    assert len(capture["frames"]) == 120
    assert all(
        abs(a["pts_s"] - b["pts_s"]) < 0.00001
        for a, b in zip(frames, capture["frames"], strict=True)
    )
    truth[kind] = dict(
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        frames=frames,
        capture=capture,
    )
    # Every decoded subject crop, not a time-sampled inspection sheet.
    sheet = Image.new("RGB", (1080, 30 * 70), "white")
    sd = ImageDraw.Draw(sheet)
    for frame, captured in zip(frames, capture["frames"], strict=True):
        crop = Image.open(output / "decoded" / captured["filename"]).crop(
            frame["subject_box"]
        )
        crop.thumbnail((268, 45))
        j = frame["index"]
        px, py = j % 4 * 270, j // 4 * 70
        sheet.paste(crop, (px, py + 18))
        sd.text((px, py), f"{frame['pts_s']:.2f}  {frame['visible']}", fill="black")
    sheet.save(ROOT / f"{kind}-all-crops.jpg")
(ROOT / "truth.json").write_text(json.dumps(truth, indent=2) + "\n")
