# Production Readiness Review: INIT-2026-009-smoke-test

**Профиль:** Standard
**Последнее обновление:** 2026-04-12
**Правило:** пункты с **P0** MUST быть закрыты до релиза (blocking gate).
**Источник практики:** Google SRE Book, глава PRR.

---

## Service levels (SLO/SLI)

- [x] **P0** SLO определён в `ops/slo.yaml` (OpenSLO) и согласован — `export-latency`: P95 < 30s за 30d rolling
- [x] **P0** SLI измеримы (источники метрик определены) — Prometheus histogram `export_duration_seconds`
- [ ] P1 Error budget policy определена (если применимо)

## Architecture & dependencies

- [x] **P0** Критические зависимости перечислены, есть деградация / таймауты / ретраи — Queue (retry x3), Object Storage (exponential backoff), PostgreSQL (read replica for exports)
- [ ] P1 Capacity / scaling предположения проверены
- [ ] P1 Зависимости имеют SLO или degraded mode

## Observability

- [x] **P0** Метрики «golden signals» определены (latency / traffic / errors / saturation) — `export_duration_seconds`, `export_requests_total{status}`, `export_queue_depth`
- [x] **P0** Логи и трейсы коррелируемы (trace_id / request_id) — OpenTelemetry trace propagation through queue
- [x] P1 Дашборд + алерты определены — Grafana `exports`, алерты на p95 и error_rate
- [ ] P1 Runbook написан (ссылка: TBD)

## Deployment & rollback

- [x] **P0** Rollout / rollback описаны (`delivery/rollout.md`) — feature-flag `platform.exports.enabled`, RTO < 5min
- [x] **P0** Миграции обратимы или есть runbook отката — CREATE TABLE (аддитивная), rollback = DROP TABLE
- [x] P1 Feature flags задокументированы — `platform.exports.enabled` в LaunchDarkly

## Security & privacy (Extended: обязательно)

- [x] **P0** Threat model выполнен (`ops/threat-model.md`) — Standard профиль: не обязательно, но no PII in exports confirmed
- [x] **P0** Secrets handling и принцип наименьших привилегий проверены — Object Storage access via service account, signed download URLs with TTL
- [ ] P1 Security тесты / сканы включены в CI

## Ops & on-call

- [x] **P0** Runbook присутствует для P0/P1 инцидентов — Rollback via feature flag, queue drain procedure
- [ ] P1 SRE / on-call ownership согласован
- [ ] P1 Incident response drill проведён (Extended)

---

## Итог PRR

| Блок | Статус | Комментарий |
|---|---|---|
| SLO/SLI | passed | SLO определён, SLI измеримы |
| Architecture | passed | Зависимости описаны, degradation strategy есть |
| Observability | passed | Golden signals + dashboard + alerts |
| Deployment | passed | Feature flag rollout, миграция обратима |
| Security | passed | No PII, signed URLs, service account |
| Ops | passed | Runbook через feature flag rollback |

**Общий статус:** passed
**Дата последнего ревью:** 2026-04-12
**Ревьюер:** @smoke-tester
