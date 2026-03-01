# Production Readiness Review: INIT-2026-000-api-key-management

**Профиль:** Standard
**Последнее обновление:** 2026-03-01
**Правило:** пункты с **P0** MUST быть закрыты до релиза (blocking gate).
**Источник практики:** Google SRE Book, глава PRR.

---

## Service levels (SLO/SLI)

- [x] **P0** SLO определён в `ops/slo.yaml` (OpenSLO) и согласован — `api-key-auth-latency` (REQ-AUTH-004): P95 < 10ms за 30d rolling
- [x] **P0** SLI измеримы (источники метрик определены) — Prometheus histogram `http_request_duration_seconds_bucket{handler="/api-keys"}`
- [ ] P1 Error budget policy определена (если применимо)

## Architecture & dependencies

- [x] **P0** Критические зависимости перечислены, есть деградация / таймауты / ретраи — PostgreSQL (timeout 500ms + retry x2), Redis (timeout 10ms + fallback to DB)
- [ ] P1 Capacity / scaling предположения проверены
- [ ] P1 Зависимости имеют SLO или degraded mode

## Observability

- [x] **P0** Метрики «golden signals» определены (latency / traffic / errors / saturation) — `api_key_auth_total{result}`, `api_key_auth_duration_seconds`
- [ ] **P0** Логи и трейсы коррелируемы (trace_id / request_id)
- [ ] P1 Дашборд + алерты определены
- [ ] P1 Runbook написан (ссылка: {ссылка на wiki/confluence/…})

## Deployment & rollback

- [x] **P0** Rollout / rollback описаны (`delivery/rollout.md`) — feature-flag `platform.api_keys.enabled`, RTO < 5min
- [x] **P0** Миграции обратимы или есть runbook отката — новая таблица `api_keys` (аддитивная, rollback = DROP TABLE)
- [ ] P1 Feature flags задокументированы

## Security & privacy (Extended: обязательно)

- [ ] **P0** Threat model выполнен (`ops/threat-model.md`) — Standard профиль: не обязательно
- [x] **P0** Secrets handling и принцип наименьших привилегий проверены — bcrypt hash (ADR-0001), секрет возвращается только один раз, не логируется
- [ ] P1 Security тесты / сканы включены в CI

## Ops & on-call

- [ ] **P0** Runbook присутствует для P0/P1 инцидентов
- [ ] P1 SRE / on-call ownership согласован
- [ ] P1 Incident response drill проведён (Extended)

---

## Итог PRR

| Блок | Статус | Комментарий |
|---|---|---|
| SLO/SLI | open | SLO определён, error budget policy pending |
| Architecture | open | Зависимости описаны, capacity анализ pending |
| Observability | open | Golden signals OK, дашборд/runbook pending |
| Deployment | open | Rollout OK, feature flags документация pending |
| Security | open | Secrets handling OK, threat model не требуется (Standard) |
| Ops | open | Runbook pending |

**Общий статус:** open
**Дата последнего ревью:** 2026-03-01
**Ревьюер:** @platform-team
