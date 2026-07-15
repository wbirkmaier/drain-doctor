from pathlib import Path

from drain_doctor.analysis import analyze_node_drain
from drain_doctor.fixtures import load_fixture


def test_analyze_node_drain_reports_expected_blockers_and_warnings() -> None:
    report = analyze_node_drain(load_fixture(Path("tests/fixtures/node-drain")), "ip-10-0-42-17")

    assert [item.kind for item in report.blockers] == [
        "daemonset_pod",
        "pdb_exhausted",
        "local_storage",
        "replica_shortfall",
    ]
    assert [item.kind for item in report.warnings] == [
        "ephemeral_storage",
        "long_termination_grace_period",
        "degraded_workload",
    ]


def test_analyze_node_drain_sums_requested_resources() -> None:
    report = analyze_node_drain(load_fixture(Path("tests/fixtures/node-drain")), "ip-10-0-42-17")

    assert report.total_cpu_millicores == 925
    assert report.total_memory_mib == 1664
