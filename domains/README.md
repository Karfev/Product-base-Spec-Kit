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
