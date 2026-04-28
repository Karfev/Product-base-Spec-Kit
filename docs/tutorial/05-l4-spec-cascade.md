# 05. L4 Spec Cascade — от feature-идеи до кода

> **Аудитория:** Dev / Tech Lead.
> **Время:** 15–20 минут.
> **Предыдущий:** [04-anatomy-of-initiative.md](./04-anatomy-of-initiative.md) | **Следующий:** [06-traceability-and-validation.md](./06-traceability-and-validation.md)

---

## TL;DR

L3 (initiative) — это **что** и **зачем** на уровне всей фичи.
L4 (feature spec) — это **как** на уровне конкретной задачи.
Цепочка: **spec → plan → tasks → implement → trace**. Каждый шаг — отдельный slash-command,
каждый — обязателен для Standard+ профиля.

---

## Зачем два уровня

Одна инициатива (`INIT-2026-099-csv-export`) обычно содержит несколько features:

```text
INIT-2026-099-csv-export/      ← L3: одна инициатива
└── (.specify/specs/)
    ├── 099-csv-export-sync/    ← L4: feature 1 — sync режим
    ├── 100-csv-export-async/   ← L4: feature 2 — async + job-store
    └── 101-csv-export-events/  ← L4: feature 3 — AsyncAPI события
```

Каждая feature — отдельный sprint-task, отдельный PR, отдельный merge.
Связь L3 → L4 — через **REQ-IDs** (одно требование может быть реализовано в нескольких features,
один feature может реализовать несколько REQ-IDs).

---

## Цепочка `spec → plan → tasks → implement → trace`

### 1. `/speckit-specify NNN-slug` → `spec.md`

**Что делает:** превращает идею в формальный feature spec.

**Вход:** пара предложений «делаем sync-режим csv-экспорта для contact, deal, event, activity».

**Выход:** `.specify/specs/099-csv-export-sync/spec.md` со всеми canonical sections:
Summary, Motivation, Scope, Requirements (REQ-IDs из родительской инициативы),
API/Contracts impact, User Stories, Acceptance Criteria, Open questions.

**Валидация:** `make check-spec-quality` — нет открытых `NEEDS CLARIFICATION`,
нет placeholder-ов вроде `{…}`.

> **💡 NEEDS CLARIFICATION.** Если по фиче остаются открытые вопросы — пометь их явно:
> ```markdown
> - [ ] **NEEDS CLARIFICATION:** какой формат date в CSV (ISO 8601 / Unix epoch / локаль) — owner: @backend-lead — due: 2026-04-30
> ```
> Пока статус `[ ]` (open) — `make check-spec-quality` падает. Это by design: ты не должен
> переходить к plan, пока вопросы открыты.

### 2. `/speckit-plan NNN-slug` → `plan.md`

**Что делает:** превращает spec в архитектурный план.

**Что внутри plan.md:**
- Architecture choices (какие модули, как разделена ответственность)
- Contracts impact (какие изменения в OpenAPI/AsyncAPI)
- Data changes (миграции, индексы)
- Observability (метрики, логи, трейсы)
- Test strategy (unit / contract / integration / perf — что обязательно)
- Rollout & rollback strategy (для нашего csv-export — feature flag, см. ADR-0001)

**Кто driver:** Tech Lead (с консультацией architect для крупных изменений).

### 3. `/speckit-tasks NNN-slug` → `tasks.md`

**Что делает:** превращает план в конкретный список задач для разработчика в **строгом порядке T1-T6**.

#### Канонический порядок T1-T6

| # | Задача | Что делается | Команда verify |
|---|---|---|---|
| **T1** | Update/add contracts | Сначала меняем `contracts/openapi.yaml` или `asyncapi.yaml` | `make lint-contracts` |
| **T2a** | Write failing tests (RED) | Пишем acceptance + contract тесты, **они падают** (фичи ещё нет) | `make test-unit` + `make test-contract` |
| **T2b** | Implementation (GREEN) | Имплементируем код, тесты T2a становятся зелёными | те же |
| **T3** | Integration tests | Тесты с реальной БД / queue / external service | `make test-integration` |
| **T4** | Observability | Метрики, алерты, обновить `ops/slo.yaml` | manual review + Grafana |
| **T5** | Update trace.md + CHANGELOG.md | Связать REQ-IDs с тестами и контрактами | `make check-trace` |
| **T6** | Complete PRR checklist | Закрыть P0/P1 пункты в `ops/prr-checklist.md` | `/speckit-prr-status` |

