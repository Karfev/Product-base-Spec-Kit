# 03. Первая инициатива за 30 минут

> **Аудитория:** Dev / Tech Lead.
> **Время:** 45–75 минут для первого раза. Если копируешь с эталона — 30 минут. Если параллельно учишь JSON Pointer и формат REQ-IDs — ближе к верхней границе.
> **Предыдущий:** [02-install-and-tooling.md](./02-install-and-tooling.md) | **Следующий:** [04-anatomy-of-initiative.md](./04-anatomy-of-initiative.md)

---

## Что будем делать

Воссоздадим учебную инициативу `INIT-2026-099-csv-export` (готовый эталон лежит в
[`examples/INIT-2026-099-csv-export/`](../../examples/INIT-2026-099-csv-export/) — открой её в
соседней вкладке для сверки).

**Кейс.** Платформа должна отдавать данные клиента в CSV через REST API. Маленькие
выгрузки — синхронно, большие — через job-pattern. Standard-профиль (Q1 на auth: нет;
PII: нет ⇒ не Extended; есть public API + SLO ⇒ не Minimal).

## Два пути

| Путь | Когда выбирать | Команда |
|---|---|---|
| **A. С AI-агентом** (рекомендуется) | Есть Claude Code / OpenCode | `/speckit-quick "csv export ..."` или `/speckit-start` |
| **B. Вручную** | Нет агента, или хочется понять «что внутри» | `./tools/init.sh ...` + редактирование файлов |

Дальше показаны оба. Можно идти по B и подсматривать, какие команды агент бы вызвал.

---

## Шаг 1. Выбор профиля (3 минуты)

Прежде чем scaffold-ить, ответь на 8 вопросов risk-assessment'а
([`/speckit-profile`](../../.claude/commands/speckit-profile.md)).
Для нашего csv-export:

| # | Вопрос | Ответ | Влияние |
|---|---|---|---|
| 1 | Handles auth/tokens? | NO (используем существующий Bearer) | — |
| 2 | Involves PII/GDPR/SOC2? | NO (экспортируем уже существующие данные клиента) | Если YES — Extended обязателен |
| 3 | Adds public API contracts? | YES (новый POST /export) | Standard+ |
| 4 | Has SLO/SLA commitments? | YES (P95 < 5s) | Standard+ |
| 5 | Requires DB migrations? | NO (stateless) | — |
| 6 | Revenue/data loss risk? | NO | — |
| 7 | IS-class ArchiMate system? | NO | — |
| 8 | Affects > 1 product/team? | NO | — |

**2 YES → Standard.** Это профиль для большинства фич зрелого SaaS.

Подробнее про профили — [07-profiles-and-risk.md](./07-profiles-and-risk.md).

---

## Шаг 2. Scaffold (1 минута)

### Путь A — через AI-агента

```text
/speckit-quick "csv export для contact, deal, event, activity. Sync до 100k, async для больших"
```

Агент:
1. Сматчит keywords (`api`, `export`) → предложит профиль Standard.
2. Спросит slug, product, owner.
3. Запустит `init.sh` под капотом.

### Путь B — вручную

```bash
./tools/init.sh INIT-2026-099-csv-export 099-csv-export \
  --profile standard \
  --product platform \
  --owner @platform-team
```

Что произошло:
- Создалась папка `initiatives/INIT-2026-099-csv-export/` со scaffold под Standard
  (PRD, requirements.yml, design.md, contracts/, ops/, decisions/, delivery/).
- Создалась L4 spec-папка `.specify/specs/099-csv-export/` (spec.md, plan.md, tasks.md, trace.md).
- Все плейсхолдеры (`{INIT-YYYY-NNN-slug}`, `{product}`, `@{team}`) подменены на реальные.

```bash
ls initiatives/INIT-2026-099-csv-export/
# README.md  prd.md  requirements.yml  design.md  contracts/  decisions/  ops/  delivery/  changelog/
```

---

## Шаг 3. Заполнить PRD (8 минут)

### Путь A

```text
/speckit-prd INIT-2026-099-csv-export
```

Агент задаст ~5 вопросов (problem, why now, outcome, in-scope, non-goals) и сформирует `prd.md`.

### Путь B

Открой `initiatives/INIT-2026-099-csv-export/prd.md`. Структура — копируй с
[`examples/INIT-2026-099-csv-export/prd.md`](../../examples/INIT-2026-099-csv-export/prd.md).
Заполни 7 секций:

1. **Цель и эффект** — проблема, why now, outcome.
2. **Пользователи** — JTBD-таблица.
3. **Метрики** — baseline / target / период.
4. **Scope** — in-scope (со ссылками REQ-EXPORT-*) и non-goals.
5. **Риски** — таблица + митигации.
6. **Требования** — только ссылка на `requirements.yml`.
7. **Приёмка** — Definition of Done.

> **💡 Не дублируй требования из YAML в PRD.** Это нарушает principle «single source of truth»
> из [`constitution.md`](../../.specify/memory/constitution.md). PRD — narrative, requirements.yml — реестр.

---

## Шаг 4. Заполнить requirements.yml (10 минут)

### Путь A

