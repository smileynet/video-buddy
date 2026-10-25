"""Fix single-line box order from preserved detections, without rerunning OCR."""

import json
from pathlib import Path
import re
import shutil


def distance(a, b):
    row = list(range(len(b) + 1))
    for i, char in enumerate(a):
        nxt = [i + 1]
        for j, other in enumerate(b):
            nxt.append(min(nxt[-1] + 1, row[j + 1] + 1, row[j] + (char != other)))
        row = nxt
    return row[-1]


root = Path(__file__).resolve().parent
cases = json.loads((root / "cases.json").read_text())
(root / "attempts").mkdir(exist_ok=True)
for path in root.glob("*-heldout.json"):
    backup = root / "attempts" / (path.stem + "-quantized-y.json")
    if not backup.exists():
        shutil.copy2(path, backup)
    data = json.loads(path.read_text())
    for frame in data["frames"]:
        for result in frame["regions"]:
            case = next(c for c in cases if c["id"] == result["id"])
            x0, y0, x1, y1 = case["box"]
            boxes = [
                b
                for b in frame["raw"]
                if x0 <= (b["box"][0] + b["box"][2]) / 2 <= x1
                and y0 <= (b["box"][1] + b["box"][3]) / 2 <= y1
            ]
            boxes.sort(key=lambda b: b["box"][0])
            text = re.sub(r"\s+", " ", " ".join(b["text"] for b in boxes)).strip()
            edits = distance(result["expected"], text)
            result.update(
                text=text,
                edits=edits,
                exact=text == result["expected"],
                cer=edits / len(result["expected"]),
                empty=not text,
            )
    data["association_rule"] = (
        "Single-line labeled ROIs: detected-box center inside ROI, then ascending x; quantized-y initial scoring preserved in attempts"
    )
    path.write_text(json.dumps(data, indent=2) + "\n")
