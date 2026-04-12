---
graduated_from: "INIT-2026-009-smoke-test"
original_id: "INIT-2026-009-ADR-0001-async-queue"
graduated_date: "2026-04-12"
---

# PLAT-0003: Async Queue for Export Processing

- **Status:** accepted
- **Date:** 2026-04-12
- **Deciders:** @smoke-tester
- **Technical Story:** REQ-EXPORT-003, REQ-EXPORT-004

## Context and Problem Statement

Экспорт проектных отчётов может занимать >10s для больших проектов. Синхронная обработка в HTTP-запросе приведёт к таймаутам и плохому UX. Нужно выбрать подход к асинхронной обработке.

## Decision Drivers

- P95 latency < 30s (REQ-EXPORT-004)
- Масштабируемость до 100 concurrent exports
- Простота реализации и мониторинга

## Considered Options

1. **Queue-based async processing** — POST → enqueue job → worker processes → event on completion
2. **Sync processing with long polling** — POST waits until complete, client uses long poll
3. **WebSocket streaming** — Server pushes progress via WebSocket

## Decision Outcome

Chosen option: **1. Queue-based async processing**, because:
- Естественно масштабируется горизонтально (добавить workers)
- HTTP request возвращается мгновенно (202 Accepted)
- Стандартный паттерн для platform — минимальный cognitive overhead
- Event-driven нотификация (AsyncAPI) интегрируется с существующей инфраструктурой

## Consequences

- **Good:** Простой retry mechanism, horizontal scaling, стандартный observability
- **Bad:** Дополнительная инфраструктура (очередь), eventual consistency для статуса
- **Neutral:** Клиент должен либо polling GET /exports/{id}, либо подписаться на event

## Доменные оценки (consilium)

> Сгенерировано `/speckit-consilium` 2026-04-12. Preset: standard.

### Прикладная архитектура

| Пункт | Статус | Комментарий |
|---|---|---|
| Решение соответствует C4 context/containers? | OK | Queue-based async — стандартный паттерн, описан в "Decision Outcome" |
| Нет архитектурных anti-patterns? | OK | Горизонтальное масштабирование workers, нет God service |
| Backward compatibility сохранена? | Замечание | Клиент должен перейти на polling/events — не описан transition path для существующих sync-клиентов |
| Альтернативы рассмотрены с trade-offs? | OK | 3 альтернативы с обоснованием в "Considered Options" |

**Итог:** Замечание — отсутствует transition path для существующих sync-клиентов

### ИБ (Information Security)

| Пункт | Статус | Комментарий |
|---|---|---|
| Auth model определён и адекватен? | Замечание | Auth для POST /exports и GET /exports/{id} не описан — кто может запускать экспорт? |
| PII/ПДн обработка соответствует 152-ФЗ? | Замечание | Экспортируемые данные могут содержать проектную информацию — classification не определён |
| Input validation на всех boundaries? | Замечание | Не описаны ограничения на входные параметры экспорта (размер проекта, частота запросов) |
| Secrets management определён? | OK | Queue credentials — стандартная инфраструктура, не специфична для решения |

**Итог:** Замечание — auth model и data classification для экспорта не определены

### Инфраструктура

| Пункт | Статус | Комментарий |
|---|---|---|
| Deployment topology определена? | Замечание | Упомянуто "добавить workers", но не описана topology (отдельный pod? sidecar?) |
| Rollback strategy описана? | Блокер | Rollback strategy полностью отсутствует — что происходит при деплое новой версии с jobs в очереди? |
| Горизонтальное масштабирование возможно? | OK | Явно описано: "Естественно масштабируется горизонтально" |
| Мониторинг и alerting настроены? | Замечание | "Стандартный observability" упомянут в Consequences, но конкретные метрики/алерты не определены |

**Итог:** Блокер — rollback strategy отсутствует

| Домен | Статус | Комментарий |
|---|---|---|
| Прикладная архитектура | Замечание | Отсутствует transition path для sync-клиентов |
| ИБ | Замечание | Auth model и data classification не определены |
| Инфраструктура | Блокер | Rollback strategy отсутствует |

**Итог:** Требует доработки

**Условия:**

| # | Условие | Источник | Приоритет |
|---|---------|----------|-----------|
| 1 | Добавить rollback strategy в delivery/rollout.md | Инфраструктура | Блокер |
| 2 | Описать auth model для POST/GET /exports | ИБ | Замечание |
| 3 | Определить data classification для экспортируемых данных | ИБ | Замечание |
| 4 | Описать transition path для существующих sync-клиентов | Прикладная архитектура | Замечание |
| 5 | Определить конкретные метрики и alerting rules | Инфраструктура | Замечание |
