---
status: "decided"
date: "2026-04-15"
decision-makers: ["@platform-team"]
consulted: ["@sre-team", "@solutions-architect"]
informed: ["@product-team"]
---

# INIT-2026-099-ADR-0001: Hybrid sync/async CSV export

## Context and problem statement

CSV export должен обслуживать датасеты от 100 до 1 000 000+ записей.

- Synchronous HTTP-ответ имеет жёсткий timeout (30 секунд на API gateway, 60 секунд на nginx).
  Для 1M записей с типичной нагрузкой 5k rows/sec это > 200 секунд — гарантированный timeout.
- Asynchronous job pattern (POST → 202 + job_id, GET для опроса) — стандарт для долгих операций,
  но усложняет UX: клиент должен опрашивать статус или подписываться на событие.
- Большинство кейсов (Pareto: ~85% по тикетам support) — выгрузки до 50k записей,
  где timeout не достигается, и async лишь добавляет шагов.

Требуется решение, которое:

1. Покрывает оба класса нагрузок без surprise-failures.
2. Не заставляет клиента писать «два разных интегратора».
3. Совместимо с существующим API-стилем (REST, Bearer, JSON).

## Decision drivers

- **Time to value (UX):** «один HTTP-запрос → файл» предпочтительнее опроса для частых случаев.
- **Reliability:** ни один сценарий не должен фейлить из-за timeout под рабочей нагрузкой.
- **Backpressure:** длинные экспорты не должны блокировать API-слот другим клиентам.
- **Operability:** одна кодовая база, один эндпойнт — меньше поверхности для bugs.

## Considered options

### Option A — Sync only

Для всех размеров возвращаем CSV в HTTP body. Если датасет слишком большой и timeout
случился — клиент должен фильтровать.

- **Good:** простейшая реализация, минимум moving parts.
- **Good:** одна интеграция со стороны клиента.
- **Bad:** не покрывает enterprise (1M+) — это блокер по REQ-EXPORT-002.
- **Bad:** длинные запросы выжирают connection-slots в API gateway.

### Option B — Async only

Для всех размеров возвращаем 202 + job_id, клиент опрашивает GET или подписывается
на event.

- **Good:** uniform model, нет «магии порога».
- **Good:** хороший backpressure — задания просто накапливаются в очереди.
- **Bad:** даже для 100 записей клиент должен писать polling-loop.
- **Bad:** UX support-инструментов («скачать сейчас») значительно хуже.
- **Bad:** дополнительная инфраструктура (queue, worker, S3) обязательна с первого дня.

### Option C — Hybrid: sync ≤ 100k / async > 100k

Сервер сам выбирает режим по размеру датасета. Клиент может также явно запросить
async (`?async=true`). Async режим возвращает 202 + ExportJob.

- **Good:** оптимальный UX для типичных кейсов (sync).
- **Good:** масштабируемость для enterprise (async).
- **Good:** клиент handles обе ветки на одном эндпойнте — switch по HTTP status (200 vs 202).
- **Bad:** клиент должен уметь обработать оба ответа.
- **Bad:** граница 100k — magic number, требует обоснования и алертинга при близости к лимиту.
- **Neutral:** требует Redis + workers + S3, но это уже есть в нашем стеке.

## Decision outcome

**Chosen: Option C — Hybrid sync/async с порогом 100 000 записей.**

Обоснование:

- Покрывает оба требования (REQ-EXPORT-001, REQ-EXPORT-002) одним эндпойнтом.
- 100k — эмпирический порог: при типичной нагрузке (5k rows/s, ~20 байт/строка)
  это ~20 секунд → укладываемся в 30s timeout с запасом.
- Полностью переиспользует существующий стек (Redis, S3, Kafka).
- Клиент пишет одну ветку обработки: `if response.status == 200: download` /
  `else if 202: poll job_id`.

### Implementation notes

1. Граница 100k вынесена в env-конфиг `CSV_EXPORT_SYNC_THRESHOLD` (на случай тюнинга).
2. SQL preflight `SELECT COUNT(*) WHERE ...` выполняется до streaming, чтобы выбрать режим.
   Стоимость counts terpима: для всех целевых таблиц есть индексы.
3. Async режим: задание в Redis stream, worker берёт, стримит в S3 multipart upload,
   публикует `export.job.completed` (см. `contracts/asyncapi.yaml`).
4. Job retention: 24 часа в S3, потом TTL-удаление.

### Consequences

- **Good:** UX оптимален для типичных кейсов, scale покрывает enterprise.
- **Good:** Один OpenAPI эндпойнт, две ветки responses.
- **Bad:** Клиенты MUST handle и 200, и 202 — описано в SDK README.
- **Bad:** Two code paths в backend (sync stream, async job) — больше поверхности для багов.
  Митигируется shared-функцией `streamCsvFromQuery()`, которой пользуются оба пути.
- **Neutral:** Магический порог 100k подлежит ревизии через 90 дней по реальным метрикам.

### Confirmation

Решение подтверждено когда:

1. `tests/api/export.spec.ts::REQ-EXPORT-001` — sync export (50k rows) возвращает 200 + CSV.
2. `tests/api/export.spec.ts::REQ-EXPORT-002` — async export (200k rows) возвращает 202 + job_id, GET /export/jobs/{id} в течение 60s показывает status=completed + download_url.
3. `tests/perf/export-latency.k6.js::REQ-EXPORT-004` — sync режим под 50 rps выдерживает P95 < 5s.
4. Ревизия через 90 дней: distribution размеров экспортов, % async, latency-quantiles.
   При необходимости — корректировка порога.
