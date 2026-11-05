# Rollout Plan: INIT-2026-099-csv-export

> Feature-flagged rollout с поэтапным расширением аудитории.
> Источник истины SLO: [`ops/slo.yaml`](../ops/slo.yaml). Источник PRR: [`ops/prr-checklist.md`](../ops/prr-checklist.md).

---

## 1. Стратегия развёртывания

- **Тип:** feature flag (LaunchDarkly).
- **Feature flag:** `platform.csv_export.enabled` (default: `off`).
- **Дополнительные флаги:**
  - `platform.csv_export.sync_threshold` (default: 100000) — порог переключения sync→async.
  - `platform.csv_export.job_retention_hours` (default: 24) — TTL S3-файлов.
- **Принцип:** prod-deploy сразу, но за выключенным флагом. Rollout = постепенное включение
  по сегментам пользователей, не передеплой.

---

## 2. Этапы

| # | Этап | Аудитория | Длительность | Критерии перехода | Ответственный |
|---|---|---|---|---|---|
| 1 | Internal | `team:platform` (15 человек) | 3 рабочих дня | Smoke tests зелёные, нет ошибок в Sentry, P95 < 5s в staging | `@platform-team` |
| 2 | Canary 10% | 10% accounts (random sample, sticky) | 5 рабочих дней | P95 < 5s удерживается, error rate < 0.1%, нет P0/P1 инцидентов, SLO budget burn < 5% | `@platform-team` + `@sre-oncall` |
| 3 | GA 100% | все accounts | ongoing | Canary criteria выполнены 5 дней подряд | `@platform-team` |

**Старт rollout:** после `make check-all` зелёного и закрытия P0 пунктов PRR.

---

## 3. Мониторинг

- **Дашборд:** `https://grafana.platform.internal/d/csv-export` (создаётся в T4 — Observability).
- **Ключевые алерты:**

| Алерт | Условие | Severity | Канал |
|---|---|---|---|
| `csv_export_p95_latency_high` | `histogram_quantile(0.95, ...) > 10s` за 5m | warning | `#platform-alerts` |
| `csv_export_p95_latency_critical` | `> 25s` за 5m | critical | PagerDuty `@platform-sre-oncall` |
| `csv_export_error_rate_high` | `errors / total > 1%` за 5m | critical | PagerDuty |
| `csv_export_job_queue_backlog` | `redis_queue_depth{queue="export"} > 1000` за 10m | warning | `#platform-alerts` |
| `csv_export_slo_budget_burn` | error budget burn > 50% за 7d | warning | `#platform-alerts` |

- **SLO tracking:** [`ops/slo.yaml`](../ops/slo.yaml) → Grafana SLO panel.
- **Сводка после каждого этапа:** thread в `#platform-launches` со скриншотом dashboard и метриками за период.

---

## 4. Rollback

**Triggers (любой ⇒ откат):**

- `csv_export_error_rate > 1%` за 5 минут подряд
- `csv_export_p95_latency > 25s` за 5 минут подряд
- P0 security-инцидент (утечка sensitive field)
- Manual решение `@platform-sre-oncall`

**Шаги отката:**

1. Flip `platform.csv_export.enabled` → `off` в LaunchDarkly (< 1 минута).
2. Подтвердить остановку трафика на дашборде (5 минут).
3. Notify `#platform-incidents` + `#customer-success` (template ниже).
4. Создать post-mortem ticket в Jira (template `PM-template`).

**RTO:** < 5 минут от triger до полной остановки трафика.
**RPO:** N/A (stateless фича — нет потери данных при откате).

**Notification template (для шага 3):**

```
:rotating_light: ROLLBACK: csv-export
- Trigger: <metric=value, time>
- Action: feature flag disabled
- Impact: ~<N> экспортов прервано/перенесено
- Customer comms: <yes/no, кто отвечает>
- Post-mortem owner: <@user>
```

---

## 5. Communication plan

| Аудитория | Канал | Когда | Содержание |
|---|---|---|---|
| Internal eng | `#platform-launches` | Старт каждого этапа | Дата, аудитория, дашборд |
| `@sre-oncall` | PagerDuty schedule | На время Canary + GA | Особое внимание к alerts первые 48h |
| Customer Success | `#customer-success-platform` | За 24h до GA | Talking points для клиентов |
| Внешние пользователи (data-admins) | Email + in-app banner | На GA | «Экспорт в CSV доступен через API. Документация: <link>» |
