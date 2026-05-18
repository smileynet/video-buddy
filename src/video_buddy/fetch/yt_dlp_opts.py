from __future__ import annotations

import shutil


class MissingRuntimeError(RuntimeError):
    """Raised when a required external runtime is missing."""


def apply_youtube_auth(ydl_opts: dict, cookies_from_browser: str | None) -> None:
    """Add cookie auth and JS runtime opts to ``ydl_opts`` in place."""
    if not cookies_from_browser:
        return
    if shutil.which("node") is None:
        raise MissingRuntimeError(
            "Node.js is required on PATH to authenticate to YouTube with cookies "
            "(yt-dlp's n-challenge solver needs a JS runtime). "
            "Install from https://nodejs.org or use `fnm`/`nvm`. "
            "Without it, cookie-auth clients return only image formats."
        )
    ydl_opts["cookiesfrombrowser"] = (cookies_from_browser,)
    ydl_opts["js_runtimes"] = {"node": {}}
