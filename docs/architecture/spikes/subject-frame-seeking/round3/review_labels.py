"""Record visual corrections to reference proposals before selector execution."""

import copy
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
proposal = ROOT / "reference-proposals.json"
data = json.loads(
    proposal.read_text()
    if proposal.exists()
    else gzip.decompress((ROOT / "reference-proposals.json.gz").read_bytes()).decode()
)
for kind, case in data.items():
    original = copy.deepcopy(case["frames"])
    for frame in case["frames"]:
        t = frame["pts_s"]
        if kind == "scroll":
            frame["hits"], frame["unknown"] = [], []
            if t >= 942.06666:
                box = (
                    [44, 548, 178, 570]
                    if t < 942.43333
                    else [44, 486, 178, 510]
                    if 942.6 <= t < 945.4
                    else [44, 218, 178, 244]
                    if t >= 945.53333
                    else None
                )
                frame["hits"].append(dict(state=0, box=box))
            if t >= 945.13333:
                box = (
                    [44, 548, 191, 570]
                    if t < 945.4
                    else [44, 281, 191, 305]
                    if t >= 945.53333
                    else None
                )
                frame["hits"].append(dict(state=1, box=box))
            if t >= 945.53333:
                frame["hits"].append(dict(state=2, box=[44, 300, 865, 490]))
        elif kind == "brief":
            frame["hits"], frame["unknown"] = [], []
            if t <= 577.0:
                frame["hits"].append(dict(state=0, box=[334, 500, 388, 510]))
            elif t >= 578.0:
                frame["hits"].append(dict(state=0, box=[346, 531, 400, 542]))
            elif t >= 577.76666:
                frame["unknown"] = [0]
        elif kind == "motion" and 480.83333 <= t < 481.93333:
            frame["hits"], frame["unknown"] = [], []
        elif kind == "occlusion" and t < 483.96666 and frame["unknown"]:
            # Clear text inspected, but proposal missed its extent. Leave geometry unknown.
            frame["hits"] = [dict(state=0, box=None)]
            frame["unknown"] = []
        frame.pop("annotation_lines")
        frame["sha256"] = hashlib.sha256(
            (
                Path(".scratch")
                / next(
                    c["folder"]
                    for c in json.loads((ROOT / "protocol.json").read_text())["cases"]
                    if c["id"] == kind
                )
                / frame["filename"]
            ).read_bytes()
        ).hexdigest()
    print(
        kind,
        "frames",
        len(case["frames"]),
        "uncertain_visibility",
        sum(bool(f["unknown"]) for f in case["frames"]),
        "uncertain_geometry",
        sum(any(h["box"] is None for h in f["hits"]) for f in case["frames"]),
    )
(ROOT / "reference.json").write_text(json.dumps(data, indent=2) + "\n")
(ROOT / "annotation-review.json").write_text(
    json.dumps(
        dict(
            reviewer="same agent; no independent human check",
            provenance="PSM11 full-frame reference proposals plus exhaustive frame contact inspection; no candidate outputs consumed",
            corrections=[
                "terminal command completion at942.066667 and945.133333; post-add status at945.533333",
                "manual terminal line extents on stable plateaus; scrolling-transition geometry retained as unknown",
                "browser absent480.833333–481.933333 during UAC/desktop switch",
                "menu text inspected manually despite failed small-font reference OCR",
                "Community label visible until483.933333; overlay transition uncertain; navigation label is not an established essential step",
            ],
            uncertainty="Unknown visibility/extent propagates to score intervals; it is not counted as a confident miss",
        ),
        indent=2,
    )
    + "\n"
)
