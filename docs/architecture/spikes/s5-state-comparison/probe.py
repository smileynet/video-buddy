"""Throwaway Windows persistence comparison; never imported by the product.

Run with Python 3.10+: python probe.py
Writes only beneath a new temporary directory and beside this script (report).
These injected crashes are observations, not a production test suite.
"""

import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import platform
import sqlite3
import sys
import tempfile
import time
import msvcrt


def digest(data):
    return hashlib.sha256(data).hexdigest()


class Manifest:
    def __init__(self, root):
        self.root = root

    def __enter__(self):
        self.lock = (self.root / "writer.lock").open("a+b")
        self.lock.write(b"0")
        self.lock.flush()
        until = time.monotonic() + 10
        while True:
            self.lock.seek(0)
            try:
                msvcrt.locking(self.lock.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                if time.monotonic() > until:
                    raise
                time.sleep(0.01)
        return self

    def read(self):
        p = self.root / "manifest.json"
        if not p.exists():
            return None
        return json.loads(p.read_text())

    def write(self, record, crash=False):
        tmp = self.root / "manifest.tmp"
        with tmp.open("w") as f:
            f.write('{"partial":' if crash else json.dumps(record))
            f.flush()
            os.fsync(f.fileno())
        if crash:
            os._exit(17)
        os.replace(tmp, self.root / "manifest.json")

    def __exit__(self, *_):
        self.lock.seek(0)
        msvcrt.locking(self.lock.fileno(), msvcrt.LK_UNLCK, 1)
        self.lock.close()


class Database:
    def __init__(self, root):
        self.root = root

    def __enter__(self):
        self.db = sqlite3.connect(self.root / "state.sqlite", timeout=10)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY, payload TEXT)"
        )
        self.db.commit()
        self.db.execute("BEGIN IMMEDIATE")
        return self

    def read(self):
        row = self.db.execute("SELECT payload FROM state WHERE id=1").fetchone()
        return json.loads(row[0]) if row else None

    def write(self, record, crash=False):
        self.db.execute(
            "INSERT OR REPLACE INTO state VALUES (1, ?)", (json.dumps(record),)
        )
        if crash:
            os._exit(17)

    def __exit__(self, exc, *_):
        self.db.rollback() if exc else self.db.commit()
        self.db.close()


def work(kind, directory, key="v1", fault=None, allow_auth=False):
    root = Path(directory)
    store = Manifest if kind == "manifest" else Database
    with store(root) as s:
        row = s.read()
        if row and row.get("status") == "needs_user" and not allow_auth:
            return
        if fault == "auth":
            s.write({"key": key, "status": "needs_user", "reason": "authentication"})
            return
        artifact = root / "artifact.bin"
        media = (root / "input.bin").read_bytes()
        expected = {"input_config_key": key, "media_sha256": digest(media)}
        expected_bytes = json.dumps(expected, sort_keys=True).encode() + b"\n" + media
        reusable = artifact.exists() and artifact.read_bytes() == expected_bytes
        if not reusable:
            with (root / "generation.log").open("a") as log:
                log.write(key + "\n")
            time.sleep(0.02)
            tmp = root / "artifact.tmp"
            with tmp.open("wb") as f:
                f.write(
                    b'{"partial":' if fault == "partial_artifact" else expected_bytes
                )
                f.flush()
                os.fsync(f.fileno())
            if fault == "partial_artifact":
                os._exit(17)
            os.replace(tmp, artifact)
        if fault == "after_artifact":
            os._exit(17)
        s.write(
            {
                "key": key,
                "status": "succeeded",
                "hash": digest(artifact.read_bytes()),
                "optional_stage": "failed" if fault == "optional" else "succeeded",
                "warnings": ["OCR unavailable"] if fault == "optional" else [],
            },
            crash=fault == "state_commit",
        )


def spawn(kind, root, **kw):
    child = mp.Process(target=work, args=(kind, str(root)), kwargs=kw)
    child.start()
    child.join(15)
    if child.is_alive():
        child.terminate()
        child.join()
        raise RuntimeError("probe child exceeded bound")
    return child.exitcode


