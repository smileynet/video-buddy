"""THROWAWAY: execute frozen guide steps in disposable shell profiles."""

import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import time
import uuid

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    rows = []
    for path in sorted(root.rglob("*")):
        row = {
            "path": path.relative_to(root).as_posix(),
            "kind": "file" if path.is_file() else "directory",
            "mtime_ns": path.stat().st_mtime_ns,
        }
        if path.is_file():
            row.update({"bytes": path.stat().st_size, "sha256": sha(path)})
        rows.append(row)
    return rows


def main():
    assert platform.system() == "Windows", (
        "Frozen target is Windows PowerShell, not a portable platform benchmark"
    )
    protocol = json.loads((HERE / "protocol.json").read_text())
    for name, digest in protocol["guide_hashes"].items():
        assert sha(HERE / name) == digest, f"Frozen guide changed: {name}"
    assert sha(HERE / "source-packet.json") == protocol["source_packet_sha256"]
    pwsh = Path(shutil.which("pwsh"))
    git = Path(shutil.which("git"))
    bash = git.parent.parent / "usr/bin/bash.exe"
    touch = git.parent.parent / "usr/bin/touch.exe"
    assert all(p.is_file() for p in [pwsh, git, bash, touch])
    base = Path(".scratch/guide-adaptation").resolve()
    base.mkdir(parents=True, exist_ok=True)
    run = base / ("run-" + uuid.uuid4().hex[:10])
    run.mkdir()
    assert run.resolve().is_relative_to(base)
    source_sh = run / "source.sh"
    source_ps = run / "source.ps1"
    source_sh.write_bytes(("\n".join(protocol["source_commands"]) + "\n").encode())
    source_ps.write_bytes(source_sh.read_bytes())
    force = run / "force.ps1"
    force.write_text(
        "New-Item -ItemType File -Path . -Name 'index.html' -Force -ErrorAction Stop | Out-Null\n"
    )
    probe = run / "probe.ps1"
    probe.write_text("""$cmd = Get-Command touch -ErrorAction SilentlyContinue
[pscustomobject]@{
    powershell = $PSVersionTable.PSVersion.ToString()
    touch_available = ($null -ne $cmd)
    touch_source = $(if ($cmd) { $cmd.Source } else { $null })
    new_item_available = ($null -ne (Get-Command New-Item -ErrorAction SilentlyContinue))
    test_path_available = ($null -ne (Get-Command Test-Path -ErrorAction SilentlyContinue))
} | ConvertTo-Json -Compress
""")
    host_env = os.environ.copy()
    native_env = host_env.copy()
    native_env["PATH"] = os.pathsep.join(
        str(p)
        for p in [pwsh.parent, git.parent, Path(os.environ["SystemRoot"]) / "System32"]
    )
    profiles = {}
    for name, env in [("host", host_env), ("native", native_env)]:
        result = subprocess.run(
            [
                str(pwsh),
                "-NoLogo",
                "-NoProfile",
                "-NonInteractive",
                "-File",
                str(probe),
            ],
            env=env,
            cwd=run,
            capture_output=True,
            text=True,
            check=True,
        )
        profiles[name] = json.loads(result.stdout)
    assert (
        profiles["host"]["touch_available"]
        and not profiles["native"]["touch_available"]
    )
    assert (
        profiles["native"]["new_item_available"]
        and profiles["native"]["test_path_available"]
    )
    canary = protocol["canary"].encode()
    canary_sha = hashlib.sha256(canary).hexdigest()
    records = []
    for case in protocol["cases"]:
        directory = run / case["id"]
        assert directory.resolve().is_relative_to(run)
        directory.mkdir()
        if case["seed"] == "existing":
            (directory / "index.html").write_bytes(canary)
            os.utime(
                directory / "index.html",
                (protocol["old_mtime_epoch"], protocol["old_mtime_epoch"]),
            )
        elif case["seed"] == "directory":
            (directory / "index.html").mkdir()
            (directory / "index.html/keep.txt").write_bytes(canary)
        before = snapshot(directory)
        env = native_env if case["profile"] == "native" else host_env
        script = (
            HERE / "adapted.ps1"
            if case["program"] == "adapted"
            else force
            if case["program"] == "force"
            else source_sh
            if case["shell"] == "bash"
            else source_ps
        )
        command = (
            [str(bash), "--noprofile", "--norc", str(script)]
            if case["shell"] == "bash"
            else [
                str(pwsh),
                "-NoLogo",
                "-NoProfile",
                "-NonInteractive",
                "-File",
                str(script),
            ]
        )
        start = time.perf_counter()
        result = subprocess.run(
            command, cwd=directory, env=env, capture_output=True, text=True
        )
        elapsed = time.perf_counter() - start
        after = snapshot(directory)
        state = {r["path"]: r for r in after}
        previous = {r["path"]: r for r in before}

        def empty_file(name):
            return (
                state.get(name, {}).get("kind") == "file" and state[name]["bytes"] == 0
            )

        if case["seed"] == "fresh" and case["id"] != "source_powershell_native_fresh":
            gates = {
                "two_empty_files": all(empty_file(n) for n in protocol["fixed_names"]),
                "no_extra_entries": set(state) == set(protocol["fixed_names"]),
                "exit_zero": result.returncode == 0,
            }
        elif case["id"] == "source_powershell_native_fresh":
            gates = {
                "touch_unavailable": not profiles["native"]["touch_available"],
                "no_requested_files": not state,
                "diagnostic_errors_present": bool(result.stderr),
            }
        elif case["id"] == "force_negative_control":
            gates = {
                "canary_truncated": empty_file("index.html")
                and state["index.html"]["sha256"] != canary_sha,
                "no_second_file": not (directory / "app.js").exists(),
            }
        elif case["seed"] == "existing":
            expected_update = case["shell"] == "bash"
            gates = {
                "canary_bytes_preserved": state["index.html"]["sha256"] == canary_sha,
                "missing_file_created": empty_file("app.js"),
                "timestamp_semantics": (
                    state["index.html"]["mtime_ns"]
                    != previous["index.html"]["mtime_ns"]
                )
                == expected_update,
                "exit_zero": result.returncode == 0,
            }
        else:
            gates = {
                "directory_preserved": state.get("index.html", {}).get("kind")
                == "directory",
                "sentinel_preserved": state.get("index.html/keep.txt", {}).get("sha256")
                == canary_sha,
                "no_false_second_file": not (directory / "app.js").exists(),
                "explicit_failure": result.returncode != 0
                and "not a file" in result.stderr,
            }
        row = {
            "case": case,
            "profile": profiles[case["profile"]],
            "before": before,
            "after": after,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "seconds": elapsed,
            "gates": gates,
            "expectations_matched": all(gates.values()),
        }
        records.append(row)
        print(
            json.dumps(
                {
                    "case": case["id"],
                    "returncode": result.returncode,
                    "seconds": elapsed,
                    "gates": gates,
                }
            ),
            flush=True,
        )
    output = {
        "date": "2026-10-26",
        "run_root": run.relative_to(Path.cwd()).as_posix(),
        "protocol_sha256": sha(HERE / "protocol.json"),
        "source_packet_sha256": sha(HERE / "source-packet.json"),
        "guide_hashes": protocol["guide_hashes"],
        "platform": platform.platform(),
        "profiles": profiles,
        "versions": {
            "git": subprocess.check_output([str(git), "--version"], text=True).strip(),
            "bash": subprocess.check_output(
                [str(bash), "--version"], text=True
            ).splitlines()[0],
            "touch": subprocess.check_output(
                [str(touch), "--version"], text=True
            ).splitlines()[0],
        },
        "native_child_path": native_env["PATH"],
        "parent_path_unchanged": os.environ.get("PATH") == host_env.get("PATH"),
        "records": records,
        "all_case_expectations_matched": all(
            r["expectations_matched"] for r in records
        ),
        "human_reader_observed": False,
        "timing_scope": "One subprocess run per case; includes startup, not reader time or a guide-efficiency comparison.",
    }
    (HERE / "results.json").write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
