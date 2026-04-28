# 01. Глоссарий

> **Аудитория:** Dev / Tech Lead.
> **Время чтения:** 7 минут (или используй как справочник).
> **Предыдущий:** [00-why-speckit.md](./00-why-speckit.md) | **Следующий:** [02-install-and-tooling.md](./02-install-and-tooling.md)

---

Термины упорядочены по логическим группам, не по алфавиту — так проще читать впервые.

## Слои и инициативы

| Термин | Что значит |
|---|---|
| **L0–L5** | Пять слоёв SpecKit: governance (L0), domain (L1), product (L2), service (L2.5), initiative (L3), feature (L4), evidence (L5). См. [`README.md`](../../README.md#architecture--five-layers). |
| **Initiative** | Атомарная единица изменения — папка `initiatives/INIT-YYYY-NNN-slug/`. Содержит PRD, requirements, контракты, дизайн, ops, delivery. Жизненный цикл: draft → active → completed → archived. |
| **Feature spec (L4)** | Конкретная фича внутри инициативы — папка `.specify/specs/NNN-slug/`. Содержит spec.md, plan.md, tasks.md, trace.md. Одна инициатива может содержать несколько features. |
| **Profile** | Уровень обязательности артефактов: **Minimal** (PRD + requirements), **Standard** (+ design, contracts, SLO, PRR), **Extended** (+ threat model, migration, compliance), **Enterprise** (+ 3-слойная онтология АИС). Выбирается по риску, не по размеру. |
| **Constitution** | `.specify/memory/constitution.md` — нормативная база (RFC 2119). Описывает правила: какие артефакты обязательны, какие ID-конвенции, какие CI gates. |

## Артефакты L3 (Initiative)

| Термин | Что это |
|---|---|
| **PRD** (Product Requirements Document) | `prd.md`. Бизнес-контекст: проблема, цель, пользователи, метрики, scope, риски. На английском или русском. Narrative-документ — не дублирует requirements.yml. |
| **BRD** (Business Requirements Document) | `brd.md`. Опционально, для крупных инициатив с бизнес-кейсом и финансовым обоснованием. Standard и выше. |
| **requirements.yml** | Машинно-проверяемый реестр требований. Каждое требование: id, title, type, priority, status, description, acceptance_criteria/metrics, trace. Валидируется JSON Schema на каждом PR. |
| **REQ-ID** | Идентификатор требования. Pattern: `REQ-<SCOPE>-NNN` (например, `REQ-AUTH-001`, `REQ-EXPORT-042`). Immutable после `status=approved`. |
| **ADR** (Architecture Decision Record) | `decisions/INIT-YYYY-NNN-ADR-NNNN-slug.md`. Формат [MADR](https://adr.github.io/madr/): context → drivers → options → decision → consequences. Один ADR = одно решение. |
| **MADR** | Markdown ADR — конкретный шаблон записи ADR. См. [`templates/ADR-template.md`](../../templates/ADR-template.md). |
| **Design doc** | `design.md`. Архитектурное описание (arc42-lite для Standard, 3-слойная онтология для Enterprise). |
| **Contracts** | `contracts/openapi.yaml` (REST), `contracts/asyncapi.yaml` (events), `contracts/schemas/*.schema.json`. Источник истины для API. |
| **OpenAPI** | Спецификация REST API. Версия 3.1.x в репо. Валидируется `redocly lint`. |
| **AsyncAPI** | Спецификация event-driven API. Версия 3.0.x в репо. Валидируется `asyncapi validate`. |
| **oasdiff** | Утилита, проверяющая breaking changes в OpenAPI. Запускается в CI на каждый PR с изменениями `contracts/openapi.yaml`. |
| **Breaking change** | Изменение контракта, ломающее существующих клиентов: удалить required параметр, изменить тип ответа, убрать эндпойнт. Детектится `oasdiff` на каждом PR. Митигация — deprecation marker (`deprecated: true`) или новая major версия. |
| **JSON Pointer** | RFC 6901 синтаксис ссылок внутри JSON/YAML. В trace используется для указания на конкретную operation в OpenAPI: `contracts/openapi.yaml#/paths/~1export/post`. Здесь `~1` — это escaped `/`, то есть `paths/~1export` = `paths/  /export`. Если в твоём path есть `~`, его экранируют как `~0`. Стандарт: [tools.ietf.org/html/rfc6901](https://tools.ietf.org/html/rfc6901). |
| **Source of truth (SSOT)** | Принцип: один объект знания = один канонический файл. PRD не дублирует requirements.yml, design.md не дублирует contracts/. Если данные есть в двух местах — гарантированно разойдутся. См. [`constitution.md`](../../.specify/memory/constitution.md). |

## Operations & Release

| Термин | Что это |
|---|---|
| **NFR** (Non-Functional Requirement) | Нефункциональное требование: latency, throughput, availability, security, и т.д. Тип `nfr` в `requirements.yml`, обязательно с `metrics`. |
| **SLO** (Service Level Objective) | Цель уровня обслуживания. Пример: «P95 latency < 5s за 30 дней». Формат [OpenSLO v1](https://openslo.com/) в `ops/slo.yaml`. |
| **SLI** (Service Level Indicator) | Метрика, измеряющая SLO. Например: `histogram_quantile(0.95, http_request_duration_seconds_bucket)`. |
| **PRR** (Production Readiness Review) | `ops/prr-checklist.md`. Чек-лист готовности к продакшену: SLO, observability, deployment, security, ops. P0 пункты — блокирующие. |
| **Rollout** | `delivery/rollout.md`. План раскатки: feature flags, canary этапы, rollback triggers, RTO/RPO. |
| **RTO** (Recovery Time Objective) | Целевое время восстановления при инциденте (например, < 5 мин для отката feature flag). |
| **RPO** (Recovery Point Objective) | Допустимая потеря данных при восстановлении. |

## Traceability & Validation

| Термин | Что это |
|---|---|
| **Traceability** | Принцип: каждый REQ-ID связан минимум с одним подтверждением (тест, contract, SLO). Гарантирует, что требование не «висит в воздухе». |
| **RTM** (Requirements Traceability Matrix) | `trace.md`. Таблица REQ-ID → ADR → Contract → Test → SLO. Генерируется `/speckit-trace` (L4) или `/speckit-rtm` (L3). |
| **check-trace** | `make check-trace` — CI-валидатор, проверяющий, что каждый REQ-ID в `trace.md` существует в `requirements.yml` и наоборот. Blocking. |
| **Evidence report** | `evidence/<INIT>-evidence-report.md`. Сводный отчёт перед релизом: RTM coverage %, PRR status, SLO readiness, gaps. Генерируется `/speckit-evidence`. |

## L4 Spec-Driven Workflow

| Термин | Что это |
|---|---|
| **Spec cascade** | Цепочка `spec → plan → tasks → implement` в `.specify/specs/NNN-slug/`. Один skill на каждый шаг. |
| **T1–T6** | Стандартный порядок задач в `tasks.md`: T1 contracts, T2a tests RED, T2b implementation GREEN, T3 integration, T4 observability, T5 trace + changelog, T6 PRR items. |
| **NEEDS CLARIFICATION** | Маркер открытого вопроса в spec.md/plan.md. Если статус `open` — `make check-spec-quality` падает. |

## Команды и инструменты

| Термин | Что это |
|---|---|
| **slash command** | `/speckit-xxx` — команда для AI-агента (Claude Code / OpenCode / Kilo Code). Файлы в `.claude/commands/*.md`. |
| **`make check-all`** | Запуск всех валидаторов: requirements, contracts, trace, spec quality. Pre-merge gate. |
| **`init.sh`** | `tools/init.sh` — bootstrap инициативы. Создаёт всю структуру по выбранному профилю. |
| **GSD** (Get Stuff Done) | Опциональная интеграция параллельного выполнения задач. Команды `/speckit-gsd-*`. Требует отдельной установки (`./tools/init.sh ... --with-gsd`). |
| **Архкомм** | Архитектурный комитет — российская governance-практика для крупных систем. Опциональный preset (`--preset archkom`). |

## ISO 25010 / 25020 (только для Enterprise)

| Термин | Что это |
|---|---|
| **ISO 25010 / ГОСТ Р ИСО/МЭК 25020** | Международная и российская модели качества ПО. В SpecKit используются `iso_characteristic` и `iso_sub_characteristic` в metrics для NFR/quality требований. |
| **АИС** (Автоматизированная информационная система) | Российская методология классификации ИС (масштаб, тип подсистемы, владелец, вид деятельности). Применяется в Enterprise профиле, маркировка вида `С.М.М`, `ПС.Т.П`. |

---

**Дальше:** [02-install-and-tooling.md](./02-install-and-tooling.md) — что поставить на машину за 10 минут.
