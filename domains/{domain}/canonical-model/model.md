# Canonical Model: {domain}

**Профиль:** Standard+
**Последнее обновление:** {YYYY-MM-DD}

## Обзор

{Описание доменной модели — основные агрегаты, их связи}

## Сущности

### {EntityName}

| Поле | Тип | Обязательное | Описание |
|---|---|---|---|
| `id` | string | MUST | Уникальный идентификатор |
| `{field}` | {type} | {MUST\|SHOULD\|MAY} | {description} |

**Инварианты:**
- {бизнес-правило 1}
- {бизнес-правило 2}

## Диаграмма (mermaid)

```mermaid
erDiagram
    {ENTITY_A} {
        string id
        string field1
    }
    {ENTITY_B} {
        string id
        string entity_a_id
    }
    {ENTITY_A} ||--o{ {ENTITY_B} : "has"
```
