from __future__ import annotations

from typing import Annotated

import typer

app = typer.Typer(
    help="Estimate Kubernetes drain disruption without issuing eviction calls.",
    no_args_is_help=True,
    pretty_exceptions_enable=False,
)


@app.callback()
def callback() -> None:
    """DrainDoctor command group."""


@app.command("version")
def version() -> None:
    typer.echo("drain-doctor 0.1.0")


def main(argv: Annotated[list[str] | None, typer.Argument(hidden=True)] = None) -> None:
    app(args=argv)
