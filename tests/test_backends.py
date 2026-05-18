from __future__ import annotations

from video_buddy.compute.registry import build_registry


def test_build_registry_filters_ssh_entries() -> None:
    registry = build_registry(
        [
            {
                "name": "homelab",
                "type": "ssh",
                "priority": 10,
                "host": "user@gpu-box.lan",
                "worker_root": "~/video-buddy-worker",
                "capabilities": ["whisper", "easyocr", "gpu"],
            },
            {"name": "other", "type": "local"},
        ]
    )

    assert registry.get("homelab") is not None
    assert registry.get("other") is None


def test_registry_reports_local_probe() -> None:
    registry = build_registry([])
    probes = registry.all_probes()
    assert probes[0].name == "local"
    assert probes[0].available is True
