# PRD: Self-Evolution Loop

**Initiative:** INIT-2026-010-self-evolution
**Owner (PM):** @dmitriy
**Last updated:** 2026-04-12
**Profile:** Minimal
**Source:** Datarim competitive analysis (`CLAUDE OUTPUTS/SpecKit/SpecKit_Datarim-Analysis_Report_v1.md`)

---

## Цель и ожидаемый эффект

- **Проблема:** SpecKit — статичный framework. Улучшения приходят только через ручные коммиты в constitution.md и шаблоны. После завершения инициативы нет механизма обучения: не фиксируется, какие артефакты реально использовались, где были bottleneck'и, какие шаблоны оказались избыточными. Это приводит к: (1) повторению одних и тех же проблем в новых инициативах, (2) накоплению dead weight в шаблонах, (3) отсутствию data-driven feedback для улучшения framework.
- **Почему сейчас:** С ростом adoption (INIT-2026-004) и числа завершённых инициатив (9 INIT на апрель 2026) накапливается опыт, который не систематизируется. Datarim решает это через `/dr-reflect` (lessons learned + evolution proposals) и `evolution-log.md`. После внедрения Session State (INIT-2026-008) и Quality Gates (INIT-2026-007) появляется достаточно structured data для автоматического анализа.
- **Цель (Outcome):** Создать feedback loop, который после каждой завершённой инициативы генерирует actionable insights и proposals для улучшения framework. Сократить cycle time обнаружения системных проблем с «когда-нибудь заметим» до 1 рабочего дня после graduation.

## Пользователи и сценарии

- **Primary persona:** SpecKit maintainer (architect / CPTO), ответственный за эволюцию framework.
- **Secondary persona:** SpecKit user (tech lead), получающий улучшения без ручной работы.
- **Top JTBD / сценарии:**
  1. **Post-mortem reflection:** Пользователь завершает инициативу → `/speckit-reflect INIT-2026-006` → агент анализирует lifecycle, генерирует `reflection.md` с findings и предложениями (REQ-EVOL-001, REQ-EVOL-002).
  2. **Evolution proposal:** Reflection выявляет паттерн (напр. «requirements.yml переписывалась 4+ раза на каждой Standard-инициативе») → предложение обновить template → proposal в формате PR-ready diff (REQ-EVOL-003, REQ-EVOL-004).
  3. **Controlled apply:** Maintainer ревьюит proposals → approve/reject → одобренные применяются через PR в constitution/templates. Никакие изменения framework не применяются автоматически (REQ-EVOL-005).

## Метрики успеха

| Метрика | Baseline | Target | Период | Источник |
|---|---:|---:|---|---|
| Инициативы с reflection | 0% | ≥ 80% (Standard+) | 90d | `initiatives/*/reflection.md` |
| Proposals → applied rate | 0 | ≥ 30% proposals принято | 90d | `evolution-log.md` |
| Cycle time: проблема → fix в constitution | Ad hoc (~weeks) | ≤ 3 рабочих дня | 90d | Git log |

## Scope

**In-scope:**
- Новый command `/speckit-reflect <INIT>` — анализ завершённой инициативы
- Template для `reflection.md` с structured findings
- Механизм evolution proposals (PR-ready формат)
- `evolution-log.md` — лог всех proposals и их статусов
- Health metrics: триггеры для автоматического audit (опционально)

**Out-of-scope:**
- Автоматическое применение proposals без human approval
- ML/LLM-based pattern detection across initiatives (future)
- Интеграция с CI/CD pipeline для автоматических PR
