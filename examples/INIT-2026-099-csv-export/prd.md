# PRD: INIT-2026-099-csv-export — экспорт записей в CSV

> Учебная инициатива из туториала [`docs/tutorial/`](../../docs/tutorial/INDEX.md).
> Профиль: **Standard**. Источник истины по требованиям: [`requirements.yml`](./requirements.yml).

---

## 1. Цель и ожидаемый эффект

- **Проблема.** Enterprise-клиенты выгружают данные через UI «по одной странице» (50 записей), либо
  пишут собственные скрипты к API. На объёмах 50k+ записей это занимает часы и периодически падает
  на rate-limit. Support-tickets категории «не могу выгрузить данные» — 12% от потока, средний RT — 4 ч.
- **Почему сейчас.** Q2 2026 — крупный enterprise-клиент (контракт $180k ARR) поставил CSV export
  в must-have для продления. Дальше тянуть нельзя.
- **Цель (Outcome).** Каждый пользователь с ролью data-admin может выгрузить произвольный
  entity-type (contact, deal, event, activity) одной HTTP-операцией; для типичного объёма
  (≤ 100k строк) — синхронно за 5 секунд P95.

---

## 2. Пользователи и сценарии (JTBD)

| Persona | Job To Be Done | Trigger |
|---|---|---|
| Data Admin клиента | «Хочу раз в неделю выгружать все active-сделки в CSV для отчёта в BI» | Понедельничный отчёт |
| Migration Engineer | «Хочу одноразово выгрузить весь history для миграции в новый CRM» | Миграция платформ |
| Support Engineer | «Хочу быстро выгрузить активности конкретного клиента для разбора инцидента» | Эскалация |

---

## 3. Метрики успеха

| Метрика | Baseline | Target | Период | Источник |
|---|---:|---:|---|---|
| `csv_export_adoption_rate` (% accounts, использующих API хотя бы 1 раз/мес) | 0% | 60% | 90d post-GA | Mixpanel |
| `support_tickets_data_export_pct` (доля тикетов категории «не могу выгрузить») | 12% | < 4% | 60d post-GA | Zendesk |
| `export_sync_latency_p95_s` (см. REQ-EXPORT-004) | — | < 5 | 30d rolling | APM |
| `export_availability_30d` | — | ≥ 99.5% | 30d rolling | APM |

---

## 4. Scope

**In-scope:**

- Synchronous CSV export для датасетов до 100k записей — `REQ-EXPORT-001`
- Asynchronous CSV export для датасетов больше 100k — `REQ-EXPORT-002`
- Column filtering (выбор полей в выгрузке) — `REQ-EXPORT-003`
- Latency SLO для синхронного режима — `REQ-EXPORT-004`
- Защита sensitive fields (password_hash, tokens, secrets) — `REQ-EXPORT-005`

**Non-goals (Phase 2+):**

- UI-кнопка «Export to CSV» в admin-консоли (отдельная инициатива, INIT-2026-103-export-ui)
- Экспорт в форматы XLSX / JSON / Parquet
- Пользовательские шаблоны столбцов (saved exports)
- Шифрование выгруженных файлов at-rest
- Scheduled/recurring exports (каждый день в 9:00)

---

## 5. Риски и ограничения

| Риск | Вероятность | Митигация |
|---|---|---|
| Rate-limit DDoS — клиент ставит export каждую минуту | Средняя | Rate limit: 10 экспортов / час / account |
| Большие выгрузки (1M+) выжирают память воркера | Высокая | Streaming write через `fast-csv`, не загружаем весь датасет в память |
| Утечка sensitive fields через колоночный API | Низкая, но критичная | `REQ-EXPORT-005`: hardcoded blocklist + регрессионный тест |
| Большие файлы выжирают object storage | Низкая | Job retention 24h (см. `delivery/rollout.md`), потом TTL-удаление |

**Compliance:** Не Extended-профиль — нет PII-расширений, GDPR DPA уже покрывает существующий API.

---

## 6. Требования

См. машинно-проверяемый реестр [`requirements.yml`](./requirements.yml).
Все REQ-ID валидируются `make validate`.

---

## 7. Приёмка (Definition of Done)

1. `make check-all` зелёный.
2. `/speckit-evidence INIT-2026-099-csv-export` показывает:
   - RTM coverage ≥ 80%
   - 0 BLOCKING items в PRR
   - SLO определён и instrumentирован (graphana dashboard ссылка в `delivery/rollout.md`)
3. Канареечный rollout 10% за 5 дней без P0/P1 инцидентов.
