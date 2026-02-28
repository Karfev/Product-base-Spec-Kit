# Architecture: {product}

**Продукт:** {product}
**Владелец:** @{tech-lead}
**Последнее обновление:** {YYYY-MM-DD}

## Контекст (C4: Context)

{Описание системы, внешних акторов и систем}

```mermaid
C4Context
  title System Context: {product}
  Person(user, "{User}", "{Description}")
  System(sys, "{product}", "{Description}")
  System_Ext(ext, "{External System}", "{Description}")
  Rel(user, sys, "uses")
  Rel(sys, ext, "calls")
```

## Контейнеры (C4: Container)

| Сервис | Ответственность | Технология | Репозиторий |
|---|---|---|---|
| `{service}` | {responsibility} | {tech} | `{repo-link}` |

## Ключевые ADR

- `decisions/{PROD}-0001-{slug}.md` — {краткий смысл}

## Домены

- Относится к домену: `domains/{domain}/`
