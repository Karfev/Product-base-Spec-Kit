# Plan: 008-consilium

**Initiative:** INIT-2026-007-quality-augmentation
**Owner:** @dmitriy
**Last updated:** 2026-04-12

## Architecture choices

- **Sequential role switching over parallel agents:** Один агент последовательно принимает роли (Datarim pattern). Параллельные агенты = координационная сложность без выигрыша для review task. Каждая роль — отдельный prompt с загрузкой context_files.
- **YAML role config over hardcoded:** Роли определяются в `.specify/memory/consilium-roles.yml`. Extensible: пользователь добавляет custom роли без модификации command.
- **ADR-template-v2 compatibility:** Output format совместим с секцией "Доменные оценки" из ADR-template-v2 Архкомма. Не изобретаем свой формат.
- **Presets from Архкомм levels:** standard (У0→У1 light), archkom-l1 (У1), archkom-l2 (У2). Mapping 1:1 с governance levels.

## Implementation approach

### Новые файлы

1. **`.claude/commands/speckit-consilium.md`** — Command file: parse ADR path → determine panel → sequential role execution → aggregate → output.

2. **`.specify/memory/consilium-roles.yml`** — Role definitions: name, id, context_files, checklist, verdict_format. 5 base roles + presets mapping.

### Role Execution Template

Для каждой роли агент получает structured prompt:

```
Ты выступаешь в роли {role.name}.
Твоя задача — проанализировать ADR {adr_path} с позиции {role.name}.

КОНТЕКСТ (загружен из артефактов):
{context_from_files}

CHECKLIST:
{role.checklist}

Для каждого пункта checklist:
1. Проверь, покрыт ли он в ADR
2. Если покрыт — OK
3. Если есть замечание — опиши конкретно, со ссылкой на артефакт
4. Если критичный пропуск — Блокер

OUTPUT FORMAT:
| Пункт | Статус | Комментарий |
|---|---|---|
| {checklist_item} | OK / Замечание / Блокер | {detail} |

ИТОГО: {OK / Замечание / Блокер} — {summary sentence}
```

### Integration с ADR

Output вставляется как markdown section:

```markdown
## Доменные оценки (consilium)

> Сгенерировано `/speckit-consilium` {date}. Preset: {preset}.

| Домен | Статус | Комментарий |
|---|---|---|
| Прикладная архитектура | OK | Решение соответствует C4, alternatives рассмотрены |
| ИБ | Замечание | Threat-model не обновлён для нового endpoint |
| БД/нагрузки | OK | Нагрузочный профиль адекватен baseline |
| Инфраструктура | Блокер | Rollback strategy отсутствует |
| Интеграции | OK | Contract backward-compatible |

**Итог:** Требует доработки. Блокер: rollback strategy.
**Условия:**

| # | Условие | Ответственный | Срок |
|---|---------|--------------|------|
| 1 | Добавить rollback strategy в delivery/rollout.md | @architect | {date+5d} |
```

## Risks

- **Shallow reviews:** Агент генерирует "OK" без реального анализа → mitigation: checklist items require specific artifact references.
- **Context overload:** 5 ролей × 2-3 context files = потенциально большой context window → mitigation: heading-level extraction, max 500 tokens per context file.
- **Format drift:** ADR formats различаются между Minimal/Standard/Extended → mitigation: section injection по markdown heading, не по line number.

## Effort estimate

- `consilium-roles.yml` (5 roles + 3 presets): ~2 часа
- `speckit-consilium.md` command: ~4-5 часов
- PoC на PLAT-0003-async-queue: ~1 час
- Testing (3 сценария): ~2 часа
- **Total: ~9-11 часов**
