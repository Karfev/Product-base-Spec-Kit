<!-- FILE: .specify/specs/002-notification-preferences/tasks.md -->
# Tasks: 002-notification-preferences

**Initiative:** INIT-2026-002-notification-preferences
**Owner:** @platform-team

> Test strategy matrix: `docs/testing/test-strategy.md`

## Task list

- [ ] **T1: Contracts** — Контракты уже заполнены в Phase 2. Проверить валидность:
  - OpenAPI: `initiatives/INIT-2026-002-notification-preferences/contracts/openapi.yaml` — 4 endpoints (GET, PATCH channels, PATCH frequency, DELETE category)
  - AsyncAPI: `initiatives/INIT-2026-002-notification-preferences/contracts/asyncapi.yaml` — 2 events (preference.updated, category.opted-out)
  - Команда: `make lint-contracts`
  - REQ: REQ-NOTIF-001, REQ-NOTIF-002, REQ-NOTIF-003, REQ-NOTIF-004, REQ-NOTIF-006

- [ ] **T2a: RED tests** — Написать falling тесты:
  - Unit tests (`tests/unit/notification-preferences/`):
    - `preference.service.spec.ts` — lazy init defaults, channel validation, frequency validation
    - `mandatory-category.guard.spec.ts` — is_mandatory=true → reject opt-out (REQ-NOTIF-004)
  - Contract tests (`tests/contract/notification-preferences/`):
    - `openapi-compliance.spec.ts` — все 4 endpoints соответствуют OpenAPI schema
    - `asyncapi-compliance.spec.ts` — event payloads соответствуют AsyncAPI schema
  - Команды: `make test-unit` + `make test-contract`
  - REQ: REQ-NOTIF-001..004, REQ-NOTIF-006

- [ ] **T2b: GREEN implementation** — Реализовать:
  - DB schema migration: `notification_preferences`, `category_preferences`, `notification_categories`, `preference_audit_log`
  - Service: `NotificationPreferenceService` — CRUD + mandatory guard + audit logging
  - Controllers: 4 REST endpoints
  - Event publisher: `notifications.preference.updated`, `notifications.category.opted-out`
  - Команды: `make test-unit` + `make test-contract` — все зелёные
  - REQ: все REQ-NOTIF-*

- [ ] **T3: Integration tests** — Интеграционные тесты в реальном окружении:
  - `tests/integration/notification-preferences.spec.ts`:
    - Full CRUD flow с реальной PostgreSQL
    - Event publishing через реальный RabbitMQ
    - Lazy init при первом GET
    - Mandatory category guard с seed data
  - Команда: `make test-integration`
  - REQ: REQ-NOTIF-001..004, REQ-NOTIF-006

- [ ] **T4: Observability** — Метрики и SLO:
  - Добавить metrics: `notification_preferences_api_latency_ms` (histogram), `notification_preferences_opt_out_total` (counter)
  - Обновить `ops/slo.yaml` — добавить SLO `notification-preferences-latency` (P95 < 200ms)
  - Structured logging: user_id, action, category_id, result
  - Perf test: `tests/perf/notification-preferences.jmx`
  - Команда: `make test-perf`
  - REQ: REQ-NOTIF-005

- [ ] **T5: Trace + Changelog** — Трассировка и документация:
  - Обновить `.specify/specs/002-notification-preferences/trace.md` — заполнить RTM
  - Обновить `initiatives/INIT-2026-002-notification-preferences/changelog/CHANGELOG.md`
  - Команда: `make check-trace`
  - REQ: все REQ-NOTIF-*

- [ ] **T6: PRR checklist** — Production Readiness:
  - Пройти все пункты `ops/prr-checklist.md`
  - Проверить: deployment config, health check, graceful shutdown, secrets management
  - Финальная проверка: `make check-all`

## Definition of done (по профилю)

| Чекпойнт | Minimal | **Standard** ← наш профиль | Extended |
|---|---|---|---|
| requirements.yml заполнен | MUST | **MUST** | MUST |
| spec/plan/tasks.md заполнены | MUST | **MUST** | MUST |
| Контракты валидны (lint/validate) | — | **MUST** | MUST |
| trace.md заполнен | — | **MUST** | MUST |
| slo.yaml и prr-checklist.md | — | **MUST** | MUST |
| threat-model.md | — | — | MUST |
| CI gates зелёные | MUST | **MUST** | MUST |
