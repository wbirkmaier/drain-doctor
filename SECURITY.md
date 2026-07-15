# Security

DrainDoctor is intended for read-only disruption analysis.

## Reporting

Use GitHub security reporting for sensitive issues.

## Guardrails

- Do not issue kubectl drain or eviction API calls.
- Do not log kubeconfig contents or cluster credentials.
- Treat fixtures as sanitized public examples only.
