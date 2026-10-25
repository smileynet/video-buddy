"""Profile validation collector only; summed sampled RSS is not unique RAM."""

import json
from pathlib import Path
import subprocess
import sys
import time

import psutil

root = Path(__file__).resolve().parent
start = time.perf_counter()
p = subprocess.Popen([sys.executable, str(root / "collect.py"), "validation"])
proc = psutil.Process(p.pid)
peak = samples = 0
while p.poll() is None:
    total = 0
    try:
        for item in [proc, *proc.children(recursive=True)]:
            try:
                total += item.memory_info().rss
            except psutil.Error:
                pass
    except psutil.Error:
        pass
    peak = max(peak, total)
    samples += 1
    time.sleep(0.02)
assert p.returncode == 0
(root / "validation-memory.json").write_text(
    json.dumps(
        dict(
            peak_summed_tree_rss=peak,
            samples=samples,
            nominal_interval_s=0.02,
            wall_s=time.perf_counter() - start,
            exclusions="decode, annotation, legacy, monitor; shared pages may double count",
        ),
        indent=2,
    )
    + "\n"
)
