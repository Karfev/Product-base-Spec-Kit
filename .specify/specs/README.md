# .specify/specs/

Директория для L4 Feature spec-kit.

## Использование

1. Скопировать папку `{NNN}-{slug}/` с новым именем: `042-export-csv/`
2. Заполнить все `{placeholder}` в файлах
3. Связать `REQ-ID` с записями в `../../../initiatives/{INIT}/requirements.yml`

## Структура

```text
{NNN}-{slug}/
  spec.md    ← что делаем и зачем
  plan.md    ← архитектурные решения и impact
  tasks.md   ← task-checklist для инженера
  trace.md   ← RTM: REQ → контракты/тесты/SLO
```
