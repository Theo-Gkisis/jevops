def read_lines(path: str) -> list[str]:
    """Read a local log file and return its lines."""
    with open(path) as f:
        return f.readlines()
