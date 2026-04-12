# Spec: 006-complexity-routing

**Initiative:** INIT-2026-006-smart-discovery
**Profile:** Minimal
**Owner:** @dmitriy
**Last updated:** 2026-04-12

## Summary

Новый command `/speckit-quick` — автоматическое определение профиля инициативы по текстовому описанию задачи с risk-keyword detection и profile override.

## Motivation / Problem

Текущий `/speckit-profile` требует 10 вопросов для определения профиля. Для Minimal-задач это overhead в ~15 мин. Datarim решает аналогичную проблему auto-routing по LOC/files/risk (L1-L4), что позволяет закрывать trivial задачи за 4 шага вместо 9.

SpecKit не может копировать LOC-based подход (у нас spec-first, а не code-first), но может определять профиль по семантике описания задачи + risk-keywords.

## Scope

- REQ-DISC-001: Auto-routing по scope description
- REQ-DISC-002: Risk-keyword detection для override suggestion
- REQ-DISC-006: Profile override из quick mode

## Non-goals

- Замена `/speckit-profile` — он остаётся для Standard+ risk assessment
- ML/NLP классификация — используем keyword heuristics
- Изменения в init.sh scaffold logic (переиспользуем существующий)

## User stories

- As a SpecKit user, I want to describe my task in one sentence and get the right profile automatically, so that I skip the 10-question interview for trivial changes.
- As a SpecKit user, I want the system to warn me if my "simple" task contains risk indicators (auth, PII, migration), so that I don't under-scope critical work.
- As a SpecKit user, I want to override the suggested profile with one command, so that I maintain control over the process depth.

## Algorithm Design

### Complexity Heuristics

```
INPUT: task_description (string)

STEP 1: Risk-keyword scan
  keywords_high = [auth, JWT, OAuth, PII, GDPR, ПДн, payment, billing, migration, breaking change, public API, SLA]
  keywords_medium = [API, REST, event, async, database, schema, contract, deploy, rollback]
  
  if any(kw in description for kw in keywords_high):
    suggested_profile = "extended" if "GDPR" or "ПДн" else "standard"
    risk_warning = "Обнаружены risk-keywords: {matched}"
  elif count(kw in description for kw in keywords_medium) >= 3:
    suggested_profile = "standard"
  else:
    suggested_profile = "minimal"

STEP 2: Component count estimation
  Scan for: "файл", "компонент", "сервис", "endpoint", "таблица", "модуль"
  if mentioned_count > 5: bump to at least "standard"
  if mentioned_count > 15: bump to at least "extended"

STEP 3: Output
  if suggested_profile == "minimal":
    → Run scaffold immediately (init.sh --profile minimal)
    → Skip /speckit-profile
  else:
    → Show: "Предложен профиль: <profile>. <risk_warning>. Подтвердить? [Да / Переопределить / Пройти /speckit-profile]"
```

### Integration с `/speckit-start`

```
/speckit-start
  ├─ "Быстрый старт? Опиши задачу в 1-2 предложениях"
  │   └─ → /speckit-quick <description>
  └─ "Полный профиль? Пройди risk assessment"
      └─ → /speckit-profile (текущий flow)
```

## Requirements

- REQ-DISC-001 (P0): Auto-routing по scope description
- REQ-DISC-002 (P0): Risk-keyword detection
- REQ-DISC-006 (P1): Profile override

## Acceptance criteria

- Given описание "Исправить опечатку в README", when `/speckit-quick`, then профиль = Minimal, scaffold создан, 0 вопросов
- Given описание "Добавить JWT auth в API gateway с rate limiting", when `/speckit-quick`, then предложен Standard, warning "auth, API"
- Given описание "Обработка ПДн пользователей по 152-ФЗ", when `/speckit-quick`, then предложен Extended, warning "ПДн"
- Given auto-routing = Minimal, when пользователь делает override → Standard, then scaffold дополнен Standard артефактами

## Open Questions

| # | Question | Owner | Deadline | Status |
|---|----------|-------|----------|--------|
| 1 | Нужно ли поддерживать Enterprise profile в auto-routing или только Minimal/Standard/Extended? | @dmitriy | 2026-04-20 | open |
| 2 | Хранить ли лог auto-routing решений для будущего self-evolution? | @dmitriy | 2026-04-20 | open |
