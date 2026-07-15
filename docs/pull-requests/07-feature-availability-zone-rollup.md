## Problem

Node and nodegroup views help with maintenance, but SREs also need a failure-domain view when a whole availability zone is impaired or being evacuated.

## Approach

- added availability-zone aggregation over member node reports
- exposed `drain-doctor az <zone> --fixtures <dir>`
- preserved embedded per-node evidence so zone output remains auditable rather than purely summarized

## Important decisions

- reused the node analysis as the single source of truth for zone rollups
- kept the AZ report narrowly focused on aggregation rather than simulating a full multi-zone rebalance
- used the same exit-code behavior as node and nodegroup commands when the requested zone is missing

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run drain-doctor az us-west-2a --fixtures tests/fixtures/node-drain`

## Known limitations

- the AZ report does not yet calculate safe concurrent drains or blast-radius tiers
- all zone membership is fixture-driven rather than cloud-provider discovered in this slice

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Disruption claims are evidence-based

## Review findings

- no material findings after local self-review
