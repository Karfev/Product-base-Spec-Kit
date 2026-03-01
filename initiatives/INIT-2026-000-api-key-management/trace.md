<!-- FILE: trace.md -->
# Traceability: INIT-2026-000-api-key-management

**Профиль:** Standard
**Последнее обновление:** 2026-03-01

> RTM генерируется автоматически из `requirements.yml` в CI (L5).
> Этот файл — человекочитаемый вид; поддерживайте синхронно с `requirements.yml`.

| REQ-ID | Priority | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|---|
| `REQ-AUTH-001` | P0 | `decisions/ADR-0001-storage.md` | `openapi.yaml#/paths/~1api-keys/post` | `schemas/api-key.schema.json` | `api-keys.spec.ts::REQ-AUTH-001` | — |
| `REQ-AUTH-002` | P0 | — | `contracts/openapi.yaml#/paths/~1api-keys~1{id}/delete` | — | `tests/api/api-keys.spec.ts::REQ-AUTH-002` | — |
| `REQ-AUTH-003` | P1 | — | `contracts/openapi.yaml#/paths/~1api-keys/get` | — | `tests/api/api-keys.spec.ts::REQ-AUTH-003` | — |
| `REQ-AUTH-004` | P1 | — | — | — | `tests/perf/auth-latency.jmx::REQ-AUTH-004` | `ops/slo.yaml#api-key-auth-latency` |
| `REQ-AUTH-005` | P1 | — | `contracts/openapi.yaml#/paths/~1api-keys/post` | — | `tests/api/api-keys.spec.ts::REQ-AUTH-005` | — |
