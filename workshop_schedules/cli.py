import itertools
import os
from pathlib import Path
from typing import List

import typer
from rich.console import Console

from workshop_schedules import _version, output
from workshop_schedules.parse import parse_file

app = typer.Typer(
    name="workshop_schedules",
    help="Render tabular schedules from linear agenda YML",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]workshop_schedules[/] version: [bold blue]{_version}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    files: List[Path] = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
    output_dir: Path = typer.Argument(
        os.getcwd(),
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
) -> None:
    for i, day in enumerate(itertools.chain.from_iterable([parse_file(fn) for fn in files])):
        output.write_day(day, filename=output_dir / f'day_{i+1}.html')


if __name__ == "__main__":
    typer.run(main)
