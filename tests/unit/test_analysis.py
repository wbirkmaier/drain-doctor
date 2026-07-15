from pathlib import Path

from drain_doctor.analysis import analyze_availability_zone, analyze_node_drain, analyze_node_group
from drain_doctor.fixtures import load_fixture


def test_analyze_node_drain_reports_expected_blockers_and_warnings() -> None:
    report = analyze_node_drain(load_fixture(Path("tests/fixtures/node-drain")), "ip-10-0-42-17")

    assert [item.kind for item in report.blockers] == [
        "daemonset_pod",
        "pdb_exhausted",
        "local_storage",
        "replica_shortfall",
        "node_selector_mismatch",
    ]
    assert [item.kind for item in report.warnings] == [
        "ephemeral_storage",
        "long_termination_grace_period",
        "degraded_workload",
        "anti_affinity_risk",
    ]


def test_analyze_node_drain_sums_requested_resources() -> None:
    report = analyze_node_drain(load_fixture(Path("tests/fixtures/node-drain")), "ip-10-0-42-17")

    assert report.total_cpu_millicores == 925
    assert report.total_memory_mib == 1664
    assert report.remaining_node_capacity_cpu_millicores == 1100
    assert report.remaining_node_capacity_memory_mib == 2496


def test_analyze_node_drain_emits_eviction_sequence_and_advisory_patches() -> None:
    report = analyze_node_drain(load_fixture(Path("tests/fixtures/node-drain")), "ip-10-0-42-17")

    assert report.eviction_sequence == [
        "payments/api-7786f8dd7b-mlwzg",
        "search/indexer-0",
        "kube-system/aws-node-9lm9x",
    ]
    assert len(report.advisory_patches) == 2


def test_analyze_node_group_rolls_up_member_reports() -> None:
    report = analyze_node_group(load_fixture(Path("tests/fixtures/node-drain")), "workers-a")

    assert report.analyzed_nodes == ["ip-10-0-42-17", "ip-10-0-42-18"]
    assert report.blocker_count == 5
    assert report.warning_count == 4


def test_analyze_availability_zone_rolls_up_member_reports() -> None:
    report = analyze_availability_zone(
        load_fixture(Path("tests/fixtures/node-drain")), "us-west-2a"
    )

    assert report.analyzed_nodes == ["ip-10-0-42-17", "ip-10-0-42-18"]
    assert report.blocker_count == 5
    assert report.warning_count == 4
