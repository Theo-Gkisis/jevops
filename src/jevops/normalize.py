import re

_DIGITS_RE = re.compile(r"\d+")


def normalize(line: str) -> str:
    """Collapse numbers so near-identical lines (same message, different timestamp/id) compare equal."""
    return _DIGITS_RE.sub("#", line)
