# Rollout Plan: INIT-2026-004-adoption-path

**Профиль:** Standard+
**Последнее обновление:** 2026-04-11

## Стратегия развёртывания

- **Тип:** {canary | blue-green | feature-flag | rolling | big-bang}
- **Feature flag:** `{flag-name}` — {описание, кто управляет}

## Этапы

| Этап | % трафика / аудитории | Критерии перехода | Ответственный |
|---|---|---|---|
| 1. Internal | 0% (только команда) | {критерии} | @{owner} |
| 2. Canary | {5–10}% | error rate < {0.1%}, p95 < {300ms} за {24h} | @{owner} |
| 3. Production | 100% | {критерии} | @{owner} |

## Мониторинг

- Дашборд: {link}
- Алерты: p95 latency > {X ms}, error rate > {Y%}
- SLO: `ops/slo.yaml`

## Rollback

**Триггер для отката:** error rate > {X%} за {Y} минут

**Шаги отката:**

1. {Шаг 1: отключить feature flag / revert deploy}
2. {Шаг 2: …}
3. {Шаг 3: уведомить команду}

**Время на откат (RTO):** {< 15 минут}
