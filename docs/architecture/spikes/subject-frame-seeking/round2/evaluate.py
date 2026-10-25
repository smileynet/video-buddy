"""Evaluate frozen selections only after collecting image-derived observations."""

from bisect import bisect_left
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--psm", type=int, default=13)
args = parser.parse_args()
config = json.loads((ROOT / "protocol.json").read_text())
truth = json.loads((ROOT / "truth.json").read_text())
observations = json.loads((ROOT / f"observations-psm{args.psm}.json").read_text())


def select(rows, mode, budget, events=False):
    groups = {}
    runs = []
    current = []
    previous = None
    for index, row in enumerate(rows):
        obs = row["observations"].get(mode)
        text = obs["text"] if obs else ""
        entry = dict(index=index, **obs) if obs and text else None
        if text != previous:
            if current:
                runs.append(current)
            current = []
        if entry:
            current.append(entry)
            groups.setdefault(text, []).append(entry)
        previous = text
    if current:
        runs.append(current)
    if events:
        groups = {}
        for run in runs:
            if len(run) >= 2:
                groups.setdefault(run[0]["text"], []).extend(run)
        ranked = sorted(groups.values(), key=lambda g: g[0]["index"])
    else:
        ranked = sorted(
            [g for g in groups.values() if len(g) >= 6], key=lambda g: -len(g)
        )
    chosen = [max(g, key=lambda r: r["sharpness"]) for g in ranked[:budget]]
    return sorted(chosen, key=lambda r: r["index"])


def measure(kind, selected):
    covered, exact = set(), set()
    duplicates = incomplete = absent = 0
    evidence = []
    for row in selected:
        target = truth[kind]["frames"][row["index"]]
        valid = target["visible"]
        box, wanted = row["box"], target["content_box"]
        complete = (
            box[0] <= wanted[0]
            and box[1] <= wanted[1]
            and box[2] >= wanted[2]
            and box[3] >= wanted[3]
        )
        # Require the actual text extent, not blank padding around the viewport.
        if valid and not complete:
            incomplete += 1
        if not valid:
            absent += 1
        hits = valid if complete else []
        duplicates += sum(state in covered for state in hits)
        covered.update(hits)
        exact.update(state for state in hits if row["text"] == config["texts"][state])
        evidence.append(
            dict(
                index=row["index"],
                pts_s=target["pts_s"],
                box=box,
                text=row["text"],
                hits=hits,
            )
        )
    return dict(
        covered=sorted(covered),
        recall=len(covered) / 3,
        exact=None
        if selected and all(r["box"] == [0, 0, 960, 540] for r in selected)
        else sorted(exact),
        selected=len(selected),
        redundant=duplicates,
        incomplete=incomplete,
        unreadable_or_occluded=absent,
        evidence=evidence,
    )


results = {}
for kind, rows in observations.items():
    result = {
        "budgets": {},
        "costs": dict(
            tracking_s=sum(row["tracking_s"] for row in rows),
            tracked_ocr_s=sum(
                row["observations"].get("tracked", {}).get("ocr_s", 0) for row in rows
            ),
            static_ocr_s=sum(row["observations"]["static"]["ocr_s"] for row in rows),
            tracking_misses=sum("tracked" not in row["observations"] for row in rows),
        ),
    }
    pts = [r["pts_s"] for r in rows]
    for budget in config["budgets"]:
        cell = {}
        for label, mode, events in [
            ("static_frequency", "static", False),
            ("tracked_frequency", "tracked", False),
            ("tracked_events", "tracked", True),
        ]:
            cell[label] = measure(kind, select(rows, mode, budget, events))
        grids = []
        for offset in config["grid_offsets"]:
            selected = []
            for i in range(budget):
                requested = (i + offset) * 6 / budget
                index = min(bisect_left(pts, requested), len(rows) - 1)
                target = truth[kind]["frames"][index]
                # Grid saves the whole image. OCR audit uses a truth crop separately;
                # it is not part of grid acquisition or selection.
                selected.append(dict(index=index, box=[0, 0, 960, 540], text=""))
            grids.append(dict(offset=offset, **measure(kind, selected)))
        cell["grid"] = grids
        result["budgets"][str(budget)] = cell
    results[kind] = result
(ROOT / f"results-psm{args.psm}.json").write_text(json.dumps(results, indent=2) + "\n")
for kind, result in results.items():
    print(kind, "costs", result["costs"])
    for budget, cell in result["budgets"].items():
        print(
            budget,
            "grid",
            [len(g["covered"]) for g in cell["grid"]],
            "static/frequency/events",
            [
                len(cell[m]["covered"])
                for m in ["static_frequency", "tracked_frequency", "tracked_events"]
            ],
        )
