## Problem

DrainDoctor had a repository baseline but no working drain analysis path.

## Approach

- added typed fixture models for nodes and pods
- implemented conservative blocker and warning detection for a single node drain
- exposed `drain-doctor node <node-name> --fixtures <dir>` with deterministic JSON output

## Important decisions

- kept the first slice limited to one node target so the blocker model could be verified before broader zone or nodegroup simulations
- treated DaemonSet pods and node-local storage as blockers rather than softer warnings
- treated long termination grace periods and `emptyDir` usage as warnings because they degrade or slow a drain without always blocking it

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run drain-doctor node ip-10-0-42-17 --fixtures tests/fixtures/node-drain`

## Known limitations

- no PodDisruptionBudget or replica math yet
- no advisory patch generation yet

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Disruption claims are evidence-based

## Review findings

- no material findings after local self-review
