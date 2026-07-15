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

    return NodeDrainReport(
        node=node.name,
        availability_zone=node.availability_zone,
        pod_count=len(pods),
        blockers=blockers,
        warnings=warnings,
        total_cpu_millicores=sum(pod.cpu_millicores for pod in pods),
        total_memory_mib=sum(pod.memory_mib for pod in pods),
        advisory_patches=[],
    )
