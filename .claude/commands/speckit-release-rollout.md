---
description: Сформировать release rollout-пакет (rollout/migration/links) и проверить консистентность с SLO/PRR
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

Ты готовишь release-пакет для инициативы `$ARGUMENTS` перед выпуском.

## Что нужно сделать

1. Прочитай:
   - `initiatives/$ARGUMENTS/requirements.yml` (определи `profile`),
   - `initiatives/$ARGUMENTS/ops/slo.yaml`,
   - `initiatives/$ARGUMENTS/ops/prr-checklist.md`,
   - `initiatives/$ARGUMENTS/design.md` и/или `trace.md` (если есть),
   - `initiatives/$ARGUMENTS/delivery/rollout.md` (если уже есть),
   - `initiatives/$ARGUMENTS/delivery/migration.md` (если уже есть).

2. Обнови `delivery/rollout.md` так, чтобы файл был **готов к релизу**, без `{placeholders}`:
   - стратегия rollout (internal/canary/production),
   - feature flag и владелец,
   - явные пороги/условия перехода,
   - мониторинг + ссылка на SLO в формате `ops/slo.yaml#<slo-id>`,
   - rollback trigger и пошаговый rollback runbook.

3. Для профилей `extended` и `enterprise` обязательно обнови `delivery/migration.md`:
   - тип(ы) миграции,
   - предусловия,
   - пошаговый план,
   - rollback по шагам,
   - post-migration validation.

4. Проверь, что в rollout добавлены **ссылки на feature flags и rollback-триггеры**.
   - Feature flag должен быть указан в секции стратегии и в шагах rollback.
   - Rollback trigger должен быть выражен измеримым условием (например, error rate / latency / saturation + окно времени).

5. Проверь консистентность с `ops/slo.yaml` и `ops/prr-checklist.md`:
   - каждый `kind: SLO` (`metadata.name`) из `ops/slo.yaml` упоминается в `delivery/rollout.md`;
   - в `ops/prr-checklist.md` есть явные пункты про `delivery/rollout.md`, rollback и feature flags;
   - для `extended|enterprise` присутствует `delivery/migration.md`.

6. Запусти проверку:

```bash
python3 tools/scripts/check-release-rollout.py --initiative $ARGUMENTS
```

7. Если проверка не проходит — внеси правки и перезапусти команду до зелёного статуса.

## Формат результата

- Покажи короткий отчёт:
  - какие файлы изменены,
  - какие SLO/feature flags/rollback triggers привязаны,
  - результат `check-release-rollout.py`.
- Не оставляй незаполненные плейсхолдеры в `delivery/*.md`.
- Не придумывай несуществующие метрики/дашборды: используй только артефакты инициативы.
