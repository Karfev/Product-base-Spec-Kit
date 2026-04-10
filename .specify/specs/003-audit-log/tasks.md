<!-- FILE: .specify/specs/003-audit-log/tasks.md -->
# Tasks: 003-audit-log

**Initiative:** INIT-2026-003-audit-log
**Owner:** @platform-team

> Test strategy matrix: `docs/testing/test-strategy.md`

## Task list

- [ ] **T1: Update contracts and validate**
  - Contracts already created in `initiatives/INIT-2026-003-audit-log/contracts/`
  - Verify: `make lint-contracts` passes for both `openapi.yaml` and `asyncapi.yaml`
  - Verify: `contracts/schemas/audit-event.schema.json` aligns with OpenAPI `AuditLogEntry` schema
  - Files: `contracts/openapi.yaml`, `contracts/asyncapi.yaml`, `contracts/schemas/audit-event.schema.json`

- [ ] **T2a: Write failing tests — RED**
  - **Unit tests** (REQ-AUDIT-001, REQ-AUDIT-002, REQ-AUDIT-003):
    - `tests/unit/audit-event-mapper.spec.ts` — domain event to AuditEvent entity mapping
    - `tests/unit/audit-filter-validator.spec.ts` — query parameter validation (date range, action_type enum)
    - `tests/unit/csv-serializer.spec.ts` — AuditEvent[] to CSV string with correct headers
  - **Contract tests** (REQ-AUDIT-002, REQ-AUDIT-003) — Standard profile requires:
    - `tests/contract/audit-logs-api.spec.ts` — GET /audit-logs returns schema-conformant response, pagination metadata present
    - `tests/contract/audit-logs-export.spec.ts` — GET /audit-logs/export returns text/csv with Content-Disposition header
  - Run: `make test-unit` — confirm tests FAIL (no implementation yet)
  - Run: `make test-contract` — confirm tests FAIL

- [ ] **T2b: Implement — GREEN**
  - DB migration: create `audit_events` table with monthly partitioning on `timestamp`
    - Columns: id (UUID), timestamp (timestamptz), user_id, action_type, resource_type, resource_id, source_ip, metadata (jsonb)
    - Indexes: (user_id, timestamp DESC), (action_type, timestamp DESC), (resource_type, timestamp DESC)
  - RabbitMQ consumer: subscribe to domain events, map to AuditEvent, INSERT into audit_events
  - REST API: GET /audit-logs with filtering + pagination, GET /audit-logs/export with CSV serialization
  - Published event: audit.event.recorded after successful persistence
  - Feature flag: `audit-log-enabled` wrapping consumer + API routes
  - Run: `make test-unit` — confirm tests PASS (GREEN)
  - Run: `make test-contract` — confirm tests PASS (GREEN)

- [ ] **T3: Integration tests in real environment**
  - `tests/integration/audit-consumer.spec.ts` — publish domain event to RabbitMQ, verify audit entry appears in PostgreSQL within 5s (REQ-AUDIT-001)
  - `tests/integration/audit-api.spec.ts` — seed audit_events table, call GET /audit-logs with filters, verify correct results against real PostgreSQL (REQ-AUDIT-002)
  - `tests/integration/audit-export.spec.ts` — seed data, call GET /audit-logs/export, parse CSV and verify content (REQ-AUDIT-003)
  - Run: `make test-integration`
  - Performance check for REQ-AUDIT-004: run `make test-perf` with load test targeting GET /audit-logs, verify P95 < 300ms

- [ ] **T4: Observability — metrics, alerts, SLO**
  - Add metrics instrumentation:
    - `audit.query.p95_latency_ms` (histogram) on GET /audit-logs handler
    - `audit.query.p99_latency_ms` (histogram)
    - `audit.events.consumer_lag` (gauge) from RabbitMQ consumer
    - `audit.events.persisted_total` (counter) on successful INSERT
    - `audit.purge.rows_deleted` (counter) on purge job
  - Fill `initiatives/INIT-2026-003-audit-log/ops/slo.yaml`:
    - SLO `audit-query-latency`: P95 < 300ms, P99 < 1000ms on GET /audit-logs
  - Add structured JSON logging for consumer errors and slow queries (> 200ms)
  - Configure alerting: P95 > 500ms for 5 minutes triggers page

- [ ] **T5: Update trace.md + CHANGELOG.md**
  - Fill `.specify/specs/003-audit-log/trace.md` — map every REQ-AUDIT-* to ADR, contract, schema, test, SLO
  - Fill `initiatives/INIT-2026-003-audit-log/trace.md` — L3 initiative-level RTM
  - Update `initiatives/INIT-2026-003-audit-log/changelog/CHANGELOG.md` — add 0.1.0 entry
  - Run: `make check-trace` — confirm zero errors

- [ ] **T6: Complete PRR checklist**
  - Review and check off all items in `initiatives/INIT-2026-003-audit-log/ops/prr-checklist.md`
  - Categories: Architecture, Observability, Deployment, Operations
  - Verify feature flag `audit-log-enabled` is documented
  - Verify rollback procedure is in `delivery/rollout.md`
  - Note: Security & privacy section was removed for Standard profile by init.sh

## Definition of done (по профилю)

| Чекпойнт | Minimal | Standard | Extended |
|---|---|---|---|
| requirements.yml заполнен | MUST | **MUST** | MUST |
| spec/plan/tasks.md заполнены | MUST | **MUST** | MUST |
| Контракты валидны (lint/validate) | — | **MUST** | MUST |
| trace.md заполнен | — | **MUST** | MUST |
| slo.yaml и prr-checklist.md | — | **MUST** | MUST |
| threat-model.md | — | — | MUST |
| CI gates зелёные | MUST | **MUST** | MUST |

**This initiative: Standard** — bold column is the applicable profile.
