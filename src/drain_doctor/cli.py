from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from drain_doctor.analysis import analyze_node_drain
from drain_doctor.exceptions import DrainDoctorError
from drain_doctor.fixtures import load_fixture

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


@app.command("node")
def node(
    node_name: Annotated[str, typer.Argument(help="Node name to simulate draining.")],
    fixtures: Annotated[
        Path,
        typer.Option(
            "--fixtures",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Directory containing cluster.json fixture data.",
        ),
    ],
) -> None:
    try:
        report = analyze_node_drain(load_fixture(fixtures), node_name)
    except DrainDoctorError as error:
        raise typer.Exit(code=error.exit_code) from error

    typer.echo(report.model_dump_json(indent=2))


def main(argv: Annotated[list[str] | None, typer.Argument(hidden=True)] = None) -> None:
    app(args=argv)
