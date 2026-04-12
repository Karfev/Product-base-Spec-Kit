# Plan: 007-codebase-first-discovery

**Initiative:** INIT-2026-006-smart-discovery
**Owner:** @dmitriy
**Last updated:** 2026-04-12

## Architecture choices

- **File convention over semantic search:** Контекст загружается по известным путям (`domains/*/glossary.md`, `products/*/architecture/overview.md`), а не через embedding search. Предсказуемо, не требует зависимостей, работает offline.
- **Heading-level extraction:** Из больших файлов извлекаются только релевантные секции по heading match. Это ограничивает context window нагрузку.
- **Max 3 files per question:** Hard limit на количество файлов, загружаемых для одного вопроса. Предотвращает context overflow при большом количестве L3 инициатив.
- **Graceful degradation:** Если артефакты не найдены — вопрос задаётся как open-ended. Нет fallback error, нет block.

## Implementation approach

### Модификация: `.claude/commands/speckit-prd.md`

Основные изменения в существующем command file:

**1. Depth mode selector (начало command):**
```
Read initiative profile from requirements.yml metadata.
Map: minimal → quick, standard → standard, extended/enterprise → deep.
Allow --depth override.
```

**2. Context loading block (перед каждым вопросом):**
```
For question about {domain}:
  1. Glob for matching files in domains/, products/, initiatives/
  2. Read matching files (max 3, sorted by last_updated desc)
  3. Extract heading-matched sections
  4. Format as proposed answer with source attribution
```

**3. Proposed answer format:**
```
Предположительно: {extracted_content}
(источник: {relative_path}, обновлён {date})
Верно? [Да / Нет / Уточнить]
```

### Question → File Mapping

| Вопрос PRD | Files to check | Heading/section |
|---|---|---|
| Цель и проблема | Last 3 L3 prd.md | "Цель и ожидаемый эффект" |
| Tech stack | L2 architecture/overview.md | "Technology", "Stack", "Components" |
| NFR targets | L2 nfr-baseline/baseline.md | Все |
| Терминология | L1 glossary.md (matching domain) | Все |
| API patterns | Last 3 L3 contracts/openapi.yaml | paths section |
| Сценарии | Last 3 L3 prd.md | "Пользователи и сценарии" |
| Security | L3 ops/threat-model.md (if Extended) | "Threats", "Mitigations" |
| Compliance | L1 regulatory/requirements.md | Все |

## Risks

- **Context staleness:** L2 overview.md не обновлялся 6 месяцев → proposed answer устаревший. Mitigation: timestamp warning > 90 дней.
- **Context overload:** Много L3 инициатив → медленный glob. Mitigation: max 3 files, sorted by date.
- **False confidence:** Пользователь бездумно подтверждает proposed answers. Mitigation: показывать source + date, форсировать [Нет] option.

## Effort estimate

- Question → File mapping table: ~1 час
- Context loading logic в speckit-prd.md: ~3-4 часа
- Depth mode selector: ~1 час
- Proposed answer formatting: ~1 час
- Testing (4 сценария): ~2 часа
- **Total: ~8-10 часов**
