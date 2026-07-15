from __future__ import annotations

from drain_doctor.exceptions import DrainDoctorError
from drain_doctor.models import DrainFinding, NodeDrainReport, RawFixture


def analyze_node_drain(fixture: RawFixture, node_name: str) -> NodeDrainReport:
    node = next((item for item in fixture.nodes if item.name == node_name), None)
    if node is None:
        raise DrainDoctorError(f"node not found in fixture: {node_name}", exit_code=3)

    pods = sorted(
        (pod for pod in fixture.pods if pod.node_name == node_name),
        key=lambda item: (item.namespace, item.name),
    )
    remaining_nodes = [item for item in fixture.nodes if item.name != node_name]
    scheduled_elsewhere = [pod for pod in fixture.pods if pod.node_name != node_name]
    remaining_cpu = sum(node.allocatable_cpu for node in remaining_nodes) - sum(
        pod.cpu_millicores for pod in scheduled_elsewhere
    )
    remaining_memory = sum(node.allocatable_memory_mib for node in remaining_nodes) - sum(
        pod.memory_mib for pod in scheduled_elsewhere
    )
    blockers: list[DrainFinding] = []
    warnings: list[DrainFinding] = []
    workload_map = {(item.namespace, item.name): item for item in fixture.workloads}
    pdb_map = {(item.namespace, item.owner_name): item for item in fixture.pod_disruption_budgets}

    for pod in pods:
        pod_ref = f"{pod.namespace}/{pod.name}"
        if pod.daemonset:
            blockers.append(
                DrainFinding(
                    kind="daemonset_pod",
                    severity="high",
                    pod=pod_ref,
                    message=(
                        "pod is managed by a DaemonSet and will not be evicted by a standard drain"
                    ),
                )
            )
        if pod.uses_host_path or pod.uses_local_persistent_volume:
            blockers.append(
                DrainFinding(
                    kind="local_storage",
                    severity="high",
                    pod=pod_ref,
                    message="pod relies on node-local storage that may require manual handling",
                )
            )
        if pod.uses_empty_dir:
            warnings.append(
                DrainFinding(
                    kind="ephemeral_storage",
                    severity="medium",
                    pod=pod_ref,
                    message="pod uses emptyDir and will lose ephemeral data on eviction",
                )
            )
        if pod.termination_grace_period_seconds > 300:
            warnings.append(
                DrainFinding(
                    kind="long_termination_grace_period",
                    severity="medium",
                    pod=pod_ref,
                    message="pod has a long termination grace period and may slow the drain",
                )
            )
        workload = workload_map.get((pod.namespace, pod.owner_name))
        if workload is not None:
            if workload.replicas - workload.unavailable_replicas <= 1:
                blockers.append(
                    DrainFinding(
                        kind="replica_shortfall",
                        severity="high",
                        pod=pod_ref,
                        message="workload has no spare healthy replica to absorb this eviction",
                    )
                )
            elif workload.unavailable_replicas > 0:
                warnings.append(
                    DrainFinding(
                        kind="degraded_workload",
                        severity="medium",
                        pod=pod_ref,
                        message="workload already has unavailable replicas before the drain",
                    )
                )
        pdb = pdb_map.get((pod.namespace, pod.owner_name))
        if pdb is not None and pdb.current_healthy <= pdb.min_available:
            blockers.append(
                DrainFinding(
                    kind="pdb_exhausted",
                    severity="high",
                    pod=pod_ref,
                    message="PodDisruptionBudget does not currently allow another eviction",
                )
            )
        if pod.node_selector:
            matches = [
                candidate
                for candidate in remaining_nodes
                if all(
                    candidate.labels.get(key) == value for key, value in pod.node_selector.items()
                )
            ]
            if not matches:
                blockers.append(
                    DrainFinding(
                        kind="node_selector_mismatch",
                        severity="high",
                        pod=pod_ref,
                        message="no remaining node matches the pod node selector",
                    )
                )
        if pod.hard_anti_affinity_key is not None:
            sibling_present = any(
                other.namespace == pod.namespace
                and other.owner_name == pod.owner_name
                and other.node_name != node_name
                for other in fixture.pods
            )
            if not sibling_present:
                warnings.append(
                    DrainFinding(
                        kind="anti_affinity_risk",
                        severity="medium",
                        pod=pod_ref,
                        message=(
                            "hard anti-affinity may limit safe rescheduling options "
                            "after eviction"
                        ),
                    )
                )

    drained_cpu = sum(pod.cpu_millicores for pod in pods)
    drained_memory = sum(pod.memory_mib for pod in pods)
    if drained_cpu > remaining_cpu:
        blockers.append(
            DrainFinding(
                kind="insufficient_remaining_cpu",
                severity="high",
                pod="node-summary",
                message="remaining nodes do not have enough free CPU for the drained workload set",
            )
        )
    if drained_memory > remaining_memory:
        blockers.append(
            DrainFinding(
                kind="insufficient_remaining_memory",
                severity="high",
                pod="node-summary",
                message=(
                    "remaining nodes do not have enough free memory for the "
                    "drained workload set"
                ),
            )
        )

    return NodeDrainReport(
        node=node.name,
        availability_zone=node.availability_zone,
        pod_count=len(pods),
        blockers=blockers,
        warnings=warnings,
        total_cpu_millicores=sum(pod.cpu_millicores for pod in pods),
        total_memory_mib=sum(pod.memory_mib for pod in pods),
        remaining_node_capacity_cpu_millicores=remaining_cpu,
        remaining_node_capacity_memory_mib=remaining_memory,
        advisory_patches=[],
    )
