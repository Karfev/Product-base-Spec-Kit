# Production Readiness Review: INIT-2026-000-api-key-management

**Профиль:** Standard
**Последнее обновление:** 2026-03-01
**Правило:** пункты с **P0** MUST быть закрыты до релиза (blocking gate).
**Источник практики:** Google SRE Book, глава PRR.

---

## Service levels (SLO/SLI)

- [x] **P0** SLO определён в `ops/slo.yaml` (OpenSLO) и согласован — `api-key-auth-latency` (REQ-AUTH-004): P95 < 10ms за 30d rolling
- [x] **P0** SLI измеримы (источники метрик определены) — Prometheus histogram `http_request_duration_seconds_bucket{handler="/api-keys"}`
- [x] P1 Error budget policy определена (если применимо) — заложена в SLO: 99.9% availability за 30d rolling window

## Architecture & dependencies

- [x] **P0** Критические зависимости перечислены, есть деградация / таймауты / ретраи — PostgreSQL (timeout 500ms + retry x2), Redis (timeout 10ms + fallback to DB)
- [x] P1 Capacity / scaling предположения проверены — design.md#т-1, 10k TPS, 4 nodes, shared-nothing architecture
- [x] P1 Зависимости имеют SLO или degraded mode — PostgreSQL fallback при Redis outage, graceful degradation

## Observability

- [x] **P0** Метрики «golden signals» определены (latency / traffic / errors / saturation) — `api_key_auth_total{result}`, `api_key_auth_duration_seconds`
- [x] **P0** Логи и трейсы коррелируемы (trace_id / request_id) — middleware инструментирует все requests с OpenTelemetry trace context
- [x] P1 Дашборд + алерты определены — Grafana dashboard in platform-dashboards repo, alerting rules in ops/alerts.yaml
- [ ] P1 Runbook написан (ссылка: ops/runbook.md — TODO)

## Deployment & rollback

- [x] **P0** Rollout / rollback описаны (`delivery/rollout.md`) — feature-flag `platform.api_keys.enabled`, RTO < 5min
- [x] **P0** Миграции обратимы или есть runbook отката — новая таблица `api_keys` (аддитивная, rollback = DROP TABLE)
- [x] P1 Feature flags задокументированы — delivery/rollout.md section "Feature Flags", gradual rollout 1% → 10% → 50% → 100%

## Security & privacy (Standard profile)

- [x] **P0** Threat model не требуется (Standard профиль) — Extended профиль обязывает ops/threat-model.md, но Standard требует только secrets handling
- [x] **P0** Secrets handling и принцип наименьших привилегий проверены — bcrypt hash (ADR-0001), секрет возвращается только один раз, не логируется
- [x] P1 Security тесты / сканы включены в CI — SAST в CI pipeline, secrets scanner (truffleHog) на всех commits

## Ops & on-call

- [ ] **P0** Runbook присутствует для P0/P1 инцидентов — ops/runbook.md (draft, pending SRE review)
- [x] P1 SRE / on-call ownership согласован — @platform-sre-oncall owns API key auth path, escalation: @platform-team lead
- [ ] P1 Incident response drill проведён (Extended profile requirement, not applicable to Standard)

---

## Итог PRR

| Блок | Статус | Комментарий |
|---|---|---|
| SLO/SLI | green | SLO определён, error budget policy согласована |
| Architecture | green | Зависимости, capacity, degradation описаны |
| Observability | amber | Golden signals + traces OK, runbook draft pending SRE review |
| Deployment | green | Rollout, rollback, feature flags все задокументированы |
| Security | green | Secrets handling OK (Standard профиль) |
| Ops | amber | On-call ownership согласовано, runbook draft in progress |

**Общий статус:** amber (ready for SRE review before production)
**Дата последнего ревью:** 2026-04-13
**Ревьюер:** @platform-team
