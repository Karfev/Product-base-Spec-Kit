<!-- FILE: .specify/specs/003-audit-log/spec.md -->
# Spec: 003-audit-log

**Initiative:** INIT-2026-003-audit-log
**Profile:** Standard
**Owner:** @platform-team
**Last updated:** 2026-04-10

## Summary

Add audit log infrastructure to the platform: an event-driven service that records significant user actions into an immutable store, and a REST API for administrators to query and export audit logs. This enables security incident investigation without engineering involvement and provides an exportable audit trail for SOC2 compliance.

## Motivation / Problem

Platform administrators currently have no audit trail for user actions. Security incident investigations require manual SQL queries by engineers, taking 2-4 hours per incident. INIT-2026-002 notification preferences initiative requires auditable opt-out (REQ-NOTIF-004) but no recording mechanism exists. SOC2 audit preparation (Q3 2026) requires audit trail capability.

See: `../../../initiatives/INIT-2026-003-audit-log/prd.md`

## Scope

- Event consumer that subscribes to domain events via RabbitMQ and persists structured audit log entries (REQ-AUDIT-001)
- REST API `GET /audit-logs` with filtering by user_id, action_type, resource_type, date range + pagination (REQ-AUDIT-002)
- REST API `GET /audit-logs/export` returning filtered results as CSV download (REQ-AUDIT-003)
- Latency SLO for audit query API (REQ-AUDIT-004)
- Retention policy: 2-year storage with automatic purge of expired entries (REQ-AUDIT-005)
- Published event `audit.event.recorded` for downstream consumers (analytics, alerting)

## Non-goals

- Real-time alerting on suspicious actions (separate initiative)
- UI for configuring retention policy (fixed config, not user-facing)
- Custom audit event type definitions (fixed set: create, update, delete, access, auth)
- Auditing system/automated actions (user-initiated only)
- Full-text search within audit event metadata

## API/Contracts

- `initiatives/INIT-2026-003-audit-log/contracts/openapi.yaml` — `GET /audit-logs`, `GET /audit-logs/export`
- `initiatives/INIT-2026-003-audit-log/contracts/asyncapi.yaml` — channel `audit.event.recorded`
- `initiatives/INIT-2026-003-audit-log/contracts/schemas/audit-event.schema.json` — audit event entity schema

## Test strategy

- Unit: business logic for event-to-audit-entry mapping, filter parameter validation, CSV serialization
- Integration/contract: RabbitMQ consumer receives domain events and persists audit entries; REST API returns correct filtered/paginated results against real PostgreSQL
- E2E/acceptance: end-to-end flow — publish domain event, verify audit entry appears via GET /audit-logs, export as CSV and validate content

## Rollout

- Flag/guardrail: feature flag `audit-log-enabled`, canary rollout 5% -> 25% -> 100%
- Migration/backfill: new `audit_events` table via migration; no backfill of historical events (audit starts from launch date)
- Monitoring/rollback: monitor `audit.query.p95_latency_ms` and `audit.events.consumer_lag`; rollback trigger: P95 > 500ms or consumer lag > 60s; rollback: disable feature flag, audit events queue will be drained when re-enabled

## User stories

- As a Platform Admin, I want to search audit logs by user and date range, so that I can investigate security incidents quickly without involving engineers.
- As a Compliance Officer, I want to export audit logs as CSV with filters, so that I can provide audit trail evidence to SOC2 auditors.
- As a Platform Admin, I want to see who modified or deleted a resource, so that I can determine whether to escalate or rollback.

## Requirements

Ссылки на REQ-ID (реестр в `requirements.yml`):

- `REQ-AUDIT-001` (P0): Record audit event on significant user action
- `REQ-AUDIT-002` (P0): List audit log entries with filtering and pagination
- `REQ-AUDIT-003` (P1): Export filtered audit logs as CSV
- `REQ-AUDIT-004` (P1): Audit log query latency SLO
- `REQ-AUDIT-005` (P1): Audit log retention with automatic cleanup

## Acceptance criteria

- Given a user creates a resource, when the action completes and domain event is published, then an audit entry with action_type=create appears in GET /audit-logs within 5 seconds
- Given audit events exist for user 123, when GET /audit-logs?user_id=123 is called, then only events for user 123 are returned with pagination metadata
- Given a date range filter, when GET /audit-logs?date_from=2026-01-01&date_to=2026-03-31 is called, then only events within that range are returned
- Given audit events exist, when GET /audit-logs/export is called with filters, then a CSV file is returned with headers: timestamp, user_id, action_type, resource_type, resource_id, source_ip
- Given the audit API is under normal load, when queries are executed, then P95 latency is below 300ms
- Given audit entries older than 730 days exist, when the purge job runs, then those entries are deleted without impacting query latency

## Open Questions

| # | Вопрос | Владелец | Дедлайн | Статус |
|---|--------|----------|---------|--------|
| 1 | Should the audit service also consume auth events (login, logout, password change) from INIT-2026-000, or only notification events initially? | @platform-team | 2026-04-20 | open |
| 2 | What is the maximum expected CSV export size? Should we add a row limit or async export for large datasets? | @platform-team | 2026-04-20 | open |
