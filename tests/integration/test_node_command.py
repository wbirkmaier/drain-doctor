import json
from pathlib import Path

from typer.testing import CliRunner

from drain_doctor.cli import app


def test_node_command_matches_expected_output() -> None:
    fixture_dir = Path("tests/fixtures/node-drain")
    expected = json.loads((fixture_dir / "expected-node-report.json").read_text())

    result = CliRunner().invoke(app, ["node", "ip-10-0-42-17", "--fixtures", str(fixture_dir)])

    assert result.exit_code == 0
    assert json.loads(result.stdout) == expected


def test_node_command_returns_distinct_exit_code_for_missing_node() -> None:
    fixture_dir = Path("tests/fixtures/node-drain")
    result = CliRunner().invoke(app, ["node", "missing-node", "--fixtures", str(fixture_dir)])

    assert result.exit_code == 3
