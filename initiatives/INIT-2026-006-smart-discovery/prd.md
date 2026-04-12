# PRD: Smart Discovery — Auto-Routing + Codebase-First Elicitation

**Initiative:** INIT-2026-006-smart-discovery
**Owner (PM):** @dmitriy
**Last updated:** 2026-04-12
**Profile:** Minimal
**Source:** Datarim competitive analysis (`CLAUDE OUTPUTS/SpecKit/SpecKit_Datarim-Analysis_Report_v1.md`)

---

## Цель и ожидаемый эффект

- **Проблема:** SpecKit требует ручного профилирования (`/speckit-profile`, 10 вопросов) даже для тривиальных задач уровня Minimal. `/speckit-prd` задаёт 5 открытых вопросов без учёта контекста — пользователь формулирует ответы с нуля, хотя 60-80% информации уже есть в L1 domains, L2 architecture и предыдущих L3 инициативах. Конкурент Datarim решает обе проблемы: auto-routing по LOC/risk и proposed-answer discovery.
- **Почему сейчас:** INIT-2026-004-adoption-path установил SLO time-to-first-validate ≤ 30 мин (REQ-ADOPT-007). Текущий friction на этапе profiling + PRD — основной bottleneck для достижения этого SLO. Datarim демонстрирует работающую альтернативу (1000+ задач/год одним человеком).
- **Цель (Outcome):** Сократить время от идеи до валидированного `requirements.yml` с ~45 мин до ~15 мин для Minimal-профиля и с ~2-4 часов до ~1-1.5 часа для Standard.

## Пользователи и сценарии

- **Primary persona:** SpecKit user (tech lead / architect), запускающий новую инициативу.
- **Top JTBD / сценарии:**
  1. **Quick fix routing:** Пользователь описывает задачу в 1-2 предложениях → система автоматически определяет Minimal профиль → scaffold без интервью (REQ-DISC-001, REQ-DISC-002).
  2. **Codebase-first PRD:** Пользователь запускает `/speckit-prd` → система проверяет L1 glossary, L2 architecture, L3 паттерны → предлагает pre-filled ответы → пользователь подтверждает/корректирует (REQ-DISC-003, REQ-DISC-004, REQ-DISC-005).
  3. **Profile override:** Система предложила Minimal, пользователь знает о скрытых рисках (auth, PII) → override до Standard+ одной командой (REQ-DISC-006).

## Метрики успеха

| Метрика | Baseline | Target | Период | Источник |
|---|---:|---:|---|---|
| Time-to-first-validate (Minimal) | ~45 мин | ≤ 15 мин | 30d | Manual timing |
| Time-to-first-validate (Standard) | ~2-4 ч | ≤ 1.5 ч | 30d | Manual timing |
| Profile accuracy (auto vs manual) | N/A | ≥ 90% match | 90d | Retrospective |
| PRD questions skipped (codebase-first) | 0/5 | ≥ 2/5 avg | 30d | Command telemetry |

## Scope

**In-scope:**
- Новый command `/speckit-quick` — auto-routing по scope description
- Модификация `/speckit-prd` — codebase-first proposed answers
- Модификация `/speckit-start` — интеграция с quick routing
- Три режима discovery depth: Quick (3-5 Q), Standard (5-10 Q), Deep (10-15 Q)

**Non-goals:**
- Замена `/speckit-profile` — он остаётся для явного risk assessment (Standard+)
- Автоматическое повышение профиля (только предложение + human confirm)
- Machine-readable profile inference (heuristic достаточно для v1)
- Изменения в constitution.md или JSON schemas

## Риски и ограничения

- **False Minimal:** Auto-routing может недооценить complexity → пропустить auth/PII → mitigated by risk-keyword detection (auth, PII, GDPR, migration, payment → suggest Standard+)
- **Stale context:** L1/L2/L3 артефакты могут быть устаревшими → proposed answers будут неточными → mitigated by timestamp check + warning "[Контекст L2 обновлён > 90 дней назад]"
- **Adoption friction:** Два пути входа (quick vs profile) могут запутать новых пользователей → mitigated by QUICKSTART.md update + `/speckit-start` routing logic

## Требования (ссылки на REQ)

Реестр требований — в `requirements.yml`. Здесь только ссылки:

- `REQ-DISC-001` (P0): Auto-routing по scope description
- `REQ-DISC-002` (P0): Risk-keyword detection для override suggestion
- `REQ-DISC-003` (P0): Codebase-first context loading в PRD
- `REQ-DISC-004` (P0): Proposed answers generation
- `REQ-DISC-005` (P1): Discovery depth modes (Quick/Standard/Deep)
- `REQ-DISC-006` (P1): Profile override из quick mode

## Приёмка

- Acceptance tests: Manual walkthrough — 3 сценария (Quick fix, Standard feature, False Minimal catch)
- Definition of done по профилю: `.specify/memory/constitution.md#профили` (Minimal)
