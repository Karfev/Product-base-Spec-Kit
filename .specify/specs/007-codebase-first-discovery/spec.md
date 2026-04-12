# Spec: 007-codebase-first-discovery

**Initiative:** INIT-2026-006-smart-discovery
**Profile:** Minimal
**Owner:** @dmitriy
**Last updated:** 2026-04-12

## Summary

Обогащение `/speckit-prd` codebase-first логикой: перед каждым вопросом проверять L1/L2/L3 артефакты и предлагать pre-filled ответы. Три режима глубины discovery.

## Motivation / Problem

Текущий `/speckit-prd` задаёт 5 открытых вопросов. Пользователь формулирует ответы с нуля, хотя значительная часть контекста уже существует в репозитории:

- L1 domain glossary определяет терминологию
- L2 architecture задаёт tech stack и patterns
- L2 NFR baseline устанавливает SLO targets
- Предыдущие L3 инициативы содержат паттерны (CRUD API, notification flow, auth patterns)

Datarim решает это через Discovery skill с proposed answers и codebase-first проверкой. У автора это сокращает elicitation в 2-3 раза.

## Scope

- REQ-DISC-003: Codebase-first context loading
- REQ-DISC-004: Proposed answers generation
- REQ-DISC-005: Discovery depth modes

## Non-goals

- Автоматическое заполнение PRD без подтверждения пользователя
- Semantic search по codebase (используем file path conventions)
- Генерация requirements.yml из PRD (это отдельный `/speckit-requirements`)

## User stories

- As a SpecKit user, I want PRD questions to come with suggested answers based on my existing architecture, so that I confirm rather than type from scratch.
- As a SpecKit user starting a notification feature, I want the system to find my existing notification domain glossary and suggest terms, so that I maintain consistency.
- As a SpecKit user working on a Minimal feature, I want fewer PRD questions (3-5), so that I don't over-document trivial changes.

## Algorithm Design

### Context Loading Strategy

```
BEFORE each PRD question:

1. Identify question domain:
   - "tech stack?" → check L2 architecture
   - "NFR targets?" → check L2 NFR baseline
   - "similar features?" → check L3 initiatives
   - "terminology?" → check L1 domain glossary
   - "API patterns?" → check L3 contracts

2. Load relevant files (max 3 per question to limit context):
   - products/{product}/architecture/overview.md
   - products/{product}/nfr-baseline/baseline.md
   - domains/{domain}/glossary.md
   - initiatives/INIT-*/requirements.yml (last 3 by date)
   - initiatives/INIT-*/prd.md (last 3 by date)

3. Extract relevant sections (heading-level match)

4. Generate proposed answer:
   FORMAT: "Предположительно: {answer} (источник: {file}:{section}, обновлён {date}). Верно?"
   
   If source.last_updated > 90 days:
     APPEND: "⚠️ Источник обновлён > 90 дней назад — проверьте актуальность"
   
   If no relevant context found:
     → Ask as open-ended question (current behavior)
```

### Discovery Depth Modes

```
QUICK (3-5 questions) — for Minimal profile:
  1. Цель и проблема (1 вопрос)
  2. Scope: in/out (1 вопрос)
  3. Основные REQs (1 вопрос)
  4. Риски (1 вопрос, optional)
  5. Метрики успеха (1 вопрос, optional)

STANDARD (5-10 questions) — for Standard profile:
  = QUICK +
  6. Пользователи и сценарии (1-2 вопроса)
  7. Архитектурные constraints (1 вопрос)
  8. Contract changes (1 вопрос)
  9. NFR targets vs L2 baseline (1 вопрос)
  10. Dependencies (1 вопрос)

DEEP (10-15 questions) — for Extended+ profile:
  = STANDARD +
  11. Security / threat model scope (1-2 вопроса)
  12. Compliance requirements (1 вопрос)
  13. Migration strategy (1 вопрос)
  14. Rollout constraints (1 вопрос)
  15. Cross-initiative impact (1 вопрос)
```

### Integration Points

Модификация `.claude/commands/speckit-prd.md`:
1. В начале — определить depth mode по профилю (или `--depth` flag)
2. Перед каждым вопросом — context loading (файлы по convention)
3. Для каждого найденного контекста — proposed answer
4. Пользователь: Да / Нет / Уточнить

## Requirements

- REQ-DISC-003 (P0): Codebase-first context loading
- REQ-DISC-004 (P0): Proposed answers generation
- REQ-DISC-005 (P1): Discovery depth modes

## Acceptance criteria

- Given `domains/notifications/glossary.md` exists, when PRD for notification feature, then terms from glossary proposed in context
- Given `products/platform/architecture/overview.md` mentions PostgreSQL, when PRD asks about storage, then proposed "PostgreSQL (источник: overview.md)"
- Given INIT-2026-002 used OpenAPI 3.1, when PRD asks about contract format, then proposed "OpenAPI 3.1 (источник: INIT-2026-002)"
- Given no relevant L1/L2/L3 context, when PRD asks question, then question asked as open-ended (no proposed answer)
- Given profile = Minimal, when `/speckit-prd`, then 3-5 questions asked
- Given `--depth deep` flag, when Minimal profile, then 10-15 questions asked regardless of profile

## Open Questions

| # | Question | Owner | Deadline | Status |
|---|----------|-------|----------|--------|
| 1 | Кешировать ли context loading между вопросами в одной сессии PRD? | @dmitriy | 2026-04-20 | open |
| 2 | Как обрабатывать конфликты между L1 и L2 контекстом (e.g., glossary vs architecture)? | @dmitriy | 2026-04-20 | open |
