<!-- FILE: .specify/specs/{NNN}-{slug}/tasks.md -->
# Tasks: {NNN}-{slug}

**Initiative:** {INIT-YYYY-NNN-slug}
**Owner:** @{engineer-or-team}

> Test strategy matrix: `docs/testing/test-strategy.md`

## Task list

- [ ] **T1:** Добавить/обновить контракт (OpenAPI/AsyncAPI) + прогнать линтеры локально (`make lint-contracts`)
- [ ] **T2a:** Написать тесты по матрице из `docs/testing/test-strategy.md` (unit + contract при Standard/Extended) — убедиться что тесты **падают** (RED), выполнить: `make test-unit` (+ `make test-contract` при необходимости)
- [ ] **T2b:** Реализовать изменение (код) — убедиться что тесты **зелёные** (GREEN)
- [ ] **T3:** Интеграционные тесты в реальном окружении (если применимо), выполнить: `make test-integration`
- [ ] **T4:** Observability — добавить метрики/алерты, обновить `ops/slo.yaml` (Standard/Extended)
- [ ] **T5:** Обновить `trace.md` + `changelog/CHANGELOG.md`, выполнить: `make check-trace`
- [ ] **T6:** Пройти PRR пункты из `ops/prr-checklist.md` (Standard/Extended)

## Definition of done (по профилю)

| Чекпойнт | Minimal | Standard | Extended |
|---|---|---|---|
| requirements.yml заполнен | MUST | MUST | MUST |
| spec/plan/tasks.md заполнены | MUST | MUST | MUST |
| Контракты валидны (lint/validate) | — | MUST | MUST |
| trace.md заполнен | — | MUST | MUST |
| slo.yaml и prr-checklist.md | — | MUST | MUST |
| threat-model.md | — | — | MUST |
| CI gates зелёные | MUST | MUST | MUST |
