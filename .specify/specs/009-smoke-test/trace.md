# Traceability: 009-smoke-test

**Initiative:** INIT-2026-009-smoke-test
**Последнее обновление:** 2026-04-12

| REQ-ID | Priority | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|---|
| `REQ-EXPORT-001` | P0 | `decisions/INIT-2026-009-ADR-0001-async-queue.md` | `contracts/openapi.yaml#/paths/~1exports/post` | `contracts/schemas/export.schema.json` | `tests/e2e/export.spec.ts::REQ-EXPORT-001` | — |
| `REQ-EXPORT-002` | P1 | — | `contracts/openapi.yaml#/paths/~1exports/post` | — | `tests/e2e/export.spec.ts::REQ-EXPORT-002` | — |
| `REQ-EXPORT-003` | P1 | `decisions/INIT-2026-009-ADR-0001-async-queue.md` | `contracts/asyncapi.yaml#/channels/export.report.completed` | — | `tests/e2e/export.spec.ts::REQ-EXPORT-003` | — |
| `REQ-EXPORT-004` | P1 | — | — | — | `tests/perf/export-latency.jmx::REQ-EXPORT-004` | `ops/slo.yaml#export-latency` |
