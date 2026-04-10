<!-- FILE: .specify/specs/002-notification-preferences/plan.md -->
# Plan: 002-notification-preferences

**Initiative:** INIT-2026-002-notification-preferences
**Owner:** @platform-team
**Last updated:** 2026-04-10

## Architecture choices

- **Lazy initialization pattern** — preferences создаются при первом GET запросе с дефолтами, а не при регистрации пользователя. Уменьшает coupling с auth-сервисом. → ADR: `decisions/INIT-2026-002-ADR-0001-lazy-init.md` (proposed)
- **Aggregate root = UserPreference** — все изменения категорий идут через агрегат, не напрямую. Обеспечивает консистентность mandatory-guard. → Без ADR (стандартный DDD паттерн)
- **Event sourcing не используется** — CRUD достаточен для данного объёма. Audit trail через отдельную таблицу preference_audit_log. → Без ADR

## Contracts impact

> Все пути ниже — относительно директории инициативы `initiatives/INIT-2026-002-notification-preferences/`.

**OpenAPI** (`contracts/openapi.yaml`):
- `GET /notification-preferences` — добавляем (REQ-NOTIF-001)
- `PATCH /notification-preferences/channels` — добавляем (REQ-NOTIF-002)
- `PATCH /notification-preferences/frequency` — добавляем (REQ-NOTIF-003)
- `DELETE /notification-preferences/categories/{categoryId}` — добавляем (REQ-NOTIF-004)

**AsyncAPI** (`contracts/asyncapi.yaml`):
- Channel `notifications.preferences.updated` — добавляем (REQ-NOTIF-006)
- Channel `notifications.preferences.category-opted-out` — добавляем (REQ-NOTIF-004)

**Schemas** (`contracts/schemas/`):
- NotificationPreferences, CategoryPreference, UpdateChannelsRequest, UpdateFrequencyRequest — inline в openapi.yaml
- PreferenceUpdatedPayload, CategoryOptedOutPayload — inline в asyncapi.yaml

## Data changes

- Таблица `notification_preferences`: user_id (PK), default_channel, digest_frequency, quiet_hours_start, quiet_hours_end, created_at, updated_at
- Таблица `category_preferences`: user_id + category_id (composite PK), enabled, channel_override, updated_at
- Таблица `notification_categories`: category_id (PK), name, description, is_mandatory — seed data
- Таблица `preference_audit_log`: id, user_id, action, changed_fields, previous_values, new_values, created_at — GDPR audit trail
- Migration: one-time schema creation, no backfill (lazy init)
- Индексы: notification_preferences(user_id), category_preferences(user_id, category_id)

## Observability & SLO impact

- Метрики:
  - `notification_preferences_api_latency_ms` (histogram) — P95/P99 по endpoint
  - `notification_preferences_opt_out_total` (counter) — opt-out events по category
  - `notification_preferences_channel_distribution` (gauge) — distribution по каналам
- Логи: structured JSON — user_id, action, category_id, result (success/error)
- Трейсы: span на каждый API call + span на event publish
- SLO: `ops/slo.yaml#notification-preferences-latency` — P95 < 200ms, P99 < 500ms (REQ-NOTIF-005)

## Rollout & rollback

- Feature flag: `notification-preferences-enabled` — Unleash/LaunchDarkly
- Canary: 5% → 25% → 100% (по 24h на каждый этап)
- Rollback: отключить feature flag → API возвращает 404 → fallback на дефолтные предпочтения
- Подробности: `delivery/rollout.md`

## Risks

- **Нагрузка при launch** — массовые GET запросы с lazy init создают burst writes. Mitigation: rate limiting на init, connection pool sizing
- **GDPR audit log рост** — при частых изменениях audit_log растёт. Mitigation: retention policy 2 года, partitioning по дате
- **Event delivery guarantee** — at-least-once delivery может привести к дублям в consumers. Mitigation: idempotent consumers по eventId
