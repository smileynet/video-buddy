def select(rows, mode, budget, events=False):
    groups = {}
    runs = []
    current = []
    previous = None
    for index, row in enumerate(rows):
        obs = row["observations"].get(mode)
        text = obs["text"] if obs else ""
        entry = dict(index=index, **obs) if obs and text else None
        if text != previous:
            if current:
                runs.append(current)
            current = []
        if entry:
            current.append(entry)
            groups.setdefault(text, []).append(entry)
        previous = text
    if current:
        runs.append(current)
    if events:
        groups = {}
        for run in runs:
            if len(run) >= 2:
                groups.setdefault(run[0]["text"], []).extend(run)
        ranked = sorted(groups.values(), key=lambda g: g[0]["index"])
    else:
        ranked = sorted(
            [g for g in groups.values() if len(g) >= 6], key=lambda g: -len(g)
        )
    chosen = [max(g, key=lambda r: r["sharpness"]) for g in ranked[:budget]]
    return sorted(chosen, key=lambda r: r["index"])
