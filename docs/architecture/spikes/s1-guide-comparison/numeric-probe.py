"""Throwaway numerical observation, not a reader or production implementation."""

import csv
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parent
results = []
for name, offset in [("quarter_turn", math.pi / 2), ("zero_offset_control", 0)]:
    rows = []
    for i in range(360):
        phase = 2 * math.pi * i / 360
        rows.append((phase, math.sin(phase), math.sin(phase + offset)))
    with (root / f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["theta", "x", "y"])
        writer.writerows(rows)
    error = max(abs(x * x + y * y - 1) for _, x, y in rows)
    results.append(
        {
            "configuration": name,
            "rows": len(rows),
            "max_radius_squared_error": error,
            "radius_gate_passed": error <= 1e-12,
            "first_point": list(rows[0][1:]),
        }
    )
output = {
    "kind": "experimenter_written_numeric_probe",
    "reader_study_performed": False,
    "format_winner": "unresolved",
    "observations": results,
    "square_wave": {
        "result": "underconstrained_from_transcript_packet",
        "implemented": False,
    },
}
(root / "observations.json").write_text(
    json.dumps(output, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(output, indent=2))
