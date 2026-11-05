# Production Readiness Review: INIT-2026-099-csv-export

**Профиль:** Standard
**Последнее обновление:** 2026-04-28
**Правило:** пункты с **P0** MUST быть закрыты до релиза (blocking gate).
**Команда верификации:** `/speckit-prr-status INIT-2026-099-csv-export`

---

## 1. Service levels (SLO/SLI)

- [x] **P0** SLO определены в [`ops/slo.yaml`](./slo.yaml): `csv-export-sync-latency` (REQ-EXPORT-004), `csv-export-availability` (PRR)
- [x] **P0** SLI измеримы — Prometheus histogram `http_request_duration_seconds_bucket{endpoint="/export"}`
- [x] P1 Error budget policy: 0.5% downtime/month → 3.6h. При burn > 50% за 7 дней — пауза релизов.

## 2. Architecture & dependencies

- [x] **P0** Критические зависимости с таймаутами:
  - PostgreSQL: timeout 10s на streaming query, fallback — partial export + warning header
  - Redis: timeout 100ms на queue ops, fallback — синхронный режим (degraded)
  - S3: timeout 30s на multipart upload, retry 3x с exp backoff
- [x] P1 Capacity: 1M записей/экспорт, 10k экспортов/день, < 2 GB RAM/процесс (streaming, не материализация)
- [x] P1 Graceful degradation: при сбое S3 — fallback на синхронный режим до 100k

## 3. Observability

- [x] **P0** Golden signals: latency (P50/P95/P99), traffic (exports/min), errors (rate by code), saturation (CPU/mem)
- [x] **P0** Логи: `export_started`, `export_completed`, `export_failed` с trace_id и job_id (OpenTelemetry)
- [x] **P0** Trace: span на каждую SQL-query, S3-upload, queue-op
- [ ] P1 Runbook (draft, pending SRE review, ETA 2026-05-05)

## 4. Deployment & rollback

- [x] **P0** Rollout описан в [`delivery/rollout.md`](../delivery/rollout.md) — feature flag `platform.csv_export.enabled`
- [x] **P0** Rollback: flip feature flag через LaunchDarkly, RTO < 1 минута
- [x] **P0** Миграции БД: нет (stateless)
- [x] P1 Feature flags задокументированы:
  - `platform.csv_export.enabled` (default: off)
  - `platform.csv_export.sync_threshold` (default: 100000)
  - `platform.csv_export.job_retention_hours` (default: 24)

## 5. Security & privacy

- [x] **P0** Sensitive fields exclusion (REQ-EXPORT-005): hardcoded blocklist + регрессионный тест
- [x] **P0** Authorization: только владелец account может экспортировать, role data-admin или admin
- [x] **P0** Signed URLs для async-файлов: HMAC-SHA256, 24h expiration, single-use
- [x] P1 Audit log: каждый export пишется в `audit_events` с user_id, account_id, entity_type, record_count
- [x] P1 SAST + secrets scanner в CI

## 6. Ops & on-call

- [x] **P0** Ownership: `@platform-sre-oncall`
- [x] P1 Escalation: `@platform-team-lead` при P0/P1 инцидентах
- [ ] P1 Runbook сценария «export job stuck в processing > 1h» (TODO, blocker для P1)
- [ ] P1 Drill: симуляция отказа S3 на staging — запланировать на 2026-05-10

---

## Итог PRR

| Блок | Статус | Комментарий |
|---|---|---|
| Service levels | green | SLO + SLI определены, error budget policy утверждена |
| Architecture | green | Dependencies с таймаутами/фолбэками, capacity подтверждён |
| Observability | amber | Golden signals + logs OK, runbook в работе |
| Deployment | green | Rollout/rollback план, FF задокументированы |
| Security | green | Blocklist + audit log + signed URLs |
| Ops | amber | Ownership согласован, runbook + drill — TODO |

**Общий статус:** **amber** (готов на 80%, blocking — runbook draft).
**Готовность к релизу:** после закрытия двух P1 пунктов в Observability и Ops.
**Дата следующего ревью:** 2026-05-05.
