# Rollout Plan: INIT-2026-000-api-key-management

**Профиль:** Standard
**Последнее обновление:** 2026-03-01

## Стратегия развёртывания

- **Тип:** feature-flag
- **Feature flag:** `platform.api_keys.enabled` — управляется через LaunchDarkly; по умолчанию выключен для всех

## Этапы

| Этап | % трафика / аудитории | Критерии перехода | Ответственный |
|---|---|---|---|
| 1. Internal (2026-03-15) | 0% (только внутренние команды) | Нет ошибок в auth_p95_ms, smoke tests зелёные | @platform-team |
| 2. Canary 5% (2026-03-22) | 5% enterprise-клиентов | auth_p95_ms < 10ms за 24h, key_creation_error_rate < 0.5%, нет инцидентов P0/P1 | @platform-team |
| 3. Production (2026-04-01) | 100% всех клиентов | Критерии Canary соблюдены за 7 дней, SLO active monitoring подтверждён | @platform-team |

## Мониторинг

- Дашборд: `https://grafana.platform.internal/d/api-keys`
- Алерты:
  - `auth_p95_ms > 25ms` за 5 минут → warning
  - `auth_p95_ms > 50ms` за 5 минут → critical (triager PagerDuty)
  - `key_creation_error_rate > 1%` за 5 минут → critical
- SLO: `ops/slo.yaml#api-key-auth-latency`

## Rollback

**Триггер для отката:** `auth_p95_ms > 50ms` ИЛИ `key_creation_error_rate > 1%` — устойчиво 5 минут

**Шаги отката:**

1. Выключить feature flag `platform.api_keys.enabled` через LaunchDarkly (< 1 минуты)
2. Убедиться, что метрики вернулись к baseline (мониторинг 5 минут)
3. Уведомить команду в #platform-incidents о rollback и причинах
4. Создать post-mortem ticket в Jira с тегом `api-key-management`

**Время на откат (RTO):** < 5 минут (feature flag — мгновенная инвалидация)
