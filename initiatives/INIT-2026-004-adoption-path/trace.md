<!-- FILE: trace.md -->
# Traceability: INIT-2026-004-adoption-path

**Профиль:** Standard+
**Последнее обновление:** 2026-04-11

> RTM генерируется автоматически из `requirements.yml` в CI (L5).
> Этот файл — человекочитаемый вид; поддерживайте синхронно с `requirements.yml`.

| REQ-ID | Priority | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|---|
| `REQ-{SCOPE}-001` | P0 | `decisions/{INIT}-ADR-0001-{slug}` | `contracts/openapi.yaml#/paths/~1{path}/post` | `contracts/schemas/{entity}.schema.json` | `tests/e2e/{test}::REQ-{SCOPE}-001` | `ops/slo.yaml#{slo-name}` |
| `REQ-{SCOPE}-002` | P1 | — | — | — | `tests/perf/{test}.jmx::REQ-{SCOPE}-002` | `ops/slo.yaml#{slo-name}` |
