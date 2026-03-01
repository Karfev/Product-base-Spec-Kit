# INIT-2026-000-api-key-management

**Initiative:** INIT-2026-000-api-key-management
**Profile:** Standard
**Status:** product
**Owner (PM):** @platform-team
**Tech Lead:** @platform-team
**Last updated:** 2026-03-01

## Описание

Управление API-ключами для аутентификации запросов в платформе. Позволяет enterprise-клиентам создавать долгосрочные credentials для программного доступа без использования логина/пароля.

## Артефакты инициативы

| Файл | Статус | Описание |
|---|---|---|
| `prd.md` | draft | Product Requirements Document |
| `requirements.yml` | draft | Machine-readable registry |
| `design.md` | draft | Architecture design (arc42-lite) |
| `trace.md` | draft | Traceability matrix |
| `contracts/openapi.yaml` | draft | REST API contract |
| `ops/slo.yaml` | draft | SLO definition |
| `ops/prr-checklist.md` | open | Production Readiness Review |
| `changelog/CHANGELOG.md` | current | Change log |

## Связанные L4 спеки

- `.specify/specs/000-api-key-management/` — создание, отзыв и листинг API-ключей с опциональным сроком действия

## Связанные домены и продукты

- Domain: `domains/auth/`
- Product: `products/platform/`
