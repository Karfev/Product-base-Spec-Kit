# tools/schemas/

CI-валидаторы (JSON Schema) для machine-readable артефактов.

| Схема | Валидирует | Инструмент | Профиль |
|---|---|---|---|
| `requirements.schema.json` | `requirements.yml` во всех инициативах | `check-jsonschema` | все |
| `subsystem-classification.schema.json` | `subsystem-classification.yaml` в Enterprise-инициативах | `check-jsonschema` | Enterprise |

## Использование

```bash
# Все requirements.yml (все профили)
check-jsonschema --schemafile tools/schemas/requirements.schema.json \
  initiatives/{INIT}/requirements.yml

# subsystem-classification.yaml (только Enterprise-инициативы)
check-jsonschema --schemafile tools/schemas/subsystem-classification.schema.json \
  initiatives/{INIT}/subsystem-classification.yaml

# Или через make (проверяет всё сразу)
make validate
```
