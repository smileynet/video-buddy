"""Coarse target-box containment only; not a held-out GUI accuracy estimate."""

import json
from pathlib import Path
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent
summary = {
    "limits": "One known screenshot, corrected prompts after invalid reference pass, different precision/processing budgets. Success requires one point inside intended coarse box; no actions executed."
}
for filename in ["qwen-scoped-gui.json", "molmopoint-gui.json"]:
    data = json.loads((root / filename).read_text())
    rows = []
    for row in data["observations"]:
        if filename.startswith("qwen"):
            points = []
            try:
                attrs = ET.fromstring(row["output"]).attrib
                for i in range(1, 10):
                    if f"x{i}" in attrs and f"y{i}" in attrs:
                        points.append(
                            [
                                float(attrs[f"x{i}"]) * 3240 / 1000,
                                float(attrs[f"y{i}"]) * 2160 / 1000,
                            ]
                        )
            except ET.ParseError:
                pass
        else:
            points = [[p[2], p[3]] for p in row["points"] if p[1] == 0]
        box = row["reference_box"]
        hit = (
            len(points) == 1
            and box[0] <= points[0][0] <= box[2]
            and box[1] <= points[0][1] <= box[3]
        )
        rows.append(
            {
                "target": row["target"],
                "pixel_points": points,
                "reference_box": box,
                "single_point_inside": hit,
            }
        )
    summary[filename] = {
        "hits": sum(r["single_point_inside"] for r in rows),
        "n": len(rows),
        "rows": rows,
    }
(root / "scoped-gui-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(
    json.dumps(
        {
            k: {a: b for a, b in v.items() if a != "rows"} if isinstance(v, dict) else v
            for k, v in summary.items()
        },
        indent=2,
    )
)
