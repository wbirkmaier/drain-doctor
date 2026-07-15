# Examples

```bash
uv run drain-doctor node ip-10-0-42-17 --fixtures tests/fixtures/node-drain
```

The shipped fixture includes a non-evictable DaemonSet pod, a workload with local storage, a long termination grace period, a PodDisruptionBudget at minimum availability, and generated advisory patch suggestions for the tightest blockers.
