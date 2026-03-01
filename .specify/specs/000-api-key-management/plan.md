<!-- FILE: .specify/specs/{NNN}-{slug}/plan.md -->
# Plan: 000-api-key-management

**Initiative:** INIT-2026-000-api-key-management
**Owner:** @platform-team
**Last updated:** 2026-03-01

## Architecture choices

- Bcrypt hashing (work_factor=10) для хранения секретов API-ключей → ADR: `decisions/INIT-2026-000-ADR-0001-storage.md`
- Redis-кэш (TTL 60s) для fast-path аутентификации с явной инвалидацией при revoke

## Contracts impact

> Все пути ниже — относительно директории инициативы `initiatives/INIT-2026-000-api-key-management/`.

**OpenAPI** (`contracts/openapi.yaml`):

- `GET /api-keys` — новый endpoint: листинг ключей аутентифицированного пользователя (REQ-AUTH-003)
- `POST /api-keys` — новый endpoint: создание ключа, возвращает secret однократно (REQ-AUTH-001, REQ-AUTH-005)
- `DELETE /api-keys/{id}` — новый endpoint: отзыв ключа (REQ-AUTH-002)

**AsyncAPI** (`contracts/asyncapi.yaml`):

- Не используется — sync-only API

**Schemas** (`contracts/schemas/`):

- `api-key.schema.json` — новая схема объекта ApiKey (без поля secret)

## Data changes

- Новая таблица `api_keys`: id UUID PK, user_id FK→users, name TEXT, secret_hash TEXT, created_at TIMESTAMPTZ, expires_at TIMESTAMPTZ nullable, last_used_at TIMESTAMPTZ nullable
- Индекс: `api_keys_user_id_idx ON api_keys(user_id)` для быстрого листинга по пользователю
- Migration script: аддитивная миграция, полностью обратимая через `DROP TABLE api_keys`

## Observability & SLO impact

- Метрики:
  - Counter `api_key_auth_total{result: success|expired|revoked|not_found}` — трафик аутентификации по результату
  - Histogram `api_key_auth_duration_seconds` — задержка auth middleware (цель: P95 < 10ms при cache hit)
  - Counter `api_key_operations_total{operation: create|revoke|list}` — CRUD операции
- Логи: структурированные с полями `key_id`, `user_id`, `result`, `cache_hit`; секрет никогда не логируется
- Трейсы: span `auth.api_key.validate` с атрибутами `cache.hit`, `key.expired`
- SLO: `ops/slo.yaml#api-key-auth-latency` — новый SLO, создаём (REQ-AUTH-004)

## Rollout & rollback

- Feature flag: `platform.api_keys.enabled` — поэтапное включение через LaunchDarkly
- Canary: да, 5% enterprise-клиентов на этапе 2
- Rollback: выключить feature flag (RTO < 5 минут)
- Подробности: `delivery/rollout.md`

## Risks

- **Cache invalidation lag при revoke:** Redis TTL 60s создаёт окно компрометации → mitigation: явная инвалидация `DEL api_key:{hash}` при каждом DELETE-запросе; TTL только как failsafe
- **bcrypt latency при создании ключа:** ~100ms на хэширование → mitigation: хэширование только при создании, не при каждом auth-запросе; допустимо для редкой операции
