# 04. Анатомия инициативы

> **Аудитория:** Dev / Tech Lead, кто прошёл [03-first-initiative.md](./03-first-initiative.md).
> **Время:** 15 минут.
> **Предыдущий:** [03-first-initiative.md](./03-first-initiative.md) | **Следующий:** [05-l4-spec-cascade.md](./05-l4-spec-cascade.md)

---

## TL;DR

Инициатива (`initiatives/INIT-YYYY-NNN-slug/`) состоит из 8 функциональных папок и 4 корневых файлов.
Каждая папка — отдельный артефакт-семейство со своим владельцем, валидатором и lifecycle.
В этом файле — карта «что-где-зачем-кто меняет».

Сверяйся с эталоном [`examples/INIT-2026-099-csv-export/`](../../examples/INIT-2026-099-csv-export/).

---

## Полное дерево (Standard-профиль)

```text
initiatives/INIT-2026-099-csv-export/
├── README.md                   # Обзор: метаданные + ссылки на все артефакты
├── prd.md                      # Бизнес-контекст, цели, метрики, scope
├── requirements.yml            # Машиночитаемый реестр REQ-IDs
├── design.md                   # Архитектурное описание (arc42-lite)
├── trace.md                    # RTM (опционально на L3, обязательно на L4)
├── changelog/
│   └── CHANGELOG.md            # Keep a Changelog
├── contracts/
│   ├── openapi.yaml            # REST API — источник истины
│   ├── asyncapi.yaml           # Event-driven API
│   └── schemas/
│       └── *.schema.json       # JSON Schema для DTO
├── decisions/
│   ├── INIT-2026-099-ADR-0001-sync-vs-async.md
│   └── INIT-2026-099-ADR-NNNN-...
├── ops/
│   ├── slo.yaml                # OpenSLO v1
│   └── prr-checklist.md        # Production Readiness Review
└── delivery/
    └── rollout.md              # Feature flag, canary, rollback triggers
```

**Extended добавляет:** `compliance/regulatory-review.md`, `ops/threat-model.md`, `ops/nfr-validation.md`, `delivery/migration.md`.

**Enterprise добавляет:** `architecture-views/` (11 view-types), `subsystem-classification.yaml`, `hld.md`.

---

## Корневые файлы

### `README.md`

**Зачем:** entry point. Любой, открывший инициативу, должен за 30 секунд понять статус и найти нужный артефакт.

**Что внутри:** TL;DR в одном абзаце, метаданные (ID, profile, owner, product, status), таблица-карта артефактов с прямыми ссылками.

**Кто меняет:** PM/Tech Lead на старте; обновляется при значимых изменениях статуса.

**Валидация:** нет (manual review).

---

### `prd.md` — Product Requirements Document

**Зачем:** narrative-документ для понимания контекста. Отвечает на «зачем».

**Что внутри:** проблема, цель (outcome), пользователи (JTBD), метрики успеха, scope (in/out), риски, приёмка.

**Кто меняет:** PM (driver), Tech Lead consult.

**Валидация:** нет автоматической. Manual review в PR.

> **💡 Антипаттерн.** PRD на 20 страниц с детальными API-спеками. PRD — это «зачем»,
> а не «как». «Как» живёт в `design.md` и `contracts/`. Если PRD растёт — режь на phases.

---

### `requirements.yml`

**Зачем:** машиночитаемый реестр требований. Источник истины для traceability.

**Что внутри:** массив `requirements`, каждое с id (REQ-XXX-NNN), title, type, priority, status, description, acceptance_criteria/metrics, trace.

**Кто меняет:** PM (создаёт), разработчик (обновляет status при имплементации, добавляет ссылки в `trace`).

**Валидация:**
- `make validate` — JSON Schema (`tools/schemas/requirements.schema.json`)
- `make check-trace` — каждый REQ-ID должен иметь хотя бы одну запись в `trace`

> **💡 Immutable IDs.** После `status: approved` REQ-ID НЕЛЬЗЯ переименовывать — это сломает все
> ссылки в контрактах, тестах, ADR. Если требование изменилось радикально —
> deprecate старый REQ-ID и создай новый.

---

### `design.md`

**Зачем:** архитектурное описание системы. Отвечает на «как».

**Что внутри (Standard):** цели и constraints → контекст (C4) → стратегия (high-level подход) → представления (диаграммы) → контракты → NFR → развёртывание.

**Кто меняет:** Tech Lead / Architect (driver), команда — review.

**Валидация:** нет автоматической. Standard и выше — обязательно ссылки на ADR из decisions/.

> **💡 Для Enterprise.** Структура расширяется до 3-слойной онтологии АИС
> (Activity / Application / Technology), 11 видов представлений (Д-1, Д-3, П-1, Т-1 и т.д.).
> Подробнее в [`/speckit-architecture`](../../.claude/commands/speckit-architecture.md).

---

### `trace.md` (опционально на L3)

**Зачем:** RTM таблица REQ → ADR → Contract → Test → SLO для быстрого аудита.

**Когда нужна:** перед релизом, для evidence report, для compliance аудита.

**Кто меняет:** автогенерация через `/speckit-rtm INIT-...`. Руками не пиши.

---

## Папка `contracts/`

