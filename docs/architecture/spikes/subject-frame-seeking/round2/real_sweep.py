"""Offset/budget sweep on the earlier frozen real-window labels and OCR."""

from bisect import bisect_left
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
original = json.loads((ROOT.parent / "results.json").read_text(encoding="utf-8"))
config = json.loads((ROOT / "protocol.json").read_text())
results = {}
for case in original["cases"]:
    labels = case["case"]["states"]
    frames = case["capture"]["frames"]
    pts = [f["pts_s"] for f in frames]

    def score(times):
        hits = [
            [s["id"] for s in labels if any(a <= t < b for a, b in s["spans"])]
            for t in times
        ]
        covered = set(sum(hits, []))
        return dict(
            times=times,
            covered=sorted(covered),
            recall=len(covered) / len(labels),
            redundant=sum(bool(h) for h in hits) - len(covered),
            nonessential=sum(not h for h in hits),
        )

    groups = {}
    for row in case["rows"]:
        if row["text"]:
            groups.setdefault(row["text"], []).append(row)
    ranked = sorted([g for g in groups.values() if len(g) >= 6], key=lambda g: -len(g))
    cells = {}
    start, end = case["capture"]["start"], case["capture"]["end"]
    for budget in config["budgets"]:
        grids = []
        for offset in config["grid_offsets"]:
            requested = [
                start + (i + offset) * (end - start) / budget for i in range(budget)
            ]
            displayed = [pts[min(bisect_left(pts, t), len(pts) - 1)] for t in requested]
            grids.append(dict(offset=offset, requested=requested, **score(displayed)))
        chosen = [
            max(g, key=lambda r: r["sharpness"])["pts_s"] for g in ranked[:budget]
        ]
        cells[str(budget)] = dict(grid=grids, subject_frequency=score(sorted(chosen)))
    results[case["case"]["id"]] = dict(total_states=len(labels), budgets=cells)
(ROOT / "real-sweep.json").write_text(json.dumps(results, indent=2) + "\n")
for name, data in results.items():
    print(name)
    for budget, cell in data["budgets"].items():
        print(
            budget,
            [len(g["covered"]) for g in cell["grid"]],
            len(cell["subject_frequency"]["covered"]),
        )
