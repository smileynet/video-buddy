from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .ssh import ProbeResult, SshBackend, SshBackendConfig


@dataclass(frozen=True, slots=True)
class BackendRegistry:
    ssh_backends: tuple[SshBackend, ...]

    def all_probes(self) -> list[ProbeResult]:
        results = [ProbeResult("local", True, "ready")]
        results.extend(backend.probe() for backend in self.ssh_backends)
        return results

    def get(self, name: str) -> SshBackend | None:
        for backend in self.ssh_backends:
            if backend.name == name:
                return backend
        return None


def build_registry(compute_entries: list[dict]) -> BackendRegistry:
    backends = []
    for entry in compute_entries:
        if entry.get("type") != "ssh":
            continue
        backends.append(
            SshBackend(
                SshBackendConfig(
                    name=str(entry.get("name") or ""),
                    priority=int(entry.get("priority") or 0),
                    host=str(entry.get("host") or ""),
                    worker_root=str(entry.get("worker_root") or ""),
                    capabilities=tuple(
                        str(item) for item in entry.get("capabilities") or []
                    ),
                    ssh_opts=tuple(str(item) for item in entry.get("ssh_opts") or []),
                    python=str(entry.get("python")) if entry.get("python") else None,
                )
            )
        )
    return BackendRegistry(tuple(backends))


def workers_dir(repo_root: Path) -> Path:
    return repo_root / "workers"
