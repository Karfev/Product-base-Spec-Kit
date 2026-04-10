# PRD: Audit Log Infrastructure

**Initiative:** INIT-2026-003-audit-log
**Owner (PM):** @platform-team
**Last updated:** 2026-04-10
**Profile:** Standard

---

## Цель и ожидаемый эффект

- **Проблема:** При инцидентах безопасности у платформы нет аудит-трейла. Расследование требует ручных SQL-запросов инженерами и занимает 2–4 часа на инцидент. REQ-NOTIF-004 (INIT-2026-002) требует "auditable opt-out", но механизма записи и просмотра аудит-событий не существует. `compliance-service` фигурирует как consumer в event-catalog домена notifications, но сервис не реализован.
- **Почему сейчас:** Подготовка к SOC2 аудиту (Q3 2026) — аудитор потребует audit trail capability. Два customer escalation в Q1 2026 потребовали ручного расследования (суммарно >8 часов инженерного времени).
- **Цель (Outcome):** Администраторы платформы расследуют инциденты безопасности через API за минуты, а не часы. Compliance Officer получает экспортируемый audit trail для SOC2 ревью.

## Пользователи и сценарии

- **Primary personas:**
  - Platform Admin — расследует инциденты, отвечает за безопасность
  - Compliance Officer — готовит отчёты для SOC2 аудиторов

- **Top JTBD / сценарии:**
  1. Platform Admin хочет найти все действия конкретного пользователя за последние 24 часа, чтобы расследовать подозрительную активность
  2. Compliance Officer хочет экспортировать все opt-out действия за квартал в CSV, чтобы предоставить аудитору доказательство GDPR compliance
  3. Platform Admin хочет увидеть кто и когда удалил/изменил ресурс, чтобы откатить или эскалировать

## Метрики успеха

| Метрика | Baseline | Target | Период | Источник |
|---|---:|---:|---|---|
| Mean time to investigate (MTTI) | 3h | 15min | 30d после launch | Incident tracker |
| % инцидентов, расследованных без привлечения инженеров | 0% | 80% | 90d после launch | Incident tracker |

## Scope

**In-scope:**

- Запись audit events при значимых действиях пользователей (CRUD на ресурсах, изменения настроек, opt-out) → `REQ-AUDIT-001` [PROPOSED]
- REST API для просмотра audit logs с фильтрами (user, action, date range, resource type) → `REQ-AUDIT-002` [PROPOSED]
- Экспорт отфильтрованных логов в CSV → `REQ-AUDIT-003` [PROPOSED]
- Query latency SLO для API audit logs → `REQ-AUDIT-004` [PROPOSED]
- Retention policy: хранение 2 года, автоочистка → `REQ-AUDIT-005` [PROPOSED]

**Non-goals:**

- Real-time alerting на подозрительные действия (scope для отдельной инициативы)
- UI для настройки retention policy (фиксированная policy, изменяемая через config)
- Определение custom audit event types (фиксированный набор: create, update, delete, access, auth)
- Аудит системных/автоматических действий (только user-initiated actions)

## Риски и ограничения

- **Объём данных:** Audit log может расти быстро при высоком RPS. Mitigation: pagination обязательна, retention с автоочисткой, рассмотреть append-only storage strategy (ADR).
- **Latency на больших данных:** Query по 2-летнему архиву может быть медленным. Mitigation: индексы по (user_id, action, timestamp), SLO на P95 latency, возможно partitioning по дате.
- **Cross-initiative зависимость:** Audit events должны приходить от других сервисов (notifications, auth). Mitigation: event-driven architecture — слушаем domain events через RabbitMQ, не требуем изменений в source сервисах.

## Требования (ссылки на REQ)

Реестр требований — в `requirements.yml`. Здесь только ссылки:

- `REQ-AUDIT-001` (P0): Запись audit event при значимом действии [PROPOSED]
- `REQ-AUDIT-002` (P0): Просмотр audit logs с фильтрами [PROPOSED]
- `REQ-AUDIT-003` (P1): Экспорт в CSV [PROPOSED]
- `REQ-AUDIT-004` (P1): Query latency SLO [PROPOSED]
- `REQ-AUDIT-005` (P1): Retention 2 года + автоочистка [PROPOSED]

## Приёмка

- Acceptance tests: `tests/api/audit-logs.spec.ts` — CRUD + фильтрация + экспорт
- Definition of done по профилю: `.specify/memory/constitution.md#профили`
