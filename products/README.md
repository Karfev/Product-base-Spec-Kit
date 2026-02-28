# products/

L2 Product-уровень. Каждая папка — один продукт.

Переименуйте `{product}` в реальное название продукта (например: `analytics`, `billing`, `api-gateway`).

| Файл | Когда создавать | Профиль |
|---|---|---|
| `architecture/overview.md` | При изменении product context | Minimal |
| `decisions/{PROD}-0001-{slug}.md` | При архитектурных развилках | Standard+ |
| `nfr-baseline/baseline.md` | Privacy/security/reliability baseline | Standard+ |