def generations(root):
    p = root / "generation.log"
    return len(p.read_text().splitlines()) if p.exists() else 0


def observe(kind, base, name):
    root = base / kind / name
    root.mkdir(parents=True)
    (root / "input.bin").write_bytes((base / "input.bin").read_bytes())
    checks = {}
    if name in ("after_artifact", "partial_artifact", "state_commit"):
        checks["injected_exit_17"] = spawn(kind, root, fault=name) == 17
        checks["resume_exit_0"] = spawn(kind, root) == 0
        checks["generation_count"] = generations(root) == (
            2 if name == "partial_artifact" else 1
        )
    elif name == "corrupt":
        spawn(kind, root)
        (root / "artifact.bin").write_text("broken")
        spawn(kind, root)
        checks["regenerated"] = generations(root) == 2
    elif name == "missing":
        spawn(kind, root)
        (root / "artifact.bin").unlink()
        spawn(kind, root)
        checks["regenerated"] = generations(root) == 2
    elif name == "config_changed":
        spawn(kind, root)
        spawn(kind, root, key="v2")
        checks["invalidated"] = generations(root) == 2
    elif name == "duplicate":
        children = [mp.Process(target=work, args=(kind, str(root))) for _ in range(2)]
        for p in children:
            p.start()
        for p in children:
            p.join(15)
            if p.is_alive():
                p.terminate()
                p.join()
                raise RuntimeError("concurrent child exceeded bound")
        checks["both_completed"] = all(p.exitcode == 0 for p in children)
        checks["one_generation"] = generations(root) == 1
    elif name == "auth":
        spawn(kind, root, fault="auth")
        spawn(kind, root)
        checks["no_blind_retry"] = generations(root) == 0
        spawn(kind, root, allow_auth=True)
        checks["explicit_recovery"] = generations(root) == 1
    elif name == "optional":
        spawn(kind, root, fault="optional")
    elif name == "edits":
        (root / "user-edits.md").write_text("Keep this human edit")
        spawn(kind, root)
        spawn(kind, root, key="v2")
        checks["sidecar_untouched"] = (
            root / "user-edits.md"
        ).read_text() == "Keep this human edit"
    store = Manifest if kind == "manifest" else Database
    with store(root) as s:
        row = s.read()
    checks["state_complete"] = row["status"] == "succeeded"
    checks["hash_matches_disk"] = row["hash"] == digest(
        (root / "artifact.bin").read_bytes()
    )
    if name == "optional":
        checks["optional_failure_visible"] = row["optional_stage"] == "failed" and bool(
            row["warnings"]
        )
    return {
        "option": kind,
        "case": name,
        "passed": all(checks.values()),
        "checks": checks,
        "generations": generations(root),
    }


if __name__ == "__main__":
    started = time.perf_counter()
    base = Path(tempfile.mkdtemp(prefix="video-buddy-THROWAWAY-state-"))
    fixture = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).parent / "fixture.jpg"
    )
    media = fixture.read_bytes()
    (base / "input.bin").write_bytes(media)
    cases = [
        "after_artifact",
        "partial_artifact",
        "state_commit",
        "corrupt",
        "missing",
        "config_changed",
        "duplicate",
        "auth",
        "optional",
        "edits",
    ]
    results = [
        observe(kind, base, case) for kind in ("manifest", "sqlite") for case in cases
    ]
    report = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "sqlite": sqlite3.sqlite_version,
        "scratch_store": str(base),
        "fixture_path": str(fixture),
        "fixture_bytes": len(media),
        "fixture_sha256": digest(media),
        "elapsed_seconds": time.perf_counter() - started,
        "all_passed": all(x["passed"] for x in results),
        "observations": results,
        "limits": [
            "dummy stage, not a downloader or media pipeline",
            "both options serialize writers across the whole scratch store",
            "process crashes, not power loss or network filesystem failure",
            "known expected fixture bytes substitute for stage-specific artifact validation",
            "no multi-machine lock or high-throughput evaluation",
        ],
    }
    (Path(__file__).parent / "observations.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "all_passed": report["all_passed"],
                "cases": len(results),
                "elapsed_seconds": report["elapsed_seconds"],
            },
            indent=2,
        )
    )
