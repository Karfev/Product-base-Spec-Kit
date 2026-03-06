# .specify/specs/

Директория для L4 Feature spec-kit.

## Использование

1. Скопировать папку `{NNN}-{slug}/` с новым именем: `042-export-csv/`
2. Заполнить все `{placeholder}` в файлах по каноническому формату `spec.md`
3. Связать `REQ-ID` с записями в `../../../initiatives/{INIT}/requirements.yml`

## Структура

```text
{NNN}-{slug}/
  spec.md    ← канонический формат: Summary, Scope, Non-goals, API/Contracts, Test strategy, Rollout
  plan.md    ← архитектурные решения и impact
  tasks.md   ← task-checklist для инженера
  trace.md   ← RTM: REQ → контракты/тесты/SLO
```

## Канонический формат spec.md

Обязательные разделы в `spec.md`:

1. Summary
2. Motivation / Problem
3. Scope
4. Non-goals
5. API/Contracts
6. User stories
7. Requirements
8. Test strategy
9. Acceptance criteria
10. Rollout
11. Open Questions
