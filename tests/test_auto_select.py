"""Tests for engine auto-selection logic."""

from __future__ import annotations

from unittest.mock import MagicMock

from video_buddy.compute.registry import BackendRegistry, _probe_cache
from video_buddy.compute.ssh import ProbeResult, SshBackend, SshBackendConfig
from video_buddy.config import WhisperConfig


def _make_backend(name: str, priority: int, capabilities: tuple, available: bool):
    config = SshBackendConfig(
        name=name,
        priority=priority,
        host=f"user@{name}",
        worker_root="/work",
        capabilities=capabilities,
        crisperwhisper_python="/venv/bin/python3",
    )
    backend = SshBackend(config)
    backend.probe = MagicMock(return_value=ProbeResult(name, available, "ready" if available else "offline"))
    return backend


class TestFindCapable:
    def setup_method(self):
        _probe_cache.clear()

    def test_returns_highest_priority_available(self) -> None:
        low = _make_backend("low", priority=10, capabilities=("crisperwhisper",), available=True)
        high = _make_backend("high", priority=20, capabilities=("crisperwhisper",), available=True)
        registry = BackendRegistry(ssh_backends=(low, high))

        result = registry.find_capable("crisperwhisper")

        assert result is not None
        assert result.config.name == "high"

    def test_skips_unavailable_backend(self) -> None:
        offline = _make_backend("offline", priority=30, capabilities=("crisperwhisper",), available=False)
        online = _make_backend("online", priority=10, capabilities=("crisperwhisper",), available=True)
        registry = BackendRegistry(ssh_backends=(offline, online))

        result = registry.find_capable("crisperwhisper")

        assert result is not None
        assert result.config.name == "online"

    def test_returns_none_when_no_capable_backend(self) -> None:
        whisper_only = _make_backend("box", priority=10, capabilities=("whisper",), available=True)
        registry = BackendRegistry(ssh_backends=(whisper_only,))

        result = registry.find_capable("crisperwhisper")

        assert result is None

    def test_returns_none_when_all_offline(self) -> None:
        offline = _make_backend("dead", priority=10, capabilities=("crisperwhisper",), available=False)
        registry = BackendRegistry(ssh_backends=(offline,))

        result = registry.find_capable("crisperwhisper")

        assert result is None

    def test_caches_probe_result(self) -> None:
        backend = _make_backend("cached", priority=10, capabilities=("crisperwhisper",), available=True)
        registry = BackendRegistry(ssh_backends=(backend,))

        registry.find_capable("crisperwhisper")
        registry.find_capable("crisperwhisper")

        # probe() should only be called once despite two find_capable calls
        backend.probe.assert_called_once()

    def test_returns_none_for_empty_registry(self) -> None:
        registry = BackendRegistry(ssh_backends=())
        assert registry.find_capable("crisperwhisper") is None


class TestAutoEngineDefault:
    def test_default_engine_is_auto(self) -> None:
        config = WhisperConfig()
        assert config.engine == "auto"
