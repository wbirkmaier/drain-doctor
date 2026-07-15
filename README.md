# DrainDoctor

DrainDoctor estimates what will block or degrade a Kubernetes node drain before anyone touches the cluster.

## Current focus

- offline disruption analysis from realistic fixtures
- read-only blocker and warning output
- explicit separation between findings and advisory patches

## Deliberate limits

- no eviction calls
- no patch application
- no claim of perfect scheduler parity

## Running modes

- Offline: fixture-backed node and workload disruption analysis
- Live: planned read-only cluster adapters for pods, PDBs, and node inventory

## Safety

- read-only by default
- deterministic JSON output
- advisory recommendations only

## Status

```bash
uv run drain-doctor node ip-10-0-42-17 --fixtures tests/fixtures/node-drain
uv run drain-doctor nodegroup workers-a --fixtures tests/fixtures/node-drain
```

The current slice analyzes a node or nodegroup from offline fixtures and reports blockers, warnings, PodDisruptionBudget exhaustion, replica shortfall risk, conservative rescheduling risk, ordered eviction guidance, and advisory patch suggestions. Broader zone analysis lands in later slices.
