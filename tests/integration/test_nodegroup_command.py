import json
from pathlib import Path

from typer.testing import CliRunner

from drain_doctor.cli import app


def test_nodegroup_command_matches_expected_output() -> None:
    fixture_dir = Path("tests/fixtures/node-drain")
    expected = json.loads((fixture_dir / "expected-nodegroup-report.json").read_text())

    result = CliRunner().invoke(app, ["nodegroup", "workers-a", "--fixtures", str(fixture_dir)])

    assert result.exit_code == 0
    assert json.loads(result.stdout) == expected
