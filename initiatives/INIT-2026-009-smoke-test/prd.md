<!-- FILE: prd.md -->
# PRD: Export Project Reports

**Initiative:** INIT-2026-009-smoke-test
**Owner (PM):** @smoke-tester
**Last updated:** 2026-04-12
**Profile:** Standard
**BRD:** `brd.md` (если есть)

---

## Цель и ожидаемый эффект

- **Проблема:** {Пользователи не могут выгрузить отчёты по проектам для внешнего анализа}
- **Почему сейчас:** {Запросы от enterprise-клиентов на интеграцию с BI-системами}
- **Цель (Outcome):** {Снижение time-to-insight для project managers на 40% за счёт автоматической выгрузки}

## Пользователи и сценарии

- **Primary personas:** {Project Manager, Team Lead}
- **Top JTBD / сценарии:**
  1. {PM экспортирует сводный отчёт по проекту в CSV для анализа в Excel}
  2. {Team Lead выгружает JSON-отчёт для автоматической загрузки в BI-дашборд}
  3. {Admin запрашивает массовый экспорт для аудита}

## Метрики успеха

| Метрика | Baseline | Target | Период | Источник |
|---|---:|---:|---|---|
| {export_requests_per_week} | {0} | {100} | {30d} | {APM} |
| {export_p95_duration_seconds} | {n/a} | {30} | {30d} | {APM} |

## Scope

**In-scope:**
- REST API для инициирования экспорта проектного отчёта (REQ-EXPORT-001)
- Поддержка форматов JSON и CSV (REQ-EXPORT-002)
- Асинхронная генерация с нотификацией о готовности (REQ-EXPORT-003)

**Non-goals:**
- Real-time streaming экспорт
- Экспорт в PDF/XLSX (будущие итерации)

## Риски и ограничения

- **{Большие проекты}:** {Экспорт проектов >10K записей может занять >30s — требуется async обработка}
- **{Нагрузка на БД}:** {Массовые экспорты могут создать нагрузку — mitigation: rate limiting}

## Требования (ссылки на REQ)

Реестр требований — в `requirements.yml`. Здесь только ссылки:

- `REQ-EXPORT-001` (P0): {REST API для создания экспорта}
- `REQ-EXPORT-002` (P1): {Поддержка JSON и CSV форматов}
- `REQ-EXPORT-003` (P1): {Асинхронная генерация с нотификацией}
- `REQ-EXPORT-004` (P1): {Latency P95 < 30s для экспорта}

## Приёмка

- Acceptance tests: `tests/e2e/export.spec.ts` — {end-to-end тесты экспорта}
- Definition of done по профилю: `.specify/memory/constitution.md#профили`
