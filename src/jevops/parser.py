from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from jevops.classifier import classify
from jevops.normalize import normalize


def classify_all(lines: list[str], on_progress=None) -> list[tuple[str, str, float, float]]:
    """Classify every non-empty line; calls JEV once per unique pattern (ignoring numbers),
    then applies that result to every line sharing the pattern. Returns
    (line, category, confidence, cost_usd) - cost is only counted once per unique pattern."""
    non_empty = [line.strip() for line in lines if line.strip()]

    groups: dict[str, list[str]] = defaultdict(list)
    for line in non_empty:
        groups[normalize(line)].append(line)

    keys = list(groups.keys())
    results_by_key: dict[str, tuple[str, float, float]] = {}

    with ThreadPoolExecutor(max_workers=50) as pool:
        future_to_key = {pool.submit(classify, groups[key][0]): key for key in keys}
        done = 0
        for future in as_completed(future_to_key):
            results_by_key[future_to_key[future]] = future.result()
            done += 1
            if on_progress:
                on_progress(done, len(keys))

    output = []
    for key, group_lines in groups.items():
        category, confidence, cost = results_by_key[key]
        for i, line in enumerate(group_lines):
            output.append((line, category, confidence, cost if i == 0 else 0.0))
    return output


def parse_errors(lines: list[str]) -> list[str]:
    """Keep only lines JEV classifies as an error or critical problem."""
    return [line for line, category, _, _ in classify_all(lines) if category in ("error", "critical")]
