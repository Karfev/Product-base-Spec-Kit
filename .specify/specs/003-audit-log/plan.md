<!-- FILE: .specify/specs/003-audit-log/plan.md -->
# Plan: 003-audit-log

**Initiative:** INIT-2026-003-audit-log
**Owner:** @platform-team
**Last updated:** 2026-04-10

## Architecture choices

- **Audit event storage:** PostgreSQL append-only table with monthly date-based partitioning. Chosen over ClickHouse/Elasticsearch for operational simplicity — existing PG infrastructure handles expected volume (< 10M events/year) with proper indexing. ADR: `decisions/INIT-2026-003-ADR-0001-storage-strategy.md`
- **Event capture pattern:** RabbitMQ consumer subscribes to domain events from existing services (notifications, auth). No changes to source services required — audit service is a passive listener. This follows the platform's existing event-driven architecture (RabbitMQ).
- **Immutability:** Audit events are INSERT-only. No UPDATE/DELETE operations exposed via API or internal service. Purge is handled via partition DROP at retention boundary.

## Contracts impact

> Все пути ниже — относительно директории инициативы `initiatives/INIT-2026-003-audit-log/`.

**OpenAPI** (`contracts/openapi.yaml`):

- `GET /audit-logs` — new endpoint, filtered list with pagination (REQ-AUDIT-002)
- `GET /audit-logs/export` — new endpoint, CSV download (REQ-AUDIT-003)

**AsyncAPI** (`contracts/asyncapi.yaml`):

- Channel `audit.event.recorded` — new, published after successful event persistence (REQ-AUDIT-001)

**Schemas** (`contracts/schemas/`):

- `audit-event.schema.json` — new schema defining AuditEvent entity

## Data changes

- **New table `audit_events`:** partitioned by month on `timestamp` column
  - Columns: `id` (UUID PK), `timestamp` (timestamptz, NOT NULL), `user_id` (varchar, NOT NULL, indexed), `action_type` (varchar, NOT NULL, indexed), `resource_type` (varchar, NOT NULL, indexed), `resource_id` (varchar, NOT NULL), `source_ip` (varchar), `metadata` (jsonb)
  - Indexes: composite `(user_id, timestamp DESC)`, `(action_type, timestamp DESC)`, `(resource_type, timestamp DESC)`
  - Partitioning: RANGE on `timestamp`, monthly partitions, auto-created via cron
- **No backfill** of historical events — audit starts from launch date
- Migration script reference: `delivery/rollout.md`

## Observability & SLO impact

- **Metrics:**
  - `audit.query.p95_latency_ms` (histogram) — query latency for GET /audit-logs
  - `audit.query.p99_latency_ms` (histogram) — tail latency
  - `audit.events.consumer_lag` (gauge) — RabbitMQ consumer lag in seconds
  - `audit.events.persisted_total` (counter) — total events recorded
  - `audit.purge.rows_deleted` (counter) — rows purged per run
- **Logs:** structured JSON logs for consumer errors, query slow-log (> 200ms)
- **SLO:** `ops/slo.yaml#audit-query-latency` — new SLO: P95 < 300ms, P99 < 1000ms for GET /audit-logs

## Rollout & rollback

- Feature flag: `audit-log-enabled` — controls both consumer activation and API endpoint availability
- Canary: 5% -> 25% -> 100% over 3 days, monitored via `audit.query.p95_latency_ms`
- Rollback triggers: P95 > 500ms sustained for 5 minutes OR consumer lag > 60 seconds
- Rollback steps: disable feature flag (stops consumer, returns 404 on API); queued events will be drained when re-enabled
- Details: `delivery/rollout.md`

## Risks

- **Data volume growth** — at high RPS, audit table could grow faster than expected. Mitigation: monthly partitioning enables efficient purge; monitor `audit.events.persisted_total` rate; if >10M/year, re-evaluate storage strategy per ADR confirmation criteria.
- **Consumer lag during traffic spikes** — RabbitMQ consumer may fall behind. Mitigation: monitor `audit.events.consumer_lag`; consumer is idempotent (duplicate events are safe due to INSERT with UUID PK); can scale consumer horizontally.
- **Query latency on large datasets** — 2-year retention window could have 20M+ rows. Mitigation: partition pruning ensures queries only scan relevant months; composite indexes cover common filter patterns; P95 SLO monitored with automatic alerting.
