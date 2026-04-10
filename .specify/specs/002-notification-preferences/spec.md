<!-- FILE: .specify/specs/002-notification-preferences/spec.md -->
# Spec: 002-notification-preferences

**Initiative:** INIT-2026-002-notification-preferences
**Profile:** Standard
**Owner:** @platform-team
**Last updated:** 2026-04-10

## Summary

Реализация API для управления предпочтениями уведомлений пользователей: выбор каналов доставки (email/push/SMS), настройка частоты (immediate/daily/weekly digest), opt-out по категориям. Обеспечивает GDPR compliance через гранулярный opt-out и audit trail.

## Motivation / Problem

Пользователи не могут управлять уведомлениями — всё включено по умолчанию. GDPR-аудит выявил отсутствие гранулярного opt-out. Тикеты поддержки по теме растут на 20%/месяц. Подробнее: `../../../initiatives/INIT-2026-002-notification-preferences/prd.md`

## Scope

- GET /notification-preferences — получение текущих предпочтений (REQ-NOTIF-001)
- PATCH /notification-preferences/channels — обновление каналов доставки (REQ-NOTIF-002)
- PATCH /notification-preferences/frequency — настройка частоты (REQ-NOTIF-003)
- DELETE /notification-preferences/categories/{categoryId} — opt-out по категориям (REQ-NOTIF-004)
- SLO на латентность API P95 < 200ms (REQ-NOTIF-005)
- Доменное событие notifications.preference.updated при изменениях (REQ-NOTIF-006)

## Non-goals

- Управление контентом и шаблонами уведомлений
- Инфраструктура доставки (push-провайдер, SMTP-сервер)
- Admin UI для управления категориями уведомлений
- Bulk-операции для массового изменения preferences

## API/Contracts

- REST: `initiatives/INIT-2026-002-notification-preferences/contracts/openapi.yaml` — 4 endpoint'а
- AsyncAPI: `initiatives/INIT-2026-002-notification-preferences/contracts/asyncapi.yaml` — 2 события
- Schemas: `contracts/schemas/` — NotificationPreferences, CategoryPreference, event payloads

## Test strategy

- Unit: бизнес-логика предпочтений (mandatory category guard, frequency validation, channel validation)
- Integration/contract: API endpoints vs OpenAPI spec, event publishing vs AsyncAPI spec
- E2E/acceptance: полный сценарий "создание → изменение → opt-out → событие опубликовано"

## Rollout

- Flag/guardrail: feature flag `notification-preferences-enabled`, canary 5% → 25% → 100%
- Migration/backfill: lazy initialization — preferences создаются при первом GET запросе с дефолтами
- Monitoring/rollback: P95 latency dashboard, opt-out rate metric, rollback = отключить feature flag

## User stories

- As an end user, I want to see my current notification preferences, so that I know what notifications I will receive and how.
- As an end user, I want to change my notification delivery channel from email to push, so that I receive notifications on my phone instead of inbox.
- As an end user, I want to switch to weekly digest, so that I am not interrupted by individual notifications during the workday.
- As an end user, I want to opt out of marketing notifications, so that I only receive relevant transactional and security alerts.

## Requirements

Ссылки на REQ-ID (реестр в `requirements.yml`):

- `REQ-NOTIF-001` (P0): Получение предпочтений уведомлений
- `REQ-NOTIF-002` (P0): Обновление каналов доставки
- `REQ-NOTIF-003` (P1): Настройка частоты уведомлений
- `REQ-NOTIF-004` (P0): Opt-out по категориям (GDPR)
- `REQ-NOTIF-005` (P1): SLO на латентность API
- `REQ-NOTIF-006` (P1): Событие изменения предпочтений

## Acceptance criteria

- Given авторизованный пользователь When GET /notification-preferences Then 200 с полным набором предпочтений (каналы, частота, категории)
- Given авторизованный пользователь When PATCH /notification-preferences/channels с defaultChannel=push Then 200 и канал обновлён
- Given авторизованный пользователь When PATCH /notification-preferences/frequency с digestFrequency=weekly Then 200 и частота обновлена
- Given не-mandatory категория When DELETE /notification-preferences/categories/{id} Then 200 и категория отключена
- Given mandatory категория (security) When DELETE /notification-preferences/categories/{id} Then 403
- Given любое изменение preferences When сохранено Then событие notifications.preference.updated опубликовано
- Given неавторизованный запрос When любой endpoint Then 401

## Open Questions

| # | Вопрос | Владелец | Дедлайн | Статус |
|---|--------|----------|---------|--------|
| 1 | Нужна ли quiet hours (тихие часы) как отдельная настройка? | @platform-team | 2026-04-20 | open |
| 2 | Максимальное количество категорий — фиксированный список или динамический? | @platform-team | 2026-04-20 | open |
