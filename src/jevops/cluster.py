from jevops.normalize import normalize


def cluster_errors(messages: list[str]) -> dict[str, int]:
    """Group messages that are the same once numbers (timestamps, ids, ports...) are ignored."""
    counts: dict[str, int] = {}
    first_seen: dict[str, str] = {}
    for message in messages:
        key = normalize(message)
        first_seen.setdefault(key, message)
        counts[key] = counts.get(key, 0) + 1
    return {first_seen[key]: count for key, count in counts.items()}
