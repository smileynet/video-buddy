"""Sample summed process-tree RSS; this is not unique physical memory or VRAM."""

import json
from pathlib import Path
import subprocess
import sys
import time

import psutil

root = Path(__file__).resolve().parent
start = time.perf_counter()
p = subprocess.Popen([sys.executable, str(root / "collect.py")])
proc = psutil.Process(p.pid)
peak = 0
samples = 0
while p.poll() is None:
    try:
        total = 0
        for child in [proc, *proc.children(recursive=True)]:
            try:
                total += child.memory_info().rss
            except psutil.Error:
                pass
        peak = max(peak, total)
        samples += 1
    except psutil.Error:
        pass
    time.sleep(0.02)
assert p.returncode == 0
(root / "memory.json").write_text(
    json.dumps(
        dict(
            peak_summed_tree_rss_bytes=peak,
            samples=samples,
            interval_s=0.02,
            wall_s=time.perf_counter() - start,
        ),
        indent=2,
    )
    + "\n"
)
