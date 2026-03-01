<!-- FILE: .specify/specs/{NNN}-{slug}/tasks.md -->
# Tasks: 000-api-key-management

**Initiative:** INIT-2026-000-api-key-management
**Owner:** @platform-team

## Task list

- [ ] **T1:** Добавить пути `/api-keys` (GET, POST) и `/api-keys/{id}` (DELETE) в `contracts/openapi.yaml` + прогнать линтеры локально (`make lint-contracts`)
- [ ] **T2a:** Написать `tests/api/api-keys.spec.ts` с тест-кейсами для REQ-AUTH-001..005 (create, revoke, list, expiry, secret-never-returned) — убедиться что тесты **падают** (RED)
- [ ] **T2b:** Реализовать `KeyService` (CRUD в PostgreSQL) + `AuthMiddleware` (Redis lookup → DB fallback, bcrypt verify) — убедиться что тесты **зелёные** (GREEN)
- [ ] **T3:** Интеграционные тесты с реальным PostgreSQL + Redis (docker-compose в CI) — проверить revocation propagation < 60s
- [ ] **T4:** Добавить Prometheus-метрики (`api_key_auth_total`, `api_key_auth_duration_seconds`), обновить `ops/slo.yaml` с реальными alert-порогами (`auth_p95_ms > 25ms` warning, `> 50ms` critical)
- [ ] **T5:** Обновить `.specify/specs/000-api-key-management/trace.md` + `initiatives/INIT-2026-000-api-key-management/changelog/CHANGELOG.md` (версия 0.2.0 после реализации)
- [ ] **T6:** Пройти все P0-пункты из `ops/prr-checklist.md`: runbook, dashboard link, trace_id в логах, feature flag документация

## Definition of done (по профилю)

| Чекпойнт | Minimal | Standard | Extended |
|---|---|---|---|
| requirements.yml заполнен | MUST | MUST | MUST |
| spec/plan/tasks.md заполнены | MUST | MUST | MUST |
| Контракты валидны (lint/validate) | — | MUST | MUST |
| trace.md заполнен | — | MUST | MUST |
| slo.yaml и prr-checklist.md | — | MUST | MUST |
| threat-model.md | — | — | MUST |
| CI gates зелёные | MUST | MUST | MUST |
