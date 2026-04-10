# Rollout Plan: INIT-2026-003-audit-log

**Профиль:** Standard
**Последнее обновление:** 2026-04-10

## Стратегия развёртывания

- **Тип:** feature-flag + canary
- **Feature flag:** `audit-log-enabled` — управляет активацией RabbitMQ consumer и доступностью REST API endpoints. Владелец: @platform-team.

## Этапы

| Этап | % трафика / аудитории | Критерии перехода | Ответственный |
|---|---|---|---|
| 1. Internal | 0% (только platform-team) | Smoke test пройден, consumer обрабатывает события, GET /audit-logs возвращает данные | @platform-team |
| 2. Canary | 5% | error rate < 0.1%, p95 < 300ms за 24h, consumer lag < 10s | @platform-team |
| 3. Expanded | 25% | те же критерии за 48h | @platform-team |
| 4. Production | 100% | те же критерии за 72h | @platform-team |

## Мониторинг

- Метрики: `audit.query.p95_latency_ms`, `audit.events.consumer_lag`, `audit.events.persisted_total`
- Алерты: p95 latency > 500ms за 5 минут, consumer lag > 60s за 5 минут
- SLO: `ops/slo.yaml#audit-query-latency` — P95 < 300ms, rolling 30d window

## Rollback

**Rollback trigger:** P95 latency > 500ms sustained for 5 minutes OR consumer lag > 60 seconds sustained for 5 minutes OR error rate > 1% on GET /audit-logs for 5 minutes.

**Шаги отката:**

1. Отключить feature flag `audit-log-enabled` — consumer останавливается, API endpoints возвращают 404
2. Проверить что consumer остановлен (consumer lag перестаёт расти)
3. Уведомить команду в Slack #platform-incidents
4. Создать incident ticket для post-mortem
5. После фикса: при повторном включении flag consumer дренажит очередь (события не теряются)

**Время на откат (RTO):** < 5 минут (отключение feature flag)
