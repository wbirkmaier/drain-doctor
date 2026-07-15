## Problem

Operators rarely think about one node in isolation. They need to see whether a whole worker group has recurring blockers or whether one bad node is the outlier.

## Approach

- added nodegroup metadata to fixture nodes
- rolled up per-node drain reports into a nodegroup report
- exposed `drain-doctor nodegroup <name> --fixtures <dir>`

## Important decisions

- reused the existing node analysis rather than creating a second analysis path for nodegroups
- kept the rollup explicit by embedding member node reports instead of collapsing everything into counters only
- used the same exit-code behavior as single-node analysis when a requested group is missing

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run drain-doctor nodegroup workers-a --fixtures tests/fixtures/node-drain`

## Known limitations

- nodegroup membership is fixture-driven and not cloud-provider aware yet
- the rollup does not yet compute recommended batch sizes or parallel drain limits

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Disruption claims are evidence-based

## Review findings

- fixed the expected remaining-memory value for the second node after validating the nested nodegroup output against the actual report
