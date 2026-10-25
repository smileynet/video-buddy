"""Forward the existing HF token in process environment only; never in argv/logs."""

import os
from pathlib import Path
import subprocess
import sys

from hf_context import configure

configure()
env = os.environ.copy()
env["WSLENV"] = ":".join(x for x in [env.get("WSLENV", ""), "HF_TOKEN/u"] if x)
version = sys.argv[1]
cmd = f".venvs/sam3-linux/bin/python docs/architecture/spikes/image-models/sam3_bench.py {version}"
subprocess.run(
    [
        "wsl",
        "--distribution",
        "Ubuntu",
        "--cd",
        str(Path.cwd()),
        "--exec",
        "bash",
        "-lc",
        cmd,
    ],
    env=env,
    check=True,
)
