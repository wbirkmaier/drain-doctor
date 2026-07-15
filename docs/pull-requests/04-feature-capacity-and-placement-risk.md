## Problem

Replica and PDB checks are not enough on their own. Operators also need a conservative view of whether the rest of the cluster appears able to absorb evicted pods.

## Approach

- added remaining-node free CPU and memory calculations from fixture inputs
- added node selector mismatch blockers and hard anti-affinity warnings
- surfaced remaining capacity values in the node drain report

## Important decisions

- treated the capacity model as conservative rather than pretending to be a full scheduler simulation
- blocked on node selector mismatch because the pod would have nowhere obvious to go in the remaining inventory
- exposed remaining free capacity directly in the report so reviewers can inspect the underlying budget rather than only consuming derived findings

## Test evidence

- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- `uv run pytest --cov=src --cov-report=term-missing`
- `uv build`
- `uv run drain-doctor node ip-10-0-42-17 --fixtures tests/fixtures/node-drain`

## Known limitations

- no topology spread or taint/toleration modeling yet
- remaining capacity is computed from fixture allocatable resources and scheduled requests, not real kube-scheduler scoring

## Self-review

- [x] Security reviewed
- [x] No write operations introduced
- [x] Output ordering is deterministic
- [x] Disruption claims are evidence-based

## Review findings

- fixed a unit mismatch bug during review where CPU allocatable was incorrectly multiplied during remaining-capacity calculation