Источник истины для всех API. Если в коде эндпойнт есть, а в OpenAPI — нет, **OpenAPI прав**.

| Файл | Когда нужен | Кто меняет | Валидация |
|---|---|---|---|
| `openapi.yaml` | Любой REST API | Backend dev | `redocly lint` + `oasdiff` (breaking) |
| `asyncapi.yaml` | События (Kafka/Rabbit) | Backend dev | `asyncapi validate` |
| `schemas/*.schema.json` | Сложные DTO с переиспользованием | Backend dev | JSON Schema lint |

**Конвенция:** в `summary` каждой operation/channel пиши ссылку на REQ-ID:
```yaml
post:
  summary: "Export records to CSV (REQ-EXPORT-001, REQ-EXPORT-003)"
```

Это парсит `make check-trace`.

---

## Папка `decisions/`

ADR в формате [MADR](https://adr.github.io/madr/). Один ADR = одно решение.

**Имя файла:** `INIT-YYYY-NNN-ADR-NNNN-slug.md`. Например, `INIT-2026-099-ADR-0001-sync-vs-async.md`.

**Структура (см. [`templates/ADR-template.md`](../../templates/ADR-template.md)):**
1. Context and problem statement
2. Decision drivers (3-6 проверяемых критериев)
3. Considered options (минимум 2, желательно 3)
4. Decision outcome (выбор + одно предложение «почему»)
5. Consequences (good / bad / neutral)
6. Confirmation (как проверим, что работает)

**Когда писать ADR:**
- Выбор технологии/библиотеки с долгосрочными последствиями.
- Спорное решение, где команда разошлась во мнениях.
- Решение, на которое будет ссылаться несколько REQ-IDs.

**Когда НЕ писать:** «использовать UTF-8 для CSV» — это не решение, а стандарт. ADR не нужен.

---

## Папка `ops/`

Operations, готовность к продакшену.

### `slo.yaml` — OpenSLO v1

**Зачем:** формальные цели уровня обслуживания, привязанные к конкретным NFR из requirements.yml.

**Что внутри:** `DataSource` (откуда метрики), `SLI` (как меряем), `SLO` (что обещаем).

**Кто меняет:** SRE / Tech Lead.

**Валидация:** часть `make check-release-rollout` — проверяет, что SLO упомянуты в `delivery/rollout.md`.

### `prr-checklist.md` — Production Readiness Review

**Зачем:** чек-лист готовности к продакшену. Без него — нельзя в GA.

**Что внутри:** 6 блоков (Service levels, Architecture, Observability, Deployment, Security, Ops).
Каждый пункт — P0 (blocking) или P1 (recommended).

**Кто меняет:** разработчик (заполняет), SRE (review).

**Валидация:** `/speckit-prr-status INIT-...` показывает DONE / OPEN / BLOCKING.

### `threat-model.md` (только Extended)

**Зачем:** STRIDE-анализ угроз для критичных к безопасности фич.

---

## Папка `delivery/`

### `rollout.md`

**Зачем:** план раскатки в продакшн.

**Что внутри:** стратегия (feature flag / blue-green / canary), этапы, monitoring & alerts, rollback triggers, RTO/RPO, communication plan.

**Кто меняет:** Tech Lead (driver), SRE (review).

**Валидация:** `make check-release-rollout` — сверяет с SLO и PRR.

### `migration.md` (только Extended+)

**Зачем:** план миграции данных. Какие шаги, какой rollback, какие risks.

---

## Папка `changelog/`

`CHANGELOG.md` в формате [Keep a Changelog](https://keepachangelog.com/).
Версионирование — SemVer в `metadata.version` файла `requirements.yml`.

---

## Жизненный цикл инициативы

```text
draft (scaffold)
  ↓
active (в работе, REQ статусы proposed → approved → implemented)
  ↓ (PRR closed, evidence report зелёный)
completed (выкатили, в проде)
  ↓ (/speckit-graduate перенёс знания в L2 products/)
archived (make archive INIT=...)
```

Управляется полем `metadata.initiative_status` в `requirements.yml`.

---

## Кто что меняет — сводная таблица

| Артефакт | Driver | Reviewer | Когда |
|---|---|---|---|
| `prd.md` | PM | Tech Lead | Discovery |
| `requirements.yml` | PM + Tech Lead | Architect | Discovery → Implementation |
| `design.md` | Tech Lead / Architect | Команда | Architecture phase |
| `contracts/` | Backend dev | API consumers | Перед implementation |
| `decisions/` | Кто принимает решение | Архкомитет / Tech Lead | По мере появления решений |
| `ops/slo.yaml` | SRE / Tech Lead | Product | Перед PRR |
| `ops/prr-checklist.md` | Tech Lead | SRE | Перед release |
| `delivery/rollout.md` | Tech Lead | SRE | Перед release |
| `trace.md` | Auto (`/speckit-rtm`) | — | Перед evidence report |
| `changelog/` | Все | — | На каждое значимое изменение |

---

> **💡 Для тимлида.** Эту таблицу полезно положить в onboarding wiki команды.
> Конфликты «кто меняет requirements.yml» — частая болезнь первых месяцев adoption.

---

**Дальше:** [05-l4-spec-cascade.md](./05-l4-spec-cascade.md) — переход на feature-уровень и порядок T1-T6.
