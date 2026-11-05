# Spec: {NNN-feature-slug}

> **L4 Feature Specification.** Расположение: `.specify/specs/{NNN-feature-slug}/spec.md`.
> Заполняется через `/speckit-specify {NNN-feature-slug}`.
> Validation: `make check-spec-quality` + `make check-spec-structure`.

> **golden comment.** Перед коммитом удалить эту блок-цитату.
> Все секции ниже обязательны (canonical sections — проверяются `check-spec-structure.py`).
> Не оставляй placeholder-маркеры (`{…}`, `TBD`, `NEEDS CLARIFICATION`) с открытым статусом —
> `check-spec-quality.py` падает.

---

## Summary

> **golden comment.** Один абзац. Что фича делает, для кого, какой основной флоу.
> Не описание дизайна, а суть user-visible поведения.

{Что эта feature делает за один абзац. Каков основной user flow в одной фразе.}

---

## Motivation

> **golden comment.** Почему эта фича нужна именно сейчас, как связана с parent
> initiative. 2-3 абзаца. Ссылка на REQ-* из L3 requirements.yml.

{Контекст. Какую проблему из parent initiative ({INIT-YYYY-NNN-slug}) эта фича закрывает.
Конкретные REQ-IDs (например REQ-EXPORT-001, REQ-EXPORT-002).}

---

## Scope

**In-scope:**

- {что эта feature делает} → REQ-XXX-NNN
- {что эта feature делает} → REQ-XXX-NNN

**Out-of-scope:**

- {что НЕ делает (соседние фичи или Phase 2)}

---

## Requirements (REQ-IDs)

> **golden comment.** Перечисли все REQ-* из parent `initiatives/<INIT>/requirements.yml`,
> которые эта feature реализует. Это вход для `make check-trace`.

| REQ-ID | Title | Priority | Status |
|---|---|---|---|
| REQ-XXX-001 | … | P0 | proposed |
| REQ-XXX-002 | … | P1 | proposed |

---

## API / Contracts impact

> **golden comment.** Что меняется в OpenAPI/AsyncAPI. Если breaking — отметить явно.
> Ссылки на parent contracts.

- {новые / изменённые operations}: `contracts/openapi.yaml#/paths/...`
- {новые / изменённые events}: `contracts/asyncapi.yaml#/channels/...`

---

## User Stories

> **golden comment.** Минимум 1, обычно 2-4. Формат «As a <role>, I want <action>,
> so that <outcome>». Покрывают основные пути (happy + critical edge case).

1. As a {role}, I want to {action}, so that {outcome}.
2. As a {role}, I want to {action}, so that {outcome}.

---

## Acceptance Criteria

> **golden comment.** Given-When-Then. Должны проверяться автоматически (или явно
> отмечено «manual review»). Каждый acceptance — кандидат в test case.

- **AC1.** Given <предусловие>, when <действие>, then <результат>. (REQ-XXX-001)
- **AC2.** Given <предусловие>, when <действие>, then <результат>. (REQ-XXX-001)
- **AC3.** Given <предусловие>, when <действие>, then <результат>. (REQ-XXX-002)

---

## Open questions / NEEDS CLARIFICATION

> **golden comment.** Все вопросы, на которые нужен ответ перед /speckit-plan.
> Каждый — отдельная строка с владельцем и сроком. После закрытия — снять статус
> «open» (иначе `check-spec-quality.py` падает).

- [ ] **NEEDS CLARIFICATION:** {вопрос} — owner: @user — due: YYYY-MM-DD
