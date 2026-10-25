"""THROWAWAY boundary policies. No labels or source-specific command vocabulary."""

from collections import Counter, defaultdict
import re


def settled(rows, budget, quiet_s=0.2):
    groups = defaultdict(list)
    start = 0
    for end in range(1, len(rows) + 1):
        if end < len(rows) and rows[end]["text"] == rows[start]["text"]:
            continue
        run = rows[start:end]
        step = rows[1]["pts_s"] - rows[0]["pts_s"] if len(rows) > 1 else 0
        duration = run[-1]["pts_s"] - run[0]["pts_s"] + step
        if duration >= quiet_s and run[0]["text"].strip():
            representative = max(range(start, end), key=lambda i: rows[i]["sharpness"])
            groups[run[0]["text"]].append((duration, representative))
        start = end
    candidates = [max(g) for g in groups.values()]
    candidates.sort(key=lambda r: (r[0], rows[r[1]]["sharpness"]), reverse=True)
    return [
        dict(index=i, reason="settled visual context; execution unverified")
        for _, i in candidates[:budget]
    ]


def prompt(text):
    return bool(
        re.fullmatch(r"[$#>]\s*[|_]*", text.strip())
        or "~/" in text
        or "@" in text
        and "/" in text
    )


def commands(row):
    found = []
    prior_prompt = False
    for line in row["lines"]:
        text = line["text"].strip()
        match = re.match(r"^[$#>]\s*(.*)$", text)
        candidate = (
            match.group(1)
            if match
            else text
            if prior_prompt and not prompt(text)
            else ""
        )
        if re.match(r"^[A-Za-z][A-Za-z0-9_.-]*(?:\s|$)", candidate):
            found.append(dict(text=candidate, y=line["y"]))
        prior_prompt = prompt(text)
    return found


def packets(rows, budget, height):
    initial = commands(rows[0])
    counts = Counter(c["text"] for c in initial)
    initial_y = {
        c["text"]: max(x["y"] for x in initial if x["text"] == c["text"])
        for c in initial
    }
    candidates = []
    for index, row in enumerate(rows):
        occurrences = Counter()
        features = set()
        for command in commands(row):
            text, y = command["text"], command["y"]
            occurrences[text] += 1
            novel = (
                occurrences[text] > counts[text]
                or y > initial_y.get(text, float("inf")) + height * 0.15
            )
            later_prompts = [
                line["y"]
                for line in row["lines"]
                if line["y"] > y and prompt(line["text"])
            ]
            if not novel or not later_prompts:
                continue
            key = f"{text}#{occurrences[text]}"
            features.add("command:" + key)
            stop = min(later_prompts)
            if any(
                y < line["y"] < stop and not prompt(line["text"])
                for line in row["lines"]
            ):
                features.add("response:" + key)
        if features:
            candidates.append(
                dict(
                    index=index,
                    features=features,
                    reason="later prompt observed; success not inferred",
                )
            )
    if not candidates:
        return settled(rows, budget)
    covered = set()
    selected = []
    for _ in range(budget):
        best = max(
            candidates,
            key=lambda c: (
                len(c["features"] - covered),
                sum(line["confidence"] for line in rows[c["index"]]["lines"])
                / max(1, len(rows[c["index"]]["lines"])),
                rows[c["index"]]["sharpness"],
                -c["index"],
            ),
        )
        if not best["features"] - covered:
            break
        covered.update(best["features"])
        selected.append({**best, "features": sorted(best["features"])})
    return selected
