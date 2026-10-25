from pathlib import Path
import json
import hashlib
import shutil
import subprocess
import platform

root = Path("docs/architecture/spikes/real-video-ocr")
home = Path.home()
paths = list((home / ".EasyOCR/model").glob("*.pth"))
for name in ["PP-OCRv5_mobile_det", "en_PP-OCRv5_mobile_rec"]:
    paths += [
        p
        for p in (home / ".paddlex/official_models" / name).glob("*")
        if p.is_file() and p.suffix in [".json", ".pdiparams", ".yml"]
    ]
tess = Path(shutil.which("tesseract"))
paths += list((tess.parent / "tessdata").glob("eng.traineddata"))
assets = [
    dict(
        asset=p.name,
        parent=p.parent.name,
        bytes=p.stat().st_size,
        sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
    )
    for p in paths
]
(root / "runtime-and-assets.json").write_text(
    json.dumps(
        dict(
            platform=platform.platform(),
            python=platform.python_version(),
            tesseract=str(tess),
            tesseract_version=subprocess.run(
                ["tesseract", "--version"], capture_output=True, text=True
            ).stdout,
            assets=assets,
        ),
        indent=2,
    )
    + "\n"
)
summary = {}
for path in root.glob("*-heldout.json"):
    d = json.loads(path.read_text())
    engine = d["engine"]
    summary[engine] = {}
    for mode, rows in [
        ("crop", d["cases"]),
        ("full_frame", [r for f in d["frames"] for r in f["regions"]]),
    ]:
        summary[engine][mode] = {
            "regions": len(rows),
            "exact": sum(x["exact"] for x in rows),
            "edits": sum(x["edits"] for x in rows),
            "characters": sum(len(x["expected"]) for x in rows),
            "micro_cer": sum(x["edits"] for x in rows)
            / sum(len(x["expected"]) for x in rows),
            "empty": sum(x["empty"] for x in rows),
            "ocr_seconds": sum(x["ocr_seconds"] for x in rows)
            if mode == "crop"
            else sum(x["ocr_seconds"] for x in d["frames"]),
        }
    summary[engine]["load_seconds"] = d["load_seconds"]
    summary[engine]["selected"] = json.loads(
        (root / f"{engine}-selection.json").read_text()
    )["selected"]
    summary[engine]["peak_cuda_allocated_bytes"] = d.get("peak_cuda_allocated_bytes")
(root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
