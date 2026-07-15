# Architecture

DrainDoctor separates inventory loading, normalization, disruption reasoning, and recommendation rendering.

## Planned flow

1. Adapters load pods, controllers, PDBs, and node state.
2. Normalizers convert cluster data into typed disruption inputs.
3. Analysis identifies blockers, warnings, and conservative eviction order.
4. Renderers emit JSON and advisory patch suggestions.
