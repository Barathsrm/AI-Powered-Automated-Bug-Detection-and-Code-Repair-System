def format_diff_for_display(raw_diff: str) -> list[dict]:
    """Splits a unified diff into per-line entries tagged add/remove/context
    for the frontend's CodeDiffViewer to render side by side."""
    lines = []
    for line in raw_diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            lines.append({"type": "add", "text": line[1:]})
        elif line.startswith("-") and not line.startswith("---"):
            lines.append({"type": "remove", "text": line[1:]})
        else:
            lines.append({"type": "context", "text": line})
    return lines
