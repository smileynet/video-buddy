from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
import shlex
import subprocess
import tempfile


@dataclass(frozen=True, slots=True)
class SshBackendConfig:
    name: str
    priority: int
    host: str
    worker_root: str
    capabilities: tuple[str, ...]
    ssh_opts: tuple[str, ...] = ()
    python: str | None = None

    @property
    def remote_python(self) -> str:
        return self.python or f"{self.worker_root}/.venv/bin/python3"


@dataclass(frozen=True, slots=True)
class ProbeResult:
    name: str
    available: bool
    reason: str


class SshBackend:
    def __init__(self, config: SshBackendConfig) -> None:
        self.config = config

    @property
    def name(self) -> str:
        return self.config.name

    def probe(self) -> ProbeResult:
        try:
            self._ssh(["true"], timeout=15)
        except subprocess.SubprocessError as exc:
            return ProbeResult(self.name, False, f"ssh failed: {exc}")

        checks = [f"test -x {shlex.quote(self.config.remote_python)}"]
        if "whisper" in self.config.capabilities:
            checks.append(
                f"{shlex.quote(self.config.remote_python)} -c {shlex.quote('import faster_whisper, ctranslate2')}"
            )
        if "easyocr" in self.config.capabilities:
            checks.append(
                f"{shlex.quote(self.config.remote_python)} -c {shlex.quote('import easyocr')}"
            )
        if "gpu" in self.config.capabilities:
            checks.append("command -v nvidia-smi >/dev/null 2>&1")
        try:
            self._ssh([" && ".join(checks)], timeout=30, shell=True)
        except subprocess.SubprocessError as exc:
            return ProbeResult(self.name, False, f"probe failed: {exc}")
        return ProbeResult(self.name, True, "ready")

    def deploy(self, *, workers_dir: Path) -> ProbeResult:
        self._ssh(
            [f"mkdir -p {shlex.quote(self.config.worker_root)}"], timeout=30, shell=True
        )
        self._scp_to(
            workers_dir / "ocr_worker.py",
            f"{self.config.worker_root}/ocr_worker.py",
            timeout=60,
        )
        self._scp_to(
            workers_dir / "transcribe_worker.py",
            f"{self.config.worker_root}/transcribe_worker.py",
            timeout=60,
        )
        return self.probe()

    def run_whisper(
        self,
        audio_path: Path,
        *,
        model: str,
        device: str,
        compute_type: str,
    ) -> list[dict]:
        with tempfile.TemporaryDirectory(prefix="video-buddy-ssh-") as tmp:
            local_tmp = Path(tmp)
            remote_dir = self._make_remote_tempdir("video-buddy-transcribe")
            remote_audio = f"{remote_dir}/audio{audio_path.suffix or '.bin'}"
            remote_output = f"{remote_dir}/captions.json"
            try:
                self._scp_to(audio_path, remote_audio, timeout=120)
                command = (
                    f"{shlex.quote(self.config.remote_python)} "
                    f"{shlex.quote(self.config.worker_root + '/transcribe_worker.py')} "
                    f"{shlex.quote(remote_audio)} --output {shlex.quote(remote_output)} "
                    f"--model {shlex.quote(model)} --device {shlex.quote(device)} "
                    f"--compute-type {shlex.quote(compute_type)}"
                )
                self._ssh([command], timeout=1200, shell=True)
                local_output = local_tmp / "captions.json"
                self._scp_from(remote_output, local_output, timeout=120)
                return json.loads(local_output.read_text(encoding="utf-8"))
            finally:
                self._cleanup_remote_dir(remote_dir)

    def run_easyocr(self, frames_dir: Path, frame_names: list[str]) -> dict[str, dict]:
        with tempfile.TemporaryDirectory(prefix="video-buddy-ssh-") as tmp:
            remote_dir = self._make_remote_tempdir("video-buddy-ocr")
            try:
                for name in frame_names:
                    self._scp_to(frames_dir / name, f"{remote_dir}/{name}", timeout=120)
                command = (
                    f"{shlex.quote(self.config.remote_python)} "
                    f"{shlex.quote(self.config.worker_root + '/ocr_worker.py')} "
                    f"{shlex.quote(remote_dir)}"
                )
                self._ssh([command], timeout=1200, shell=True)
                local_results = Path(tmp) / "results.json"
                self._scp_from(f"{remote_dir}/results.json", local_results, timeout=120)
                return json.loads(local_results.read_text(encoding="utf-8"))
            finally:
                self._cleanup_remote_dir(remote_dir)

    def _make_remote_tempdir(self, prefix: str) -> str:
        safe_prefix = "".join(
            ch if ch.isalnum() or ch in "-_" else "-" for ch in prefix
        )
        cmd = f"mktemp -d -t {shlex.quote(safe_prefix)}.XXXXXXXX"
        result = self._ssh([cmd], timeout=30, shell=True)
        return result.stdout.strip()

    def _cleanup_remote_dir(self, remote_dir: str | None) -> None:
        if not remote_dir:
            return
        try:
            self._ssh([f"rm -rf {shlex.quote(remote_dir)}"], timeout=30, shell=True)
        except subprocess.SubprocessError:
            pass

    def _ssh(
        self, args: list[str], *, timeout: int, shell: bool = False
    ) -> subprocess.CompletedProcess[str]:
        if shell:
            command = ["ssh", *self.config.ssh_opts, self.config.host, args[0]]
        else:
            command = ["ssh", *self.config.ssh_opts, self.config.host, *args]
        return subprocess.run(
            command, check=True, capture_output=True, text=True, timeout=timeout
        )

    def _scp_to(self, local_path: Path, remote_path: str, *, timeout: int) -> None:
        command = [
            "scp",
            *self.config.ssh_opts,
            str(local_path),
            f"{self.config.host}:{remote_path}",
        ]
        subprocess.run(
            command, check=True, capture_output=True, text=True, timeout=timeout
        )

    def _scp_from(self, remote_path: str, local_path: Path, *, timeout: int) -> None:
        command = [
            "scp",
            *self.config.ssh_opts,
            f"{self.config.host}:{remote_path}",
            str(local_path),
        ]
        subprocess.run(
            command, check=True, capture_output=True, text=True, timeout=timeout
        )
