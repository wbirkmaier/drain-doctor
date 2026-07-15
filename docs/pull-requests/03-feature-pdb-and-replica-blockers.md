## Problem

Basic pod inventory is not enough to decide whether a node drain is safe. Replica availability and PodDisruptionBudget limits often determine the real blocker.

## Approach

- added workload and PodDisruptionBudget fixture models
- blocked drains when a workload has no spare healthy replica or when the relevant PDB is already at minimum availability
- surfaced already-degraded workloads as warnings before any eviction is attempted

## Important decisions

- keyed PDBs to workload owner names in the fixture model to keep the first slice explicit and deterministic
- treated replica shortfall and exhausted PDBs as blockers rather than soft warnings
- preserved pod traversal ordering in output so findings stay stable and explainable

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run drain-doctor node ip-10-0-42-17 --fixtures tests/fixtures/node-drain`

## Known limitations

- no topology spread, anti-affinity, or remaining capacity analysis yet
- PDB matching is fixture-driven and not yet selector-based

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Disruption claims are evidence-based

## Review findings

- no material findings after local self-review
