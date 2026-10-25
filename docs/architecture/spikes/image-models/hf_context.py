"""Experiment-only credential discovery. Never writes or displays a credential."""

import os
import json
from pathlib import Path
import subprocess
import tomllib


def configure():
    from huggingface_hub import get_token

    token = os.environ.get("HF_TOKEN")
    roots = [Path.cwd()]
    try:
        common = subprocess.check_output(
            ["git", "rev-parse", "--git-common-dir"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        roots.append((Path.cwd() / common).resolve().parent)
    except (OSError, subprocess.CalledProcessError):
        pass
    if not token:
        for root in dict.fromkeys(roots):
            local = root / ".env.local"
            if not local.exists():
                continue
            for line in local.read_text(encoding="utf-8").splitlines():
                key, sep, value = line.partition("=")
                if sep and key.strip() == "HF_TOKEN":
                    value = value.strip()
                    token = (
                        json.loads(value) if value.startswith('"') else value.strip("'")
                    )
                    break
            if token:
                break
    if not token:
        token = get_token()
    if not token:
        paths = [
            Path.home() / ".config/mise/config.toml",
            Path.home() / ".codex/config.toml",
        ]

        def values(x):
            if isinstance(x, dict):
                for v in x.values():
                    yield from values(v)
            elif isinstance(x, list):
                for v in x:
                    yield from values(v)
            elif isinstance(x, str) and x.startswith("hf_") and len(x) > 12:
                yield x

        for path in paths:
            if path.exists():
                try:
                    token = next(
                        values(tomllib.loads(path.read_text(encoding="utf-8"))), None
                    )
                except (ValueError, OSError):
                    continue
                if token:
                    break
    if token:
        os.environ["HF_TOKEN"] = token
    return token
