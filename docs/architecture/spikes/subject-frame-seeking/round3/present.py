"""Preserve every inspected crop and a compact dashboard snapshot."""

import gzip
import hashlib
import json
from pathlib import Path
import shutil

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
protocol = json.loads((ROOT / "protocol.json").read_text())
reference = json.loads((ROOT / "reference.json").read_text())
data = json.loads((ROOT / "results.json").read_text())
summary = {}
for case in protocol["cases"]:
    kind = case["id"]
    folder = Path(".scratch") / case["folder"]
    for part in folder.glob("inspect-*.jpg"):
        shutil.copy2(part, ROOT / f"{kind}-{part.name}")
    row = data[kind]
    summary[kind] = dict(total=row["total_states"], frames=row["frames"], budgets={})
    for budget, cell in row["budgets"].items():
        summary[kind]["budgets"][budget] = dict(
            grid=[[len(g["covered_min"]), len(g["covered_max"])] for g in cell["grid"]],
            candidate=[
                len(cell["candidate"]["covered_min"]),
                len(cell["candidate"]["covered_max"]),
            ],
        )
    sheet = Image.new("RGB", (1280, 440), "white")
    draw = ImageDraw.Draw(sheet)
    cell = row["budgets"]["4"]
    for j, (name, method) in enumerate(
        [("Grid, offset .5", cell["grid"][2]), ("Frozen candidate", cell["candidate"])]
    ):
        draw.text((10, j * 220), name + " " + str(method["covered_min"]), fill="black")
        for i, e in enumerate(method["evidence"]):
            f = reference[kind]["frames"][e["index"]]
            im = Image.open(folder / f["filename"]).convert("RGB")
            ImageDraw.Draw(im).rectangle(e["box"], outline="red", width=3)
            im.thumbnail((320, 180))
            sheet.paste(im, (i * 320, j * 220 + 32))
            draw.text((i * 320, j * 220 + 17), str(e["pts_s"]), fill="black")
    sheet.save(ROOT / f"{kind}-comparison.jpg")
source = Path(reference["scroll"]["capture"]["source"])
(ROOT / "source-manifest.json").write_text(
    json.dumps(
        dict(
            url=protocol["source"],
            title="Git & GitHub Crash Course For Beginners",
            creator="Traversy Media",
            sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            bytes=source.stat().st_size,
            window_frames=456,
            unique_source_frames=405,
            reference_freeze_commit="834036e",
            candidate_unchanged=True,
        ),
        indent=2,
    )
    + "\n"
)
(ROOT / "dashboard-data.json").write_text(json.dumps(summary, indent=2) + "\n")
if (ROOT / "reference-proposals.json").exists():
    with gzip.open(ROOT / "reference-proposals.json.gz", "wb") as f:
        f.write((ROOT / "reference-proposals.json").read_bytes())
