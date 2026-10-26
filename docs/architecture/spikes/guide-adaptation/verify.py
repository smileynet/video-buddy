"""Independently inspect persisted fixture files and frozen-input provenance."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


protocol = json.loads((HERE / "protocol.json").read_text())
results = json.loads((HERE / "results.json").read_text())
packet = json.loads((HERE / "source-packet.json").read_text())
assert results["protocol_sha256"] == sha(HERE / "protocol.json")
assert packet["frame_sha256"] == sha(HERE / packet["frame"])
for name, digest in protocol["guide_hashes"].items():
    assert sha(HERE / name) == digest
assert not subprocess.check_output(
    [
        "git",
        "diff",
        "b442b1b",
        "--",
        str(HERE / "protocol.json"),
        str(HERE / "source-packet.json"),
        *[str(HERE / n) for n in protocol["guide_hashes"]],
    ]
)
restore_names = [
    "adapted.ps1",
    "guide-a-source-faithful.md",
    "guide-b-two-layer.md",
    "protocol.json",
    "source-packet.json",
]
with tempfile.TemporaryDirectory(prefix="vb-guide-input-restore-") as target:
    with zipfile.ZipFile(HERE / "frozen-inputs.zip") as archive:
        assert set(archive.namelist()) == set(restore_names)
        for name in restore_names:
            restored = Path(target) / name
            restored.write_bytes(archive.read(name))
            assert sha(restored) == sha(HERE / name)

run = Path(results["run_root"]).resolve()
assert run.is_relative_to(Path(".scratch/guide-adaptation").resolve())
assert len(results["records"]) == 8
assert results["parent_path_unchanged"] is True
assert results["profiles"]["host"]["touch_available"] is True
assert results["profiles"]["native"]["touch_available"] is False
guide_a = (HERE / "guide-a-source-faithful.md").read_text()
guide_b = (HERE / "guide-b-two-layer.md").read_text()
for guide in [guide_a, guide_b]:
    assert re.search(r"```bash\n(.*?)```", guide, re.S).group(1).strip() == "\n".join(
        protocol["source_commands"]
    )
adapted = "\n".join((HERE / "adapted.ps1").read_text().splitlines()[1:]).strip()
assert re.search(r"```powershell\n(.*?)```", guide_b, re.S).group(1).strip() == adapted
assert all(
    value in guide_b
    for value in [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "new-item?view=powershell-7.5",
        "test-path?view=powershell-7.5",
        "about_commonparameters?view=powershell-7.5",
    ]
)
canary = protocol["canary"].encode()
checks = []
for row in results["records"]:
    name = row["case"]["id"]
    directory = run / name
    assert directory.resolve().is_relative_to(run)
    actual = {p.relative_to(directory).as_posix(): p for p in directory.rglob("*")}
    assert set(actual) == {p["path"] for p in row["after"]}
    for entry in row["after"]:
        path = actual[entry["path"]]
        if entry["kind"] == "file":
            assert (
                path.is_file()
                and sha(path) == entry["sha256"]
                and path.stat().st_size == entry["bytes"]
            )
        else:
            assert path.is_dir()
    if name == "source_powershell_native_fresh":
        assert not actual and row["stderr"]
        verdict = f"blocked with exit{row['returncode']}; no false task success"
    elif name == "force_negative_control":
        assert (directory / "index.html").read_bytes() == b"" and not (
            directory / "app.js"
        ).exists()
        verdict = "owned canary erased; negative control not recommended"
    elif name == "adapted_directory_conflict":
        assert (directory / "index.html/keep.txt").read_bytes() == canary
        assert not (directory / "app.js").exists() and row["returncode"] != 0
        verdict = "blocked explicitly; sentinel preserved"
    elif row["case"]["seed"] == "existing":
        assert (directory / "index.html").read_bytes() == canary
        assert (directory / "app.js").read_bytes() == b""
        previous = next(
            p["mtime_ns"] for p in row["before"] if p["path"] == "index.html"
        )
        expected_changed = row["case"]["shell"] == "bash"
        assert (
            (directory / "index.html").stat().st_mtime_ns != previous
        ) == expected_changed
        verdict = "contents preserved; declared timestamp behavior verified"
    else:
        assert set(actual) == set(protocol["fixed_names"])
        assert all(
            (directory / n).is_file() and (directory / n).read_bytes() == b""
            for n in protocol["fixed_names"]
        )
        verdict = "fresh placeholders verified"
    checks.append({"case": name, "verified": True, "observation": verdict})
output = {
    "date": "2026-10-26",
    "frozen_inputs": "b442b1b",
    "frozen_guide_and_source_hashes_verified": True,
    "persisted_files_independently_rechecked": True,
    "case_checks": checks,
    "all_checks_passed": True,
    "human_reader_observed": False,
    "frozen_text_files_restored": 5,
    "source_and_adapted_blocks_match": True,
    "adaptation_labels_and_support_links_present": True,
    "limits": "Checks establish these fixture postconditions only, not universal translation or usability.",
}
(HERE / "verification.json").write_text(json.dumps(output, indent=2) + "\n")
print(
    "PASS:8 persisted fixture checks,source/guide hashes,declared profiles,negative controls; no human usability claim"
)
