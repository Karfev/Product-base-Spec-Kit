---
status: "proposed"      # proposed | decided | deprecated | superseded by ADR-XXXX
date: "YYYY-MM-DD"
decision-makers: ["@team-or-person"]
consulted: ["@team-or-person"]
informed: ["@team-or-person"]
---

# {INIT-YYYY-NNN-ADR-NNNN-slug}: {Decision title — императив, до 8 слов}

> **golden comment.** ID для initiative-level ADR: `INIT-YYYY-NNN-ADR-NNNN-slug`.
> Для product-level ADR: `<PRODUCT>-NNNN-slug` (например `PLATFORM-0042-event-bus`).
> Один ADR = одно решение. Если решений несколько — несколько ADR.
> Удалить эту блокноут-секцию перед коммитом. Живой пример:
> [`examples/INIT-2026-099-csv-export/decisions/INIT-2026-099-ADR-0001-sync-vs-async.md`](../examples/INIT-2026-099-csv-export/decisions/INIT-2026-099-ADR-0001-sync-vs-async.md).

## Context and problem statement

> **golden comment.** Опиши задачу так, чтобы человек, открывший ADR через 6 месяцев,
> понял КОНТЕКСТ принятия решения, а не только сам выбор. Constraints, нагрузка,
> ограничения совместимости — всё сюда.

{2-4 абзаца. Какая ситуация, что нужно решить, какие constraints.}

## Decision drivers

> **golden comment.** 3-6 пунктов. Каждый — критерий, по которому будем сравнивать опции.
> Должны быть проверяемы (не «хорошо», а «P95 < 5s» или «не более 1 нового сервиса»).

- **{Driver 1}:** {почему важно}
- **{Driver 2}:** {почему важно}
- **{Driver 3}:** {почему важно}

## Considered options

> **golden comment.** Минимум 2, желательно 3. Включай явно отвергнутые варианты —
> чтобы было видно, что мы их рассмотрели. «Status quo / do nothing» — валидная опция.

### Option A — {краткое имя}

{Описание подхода в 1-3 абзаца.}

- **Good:** {…}
- **Good:** {…}
- **Bad:** {…}

### Option B — {краткое имя}

{…}

- **Good:** {…}
- **Bad:** {…}

### Option C — {краткое имя}

{…}

- **Good:** {…}
- **Bad:** {…}

## Decision outcome

> **golden comment.** Выбранная опция + ОДНО предложение «потому что…» — самое
> важное обоснование. Остальное — в Implementation notes / Consequences.

**Chosen: Option {X} — {имя}**, because {ключевая причина в одно предложение}.

### Implementation notes

> **golden comment.** Что критично знать инженеру, который будет это реализовывать.
> Magic numbers, env-конфиги, edge cases.

1. {…}
2. {…}

### Consequences

- **Good:** {положительный эффект}
- **Good:** {положительный эффект}
- **Bad:** {компромисс, который мы принимаем}
- **Neutral:** {побочный эффект без явной оценки}

### Confirmation

> **golden comment.** Конкретные тесты/метрики/ревью, которые подтвердят, что
> решение работает. Без этого ADR — просто декларация.

Решение подтверждено когда:

1. `tests/<file>::REQ-XXX-NNN` — {что проверяет}
2. `tests/perf/<file>` — {какая метрика, какой порог}
3. {Ревью через N дней — какие данные смотрим}
