<!-- FILE: .specify/specs/{NNN}-{slug}/spec.md -->
# Spec: 000-api-key-management

**Initiative:** INIT-2026-000-api-key-management
**Profile:** Standard
**Owner:** @platform-team
**Last updated:** 2026-03-01

## Summary

Добавляем API-ключи — долгосрочные credentials для программного доступа к платформе. Пользователи смогут создавать, просматривать и отзывать ключи через REST API. Секрет ключа возвращается единственный раз при создании и нигде не хранится в открытом виде.

## Motivation / Problem

Enterprise-клиенты не могут автоматизировать интеграции без постоянных credentials. Bearer token-сессии истекают, вынуждая сервисные аккаунты регулярно переаутентифицироваться — это неприемлемо для unattended-процессов. Детали в PRD: `../../../initiatives/INIT-2026-000-api-key-management/prd.md`

## Scope / Non-goals

**In-scope:**
- Создание именованного API-ключа (с опциональным сроком действия)
- Отзыв API-ключа с распространением < 60s
- Листинг API-ключей без раскрытия секрета
- SLO на задержку аутентификации: P95 < 10ms

**Non-goals:**
- UI-консоль управления ключами (Phase 2)
- Автоматическая ротация ключей
- Scope/permission-ограничения для ключей
- Webhook-уведомления об истечении срока

## User stories

- As a platform integrator, I want to create an API key, so that my service can authenticate without a user session.
- As a platform integrator, I want to list my API keys (without secrets), so that I can audit which keys are active.
- As a platform integrator, I want to revoke a compromised API key, so that unauthorized access is stopped immediately.
- As a platform integrator, I want to set an expiration date on a key, so that temporary access is time-limited automatically.

## Requirements

Ссылки на REQ-ID (реестр в `requirements.yml`):

- `REQ-AUTH-001` (P0): Создание API-ключа — аутентифицированный пользователь создаёт именованный ключ, секрет возвращается один раз
- `REQ-AUTH-002` (P0): Отзыв API-ключа — немедленная инвалидация, распространение < 60s
- `REQ-AUTH-003` (P1): Листинг API-ключей — без поля secret в ответе
- `REQ-AUTH-004` (P1): SLO задержки аутентификации — накладные расходы auth P95 < 10ms
- `REQ-AUTH-005` (P1): Опциональное истечение срока — HTTP 401 KEY_EXPIRED для просроченных ключей

## Acceptance criteria

- Given an authenticated user, When they POST /api-keys with {name}, Then HTTP 201 and plaintext secret returned exactly once in response body
- Given a created key, When stored, Then secret_hash in DB (bcrypt) and secret field absent from all subsequent GET responses
- Given a valid API key, When the owner DELETEs /api-keys/{id}, Then subsequent requests with that key return HTTP 401 within 60 seconds
- Given an authenticated user, When they GET /api-keys, Then all keys returned with id/name/created_at/last_used_at/expires_at and no secret field
- Given a key with expires_at in the past, When used for authentication, Then HTTP 401 with body {code: "KEY_EXPIRED"} is returned
- Given POST /api-keys with expires_at in the past, When submitted, Then HTTP 422 is returned

## Open Questions

<!-- Маркер [NEEDS CLARIFICATION] — канонический тег для незакрытых вопросов.
     Допустимые значения Статус: open | resolved -->
| # | Вопрос | Владелец | Дедлайн | Статус |
|---|--------|----------|---------|--------|
| 1 | [NEEDS CLARIFICATION] Нужна ли поддержка scope-ограничений для ключей? | @pm | 2026-02-20 | resolved |
