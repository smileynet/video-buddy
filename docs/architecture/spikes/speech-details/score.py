"""THROWAWAY: score frozen lexical aliases and phrase-envelope timing."""

import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def tokens(text):
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())


def edit_counts(reference, hypothesis):
    # Cost, substitutions, deletions, insertions; stable lexical tie break.
    prev = [(i, 0, 0, i) for i in range(len(hypothesis) + 1)]
    for i, ref in enumerate(reference):
        row = [(i + 1, 0, i + 1, 0)]
        for j, hyp in enumerate(hypothesis):
            if ref == hyp:
                row.append(prev[j])
            else:
                c, s, d, n = prev[j]
                sub = (c + 1, s + 1, d, n)
                c, s, d, n = prev[j + 1]
                delete = (c + 1, s, d + 1, n)
                c, s, d, n = row[-1]
                insert = (c + 1, s, d, n + 1)
                row.append(min(sub, delete, insert))
        prev = row
    return dict(zip(["errors", "substitutions", "deletions", "insertions"], prev[-1]))


references = json.loads((HERE / "references.json").read_text())["fixtures"]
scores = []
for path in sorted(HERE.glob("raw-*.json")):
    if path.stem.endswith(("-natural", "-tutorial", "-model-reviewed")):
        continue
    raw = json.loads(path.read_text())
    rows = []
    for fixture in references:
        output = next(o for o in raw["outputs"] if o["fixture"] == fixture["id"])
        text = " ".join(s["text"] for s in output["segments"])
        words = [w for s in output["segments"] for w in s["words"]]
        flat = [
            (token, w["start"], w["end"]) for w in words for token in tokens(w["word"])
        ]
        lexical = [x[0] for x in flat]
        row = {
            "fixture": fixture["id"],
            "kind": fixture["kind"],
            "split": fixture["split"],
            "text": text,
            "word_timestamps_present": bool(words),
            "duration": output["duration"],
            "seconds": output["seconds"],
            "worker_wall_seconds": output["worker_wall_seconds"],
            "phrases": [],
        }
        if fixture["text"] is not None:
            r, h = tokens(fixture["text"]), tokens(text)
            row["word_counts"] = {
                "reference": len(r),
                "hypothesis": len(h),
                **edit_counts(r, h),
            }
            # Normalized CER ignores punctuation/spacing, retains numerals.
            r, h = "".join(r), "".join(h)
            row["character_counts"] = {
                "reference": len(r),
                "hypothesis": len(h),
                **edit_counts(r, h),
            }
        cursor = 0
        for phrase in fixture["phrases"]:
            hits = []
            for alias in phrase["aliases"]:
                target = tokens(alias)
                for i in range(cursor, len(lexical) - len(target) + 1):
                    if lexical[i : i + len(target)] == target:
                        hits.append((i, i + len(target), alias))
            result = {
                "text": phrase["text"],
                "recovered": bool(hits),
                "reference_start": phrase["start"],
                "reference_end": phrase["end"],
            }
            if hits:
                first, last, alias = min(hits)
                cursor = last
                start, end = flat[first][1], flat[last - 1][2]
                result.update(
                    {
                        "matched_alias": alias,
                        "start": start,
                        "end": end,
                        "start_error": start - phrase["start"],
                        "end_error": end - phrase["end"],
                    }
                )
            row["phrases"].append(result)
        if fixture["id"] == "jfk":
            matches = [w for w in words if tokens(w["word"]) == ["americans"]]
            row["upstream_timing_check"] = {
                "target_time": 1.8,
                "matches": matches,
                "passes": any(w["start"] <= 1.8 <= w["end"] for w in matches),
            }
        rows.append(row)
    target_rows = [
        r
        for r in rows
        if r["kind"] == "synthetic-authored" and r["split"] == "validation"
    ]
    phrases = [p for r in target_rows for p in r["phrases"]]
    counts = {
        k: sum(r["word_counts"][k] for r in target_rows)
        for k in [
            "reference",
            "hypothesis",
            "errors",
            "substitutions",
            "deletions",
            "insertions",
        ]
    }
    chars = {
        k: sum(r["character_counts"][k] for r in target_rows)
        for k in [
            "reference",
            "hypothesis",
            "errors",
            "substitutions",
            "deletions",
            "insertions",
        ]
    }
    timing = [
        abs(p[k])
        for p in phrases
        if p["recovered"]
        for k in ["start_error", "end_error"]
    ]
    scores.append(
        {
            "option": raw["option"]["id"],
            "validation_critical_phrases": {
                "recovered": sum(p["recovered"] for p in phrases),
                "total": len(phrases),
            },
            "validation_word_counts": counts,
            "validation_wer": counts["errors"] / counts["reference"],
            "validation_character_counts": chars,
            "validation_cer": chars["errors"] / chars["reference"],
            "mean_absolute_phrase_boundary_error": sum(timing) / len(timing)
            if timing
            else None,
            "max_absolute_phrase_boundary_error": max(timing) if timing else None,
            "timing_phrases": sum(p["recovered"] for p in phrases),
            "load_seconds_sum": raw["load_seconds"],
            "inference_seconds_sum": sum(r["seconds"] for r in rows),
            "worker_wall_seconds_sum": sum(r["worker_wall_seconds"] for r in rows),
            "peak_sampled_root_children_rss": raw["peak_sampled_root_children_rss"],
            "rows": rows,
        }
    )
