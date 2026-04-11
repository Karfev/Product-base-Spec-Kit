# contracts/

Machine-readable API contracts. Источники истины для интерфейсов.

| Файл | Формат | CI инструмент |
|---|---|---|
| `openapi.yaml` | OpenAPI 3.1.1 | `redocly lint` / `spectral lint` |
| `asyncapi.yaml` | AsyncAPI 3.0 | `asyncapi validate` |
| `schemas/*.json` | JSON Schema 2020-12 | `check-jsonschema` |

## Проверка breaking changes

```bash
# OpenAPI
oasdiff breaking contracts/openapi.yaml <base-version>

# AsyncAPI
asyncapi diff contracts/asyncapi.yaml <base-version>
```
