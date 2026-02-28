# decisions/

Architecture Decision Records (ADR) для данной инициативы.

Формат: [MADR](https://adr.github.io/madr/) с YAML front-matter.

## Именование файлов

```text
{INIT-YYYY-NNN-slug}-ADR-0001-{short-slug}.md
{INIT-YYYY-NNN-slug}-ADR-0002-{short-slug}.md
```

## Создание нового ADR

1. Скопировать `ADR-template.md` → `{INIT}-ADR-{NNN}-{slug}.md`
2. Заполнить все секции
3. Создать PR — ADR SHOULD ревьюиться перед принятием
4. Обновить `trace.md` с ссылкой на ADR

## Статусы

- `proposed` — на ревью
- `accepted` — принято
- `rejected` — отклонено (сохраняем для истории)
- `deprecated` — устарело
- `superseded` — заменено (указать чем)
