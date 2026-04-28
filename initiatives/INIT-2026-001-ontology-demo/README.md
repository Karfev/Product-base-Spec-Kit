# INIT-2026-001-ontology-demo

> **Demo initiative — `evidence/` folder skipped intentionally.**
> This initiative exists as a reference example of the Enterprise IS profile (3-layer architecture + machine-readable subsystem classification + CI validation). It is **not** a real rollout, so the L5 evidence/ output (RTM coverage, PRR status, gaps) is omitted by design. For a worked Enterprise example with real evidence flow, see [`examples/INIT-2026-099-csv-export/`](../../examples/INIT-2026-099-csv-export/).

**Profile:** Enterprise
**Status:** demo (frozen)
**Owner:** @platform-team

## Artifacts

- [`requirements.yml`](./requirements.yml) — L3 requirements with NFR + architecture_views trace
- [`design.md`](./design.md) — architecture overview
- [`subsystem-classification.yaml`](./subsystem-classification.yaml) — IS ontology classification
- [`architecture-views/`](./architecture-views/) — design view stubs
- [`ops/`](./ops/), [`delivery/`](./delivery/) — Enterprise-profile operational artifacts

## What this demo illustrates

- `architecture_views` field in `requirements.yml#trace` (Enterprise pattern, see [`templates/requirements-template.yml`](../../templates/requirements-template.yml))
- Subsystem classification driven by IS ontology in [`domains/is-ontology/`](../../domains/is-ontology/)
- Three-layer Enterprise design.md structure (т-, д-, п- views)
