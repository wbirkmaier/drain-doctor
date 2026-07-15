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

Repository scaffolding and CLI baseline are in place. Drain simulation slices land next.
