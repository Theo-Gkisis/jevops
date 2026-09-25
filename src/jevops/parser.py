from jevops.classifier import classify


def parse_errors(lines: list[str]) -> list[str]:
    """Keep only lines JEV classifies as an error or critical problem."""
    messages = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        category, _ = classify(line)
        if category in ("error", "critical"):
            messages.append(line)
    return messages
