<!-- FILE: prd.md -->
# PRD: {Название инициативы}

**Initiative:** {INIT-YYYY-NNN-slug}
**Owner (PM):** @{team-or-person}
**Last updated:** {YYYY-MM-DD}
**Profile:** {Minimal|Standard|Extended}

---

## Цель и ожидаемый эффект

- **Проблема:** {кратко — что болит у пользователя/бизнеса}
- **Почему сейчас:** {триггер/сигналы — данные, события, дедлайны}
- **Цель (Outcome):** {измеримый результат — не output, а outcome}

## Пользователи и сценарии

- **Primary personas:** {кто пользуется}
- **Top JTBD / сценарии:**
  1. {Сценарий 1}
  2. {Сценарий 2}
  3. {Сценарий 3}

## Метрики успеха

| Метрика | Baseline | Target | Период | Источник |
|---|---:|---:|---|---|
| {kpi_1} | {x} | {y} | {30d\|90d} | {BI\|APM\|…} |
| {kpi_2} | {x} | {y} | {30d\|90d} | {BI\|APM\|…} |

## Scope

**In-scope:** {что делаем}

**Non-goals:** {что сознательно не делаем — это важно}

## Риски и ограничения

- **{Risk 1}:** {mitigation}
- **{Risk 2}:** {mitigation}

## Требования (ссылки на REQ)

Реестр требований — в `requirements.yml`. Здесь только ссылки:

- `REQ-{SCOPE}-{NNN}` (P0): {краткий смысл}
- `REQ-{SCOPE}-{NNN}` (P1): {краткий смысл}

## Приёмка

- Acceptance tests: `tests/{path}` — {описание}
- Definition of done по профилю: `.specify/memory/constitution.md#профили`
