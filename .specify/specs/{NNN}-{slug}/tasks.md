<!-- FILE: .specify/specs/{NNN}-{slug}/tasks.md -->
# Tasks: {NNN}-{slug}

**Initiative:** {INIT-YYYY-NNN-slug}
**Owner:** @{engineer-or-team}

## Task list

- [ ] **T1:** Добавить/обновить контракт (OpenAPI/AsyncAPI) + прогнать линтеры локально
- [ ] **T2:** Реализовать изменение (код) + unit tests
- [ ] **T3:** Contract tests / интеграционные тесты (если применимо)
- [ ] **T4:** Observability — добавить метрики/алерты, обновить `ops/slo.yaml` (Standard/Extended)
- [ ] **T5:** Обновить `trace.md` + `changelog/CHANGELOG.md`
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
