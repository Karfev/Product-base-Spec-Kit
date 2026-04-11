# Tasks: 004-adoption-path

**Initiative:** INIT-2026-004-adoption-path
**Owner:** @karfev

> Test strategy matrix: `docs/testing/test-strategy.md`

## Task list

- [x] **T1:** Update contracts — no API contracts for this tooling initiative. OpenAPI/AsyncAPI stubs marked as empty. (`make lint-contracts` passes)
- [x] **T2a:** Write tests for archkom decoupling and upgrade.sh — shell test scripts that verify: scaffold output, upgrade path, backup creation, downgrade rejection. Tests confirm expected behavior (RED for missing features before implementation).
- [x] **T2b:** Implement changes: speckit-start.md, QUICKSTART.md, archkom decoupling in init.sh, upgrade.sh, speckit-trace-viz.md (GREEN — all tests pass)
- [ ] **T3:** Integration tests — end-to-end flow: init minimal → upgrade standard → validate. User testing for Gate 1 (<30 min target).
- [ ] **T4:** Observability — not applicable for tooling initiative. No SLO metrics beyond user testing.
- [ ] **T5:** Update trace.md + changelog/CHANGELOG.md, run: `make check-trace`
- [ ] **T6:** PRR checklist review: `ops/prr-checklist.md` (Standard profile items)

## Definition of done (by profile)

| Checkpoint | Minimal | Standard | Extended |
|---|---|---|---|
| requirements.yml filled | MUST | MUST | MUST |
| spec/plan/tasks.md filled | MUST | MUST | MUST |
| Contracts valid (lint/validate) | — | MUST | MUST |
| trace.md filled | — | MUST | MUST |
| slo.yaml and prr-checklist.md | — | MUST | MUST |
| threat-model.md | — | — | MUST |
| CI gates green | MUST | MUST | MUST |
