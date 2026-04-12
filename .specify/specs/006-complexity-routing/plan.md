# Plan: 006-complexity-routing

**Initiative:** INIT-2026-006-smart-discovery
**Owner:** @dmitriy
**Last updated:** 2026-04-12

## Architecture choices

- **Keyword heuristics over ML:** Простой regex/keyword matching. Не требует зависимостей, работает offline, предсказуем. ML-классификация — overkill для v1.
- **Reuse init.sh:** `/speckit-quick` вызывает существующий `init.sh --profile <detected>`. Нет дублирования scaffold logic.
- **Command composition:** `/speckit-quick` = routing logic + `/speckit-start` flow. Не отдельный pipeline — встраивается в существующий.

## Implementation approach

### Новый файл: `.claude/commands/speckit-quick.md`

SKILL.md command file, аналогичный существующим speckit-* commands. Содержит:
1. Risk-keyword dictionary (hardcoded, ~30 keywords в 2 группах)
2. Component count heuristic
3. Profile suggestion logic
4. Integration с init.sh

### Модификация: `.claude/commands/speckit-start.md`

Добавить routing choice в начало:
- "Быстрый старт (опиши задачу)" → `/speckit-quick`
- "Полный профиль" → `/speckit-profile`

### Risk-keyword dictionary

Вынести в отдельный файл `.specify/memory/risk-keywords.yml` для maintainability:

```yaml
high_risk:
  - pattern: "auth|authentication|JWT|OAuth|OIDC"
    min_profile: standard
    reason: "Authentication affects security posture"
  - pattern: "PII|GDPR|ПДн|152-ФЗ|персональн"
    min_profile: extended
    reason: "PII/GDPR requires threat model and compliance review"
  - pattern: "payment|billing|платёж|тариф"
    min_profile: standard
    reason: "Financial transactions require audit trail"
  - pattern: "migration|миграц"
    min_profile: standard
    reason: "Data migrations require rollback strategy"

medium_risk:
  - pattern: "API|REST|endpoint"
  - pattern: "event|async|kafka|rabbitmq"
  - pattern: "database|schema|таблиц"
  - pattern: "contract|контракт"
  - pattern: "deploy|rollback|canary"
```

## Risks

- **Over-classification:** Keyword "API" встречается в описании 80% задач → может всегда предлагать Standard. Mitigation: medium_risk требует ≥ 3 совпадений, не 1.
- **Под-classification:** Задача без keywords, но высокого risk (e.g., "переделать модуль X"). Mitigation: всегда показывать "Override? [Да / /speckit-profile]".

## Effort estimate

- `/speckit-quick` command: ~2-3 часа
- Risk-keyword dictionary: ~1 час
- `/speckit-start` modification: ~1 час
- Testing (3 сценария): ~1 час
- **Total: ~5-6 часов**
