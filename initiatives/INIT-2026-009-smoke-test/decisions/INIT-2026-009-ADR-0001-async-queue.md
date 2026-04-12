# INIT-2026-009-ADR-0001: Async Queue for Export Processing

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
