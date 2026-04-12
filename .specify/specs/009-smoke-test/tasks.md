# Tasks: 009-smoke-test

**Initiative:** INIT-2026-009-smoke-test
**Profile:** Standard
**Last updated:** 2026-04-12

---

## T1: Contracts & API paths

- [x] Verify `contracts/openapi.yaml` — endpoints `POST /exports`, `GET /exports/{id}` (REQ-EXPORT-001, REQ-EXPORT-003)
- [x] Verify `contracts/asyncapi.yaml` — channel `export.report.completed` (REQ-EXPORT-003)
- [x] Verify `contracts/schemas/export.schema.json` — Export entity schema
- [x] Run: `make lint-contracts` ✅ passed

## T2a: RED — Write failing tests (SIMULATED — smoke test)

- [x] Unit tests: `tests/unit/export-service.spec.ts` — format conversion (JSON/CSV), input validation, error cases (REQ-EXPORT-002)
  - Run: `make test-unit` — SIMULATED (no real codebase)
- [x] Contract tests: OpenAPI lint + AsyncAPI validate (REQ-EXPORT-001, REQ-EXPORT-003)
  - Run: `make test-contract` — SIMULATED
- [x] Integration tests: `tests/e2e/export.spec.ts` — create → poll → download → validate file (REQ-EXPORT-001, REQ-EXPORT-002, REQ-EXPORT-003)
  - Run: `make test-integration` — SIMULATED
- [x] Performance tests: `tests/perf/export-latency.jmx` — P95 < 30s at 100 concurrent (REQ-EXPORT-004)
  - Run: `make test-perf` — SIMULATED

## T2b: GREEN — Implementation (SIMULATED — smoke test)

- [x] Implement export service — SIMULATED
- [x] Implement format converters (JSON, CSV) — SIMULATED
- [x] Implement status polling endpoint `GET /exports/{id}` — SIMULATED
- [x] Implement event publishing `export.completed` — SIMULATED
- [x] DB migration: CREATE TABLE `exports` — SIMULATED
- [x] Re-run all tests — SIMULATED

## T3: Integration tests in real environment (SIMULATED — smoke test)

- [x] Deploy to staging — SIMULATED
- [x] Run: `make test-integration` — SIMULATED
- [x] Verify end-to-end flow — SIMULATED
- [x] Verify event publishing — SIMULATED

## T4: Observability & SLO

- [x] Add metrics: `export_duration_seconds` (histogram), `export_requests_total{status}` (counter), `export_queue_depth` (gauge) — defined in plan.md
- [x] Verify `ops/slo.yaml#export-latency` — P95 < 30s, 30d rolling ✅
- [x] Configure alerts — defined in delivery/rollout.md
- [x] Grafana dashboard reference: `https://grafana.platform.internal/d/exports`

## T5: Traceability & changelog

- [x] Update `trace.md` (L3) — verified all REQ-EXPORT-* have trace links ✅
- [x] Update `.specify/specs/009-smoke-test/trace.md` (L4) — created with all 4 REQ-IDs ✅
- [x] Update `changelog/CHANGELOG.md` — added export feature under [Unreleased] ✅
- [x] Run: `make check-trace` — 0 errors, 36 warnings (pre-existing from other initiatives) ✅

## T6: PRR checklist

- [x] Review `ops/prr-checklist.md` — all P0 items marked [x] ✅
- [x] Verify all **P0** items are addressed:
  - SLO/SLI defined ✅
  - Critical dependencies listed ✅
  - Golden signals metrics defined ✅
  - Rollout/rollback described ✅
- [x] Set PRR status to `passed` ✅

---

## Definition of Done (by profile)

| Checkpoint | Minimal | Standard | Extended |
|---|---|---|---|
| `requirements.yml` valid | ✅ | ✅ | ✅ |
| `prd.md` filled | ✅ | ✅ | ✅ |
| `contracts/` linted | — | ✅ | ✅ |
| `trace.md` complete | — | ✅ | ✅ |
| `ops/slo.yaml` filled | — | ✅ | ✅ |
| `ops/prr-checklist.md` P0 passed | — | ✅ | ✅ |
| `delivery/rollout.md` filled | — | ✅ | ✅ |
| `ops/threat-model.md` filled | — | — | ✅ |
| `ops/nfr-validation.md` filled | — | — | ✅ |
| Unit tests pass | ✅ | ✅ | ✅ |
| Contract tests pass | — | ✅ | ✅ |
| Integration tests pass | — | — | ✅ |
| Perf tests pass (if NFR) | — | ✅ | ✅ |
