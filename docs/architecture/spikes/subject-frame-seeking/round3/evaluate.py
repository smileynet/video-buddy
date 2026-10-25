"""Use frozen candidate; score fresh labels with explicit uncertainty bounds."""

import hashlib
import json
from pathlib import Path

from candidate_frozen import select

ROOT = Path(__file__).resolve().parent
protocol = json.loads((ROOT / "protocol.json").read_text())
assert (
    hashlib.sha256(
        (ROOT / "candidate_frozen.py").read_text().rstrip("\n").encode()
    ).hexdigest()
    == protocol["candidate_source_sha256"]
)
reference = json.loads((ROOT / "reference.json").read_text())
observations = json.loads((ROOT / "observations.json").read_text())
audit = json.loads((ROOT / "grid-audit.json").read_text())


def measure(kind, chosen):
    lower, upper, exact = set(), set(), set()
    duplicates = incomplete = irrelevant = 0
    evidence = []
    for row in chosen:
        frame = reference[kind]["frames"][row["index"]]
        box = row["box"]
        full = box == [0, 0, 1280, 720]
        hits, possible = [], list(frame["unknown"])
        for hit in frame["hits"]:
            extent = hit["box"]
            if (
                full
                or extent is not None
                and box[0] <= extent[0]
                and box[1] <= extent[1]
                and box[2] >= extent[2]
                and box[3] >= extent[3]
            ):
                hits.append(hit["state"])
            elif extent is None:
                possible.append(hit["state"])
            else:
                incomplete += 1
        duplicates += sum(state in lower for state in hits)
        lower.update(hits)
        upper.update([*hits, *possible])
        irrelevant += not hits and not possible
        if not full:
            text = row["text"].removeprefix("$ ") if kind == "scroll" else row["text"]
            exact.update(
                state
                for state in hits
                if text
                == next(
                    c["states"][state] for c in protocol["cases"] if c["id"] == kind
                )
            )
        evidence.append(
            dict(
                index=row["index"],
                pts_s=frame["pts_s"],
                box=box,
                text=row["text"],
                hits=hits,
                possible=possible,
            )
        )
    return dict(
        covered_min=sorted(lower),
        covered_max=sorted(upper),
        exact=None
        if chosen and chosen[0]["box"] == [0, 0, 1280, 720]
        else sorted(exact),
        selected=len(chosen),
        redundant=duplicates,
        incomplete_regions=incomplete,
        without_target=irrelevant,
        evidence=evidence,
    )


results = {}
for case in protocol["cases"]:
    kind = case["id"]
    rows = observations[kind]
    ref = reference[kind]
    cap = ref["capture"]
    times = [r["pts_s"] for r in rows]
    result = dict(
        total_states=len(case["states"]),
        frames=len(rows),
        budgets={},
        costs=dict(
            decode_write_s=cap["decode_write_s"],
            template_s=sum(r["tracking_s"] for r in rows),
            ocr_s=sum(
                r["observations"].get("tracked", {}).get("ocr_s", 0) for r in rows
            ),
            accepted_matches=sum(bool(r["observations"]) for r in rows),
        ),
    )
    for budget in protocol["budgets"]:
        candidate = measure(kind, select(rows, "tracked", budget, events=True))
        grids = []
        for phase in protocol["offsets"]:
            requested = [
                cap["start"] + (i + phase) * (cap["end"] - cap["start"]) / budget
                for i in range(budget)
            ]
            chosen = []
            for t in requested:
                check = audit[kind][f"{t:.9f}"]
                index = check["expected_index"]
                if check["expected_error"] != 0:
                    matches = [
                        r["index"]
                        for r in check["neighboring_matches"]
                        if r["error"] == 0
                    ]
                    assert matches, "Actual seek did not match the decoded neighborhood"
                    index = min(matches, key=lambda i: abs(i - check["expected_index"]))
                chosen.append(dict(index=index, box=[0, 0, 1280, 720], text=""))
            grids.append(
                dict(offset=phase, requested=requested, **measure(kind, chosen))
            )
        result["budgets"][str(budget)] = dict(candidate=candidate, grid=grids)
    results[kind] = result
(ROOT / "results.json").write_text(json.dumps(results, indent=2) + "\n")
for kind, result in results.items():
    print(kind, result["costs"])
    for b, cell in result["budgets"].items():
        print(
            b,
            "grid",
            [(len(g["covered_min"]), len(g["covered_max"])) for g in cell["grid"]],
            "candidate",
            len(cell["candidate"]["covered_min"]),
            len(cell["candidate"]["covered_max"]),
        )
