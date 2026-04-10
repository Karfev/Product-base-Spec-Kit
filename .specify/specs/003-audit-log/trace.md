<!-- FILE: .specify/specs/003-audit-log/trace.md -->
# Traceability: 003-audit-log

| REQ-ID | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|
| `REQ-AUDIT-001` | `decisions/INIT-2026-003-ADR-0001-storage-strategy.md` | `contracts/asyncapi.yaml#/channels/audit.event.recorded` | `contracts/schemas/audit-event.schema.json` | `tests/unit/audit-event-mapper.spec.ts::REQ-AUDIT-001` | — |
| `REQ-AUDIT-002` | — | `contracts/openapi.yaml#/paths/~1audit-logs/get` | `contracts/schemas/audit-event.schema.json` | `tests/contract/audit-logs-api.spec.ts::REQ-AUDIT-002` | — |
| `REQ-AUDIT-003` | — | `contracts/openapi.yaml#/paths/~1audit-logs~1export/get` | — | `tests/contract/audit-logs-export.spec.ts::REQ-AUDIT-003` | — |
| `REQ-AUDIT-004` | `decisions/INIT-2026-003-ADR-0001-storage-strategy.md` | `contracts/openapi.yaml#/paths/~1audit-logs/get` | — | — | `ops/slo.yaml#audit-query-latency` |
| `REQ-AUDIT-005` | `decisions/INIT-2026-003-ADR-0001-storage-strategy.md` | — | — | — | `ops/slo.yaml#audit-query-latency` |