**Почему именно так:**
- **T1 раньше T2** — тесты пишутся против контракта, а не против воображаемого API.
- **T2a (RED) раньше T2b (GREEN)** — это TDD. `make check-spec-quality` валидирует этот порядок.
- **T5 раньше T6** — PRR не имеет смысла без actual traceability.

> **💡 Антипаттерн.** Сразу после spec прыгнуть в код, потом дописать contracts «как получилось»
> и в конце «нагнать» тестов. CI не остановит на этом, но код-ревью должно.

### 4. `/speckit-implement NNN-slug` → код

**Что делает:** task-by-task проводит через `tasks.md`. Берёт первую `[ ]` задачу, имплементирует, помечает `[x]`, коммитит.

Если работаешь без AI-агента — делай это вручную в том же порядке.

### 5. `/speckit-trace NNN-slug` → `trace.md`

**Что делает:** строит RTM таблицу для feature-уровня.

```markdown
| REQ-ID | ADR | Contract | Test | SLO |
|---|---|---|---|---|
| REQ-EXPORT-001 | ADR-0001 | openapi.yaml#/paths/~1export/post | tests/api/export.spec.ts::REQ-EXPORT-001 | — |
| REQ-EXPORT-004 | — | — | tests/perf/export-latency.k6.js::REQ-EXPORT-004 | slo.yaml#csv-export-sync-latency |
```

**Валидация:** `make check-trace` — каждый REQ-ID из `requirements.yml` (родительской инициативы)
имеет хотя бы одну запись в `trace.md` хотя бы одной из своих features.

---

## L3 vs L4 — кто за что отвечает

| Аспект | L3 Initiative | L4 Feature |
|---|---|---|
| Scope | Вся бизнес-фича (csv-export целиком) | Атомарный кусок (sync режим / async режим) |
| Документ | `prd.md`, `requirements.yml`, `design.md` | `spec.md`, `plan.md`, `tasks.md` |
| Длительность | Недели — кварталы | Дни — sprints |
| PR | Нет (это контейнер) | Один или несколько PR-ов |
| ID | `INIT-YYYY-NNN-slug` | `NNN-slug` (без INIT-префикса) |
| Driver | PM | Tech Lead / Senior Dev |

**Правило большого пальца:** если фичу можно выкатить отдельным PR-ом за < 2 недели — это L4 feature.
Если она требует нескольких связанных фич с координацией — это L3 initiative.

---

## Параллельная работа над несколькими features

Внутри одной инициативы можно вести несколько features параллельно:

```bash
.specify/specs/099-csv-export-sync/      # team A
.specify/specs/100-csv-export-async/     # team B
.specify/specs/101-csv-export-events/    # team C (зависит от B)
```

Координация через:
- **Общий `requirements.yml`** на уровне инициативы — конфликты REQ-IDs ловятся в PR.
- **Общий `design.md`** — большие архитектурные изменения требуют ADR.
- **`/speckit-rtm INIT-...`** — собирает RTM с **всех** features инициативы для общей картины.

---

## (Опционально) GSD — параллельное выполнение

Для очень больших фич, где tasks.md содержит 20+ задач, есть интеграция с GSD (Get Stuff Done):

```text
/speckit-gsd-bridge 099-csv-export-sync     # конвертит tasks.md в GSD phase plans
/gsd-execute-phase SPEC-099                  # выполняет в параллельных waves
/speckit-gsd-verify 099-csv-export-sync      # проверяет coverage против REQ-IDs
```

Требует установки: `./tools/init.sh ... --with-gsd`.
Для типичной фичи csv-export это **избыточно** — обычный `/speckit-implement` достаточно.

---

## Чек-лист «фича готова к merge»

```text
[ ] make check-spec-quality зелёный (нет open NEEDS CLARIFICATION)
[ ] make lint-contracts зелёный
[ ] make test-unit + test-contract + test-integration зелёные
[ ] make check-trace зелёный (REQ-IDs из родительской инициативы покрыты)
[ ] T6 (PRR) — все P0 пункты для этой фичи закрыты
[ ] CHANGELOG.md обновлён
[ ] PR ссылается на feature spec и REQ-IDs (commit message convention)
```

---

> **💡 Для тимлида.** В первый месяц adoption — настойчиво требуй порядок T1→T2a→T2b на код-ревью.
> Это формирует мышление «контракты и тесты — первичны». Через 2-3 спринта команда привыкнет.

---

**Дальше:** [06-traceability-and-validation.md](./06-traceability-and-validation.md) — что реально проверяет CI и как читать trace.md.
