"""Shared matched-budget scorer; selector modules consume no references."""

import argparse
from bisect import bisect_left
import gzip
import importlib.util
import json
from pathlib import Path
import re

from policies import packets, settled

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("phase", choices=["development", "validation"])
args = parser.parse_args()
protocol = json.loads((ROOT / "protocol.json").read_text())
reference = json.loads((ROOT / "reference.json").read_text())
oldroot = ROOT.parent / "subject-frame-seeking/round3"
spec = importlib.util.spec_from_file_location("frozen", oldroot / "candidate_frozen.py")
frozen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frozen)
legacy = (
    {"dev": json.loads((oldroot / "observations.json").read_text())["scroll"]}
    if args.phase == "development"
    else json.loads(gzip.decompress((ROOT / "legacy-validation.json.gz").read_bytes()))
)
audit = (
    json.loads((ROOT / "grid-audit.json").read_text())
    if (ROOT / "grid-audit.json").exists()
    else {}
)


def measure(ref, rows, selected):
    covered, possible, exact = set(), set(), set()
    duplicate = prefix_only = 0
    evidence = []
    for selection in selected:
        i = selection["index"]
        frame = ref["frames"][i]
        duplicate += sum(h in covered for h in frame["hits"])
        covered.update(frame["hits"])
        possible.update([*frame["hits"], *frame["unknown"]])
        literals = [
            re.sub(r"^\$\s*", "", line["text"].strip()) for line in rows[i]["lines"]
        ]
        exact.update(
            s["id"]
            for s in ref["states"]
            if s["id"] in frame["hits"]
            and s["text"] is not None
            and s["text"] in literals
        )
        is_prefix = (
            not frame["hits"]
            and not frame["unknown"]
            and (
                940.5 <= frame["pts_s"] < 942.06666
                if ref["phase"] == "development"
                else False
            )
        )
        prefix_only += is_prefix
        evidence.append(
            dict(
                **selection,
                pts_s=frame["pts_s"],
                hits=frame["hits"],
                unknown=frame["unknown"],
            )
        )
    return dict(
        covered_min=sorted(covered),
        covered_max=sorted(possible),
        exact_literals=sorted(exact),
        selected=len(selected),
        redundant=duplicate,
        prefix_only=prefix_only if ref["phase"] == "development" else None,
        missed=[s["id"] for s in ref["states"] if s["id"] not in possible],
        evidence=evidence,
    )


result = {}
for case in protocol["cases"]:
    if case["phase"] != args.phase:
        continue
    cid = case["id"]
    ref = reference[cid]
    rows = json.loads(gzip.decompress((ROOT / f"{cid}-ocr.json.gz").read_bytes()))
    cells = {}
    times = [r["pts_s"] for r in rows]
    start, end = ref["capture"]["start"], ref["capture"]["end"]
    for budget in protocol["budgets"]:
        old = frozen.select(legacy[cid], "tracked", budget, events=True)
        choices = dict(
            legacy=[
                dict(index=c["index"], reason="old event time, full-frame context")
                for c in old
            ],
            settled=settled(rows, budget),
            packets=packets(rows, budget, case["viewport"][3] - case["viewport"][1]),
        )
        cell = {
            name: measure(ref, rows, selected) for name, selected in choices.items()
        }
        grids = []
        for phase in protocol["offsets"]:
            selected = []
            for i in range(budget):
                request = start + (i + phase) * (end - start) / budget
                index = min(bisect_left(times, request), len(times) - 1)
                if cid in audit:
                    a = audit[cid][f"{request:.9f}"]
                    index = a["verified_index"]
                selected.append(dict(index=index, reason="grid", requested=request))
            metric = measure(ref, rows, selected)
            # These are only common OCR audits; the grid itself performs no OCR.
            grids.append(dict(offset=phase, **metric))
        cell["grid"] = grids
        cells[str(budget)] = cell
    result[cid] = dict(
        phase=args.phase,
        total=len(ref["states"]),
        budgets=cells,
        ocr_s=sum(r["ocr_s"] for r in rows),
        frames=len(rows),
    )
(ROOT / f"{args.phase}-results.json").write_text(json.dumps(result, indent=2) + "\n")
for cid, data in result.items():
    print(cid)
    for budget, c in data["budgets"].items():
        print(
            budget,
            {k: len(c[k]["covered_min"]) for k in ["legacy", "settled", "packets"]},
            "grid",
            [len(g["covered_min"]) for g in c["grid"]],
        )
