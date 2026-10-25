"""Exploratory displacement proposals; source capture stays in the core."""

from pathlib import Path
import json

import cv2
import numpy as np

from video_buddy.frames.capture import extract_frames, parse_timestamp_ms

folder = Path(".scratch/seek-scroll-search")
files = extract_frames(
    Path(".scratch/seek-retained-source/SWYqp7iY_Tc.mp4"),
    [(800, 1150)],
    folder,
    fps=2,
    max_candidates=1000,
)
prior = None
proposals = []
for path in files:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)[100:480, 35:640].astype(
        np.float32
    )
    if prior is not None:
        (dx, dy), response = cv2.phaseCorrelate(prior, image)
        if response > 0.3 and abs(dy) > 6:
            proposals.append(
                dict(
                    time=parse_timestamp_ms(path) / 1000,
                    dx=dx,
                    dy=dy,
                    response=response,
                )
            )
    prior = image
proposals.sort(key=lambda x: -x["response"])
folder.mkdir(exist_ok=True)
(folder / "proposals.json").write_text(json.dumps(proposals, indent=2))
print(json.dumps(proposals[:15]))