(HERE / "scores.json").write_text(json.dumps(scores, indent=2) + "\n")
for row in scores:
    print(json.dumps({k: v for k, v in row.items() if k != "rows"}))

natural_refs = json.loads((HERE / "references-natural.json").read_text())["fixtures"]
natural_scores = []
for path in sorted(HERE.glob("raw-*-natural.json")):
    raw = json.loads(path.read_text())
    rows = []
    for fixture in natural_refs:
        output = next(o for o in raw["outputs"] if o["fixture"] == fixture["id"])
        text = " ".join(s["text"] for s in output["segments"])
        r, h = tokens(fixture["text"]), tokens(text)
        row = {
            "fixture": fixture["id"],
            "text": text,
            "word_counts": {
                "reference": len(r),
                "hypothesis": len(h),
                **edit_counts(r, h),
            },
        }
        r, h = "".join(r), "".join(h)
        row["character_counts"] = {
            "reference": len(r),
            "hypothesis": len(h),
            **edit_counts(r, h),
        }
        rows.append(row)
    counts = {
        k: sum(r["word_counts"][k] for r in rows)
        for k in [
            "reference",
            "hypothesis",
            "errors",
            "substitutions",
            "deletions",
            "insertions",
        ]
    }
    chars = {
        k: sum(r["character_counts"][k] for r in rows)
        for k in [
            "reference",
            "hypothesis",
            "errors",
            "substitutions",
            "deletions",
            "insertions",
        ]
    }
    natural_scores.append(
        {
            "option": raw["option"]["id"],
            "word_counts": counts,
            "wer": counts["errors"] / counts["reference"],
            "character_counts": chars,
            "cer": chars["errors"] / chars["reference"],
            "inference_seconds": sum(x["seconds"] for x in raw["outputs"]),
            "worker_wall_seconds": sum(
                x["worker_wall_seconds"] for x in raw["outputs"]
            ),
            "load_seconds": raw["load_seconds"],
            "peak_sampled_root_children_rss": raw["peak_sampled_root_children_rss"],
            "rows": rows,
        }
    )
(HERE / "scores-natural.json").write_text(json.dumps(natural_scores, indent=2) + "\n")
for row in natural_scores:
    print(json.dumps({k: v for k, v in row.items() if k != "rows"}))

tutorial = json.loads((HERE / "references-tutorial.json").read_text())["fixtures"][0]


def term_hits(text):
    words = tokens(text)
    return [
        {
            "target": t["name"],
            "recovered": any(
                any(
                    words[i : i + len(tokens(a))] == tokens(a)
                    for i in range(len(words) - len(tokens(a)) + 1)
                )
                for a in t["aliases"]
            ),
        }
        for t in tutorial["source_task_targets"]
    ]


tutorial_scores = [
    {
        "option": "available-captions",
        "text": " ".join(c["text"] for c in tutorial["caption_cues"]),
        "targets": term_hits(" ".join(c["text"] for c in tutorial["caption_cues"])),
        "provenance": tutorial["caption_provenance"],
    }
]
for path in sorted(HERE.glob("raw-*-tutorial.json")):
    raw = json.loads(path.read_text())
    output = raw["outputs"][0]
    text = " ".join(s["text"] for s in output["segments"])
    tutorial_scores.append(
        {
            "option": raw["option"]["id"],
            "text": text,
            "targets": term_hits(text),
            "inference_seconds": output["seconds"],
            "worker_wall_seconds": output["worker_wall_seconds"],
            "peak_sampled_root_children_rss": raw["peak_sampled_root_children_rss"],
            "word_boundaries": [w for s in output["segments"] for w in s["words"]],
            "timing_accuracy": "Unscored: no independent auditory word-boundary reference. Values are model outputs only.",
        }
    )
(HERE / "scores-tutorial.json").write_text(json.dumps(tutorial_scores, indent=2) + "\n")
for row in tutorial_scores:
    print(
        json.dumps(
            {
                "option": row["option"],
                "task_terms": sum(t["recovered"] for t in row["targets"]),
                "total": len(row["targets"]),
            }
        )
    )
