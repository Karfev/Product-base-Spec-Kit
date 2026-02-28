# tools/schemas/

CI-валидаторы (JSON Schema) для machine-readable артефактов.

| Схема | Валидирует | Инструмент |
|---|---|---|
| `requirements.schema.json` | `requirements.yml` во всех инициативах | `check-jsonschema` |

## Использование

```bash
check-jsonschema --schemafile tools/schemas/requirements.schema.json \
  initiatives/{INIT}/requirements.yml
```
