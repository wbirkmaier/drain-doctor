# ADR 0001: Start With Fixture-Backed Drain Simulation

## Status

Accepted

## Context

Drain reasoning needs realistic workload and PDB relationships, but local and CI environments should not depend on a live cluster.

## Decision

Start with fixture-backed node and workload inputs, then layer live adapters on later.

## Consequences

- integration tests stay deterministic
- disruption logic can mature before cluster-specific adapters are added
