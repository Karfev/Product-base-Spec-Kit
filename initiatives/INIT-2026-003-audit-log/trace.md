# Traceability: INIT-2026-003-audit-log

**Профиль:** Standard
**Последнее обновление:** 2026-04-10

> RTM генерируется автоматически из `requirements.yml` в CI (L5).
> Этот файл — человекочитаемый вид; поддерживайте синхронно с `requirements.yml`.

| REQ-ID | Priority | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|---|
| `REQ-AUDIT-001` | P0 | `decisions/INIT-2026-003-ADR-0001-storage-strategy.md` | `contracts/asyncapi.yaml#/channels/audit.event.recorded` | `contracts/schemas/audit-event.schema.json` | `tests/unit/audit-event-mapper.spec.ts::REQ-AUDIT-001` | — |
| `REQ-AUDIT-002` | P0 | — | `contracts/openapi.yaml#/paths/~1audit-logs/get` | `contracts/schemas/audit-event.schema.json` | `tests/contract/audit-logs-api.spec.ts::REQ-AUDIT-002` | — |
| `REQ-AUDIT-003` | P1 | — | `contracts/openapi.yaml#/paths/~1audit-logs~1export/get` | — | `tests/contract/audit-logs-export.spec.ts::REQ-AUDIT-003` | — |
| `REQ-AUDIT-004` | P1 | `decisions/INIT-2026-003-ADR-0001-storage-strategy.md` | `contracts/openapi.yaml#/paths/~1audit-logs/get` | — | — | `ops/slo.yaml#audit-query-latency` |
| `REQ-AUDIT-005` | P1 | `decisions/INIT-2026-003-ADR-0001-storage-strategy.md` | — | — | — | `ops/slo.yaml#audit-query-latency` |
