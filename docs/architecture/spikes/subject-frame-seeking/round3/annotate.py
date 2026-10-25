"""OCR-assisted reference proposals, reviewed visually before candidate inference."""

import csv
import io
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
protocol = json.loads((ROOT / "protocol.json").read_text())
results = {}
for case in protocol["cases"]:
    folder = Path(".scratch") / case["folder"]
    cap = json.loads((folder / "capture.json").read_text())
    frames = []
    for frame in cap["frames"]:
        pts = frame["pts_s"]
        raw = subprocess.run(
            [
                "tesseract",
                str(folder / frame["filename"]),
                "stdout",
                "--psm",
                "11",
                "tsv",
            ],
            capture_output=True,
            check=True,
        ).stdout.decode("utf-8")
        lines = {}
        for word in csv.DictReader(io.StringIO(raw), delimiter="\t"):
            if word["text"].strip():
                key = tuple(word[k] for k in ["block_num", "par_num", "line_num"])
                x, y, w, h = [int(word[k]) for k in ["left", "top", "width", "height"]]
                lines.setdefault(key, []).append(
                    dict(text=word["text"], box=[x, y, x + w, y + h])
                )
        lines = [
            dict(
                text=" ".join(w["text"] for w in line),
                box=[
                    min(w["box"][0] for w in line),
                    min(w["box"][1] for w in line),
                    max(w["box"][2] for w in line),
                    max(w["box"][3] for w in line),
                ],
            )
            for line in lines.values()
        ]
        hits = []
        unknown = []
        expected = []
        if case["id"] == "scroll":
            if pts >= 942.0666:
                expected.append((0, "git add"))
            if pts >= 945.1333:
                expected.append((1, "git status"))
            if pts >= 945.5333:
                hits.append(dict(state=2, box=[44, 300, 865, 490]))
        elif case["id"] == "motion":
            # UAC/desktop transition removes the browser; other times are reviewed.
            if not 480.9 <= pts < 482.0:
                expected.append((0, "Downloading Git"))
        elif case["id"] == "occlusion":
            if pts < 483.9666:
                expected.append((0, "Community"))
            elif pts < 484.1:
                unknown.append(0)  # Partial transparency/overlap, not a clean label.
        elif case["id"] == "brief":
            if pts <= 577.0 or pts >= 578.0:
                expected.append((0, "Git Bash Here"))
            elif pts >= 577.7666:
                unknown.append(0)  # Menu fade-in.
        for state, phrase in expected:
            matches = [
                line for line in lines if phrase.casefold() in line["text"].casefold()
            ]
            if matches:
                # Latest terminal command is lowest; other subjects have one match.
                match = max(matches, key=lambda line: line["box"][1])
                hits.append(dict(state=state, box=match["box"]))
            else:
                unknown.append(state)
        frames.append(dict(**frame, hits=hits, unknown=unknown, annotation_lines=lines))
    results[case["id"]] = dict(capture=cap, frames=frames)
    (ROOT / "reference-proposals.json").write_text(json.dumps(results, indent=2) + "\n")
    print(
        case["id"],
        "frames",
        len(frames),
        "unresolved",
        sum(bool(f["unknown"]) for f in frames),
        flush=True,
    )
