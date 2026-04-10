---
description: Create or update the PRD for an initiative
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

You are helping write the Product Requirements Document for initiative `$ARGUMENTS`.

## Your job

1. Read `initiatives/$ARGUMENTS/prd.md` (current state — may be stub or partial).
2. Read `initiatives/$ARGUMENTS/requirements.yml` to understand existing REQ-IDs.
3. Read `.specify/memory/constitution.md` for principles and profile definitions.

4. Ask the user **5 structured questions** (skip if already answered in existing prd.md):

   - **Problem:** What specific problem does this solve? Who experiences it and what is the measurable impact?
   - **Why now:** What is the urgency driver — deadline, revenue risk, regulatory, competitive?
   - **Primary personas:** Who are the users? (role + JTBD format)
   - **Scope:** What is explicitly IN-scope and OUT-of-scope for this initiative?
   - **Success metrics:** What measurable outcomes define success? (metric name, baseline, target, timeframe, source)

5. Fill `initiatives/$ARGUMENTS/prd.md` with:
   - **Цель и ожидаемый эффект**: Problem statement, urgency, Outcome (user-facing goal)
   - **Пользователи и сценарии**: Primary personas, top 2–3 JTBD scenarios
   - **Метрики успеха**: Table — Метрика | Baseline | Target | Период | Источник
   - **Scope**: In-scope list with REQ-ID references, Non-goals list
   - **Риски и ограничения**: Top 3 risks with mitigations
   - **Требования (ссылки на REQ)**: Only REQ-ID references — full detail lives in `requirements.yml`
   - **Приёмка**: Links to test files and Definition of Done reference

6. Narrative text in `prd.md` MUST reference REQ-IDs from `requirements.yml` — do NOT duplicate requirement detail.

7. After writing, remind the user:
   - `Run /speckit-requirements $ARGUMENTS to add or update requirements`
   - `Run make validate to check requirements.yml schema`

## Rules
- `prd.md` is a narrative document — it MUST NOT duplicate machine-readable data from `requirements.yml`
- Every Scope item MUST reference at least one REQ-ID from `requirements.yml` (existing) or propose new ones with `[PROPOSED]` marker — these will be formalized by `/speckit-requirements`
- Mark unresolved questions as `[NEEDS CLARIFICATION: <question>]`
- Do not invent success metrics — ask the user for baseline and source
- Keep PRD focused: 1–2 pages maximum; link, don't embed
