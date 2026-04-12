# Rollout Plan: INIT-2026-009-smoke-test

**Профиль:** Standard
**Последнее обновление:** 2026-04-12

## Стратегия развёртывания

- **Тип:** feature-flag
- **Feature flag:** `platform.exports.enabled` — управляется через LaunchDarkly; по умолчанию выключен

## Этапы

| Этап | % трафика / аудитории | Критерии перехода | Ответственный |
|---|---|---|---|
| 1. Internal | 0% (только команда) | Smoke tests зелёные, нет ошибок | @smoke-tester |
| 2. Canary 5% | 5% enterprise-клиентов | export_p95 < 30s за 24h, error_rate < 0.5% | @smoke-tester |
| 3. Production | 100% всех клиентов | Критерии Canary соблюдены за 7 дней | @smoke-tester |

## Мониторинг

- Дашборд: `https://grafana.platform.internal/d/exports`
- Алерты:
  - `export_p95_seconds > 45s` за 5 минут → warning
  - `export_p95_seconds > 60s` за 5 минут → critical
  - `export_error_rate > 1%` за 5 минут → critical
- SLO: `ops/slo.yaml#export-latency`

## Rollback

**Триггер для отката:** `export_p95_seconds > 60s` ИЛИ `export_error_rate > 1%` — устойчиво 5 минут

**Шаги отката:**

1. Выключить feature flag `platform.exports.enabled` через LaunchDarkly (< 1 минуты)
2. Убедиться, что метрики вернулись к baseline (мониторинг 5 минут)
3. Уведомить команду в #platform-incidents о rollback и причинах

**Время на откат (RTO):** < 5 минут
