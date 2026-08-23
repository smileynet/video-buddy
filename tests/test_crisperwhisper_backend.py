"""Tests for CrisperWhisper SSH backend integration."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from video_buddy.compute.ssh import SshBackend, SshBackendConfig


def _make_config(**kwargs) -> SshBackendConfig:
    defaults = {
        "name": "test-backend",
        "priority": 10,
        "host": "sam@testhost",
        "worker_root": "/home/sam/video-buddy-worker",
        "capabilities": ("whisper", "gpu", "crisperwhisper"),
        "ssh_opts": ("-o", "BatchMode=yes"),
        "crisperwhisper_python": "/home/sam/.venvs/crisperwhisper/bin/python3",
    }
    defaults.update(kwargs)
    return SshBackendConfig(**defaults)


class TestSshBackendConfig:
    def test_remote_crisperwhisper_python_from_config(self) -> None:
        config = _make_config(
            crisperwhisper_python="/custom/path/python3"
        )
        assert config.remote_crisperwhisper_python == "/custom/path/python3"

    def test_remote_crisperwhisper_python_default(self) -> None:
        config = _make_config(crisperwhisper_python=None)
        assert (
            config.remote_crisperwhisper_python
            == "/home/sam/video-buddy-worker/.venvs/crisperwhisper/bin/python3"
        )


class TestRunCrisperwhisper:
    def test_run_crisperwhisper_returns_v2_dict(self, tmp_path: Path) -> None:
        audio_file = tmp_path / "audio.wav"
        audio_file.write_bytes(b"fake audio")

        v2_output = {
            "schema_version": "2.0",
            "metadata": {"engine": "crisperwhisper", "model": "turbo"},
            "segments": [
                {
                    "start": 0.5,
                    "duration": 3.0,
                    "text": "Hello world",
                    "words": [
                        {"start": 0.5, "end": 0.9, "text": "Hello"},
                        {"start": 1.0, "end": 1.4, "text": "world"},
                    ],
                }
            ],
        }

        backend = SshBackend(_make_config())

        def mock_ssh(args, *, timeout, shell=False):
            from unittest.mock import MagicMock

            result = MagicMock()
            result.stdout = "/tmp/test-remote-dir\n"
            return result

        def mock_scp_to(local_path, remote_path, *, timeout):
            pass

        def mock_scp_from(remote_path, local_path, *, timeout):
            Path(local_path).write_text(json.dumps(v2_output))

        def mock_cleanup(remote_dir):
            pass

        with (
            patch.object(backend, "_ssh", side_effect=mock_ssh),
            patch.object(backend, "_scp_to", side_effect=mock_scp_to),
            patch.object(backend, "_scp_from", side_effect=mock_scp_from),
            patch.object(backend, "_cleanup_remote_dir", side_effect=mock_cleanup),
        ):
            result = backend.run_crisperwhisper(
                audio_file, model="turbo", device="cuda", compute_type="float16"
            )

        assert isinstance(result, dict)
        assert result["schema_version"] == "2.0"
        assert result["metadata"]["engine"] == "crisperwhisper"
        assert len(result["segments"]) == 1
        assert len(result["segments"][0]["words"]) == 2


class TestProbeWithCrisperwhisper:
    def test_probe_includes_crisperwhisper_check(self) -> None:
        config = _make_config()
        backend = SshBackend(config)

        ssh_calls = []

        def mock_ssh(args, *, timeout, shell=False):
            from unittest.mock import MagicMock

            ssh_calls.append(args)
            result = MagicMock()
            result.stdout = ""
            return result

        with patch.object(backend, "_ssh", side_effect=mock_ssh):
            backend.probe()

        # Second SSH call contains the capability checks
        assert len(ssh_calls) == 2
        checks_cmd = ssh_calls[1][0]
        assert "import crisperwhisper" in checks_cmd
        assert "/home/sam/.venvs/crisperwhisper/bin/python3" in checks_cmd


class TestRegistryBuildsCrisperwhisperPython:
    def test_registry_passes_crisperwhisper_python(self) -> None:
        from video_buddy.compute.registry import build_registry

        entries = [
            {
                "type": "ssh",
                "name": "test",
                "priority": 10,
                "host": "user@host",
                "worker_root": "/work",
                "capabilities": ["crisperwhisper"],
                "crisperwhisper_python": "/custom/venv/bin/python3",
            }
        ]
        registry = build_registry(entries)
        backend = registry.get("test")
        assert backend is not None
        assert (
            backend.config.crisperwhisper_python == "/custom/venv/bin/python3"
        )

    def test_registry_handles_missing_crisperwhisper_python(self) -> None:
        from video_buddy.compute.registry import build_registry

        entries = [
            {
                "type": "ssh",
                "name": "test",
                "priority": 10,
                "host": "user@host",
                "worker_root": "/work",
                "capabilities": ["whisper"],
            }
        ]
        registry = build_registry(entries)
        backend = registry.get("test")
        assert backend is not None
        assert backend.config.crisperwhisper_python is None
