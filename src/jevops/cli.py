import typer

from jevops.sources import read_lines
from jevops.parser import parse_errors
from jevops.cluster import cluster_errors


def analyze(path: str):
    """Analyze a log file and print clustered error findings."""
    lines = read_lines(path)
    errors = parse_errors(lines)
    clustered = cluster_errors(errors)

    for message, count in clustered.items():
        typer.echo(f"{count}x {message}")


if __name__ == "__main__":
    typer.run(analyze)
