<!-- FILE: .specify/specs/004-adoption-path/plan.md -->
# Plan: 004-adoption-path

**Initiative:** INIT-2026-004-adoption-path
**Owner:** @karfev
**Last updated:** 2026-04-11

## Architecture choices

- {Ключевое решение 1} → ADR: `decisions/{INIT}-ADR-004-adoption-path.md`
- {Ключевое решение 2}

## Contracts impact

> Все пути ниже — относительно директории инициативы `initiatives/INIT-2026-004-adoption-path/`.

**OpenAPI** (`contracts/openapi.yaml`):
- `POST /{path}` — {добавляем / изменяем / удаляем}

**AsyncAPI** (`contracts/asyncapi.yaml`):
- Channel `{name}` — {…}

**Schemas** (`contracts/schemas/`):
- `{entity}.schema.json` — {новая / изменённая схема}

## Data changes

- {Таблица/коллекция}: {добавляем поле / индекс / миграция}
- Migration script: `delivery/migration.md`

## Observability & SLO impact

- Метрики: {gauge/counter/histogram — что добавляем}
- Логи: {что структурируем, какие поля}
- Трейсы: {span-ы, если применимо}
- SLO: `ops/slo.yaml#{slo-name}` — {обновляем / создаём}

## Rollout & rollback

- Feature flag: `{flag-name}` — {включаем постепенно / нет}
- Canary: {да/нет, процент}
- Rollback: {описание шагов отката}
- Подробности: `delivery/rollout.md`

## Risks

- {Риск 1} → mitigation: {…}
- {Риск 2} → mitigation: {…}
