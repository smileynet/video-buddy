"""Experiment-only credential discovery. Never writes or displays a credential."""

import os
from pathlib import Path
import tomllib


def configure():
    from huggingface_hub import get_token

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
