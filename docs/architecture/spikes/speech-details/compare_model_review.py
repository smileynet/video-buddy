"""THROWAWAY: machine-reference agreement, never human accuracy."""

import hashlib
import html
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def words(text):
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", html.unescape(text).lower())


def distance(a, b):
    previous = list(range(len(b) + 1))
    for i, ref in enumerate(a):
        row = [i + 1]
        for j, hyp in enumerate(b):
            row.append(
                min(row[-1] + 1, previous[j + 1] + 1, previous[j] + (ref != hyp))
            )
        previous = row
    return previous[-1]


def hits(text, aliases):
    tokens = words(text)
    return [
        (i, i + len(words(alias)), alias)
        for alias in aliases
        for i in range(len(tokens) - len(words(alias)) + 1)
        if tokens[i : i + len(words(alias))] == words(alias)
    ]


def token_word_points(tokens, timestamps):
    text = "".join(tokens)
    points = [time for token, time in zip(tokens, timestamps) for _ in token]
    result = []
    for match in re.finditer(r"[a-z0-9]+(?:'[a-z]+)?", text.lower()):
        result.append({"word": match.group(), "start": points[match.start()]})
    return result


protocol = json.loads((HERE / "model-review-protocol.json").read_text())
reference = json.loads((HERE / "model-reviewed-references.json").read_text())
packet = json.loads((HERE / "review-manifest.json").read_text())
assert reference["human_verified"] is False
assert (
    reference["raw_sha256"]
    == hashlib.sha256((HERE / "model-review-raw.json").read_bytes()).hexdigest()
)
refs = {f["id"]: f for f in reference["fixtures"]}
outputs = []
for option in ["base", "small", "turbo"]:
    raw = json.loads((HERE / f"raw-{option}-model-reviewed.json").read_text())
    assert (
        raw["references_sha256"]
        == hashlib.sha256(
            (HERE / "model-reviewed-references.json").read_bytes()
        ).hexdigest()
    )
    records = []
    for fixture in raw["outputs"]:
        ref = refs[fixture["fixture"]]
        text = " ".join(segment["text"] for segment in fixture["segments"])
        a, b = words(ref["text"]), words(text)
        flat = [
            (w, word["start"], word["end"])
            for segment in fixture["segments"]
            for word in segment["words"]
            for w in words(word["word"])
        ]
        assert [w[0] for w in flat] == b
        points = token_word_points(ref["tokens"], ref["timestamps"])
        assert [p["word"] for p in points] == a
        targets = []
        for target in [
            t for t in protocol["targets"] if t["clip"] == fixture["fixture"]
        ]:
            found = hits(text, target["spoken"])
            ref_found = hits(ref["text"], target["spoken"])
            record = {
                "target": target["id"],
                "literal_present": bool(hits(text, target["literal"])),
                "spoken_alias_present": bool(found),
                "model_reference_alias_present": bool(ref_found),
                "human_verified": False,
            }
            if found and ref_found:
                index = min(found)[0]
                ref_index = min(ref_found)[0]
                record["candidate_word_start"] = flat[index][1]
                record["reviewer_token_start"] = points[ref_index]["start"]
                record["start_difference_seconds"] = (
                    flat[index][1] - points[ref_index]["start"]
                )
                record["timing_label"] = (
                    "model-to-model start disagreement, not word-boundary error"
                )
            targets.append(record)
        records.append(
            {
                "clip": fixture["fixture"],
                "text": text,
                "reference_words": len(a),
                "hypothesis_words": len(b),
                "word_edit_distance": distance(a, b),
                "reference_chars": len("".join(a)),
                "character_edit_distance": distance("".join(a), "".join(b)),
                "targets": targets,
                "self_correction_marker": ("typed" in b and "but" in b),
                "source_and_destination_markers": (
                    "source" in b and "destination" in b
                ),
                "inference_seconds": fixture["seconds"],
                "worker_wall_seconds": fixture["worker_wall_seconds"],
            }
        )
    n = sum(r["reference_words"] for r in records)
    chars = sum(r["reference_chars"] for r in records)
    outputs.append(
        {
            "option": option,
            "reference_type": "model_reviewed_provisional",
            "human_verified": False,
            "reference_words": n,
            "word_edit_distance": sum(r["word_edit_distance"] for r in records),
            "conditional_wer": sum(r["word_edit_distance"] for r in records) / n,
            "conditional_cer": sum(r["character_edit_distance"] for r in records)
            / chars,
            "inference_seconds": sum(r["inference_seconds"] for r in records),
            "worker_wall_seconds": sum(r["worker_wall_seconds"] for r in records),
            "model_load_seconds": raw["load_seconds"],
            "peak_sampled_root_children_rss": raw["peak_sampled_root_children_rss"],
            "records": records,
        }
    )
caption_records = []
for clip in packet["clips"]:
    text = " ".join(cue["text"] for cue in clip["publisher_draft_cues"])
    caption_records.append(
        {
            "clip": clip["id"],
            "text": text,
            "reference_type": "publisher/manual-classified caption, human verification unestablished",
            "targets": [
                {
                    "target": target["id"],
                    "literal_present": bool(hits(text, target["literal"])),
                    "spoken_alias_present": bool(hits(text, target["spoken"])),
                }
                for target in protocol["targets"]
                if target["clip"] == clip["id"]
            ],
            "edge_overhang": any(
                c["start"] < clip["source_nominal_start"]
                or c["start"] + c["duration"] > clip["source_nominal_end"]
                for c in clip["publisher_draft_cues"]
            ),
            "wer": None,
            "wer_reason": "Whole cue overhang and shared publisher lineage; no forced word clipping to manufacture a full-transcript comparison.",
        }
    )
result = {
    "label": "Conditional agreement with locked machine reference; not human-verified accuracy",
    "human_verified": False,
    "reference_sha256": hashlib.sha256(
        (HERE / "model-reviewed-references.json").read_bytes()
    ).hexdigest(),
    "candidates": outputs,
    "captions": caption_records,
    "reference_target_presence": [
        {
            "target": t["id"],
            "model_reference_alias_present": bool(
                hits(refs[t["clip"]]["text"], t["spoken"])
            ),
        }
        for t in protocol["targets"]
    ],
    "limits": [
        "Known code lexeme disagreements remain uncorrected in model reference.",
        "cp expected target is at a clip edge and unconfirmed; do not treat absence as a scored audio error.",
        "SenseVoice token start points are not human word intervals.",
    ],
}
(HERE / "model-review-comparison.json").write_text(json.dumps(result, indent=2) + "\n")
for output in outputs:
    print(json.dumps({k: v for k, v in output.items() if k != "records"}))
