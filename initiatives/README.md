# initiatives/

L3 Initiative-уровень. Каждая папка — одна инициатива.

## Использование

1. Скопировать `{INIT-YYYY-NNN-slug}/` → `INIT-2026-042-my-feature/`
2. Заполнить все `{placeholder}` в файлах
3. Выбрать профиль: Minimal / Standard / Extended
4. Удалить файлы профилей выше выбранного (Extended-файлы не нужны для Minimal)

## Профили

| Профиль | Обязательные файлы |
|---|---|
| **Minimal** | README.md, prd.md, requirements.yml, changelog/CHANGELOG.md |
| **Standard** | + design.md, decisions/*, contracts/*, trace.md, delivery/rollout.md, ops/slo.yaml, ops/prr-checklist.md |
| **Extended** | + delivery/migration.md, ops/nfr-validation.md, ops/threat-model.md, compliance/regulatory-review.md |

## Инструменты CI

```bash
# Проверить requirements.yml
check-jsonschema --schemafile ../../tools/schemas/requirements.schema.json requirements.yml

# Линт OpenAPI
redocly lint contracts/openapi.yaml

# Проверить breaking changes OpenAPI
oasdiff breaking contracts/openapi.yaml <base-version>
```
