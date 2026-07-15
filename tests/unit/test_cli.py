from typer.testing import CliRunner

from drain_doctor.cli import app


def test_help_exits_successfully() -> None:
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Estimate Kubernetes drain disruption" in result.stdout


def test_version_command_prints_version() -> None:
    result = CliRunner().invoke(app, ["version"])

    assert result.exit_code == 0
    assert "drain-doctor 0.1.0" in result.stdout
