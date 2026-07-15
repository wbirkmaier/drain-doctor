# Threat Model

## Assets

- workload placement metadata
- disruption budgets
- advisory patch output

## Risks

- overstating drain safety from incomplete scheduler modeling
- accidentally mutating cluster state
- leaking cluster-specific identifiers or credentials in logs

## Mitigations

- fixture-first tests with explicit conservative assumptions
- read-only CLI boundaries
- advisory-only recommendations with no apply path
