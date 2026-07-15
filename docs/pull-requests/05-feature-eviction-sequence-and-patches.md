## Problem

DrainDoctor could identify blockers, but it still did not tell operators what order a drain would likely encounter pods in or what remediation they might consider.

## Approach

- added an ordered eviction sequence to the node report
- emitted advisory patch snippets for the strongest blockers already detected
- kept the report fully read-only by returning suggestions as plain text only

## Important decisions

- ordered eviction guidance to surface easier pods first and DaemonSet-backed pods last, since those usually require separate handling
- only generated advisory patches for currently modeled blocker types rather than inventing generic recommendations
- kept patch output as plain YAML strings to make the guidance easy to inspect without implying automation

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run drain-doctor node ip-10-0-42-17 --fixtures tests/fixtures/node-drain`

## Known limitations

- advisory patches are examples and may still require additional workload-specific review
- eviction ordering is heuristic and not a promise of exact kubectl drain behavior

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Disruption claims are evidence-based

## Review findings

- no material findings after local self-review
