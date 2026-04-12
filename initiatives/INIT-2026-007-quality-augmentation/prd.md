# PRD: Quality Augmentation — Consilium + AI Quality Gates

**Initiative:** INIT-2026-007-quality-augmentation
**Owner (PM):** @dmitriy
**Last updated:** 2026-04-12
**Profile:** Minimal
**Source:** Datarim competitive analysis (`CLAUDE OUTPUTS/SpecKit/SpecKit_Datarim-Analysis_Report_v1.md`)

---

## Цель и ожидаемый эффект

- **Проблема:** SpecKit обеспечивает traceability и governance, но два слепых пятна снижают качество выходных артефактов:
  1. **ADR single-perspective bias.** ADR пишется одним агентом в одной роли. В модели Архкомма доменные оценки (ИБ, БД, инфраструктура, интеграции) — обязательны для У1/У2, но в SpecKit pipeline нет механизма structured multi-perspective review. Агент не переключает роли систематически.
  2. **No implementation quality constraints.** T2a/T2b в tasks.md определяют порядок (tests → code), но не содержат constraints: max LOC per method, decomposition rules, architecture-first stubs. Качество кода зависит исключительно от агента. Datarim решает это через Five Pillars of AI Quality.
- **Почему сейчас:** INIT-2026-009-smoke-test показал, что graduated ADR (PLAT-0003-async-queue) принимался без формального multi-perspective review. Архкомм внедряет доменные оценки (ADR-template-v2), но SpecKit pipeline их не автоматизирует. AI quality gates отсутствуют — P16 bug в evidence report INIT-2026-002 (threat-model в Standard) подтверждает, что артефакты создаются без quality checks.
- **Цель (Outcome):** Повысить качество ADR за счёт structured multi-perspective review (consilium) и качество implementation за счёт кодифицированных AI quality gates.

## Пользователи и сценарии

- **Primary persona:** SpecKit user (architect / tech lead), работающий над Standard+ инициативами.
- **Top JTBD / сценарии:**
  1. **Consilium перед ADR:** Архитектор готовит ADR → запускает `/speckit-consilium` → получает structured review от 3 ролей (Architect, Security, Ops) → вносит корректировки → финализирует ADR с секцией "Доменные оценки" заполненной (REQ-QUAL-001, REQ-QUAL-002, REQ-QUAL-003).
  2. **AI quality gate перед T2b:** Developer готов к implementation → `/speckit-implement` проверяет pre-conditions: stubs created? tests written? → enforcement checklist перед каждым T2b (REQ-QUAL-004, REQ-QUAL-005).
  3. **Custom panel composition:** Для инициативы с PII пользователь добавляет роль Compliance в consilium panel (REQ-QUAL-006).

## Метрики успеха

| Метрика | Baseline | Target | Период | Источник |
|---|---:|---:|---|---|
| ADR с заполненными доменными оценками | ~20% | ≥ 80% (Standard+) | 90d | Git audit |
| Defects caught at consilium (before merge) | 0 | ≥ 2 per ADR avg | 90d | Consilium logs |
| Methods > 50 LOC in implementation | Unknown | < 10% | 90d | Code review |
| T2b without T2a (tests after code) | ~40% (est.) | 0% | 30d | CI check-spec-quality |

## Scope

**In-scope:**
- Новый command `/speckit-consilium` — structured multi-perspective review для ADR
- Роли consilium из модели Архкомма: доменные оценки (ИБ, БД, инфраструктура, интеграции и др.)
- Файл `tools/ai-quality-gates.md` — кодифицированные constraints для AI-assisted implementation
- Модификация `/speckit-implement` — enforcement checklist перед T2b
- Расширение `check-spec-quality.py` — lint: T2b без T2a = warning

**Non-goals:**
- Замена Архкомма как governance body — consilium дополняет, не заменяет
- Автоматический approve ADR — consilium генерирует review, человек принимает решение
- Runtime code analysis (linting, static analysis) — только spec-level quality gates
- Модификации JSON Schemas или constitution.md

## Риски и ограничения

- **Consilium theater:** Агент генерирует формальные "оценки" без реального анализа → mitigated by structured prompts per role (каждая роль загружает свой контекст: Security → threat model, Ops → SLO baseline)
- **Quality gate friction:** Слишком строгие gates блокируют Minimal профиль → mitigated by gates only for Standard+ (Minimal excluded)
- **Role hallucination:** Агент в роли Security может "придумать" уязвимости → mitigated by requiring reference to existing artifacts (threat-model.md, L2 NFR baseline)

## Требования (ссылки на REQ)

Реестр требований — в `requirements.yml`. Здесь только ссылки:

- `REQ-QUAL-001` (P1): Consilium multi-perspective review command
- `REQ-QUAL-002` (P1): Архкомм-aligned domain roles в consilium
- `REQ-QUAL-003` (P1): Consilium output в ADR "Доменные оценки"
- `REQ-QUAL-004` (P1): AI quality gates document
- `REQ-QUAL-005` (P1): Enforcement checklist в `/speckit-implement`
- `REQ-QUAL-006` (P2): Custom panel composition

## Приёмка

- Acceptance tests: Прогнать consilium на существующем ADR (PLAT-0003-async-queue), оценить добавленную ценность
- AI quality gates: Прогнать `/speckit-implement` с enforcement на INIT-2026-009-smoke-test tasks
- Definition of done по профилю: `.specify/memory/constitution.md#профили` (Minimal)
