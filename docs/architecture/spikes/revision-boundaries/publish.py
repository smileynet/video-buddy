"""Compact evidence/retention manifest; large regenerable sheets stay ignored."""

import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import time

from PIL import Image, ImageDraw

from policies import packets, settled

ROOT = Path(__file__).resolve().parent
protocol = json.loads((ROOT / "protocol.json").read_text())
reference = json.loads((ROOT / "reference.json").read_text())
freeze = json.loads((ROOT / "selection-freeze.json").read_text())
guard = {}
for name, key in [
    ("policies.py", "policy_sha256"),
    ("collect.py", "collector_sha256"),
    ("reference.json", "reference_sha256"),
]:
    historical = (
        subprocess.run(
            [
                "git",
                "show",
                f"55aeb15:docs/architecture/spikes/revision-boundaries/{name}",
            ],
            capture_output=True,
            check=True,
        )
        .stdout.decode()
        .replace("\r\n", "\n")
    )
    assert (ROOT / name).read_text() == historical, name + " changed after freeze"
    guard[name] = dict(
        normalized_sha256=hashlib.sha256(historical.encode()).hexdigest(),
        working_matches_frozen_commit=True,
        original_run_byte_sha256=freeze[key],
    )
(ROOT / "validation-guard.json").write_text(json.dumps(guard, indent=2) + "\n")
summary, stages = {}, {}
for case in protocol["cases"]:
    cid = case["id"]
    data = json.loads((ROOT / (case["phase"] + "-results.json")).read_text())[cid]
    rows = json.loads(gzip.decompress((ROOT / f"{cid}-ocr.json.gz").read_bytes()))
    assert all("\t" not in line["text"] for row in rows for line in row["lines"])
    summary[cid] = dict(phase=case["phase"], total=data["total"], budgets={})
    for budget, cell in data["budgets"].items():
        summary[cid]["budgets"][budget] = {
            name: [len(cell[name]["covered_min"]), len(cell[name]["covered_max"])]
            for name in ["legacy", "settled", "packets"]
        }
        summary[cid]["budgets"][budget]["grid"] = [
            [len(g["covered_min"]), len(g["covered_max"])] for g in cell["grid"]
        ]
    timings = {}
    for method in ["settled", "packets"]:
        start = time.perf_counter()
        selected = (
            settled(rows, 4)
            if method == "settled"
            else packets(rows, 4, case["viewport"][3] - case["viewport"][1])
        )
        timings[method + "_cap4_s"] = time.perf_counter() - start
    stages[cid] = dict(
        ocr_s=data["ocr_s"],
        capture_s=reference[cid]["capture"]["decode_write_s"],
        selection=timings,
    )
    # Two selected examples per case, not exhaustive sheets in Git.
    chosen = (
        data["budgets"]["4"]["packets"]["evidence"][:1]
        + data["budgets"]["4"]["settled"]["evidence"][-1:]
    )
    sheet = Image.new("RGB", (1280, 390), "white")
    draw = ImageDraw.Draw(sheet)
    for i, e in enumerate(chosen):
        f = reference[cid]["frames"][e["index"]]
        im = Image.open(Path(".scratch") / case["folder"] / f["filename"])
        im.thumbnail((640, 360))
        sheet.paste(im, (i * 640, 30))
        draw.text(
            (i * 640, 5),
            f"{cid} {'packet' if i == 0 else 'settled'} {e['pts_s']:.6f}s  states={e['hits']}",
            fill="black",
        )
    sheet.save(ROOT / f"{cid}-selected.jpg")
(ROOT / "dashboard-data.json").write_text(json.dumps(summary, indent=2) + "\n")
(ROOT / "stage-costs.json").write_text(json.dumps(stages, indent=2) + "\n")
manifest = dict(
    repository="smileynet/video-buddy",
    scope="new revision-boundary evidence only; no history or prior artifact audit",
    roles=dict(
        source="Python scripts",
        frozen_reference="protocol.json / reference.json / label-notes.json / selection-freeze.json",
        generated_evidence="compressed OCR and comparison JSON, three small selected JPEGs",
        regenerable_local=".scratch source captures and exhaustive ref sheets",
    ),
    storage="ordinary Git for small scoped files; no LFS, uploads, untracking or history rewrite",
    source_recovery=dict(
        hashes=protocol["source_hashes"],
        retrieval="repo experimental capture CLI with --download-source; validate source SHA before replay",
        limits="exact source bytes retained locally; no independent remote backup verified; public URL may change",
    ),
    runtime=dict(
        python=platform.python_version(),
        packages={
            n: importlib.metadata.version(n)
            for n in ["Pillow", "opencv-python", "numpy", "psutil", "yt-dlp"]
        },
    ),
    retention="retain frozen evidence on spike branch through review28; local originals/sheets retained; no deletion authorized or performed",
)
(ROOT / "artifact-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