```text
/speckit-requirements INIT-2026-099-csv-export
```

Агент:
- Прочитает scope items из PRD.
- Сгенерирует REQ-EXPORT-001..00N.
- Спросит про acceptance criteria.

### Путь B

Открой `initiatives/INIT-2026-099-csv-export/requirements.yml`. Заполни 5 требований
(см. эталон в `examples/`):

```yaml
- id: "REQ-EXPORT-001"
  title: "Synchronous CSV export"
  type: "functional"            # functional | nfr | quality | constraint | compliance
  priority: "P0"                # P0 | P1 | P2 | P3
  status: "proposed"            # draft | proposed | approved | implemented | verified | deprecated
  description: >
    An authenticated user MUST be able to export platform records (contact, deal,
    event, activity) to a UTF-8 encoded CSV file via REST API. For datasets up to
    100 000 rows the response MUST be returned synchronously in a single HTTP call.
  acceptance_criteria:          # ОБЯЗАТЕЛЬНО для type=functional
    - "Given an authenticated user with N records (N ≤ 100 000), when they POST /export with entity_type and format=csv, then HTTP 200 is returned with text/csv body"
    - "Given records contain Cyrillic or emoji, when exported, then the resulting file is valid UTF-8"
  trace:
    contracts:
      - "contracts/openapi.yaml#/paths/~1export/post"
    tests:
      - "tests/api/export.spec.ts::REQ-EXPORT-001"
```

**Топ-3 ошибки на этом шаге:**
1. `type: "operational"` — такого значения нет в схеме. Используй `constraint`.
2. Забыл `acceptance_criteria` для `type: functional` — `make validate` упадёт.
3. Забыл `metrics` для `type: nfr` — то же самое.

Полная схема — `tools/schemas/requirements.schema.json`.

---

## Шаг 5. Сгенерировать контракты (5 минут)

### Путь A

```text
/speckit-contracts INIT-2026-099-csv-export
```

Агент сгенерирует stub OpenAPI/AsyncAPI на основе REQ-IDs.

### Путь B

```bash
# Открой:
initiatives/INIT-2026-099-csv-export/contracts/openapi.yaml
```

Пропиши минимально один path, ссылающийся на REQ-EXPORT-001 (см. эталон в `examples/`).

```yaml
paths:
  /export:
    post:
      summary: "Export records to CSV (REQ-EXPORT-001)"   # ← обязательная ссылка на REQ
      operationId: createExport
      ...
```

> **💡 Зачем ссылка на REQ-ID в summary.** `make check-trace` парсит контракты и сверяет,
> что каждый REQ-ID, объявленный в `trace.contracts` в requirements.yml, реально присутствует
> в OpenAPI. Без ссылки traceability считается сломанной.

---

## Шаг 6. Валидация (1 минута)

```bash
make validate
# ==> Validating requirements.yml files...
#   Checking initiatives/INIT-2026-099-csv-export/requirements.yml
# (no errors)

make lint-contracts
# OpenAPI lint pass
# AsyncAPI validate pass
```

Если что-то падает — [08-when-it-breaks.md](./08-when-it-breaks.md).

---

## Шаг 7. Минимальный design.md + ADR (5 минут)

Standard-профиль требует `design.md` и хотя бы одну ADR на крупное решение.

```bash
# Открой:
initiatives/INIT-2026-099-csv-export/design.md
```

Минимум — секции 1–3 из шаблона `templates/spec-template.md` (цели, контекст C4, стратегия).
Mermaid-диаграммы — bonus, не required.

```bash
# ADR — отдельный файл:
initiatives/INIT-2026-099-csv-export/decisions/INIT-2026-099-ADR-0001-sync-vs-async.md
```

Используй [`templates/ADR-template.md`](../../templates/ADR-template.md). Структура:
context → drivers → 3 опции → decision → consequences.

---

## Шаг 8. Финальная проверка (1 минута)

```bash
make check-all
```

Если всё ✅ — у тебя есть валидированная инициатива Standard-профиля.

```bash
# (опционально) Сводный отчёт
/speckit-evidence INIT-2026-099-csv-export
# → evidence/INIT-2026-099-csv-export-evidence-report.md
# Покажет RTM coverage, PRR status, gaps.
```

---

## Что дальше

- **[04-anatomy-of-initiative.md](./04-anatomy-of-initiative.md)** — детальный разбор
  каждой папки и файла: что внутри, кто-когда-зачем меняет.
- **[05-l4-spec-cascade.md](./05-l4-spec-cascade.md)** — переход на feature-уровень
  (spec → plan → tasks → implement).
- **[06-traceability-and-validation.md](./06-traceability-and-validation.md)** —
  что реально проверяет CI и как читать `trace.md`.

> **💡 Для тимлида.** Засеки время первого прохождения для нового джуна. На моём опыте
> 60–90 минут — норма. Меньше 30 — либо у разработчика уже есть опыт SpecKit/Atlassian'а,
> либо он что-то пропустил и `make check-all` потом упадёт в PR.

---

**Дальше:** [04-anatomy-of-initiative.md](./04-anatomy-of-initiative.md) — что в каждой папке и зачем.
