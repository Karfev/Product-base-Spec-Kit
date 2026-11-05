# INIT-2026-099-csv-export

> **Учебная инициатива** для туториала [`docs/tutorial/`](../../docs/tutorial/INDEX.md).
> НЕ настоящая инициатива в производстве. Лежит в `examples/`, не в `initiatives/`:
> `make validate` её не проверяет, а `make check-trace` проверяет только ссылки в `trace`.

## TL;DR

Экспорт записей платформы в CSV. Один эндпойнт `POST /export`, два режима:
синхронный (≤ 100k записей) и асинхронный с job-pattern (> 100k).

## Метаданные

| Поле | Значение |
|---|---|
| Initiative ID | `INIT-2026-099-csv-export` |
| Profile | `standard` |
| Owner | `@platform-team` |
| Product | `platform` |
| Status | `draft` (учебный) |
| Last updated | 2026-04-28 |

## Артефакты

| Слой | Файл | Что внутри |
|---|---|---|
| L3 — PRD | [`prd.md`](./prd.md) | Цель, пользователи, метрики, scope |
| L3 — Requirements | [`requirements.yml`](./requirements.yml) | 5 REQ-EXPORT-001..005 |
| L3 — Design | [`design.md`](./design.md) | arc42-lite, Mermaid C4 |
| L3 — Contracts | [`contracts/openapi.yaml`](./contracts/openapi.yaml) | REST: POST /export, GET /export/jobs/{id} |
| L3 — Contracts | [`contracts/asyncapi.yaml`](./contracts/asyncapi.yaml) | Events: export.job.completed/failed |
| L3 — Schemas | [`contracts/schemas/export-job.schema.json`](./contracts/schemas/export-job.schema.json) | JSON Schema для ExportJob |
| L3 — ADR | [`decisions/INIT-2026-099-ADR-0001-sync-vs-async.md`](./decisions/INIT-2026-099-ADR-0001-sync-vs-async.md) | Hybrid strategy |
| L3 — Ops | [`ops/slo.yaml`](./ops/slo.yaml) | OpenSLO: latency + availability |
| L3 — Ops | [`ops/prr-checklist.md`](./ops/prr-checklist.md) | PRR (status: amber) |
| L3 — Delivery | [`delivery/rollout.md`](./delivery/rollout.md) | Feature flag, 3 этапа, rollback triggers |
| L3 — Changelog | [`changelog/CHANGELOG.md`](./changelog/CHANGELOG.md) | Keep a Changelog |

## Использование в туториале

| Файл туториала | Что использует из этой инициативы |
|---|---|
| `03-first-initiative.md` | walkthrough «как такое scaffold'ить с нуля» |
| `04-anatomy-of-initiative.md` | разбор каждого файла |
| `05-l4-spec-cascade.md` | пример spec/plan/tasks для feature-уровня |
| `06-traceability-and-validation.md` | прогон `make check-trace` на REQ-EXPORT-* |
| `07-profiles-and-risk.md` | почему именно Standard, а не Minimal/Extended |

## Локальная проверка

```bash
# Из корня репо:
python3 -m check_jsonschema \
  --schemafile tools/schemas/requirements.schema.json \
  examples/INIT-2026-099-csv-export/requirements.yml
# → ok -- validation done
```
