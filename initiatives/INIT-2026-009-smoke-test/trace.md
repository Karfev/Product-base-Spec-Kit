<!-- FILE: trace.md -->
# Traceability: INIT-2026-009-smoke-test

**Профиль:** Standard
**Последнее обновление:** 2026-04-12

> RTM генерируется автоматически из `requirements.yml` в CI (L5).
> Этот файл — человекочитаемый вид; поддерживайте синхронно с `requirements.yml`.

| REQ-ID | Priority | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|---|
| `REQ-EXPORT-001` | P0 | `decisions/INIT-2026-009-ADR-0001-async-queue.md` | `contracts/openapi.yaml#/paths/~1exports/post` | `contracts/schemas/export.schema.json` | `tests/e2e/export.spec.ts::REQ-EXPORT-001` | — |
| `REQ-EXPORT-002` | P1 | — | `contracts/openapi.yaml#/paths/~1exports/post` | — | `tests/e2e/export.spec.ts::REQ-EXPORT-002` | — |
| `REQ-EXPORT-003` | P1 | `decisions/INIT-2026-009-ADR-0001-async-queue.md` | `contracts/asyncapi.yaml#/channels/export.report.completed`, `contracts/openapi.yaml#/paths/~1exports~1{id}/get` | — | `tests/e2e/export.spec.ts::REQ-EXPORT-003` | — |
| `REQ-EXPORT-004` | P1 | — | — | — | `tests/perf/export-latency.jmx::REQ-EXPORT-004` | `ops/slo.yaml#export-latency` |
