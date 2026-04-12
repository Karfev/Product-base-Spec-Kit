# Spec: 009-smoke-test

**Initiative:** INIT-2026-009-smoke-test
**Profile:** Standard
**Owner:** @smoke-tester

## Summary

Добавить REST API для экспорта проектных отчётов в форматах JSON и CSV. Экспорт выполняется асинхронно с уведомлением через event при готовности файла.

## Motivation / Problem

Пользователи не могут выгрузить отчёты по проектам для внешнего анализа в BI-системах. Enterprise-клиенты запросили программный доступ к данным проектов. Подробнее: `initiatives/INIT-2026-009-smoke-test/prd.md`.

## Scope

**In-scope:**
- REST endpoint `POST /exports` для создания запроса на экспорт (REQ-EXPORT-001)
- Поддержка форматов JSON и CSV через параметр `format` (REQ-EXPORT-002)
- Асинхронная генерация отчёта с публикацией события `export.completed` (REQ-EXPORT-003)
- Endpoint `GET /exports/{id}` для получения статуса экспорта (REQ-EXPORT-003)
- NFR: P95 latency < 30s при 100 concurrent exports (REQ-EXPORT-004)

## Non-goals

- Real-time streaming экспорт
- Экспорт в PDF/XLSX (будущие итерации)
- UI для экспорта (только API)
- Scheduled/recurring exports

## API/Contracts

Затронутые файлы контрактов:
- `contracts/openapi.yaml` — два новых пути: `POST /exports`, `GET /exports/{id}`
- `contracts/asyncapi.yaml` — новый канал: `export.report.completed`
- `contracts/schemas/export.schema.json` — схема сущности Export

## User stories

1. As a **Project Manager**, I want to export a project report as CSV, so that I can analyze it in Excel.
2. As a **Team Lead**, I want to export a project report as JSON, so that I can feed it into a BI dashboard automatically.
3. As a **Project Manager**, I want to check the status of my export request, so that I know when the file is ready for download.
4. As an **API consumer**, I want to receive an event when export is ready, so that I can process it without polling.

## Requirements

| REQ-ID | Title | Priority |
|---|---|---|
| REQ-EXPORT-001 | Create export request via REST API | P0 |
| REQ-EXPORT-002 | Support JSON and CSV export formats | P1 |
| REQ-EXPORT-003 | Async export with completion notification | P1 |
| REQ-EXPORT-004 | Export latency P95 under 30 seconds | P1 |

## Test strategy

- **Unit tests:** Export service logic — format conversion, validation, error handling
- **Contract tests:** OpenAPI contract validation (`redocly lint`), AsyncAPI validation (`asyncapi validate`)
- **Integration tests:** End-to-end export flow — create → poll → download → validate file content
- **Performance tests:** P95 latency under load (100 concurrent) via JMeter (`tests/perf/export-latency.jmx`)

## Acceptance criteria

1. Given authenticated user, When `POST /exports` with valid `project_id` and `format=json`, Then return `202` with `export_id` and `status=pending`
2. Given unauthenticated request, When `POST /exports`, Then return `401`
3. Given export request with `format=json`, When export completes, Then result file is valid JSON
4. Given export request with `format=csv`, When export completes, Then result file is valid CSV with headers
5. Given export request, When processing completes, Then `export.completed` event is published with `download_url`
6. Given `export_id`, When `GET /exports/{id}`, Then return current status (`pending|processing|completed|failed`)
7. Given standard load (100 concurrent exports), When measuring P95 latency, Then < 30 seconds

## Rollout

- **Feature flag:** `platform.exports.enabled` (LaunchDarkly)
- **Migration/backfill:** Нет DB-миграций (новая таблица, аддитивное изменение)
- **Monitoring:** Grafana dashboard `exports`, алерты на `export_p95 > 45s`
- **Rollback:** Выключить feature flag (RTO < 5 min)

## Open Questions

- Нет открытых вопросов на данный момент.
