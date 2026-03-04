# domains/

L1 Domain-уровень. Каждая папка — один домен.

Переименуйте `{domain}` в реальное название домена (например: `billing`, `auth`, `analytics`).

## Профили обязательности

| Файл | Когда создавать | Профиль |
|---|---|---|
| `glossary.md` | При добавлении новых терминов/сущностей | Minimal |
| `canonical-model/model.md` | При изменении доменной модели/событий | Standard+ |
| `event-catalog/events.md` | При изменении доменных событий | Standard+ |
| `nfr/domain-nfr.md` | При затрагивании данных/зон риска | Extended |
| `regulatory/requirements.md` | При регуляторных требованиях | Extended |

## Существующие домены

| Домен | Описание | ADR |
|-------|----------|-----|
| [`is-ontology/`](is-ontology/README.md) | Онтология архитектуры ИС: глоссарий (~34 термина), трёхслойная модель ArchiMate, таксономия взаимосвязей, NFR-профиль ГОСТ 25020 | [PLAT-0002](../decisions/PLAT-0002-is-ontology-integration.md) |
