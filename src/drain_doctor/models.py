from __future__ import annotations

from pydantic import BaseModel, Field


class RawNode(BaseModel):
    name: str
    availability_zone: str
    allocatable_cpu: int
    allocatable_memory_mib: int
    labels: dict[str, str] = Field(default_factory=dict)


class RawPod(BaseModel):
    namespace: str
    name: str
    node_name: str
    owner_kind: str
    owner_name: str
    daemonset: bool = False
    uses_empty_dir: bool = False
    uses_host_path: bool = False
    uses_local_persistent_volume: bool = False
    termination_grace_period_seconds: int = 30
    cpu_millicores: int = 0
    memory_mib: int = 0
    node_selector: dict[str, str] = Field(default_factory=dict)
    hard_anti_affinity_key: str | None = None


class RawWorkload(BaseModel):
    kind: str
    namespace: str
    name: str
    replicas: int
    unavailable_replicas: int = 0


class RawPodDisruptionBudget(BaseModel):
    namespace: str
    name: str
    owner_name: str
    min_available: int
    current_healthy: int


class RawFixture(BaseModel):
    nodes: list[RawNode]
    pods: list[RawPod]
    workloads: list[RawWorkload] = Field(default_factory=list)
    pod_disruption_budgets: list[RawPodDisruptionBudget] = Field(default_factory=list)


class DrainFinding(BaseModel):
    kind: str
    severity: str
    pod: str
    message: str


class NodeDrainReport(BaseModel):
    node: str
    availability_zone: str
    pod_count: int
    blockers: list[DrainFinding]
    warnings: list[DrainFinding]
    total_cpu_millicores: int
    total_memory_mib: int
    remaining_node_capacity_cpu_millicores: int
    remaining_node_capacity_memory_mib: int
    advisory_patches: list[str] = Field(default_factory=list)
