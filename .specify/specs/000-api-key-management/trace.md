<!-- FILE: .specify/specs/{NNN}-{slug}/trace.md -->
# Traceability: 000-api-key-management

| REQ-ID | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|
| `REQ-AUTH-001` | `decisions/INIT-2026-000-ADR-0001-storage.md` | `contracts/openapi.yaml#/paths/~1api-keys/post` | `contracts/schemas/api-key.schema.json` | `tests/api/api-keys.spec.ts::REQ-AUTH-001` | — |
| `REQ-AUTH-002` | — | `contracts/openapi.yaml#/paths/~1api-keys~1{id}/delete` | — | `tests/api/api-keys.spec.ts::REQ-AUTH-002` | — |
| `REQ-AUTH-003` | — | `contracts/openapi.yaml#/paths/~1api-keys/get` | — | `tests/api/api-keys.spec.ts::REQ-AUTH-003` | — |
| `REQ-AUTH-004` | — | — | — | `tests/perf/auth-latency.jmx::REQ-AUTH-004` | `ops/slo.yaml#api-key-auth-latency` |
| `REQ-AUTH-005` | — | `contracts/openapi.yaml#/paths/~1api-keys/post` | — | `tests/api/api-keys.spec.ts::REQ-AUTH-005` | — |
