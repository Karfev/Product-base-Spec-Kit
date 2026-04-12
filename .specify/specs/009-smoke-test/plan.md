# Plan: 009-smoke-test

**Initiative:** INIT-2026-009-smoke-test
**Profile:** Standard
**Last updated:** 2026-04-12

## Architecture choices

| Decision | ADR | REQ |
|---|---|---|
| Queue-based async processing для экспорта | `decisions/INIT-2026-009-ADR-0001-async-queue.md` | REQ-EXPORT-003, REQ-EXPORT-004 |

**Подход:** POST /exports → enqueue job → worker генерирует файл → upload в Object Storage → publish `export.completed` event → клиент скачивает по download_url.

## Contracts impact

**OpenAPI (новые пути, non-breaking):**
- `POST /exports` — создание запроса на экспорт (202 Accepted)
- `GET /exports/{id}` — получение статуса и download_url

**AsyncAPI (новый канал, non-breaking):**
- `export.report.completed` — событие готовности файла

**JSON Schema:**
- `contracts/schemas/export.schema.json` — сущность Export

> Все изменения аддитивные — breaking change check не требуется. Верификация: `make lint-contracts`

## Data changes

- **Новая таблица `exports`:** id (UUID PK), project_id (UUID FK), format (enum), status (enum), download_url (nullable), created_at, completed_at
- **Миграция:** аддитивная (CREATE TABLE), rollback = DROP TABLE
- **Backfill:** не требуется

## Observability & SLO impact

**Новые метрики:**
- `export_duration_seconds` (histogram) — время генерации
- `export_requests_total{status}` (counter) — количество запросов
- `export_queue_depth` (gauge) — глубина очереди

**SLO (`ops/slo.yaml#export-latency`):**
- Target: P95 < 30s, 30d rolling window
- Budget: 5% of requests may exceed target

**Алерты:**
- `export_p95_seconds > 45s` → warning
- `export_p95_seconds > 60s` → critical
- `export_error_rate > 1%` → critical

## Test strategy

| Level | Scope | Tool | REQ |
|---|---|---|---|
| Unit | Format conversion, validation | Jest | REQ-EXPORT-002 |
| Contract | OpenAPI lint, AsyncAPI validate | redocly, asyncapi-cli | REQ-EXPORT-001, 003 |
| Integration | Create → poll → download flow | Supertest | REQ-EXPORT-001, 002, 003 |
| Performance | P95 under 100 concurrent | JMeter | REQ-EXPORT-004 |

## Rollout & rollback strategy

Подробности: `delivery/rollout.md`

- **Feature flag:** `platform.exports.enabled`
- **Этапы:** Internal → Canary 5% → Production 100%
- **Критерий перехода:** export_p95 < 30s, error_rate < 0.5%
- **Rollback:** выключить flag, RTO < 5 min

## Risks

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| Большие проекты (>10K записей) превышают 30s | P95 SLO violation | Medium | Pagination/streaming в worker, rate limiting |
| Нагрузка на БД при массовых экспортах | Деградация основного API | Low | Read replica, rate limit 10 concurrent/user |
| Object Storage недоступен | Файлы не скачиваются | Low | Retry + exponential backoff, fallback URL TTL |
