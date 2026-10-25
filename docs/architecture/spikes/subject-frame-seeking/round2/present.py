"""Publish exact comparison data and selected-frame contact sheets, no new scoring."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
config = json.loads((ROOT / "protocol.json").read_text())
data = json.loads((ROOT / "results-psm7.json").read_text())
truth = json.loads((ROOT / "truth.json").read_text())
real = json.loads((ROOT / "real-sweep.json").read_text())
summary = {}
for kind, result in data.items():
    cells = {}
    for budget, cell in result["budgets"].items():
        cells[budget] = dict(
            grid=[len(g["covered"]) for g in cell["grid"]],
            original=len(
                json.loads((ROOT / "results-psm13.json").read_text())[kind]["budgets"][
                    budget
                ]["tracked_frequency"]["covered"]
            ),
            static=len(cell["static_frequency"]["covered"]),
            tracked_frequency=len(cell["tracked_frequency"]["covered"]),
            events=len(cell["tracked_events"]["covered"]),
        )
    summary[kind] = dict(total=3, fidelity="Controlled; PSM7 diagnostic", budgets=cells)
    # All chosen full frames at budget3, including failed static crops.
    sheet = Image.new("RGB", (960, 4 * 215), "white")
    draw = ImageDraw.Draw(sheet)
    cell = result["budgets"]["3"]
    methods = [
        cell["grid"][2],
        cell["static_frequency"],
        cell["tracked_frequency"],
        cell["tracked_events"],
    ]
    names = [
        "Grid / phase .5",
        "Static / frequency",
        "Tracked / frequency",
        "Tracked / events",
    ]
    for j, (name, method) in enumerate(zip(names, methods, strict=True)):
        draw.text((8, j * 215), name + "  " + str(method["covered"]), fill="black")
        for i, evidence in enumerate(method["evidence"]):
            frame = truth[kind]["capture"]["frames"][evidence["index"]]
            im = Image.open(
                Path(".scratch/seek-round2") / kind / "decoded" / frame["filename"]
            ).convert("RGB")
            ImageDraw.Draw(im).rectangle(evidence["box"], outline="red", width=3)
            im.thumbnail((320, 180))
            sheet.paste(im, (i * 320, j * 215 + 30))
            draw.text(
                (i * 320, j * 215 + 17), str(evidence["pts_s"]) + "s", fill="black"
            )
    sheet.save(ROOT / f"{kind}-selection-comparison.jpg")
for name, result in real.items():
    cells = {
        b: dict(
            grid=[len(g["covered"]) for g in c["grid"]],
            original=len(c["subject_frequency"]["covered"]),
            static=None,
            tracked_frequency=None,
            events=None,
        )
        for b, c in result["budgets"].items()
    }
    summary[name] = dict(
        total=result["total_states"],
        fidelity="Real; earlier frozen PSM13",
        budgets=cells,
    )
(ROOT / "dashboard-data.json").write_text(json.dumps(summary, indent=2) + "\n")
