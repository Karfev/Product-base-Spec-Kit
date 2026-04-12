# Plan: 010-ai-quality-gates

**Initiative:** INIT-2026-007-quality-augmentation
**Owner:** @dmitriy
**Last updated:** 2026-04-12

## Architecture choices

- **Markdown document over YAML config:** Quality gates как human-readable markdown, не YAML. Агент читает и интерпретирует правила — формат должен быть естественным. YAML — для machine-validated artifacts (requirements, schemas).
- **Agent-enforced over CI-enforced:** Основной enforcement — через prompts в `/speckit-implement`. CI `check-spec-quality.py` — backup для post-hoc detection (T2b before T2a). Не пытаемся заменить linter/static analysis.
- **Contract-aware as 5th pillar:** Специфика SpecKit vs Datarim. Datarim's Five Pillars generic. Наш 5-й pillar — contract compliance: implementation ↔ OpenAPI/AsyncAPI match. Это differentiator.
- **Standard+ only:** Quality gates не применяются к Minimal профилю. Minimal = quick fix, overhead не оправдан.

## Implementation approach

### Новый файл: `tools/ai-quality-gates.md`

~100-150 строк. Структура:
1. Когда применять (Standard+ профиль, T2a/T2b phase)
2. Five Pillars с правилами и примерами
3. Enforcement checklist (копируется в /speckit-implement)
4. Anti-patterns (что НЕ делать)

### Модификация: `.claude/commands/speckit-implement.md`

Добавить в начало T2b phase:

```
BEFORE T2b:
  1. Read tools/ai-quality-gates.md
  2. Pre-flight checklist:
     □ T2a tests written and failing (RED)?
     □ Architecture stubs created?
     □ Stubs match contracts (make lint-contracts)?
     □ Scope declared (which files, which methods)?
  3. If any unchecked → WARNING with specific blocker
  4. If all checked → proceed to implementation
```

### Расширение: `tools/scripts/check-spec-quality.py`

Добавить функцию `check_task_ordering()`:
- Parse tasks.md checkboxes
- Detect `- [x] **T2b**` without `- [x] **T2a**` above it
- Emit warning (not blocking in v1, blocking after 2 weeks per constitution convention)

## Risks

- **Over-enforcement:** Агент отказывается писать код из-за формальных gates → mitigation: gates = warnings, не hard blocks (except T2a→T2b ordering)
- **Pillar drift:** Pillars устаревают, не обновляются → mitigation: link to evolution loop (INIT-2026-006 self-reflection, future P2)
- **False positives in CI:** T2b "checked" может означать "partially done" → mitigation: parse strictly only `[x]` pattern

## Effort estimate

- `tools/ai-quality-gates.md` (5 pillars + examples): ~3 часа
- `/speckit-implement` modification: ~2-3 часа
- `check-spec-quality.py` extension: ~2 часа
- Testing (3 сценария): ~1 час
- **Total: ~8-10 часов**
