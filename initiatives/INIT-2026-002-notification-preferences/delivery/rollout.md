# Rollout Plan: INIT-2026-002-notification-preferences

**Профиль:** Standard
**Последнее обновление:** 2026-04-10

## Стратегия развёртывания

- **Тип:** feature-flag + canary
- **Feature flag:** `notification-preferences-enabled` — управляет @platform-team через Unleash

## Этапы

| Этап | % трафика / аудитории | Критерии перехода | Ответственный |
|---|---|---|---|
| 1. Internal | 0% (только команда) | Smoke tests пройдены, мониторинг работает | @platform-team |
| 2. Canary | 5% | error rate < 0.1%, p95 < 200ms за 24h | @platform-team |
| 3. Canary expanded | 25% | error rate < 0.1%, p95 < 200ms за 24h | @platform-team |
| 4. Production | 100% | error rate < 0.1%, p95 < 200ms за 48h суммарно | @platform-team |

## Мониторинг

- Метрики: `notification_preferences_api_latency_ms` (histogram), `notification_preferences_opt_out_total` (counter)
- Алерты: p95 latency > 200ms, error rate > 1%
- SLO: `ops/slo.yaml#notification-preferences-latency` — P95 < 200ms, P99 < 500ms (REQ-NOTIF-005)

## Rollback

**Триггер для отката:** error rate > 1% за 5 минут ИЛИ p95 latency > 500ms за 10 минут

**Шаги отката:**

1. Отключить feature flag `notification-preferences-enabled` в Unleash
2. Убедиться что API возвращает 404 (feature disabled), проверить мониторинг
3. Уведомить команду в Slack #platform-incidents
4. Создать incident ticket для root cause analysis

**Время на откат (RTO):** < 5 минут (отключение feature flag)
