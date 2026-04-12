# Knowledge Log: platform

Graduation history — newest first. Auto-maintained by `/speckit-graduate`.

---

## 2026-04-12 — INIT-2026-009-smoke-test

**Outcome:** Снижение time-to-insight для project managers на 40% за счёт автоматической выгрузки

### Requirements graduated

| REQ-ID | Title | Final Status | Type |
|---|---|---|---|
| REQ-EXPORT-001 | Create export request via REST API | draft | functional |
| REQ-EXPORT-002 | Support JSON and CSV export formats | draft | functional |
| REQ-EXPORT-003 | Async export with completion notification | draft | functional |
| REQ-EXPORT-004 | Export latency P95 under 30 seconds | draft | nfr |

### ADRs graduated

| Source | Product ADR | Title |
|---|---|---|
| INIT-2026-009-ADR-0001-async-queue | PLAT-0003-async-queue | Async Queue for Export Processing |

### Contracts graduated

| Format | Artifacts | Paths/Channels Added |
|---|---|---|
| OpenAPI | baseline.openapi.yml | POST /exports, GET /exports/{id} |
| AsyncAPI | baseline.asyncapi.yml | export.report.completed |

### Key learnings

- Smoke test of Spec Kit framework — validated full chain from init to graduation
