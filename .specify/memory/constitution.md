# Spec Constitution

> Операционная система изменений для B2B SaaS-платформы.
> Версия: 1.0.0 | Последнее обновление: 2026-04-10

---

## Нормативные термины (BCP 14 / RFC 2119 + RFC 8174)

- **MUST** / **MUST NOT** — обязательное требование.
- **SHOULD** / **SHOULD NOT** — рекомендация; допустимо отклонение с явным обоснованием.
- **MAY** — необязательно, по усмотрению команды.

---

## Источники истины (Source of Truth)

| Артефакт | Канонический файл |
|---|---|
| Требования | `requirements.yml` |
| Интерфейсы REST | `contracts/openapi.yaml` |
| Интерфейсы событий | `contracts/asyncapi.yaml` |
| SLO | `ops/slo.yaml` |
| Архитектурные решения | `decisions/*.md` |
| Тарифицируемые параметры (L2.5) | `services/<code>/billing/parameters.yml` |
| Матрица ответственности (L2.5) | `services/<code>/responsibilities.yml` |
| Каталог инцидентов (L2.5) | `services/<code>/ops/incident-catalog.yml` |
| Каталог запросов (L2.5) | `services/<code>/ops/request-catalog.yml` |
| Параметры изменений (L2.5) | `services/<code>/ops/change-catalog.yml` |

Narrative-документы (`prd.md`, `design.md`, `runbooks`) MUST ссылаться на anchors выше и НЕ дублировать их.

---

## Двухконтурный workflow (обязательная модель)

### Lifecycle-контур (L3 Initiative)
```text
Discovery → Product → Architecture/Contracts → Ops/Readiness → Evidence
```

### Spec-Driven контур (L4 Feature)
```text
spec → plan → tasks → implement
```
Формат L4-файлов MUST быть совместим с `.specify/specs/` и шаблонами из этого репозитория (см. `.specify/specs/{NNN}-{slug}/`).

---

## Уровни и профили обязательности

| Уровень | Профиль | Описание |
|---|---|---|
| L0 | — | Governance: эта конституция, platform templates, platform ADR |
| L1 | Domain | `domains/<domain>/` — глоссарий, canonical model, event catalog |
| L2 | Product | `products/<product>/` — архитектура, product ADR, NFR baseline |
| L2.5 | Service | `services/<service-code>/` — внешняя/внутренняя спека, SLO, каталоги инцидентов/запросов/изменений, тарификация, РСМ, матрица ответственности |
| L3 | Initiative | Инициатива: prd.md, requirements.yml, contracts/, ops/, decisions/ |
| L4 | Feature | Фича: .specify/specs/{NNN}-{slug}/ spec/plan/tasks |
| L5 | Evidence | CI-генерируемые отчёты: RTM, coverage, PRR status |

**Профили обязательности** задают глубину L3:

- **Minimal** — prd.md, requirements.yml, README.md, CHANGELOG.md
- **Standard** — Minimal + design.md, ADR, contracts/*, rollout.md, slo.yaml, prr-checklist.md
- **Extended** — Standard + threat-model.md, nfr-validation.md, migration.md, compliance/
- **Enterprise** — Extended + `design.md` (трёхслойная онтология АИС), `architecture-views/` (11 типов представлений), `subsystem-classification.yaml` (машиночитаемая классификация). Для крупных ИС-проектов (С.М.С/Б). Требует полной трёхслойной архитектуры по методологии АИС: `domains/is-ontology/canonical-model/model.md`.

Профиль выбирается **по риску и масштабу**, а не «по размеру фичи».

---

## Принципы (MUST / SHOULD)

1. **Machine-readable first (MUST):** всё, влияющее на интеграции/совместимость/эксплуатацию, фиксируется в machine-readable anchors и валидируется CI.
2. **Single source of truth (MUST):** один объект знания — один канонический файл.
3. **Traceability by construction (MUST):** каждый `REQ-ID` имеет ссылки минимум на 1 подтверждение (тест / contract-тест / измерение SLO). `REQ-SVC-*` (Service-уровень) MUST ссылаться на `ops/slo.yaml`, `ops/incident-catalog.yml` или `ops/request-catalog.yml`.
4. **ADR-as-PR (SHOULD):** решения оформляются ADR и ревьюятся в PR.
5. **Контракты обратимо-совместимы по умолчанию (MUST):** breaking changes требуют отдельного deprecation-процесса и major-сдвига.
6. **Сервисы порождаются продуктами (MUST):** каждый `services/<code>/` MUST иметь ссылку на родительский `products/<product>/`; каждая `initiatives/{INIT}/` SHOULD ссылаться на `services/<code>/`, если реализует изменение сервиса.

---

## Feedback Loop: Ops → Spec

Любое production-событие MUST быть рассмотрено на предмет обновления спецификаций.

| Триггер | Действие | Кто |
|---|---|---|
| SLO breach (error budget < 20%) | Создать/обновить NFR-требование в `requirements.yml` + пересмотреть SLO target | On-call + Product |
| Инцидент P0/P1 | Создать ADR о решении + обновить `threat-model.md` (Extended) | Tech Lead |
| Прод-метрика отклоняется от SLI target | Пересмотреть `ops/slo.yaml` | SRE + Product |
| Новое регуляторное требование | Обновить `compliance/regulatory-review.md` + добавить REQ | Compliance |

**Процесс:** incident/metric review → PR с обновлением спеки → ревью команды → merge → новый L4 цикл (`spec → plan → tasks → implement`).

## GSD-интеграция (опциональный execution engine)

GSD (Get Shit Done) — опциональный execution engine для L4-фазы реализации. Встраивается **только в L4**, не затрагивает L0–L3.

### Когда использовать

| Сценарий | Подход |
|---|---|
| Простая фича, 1 инженер, < 1 дня | `/speckit-implement` (линейно, T1→T6 по одному) |
| Сложная фича, несколько файлов, > 1 дня | `/speckit-gsd-bridge` → `/gsd-execute-phase` (wave-параллелизация) |
| Brownfield, незнакомая кодовая база | `/speckit-gsd-map` перед spec-циклом |
| Любая фича, где важна свежесть контекста | GSD (fresh context per subagent) |

### Permission boundaries

**GSD-субагенты** (агенты, порождаемые `/gsd-execute-phase`):
- MUST NOT модифицировать артефакты L0–L3 (`constitution.md`, `domains/`, `products/`, `initiatives/`)
- MAY модифицировать только implementation/test файлы и L4-артефакты (`.specify/specs/`)
- MUST NOT использовать `--dangerously-skip-permissions` — только granular permissions

**Spec Kit команды-оркестраторы** (`/speckit-gsd-bridge`, `/speckit-gsd-verify`, `/speckit-gsd-map`):
- Работают на уровне доверия пользователя, не являются GSD-субагентами
- `/speckit-gsd-map` MAY дополнять L2-артефакты (`products/*/architecture/`) с маркерами `[GSD-MAPPED]`
- `/speckit-gsd-verify` MAY писать в `evidence/` (L5)
- `/speckit-gsd-bridge` пишет только в `.planning/`

**Общие:**
- `STATE.md` и `SUMMARY.md` живут в `.planning/` — отдельно от `requirements.yml` и `trace.md`

### Артефакт-flow

```text
L4 tasks.md ──[/speckit-gsd-bridge]──> .planning/phases/SPEC-NNN/PLAN.md
                                            │
                                       [/gsd-execute-phase]
                                            │
                                            v
                                .planning/phases/SPEC-NNN/SUMMARY.md
                                            │
                                       [/speckit-gsd-verify]
                                            │
                                            v
                                     evidence/SPEC-NNN-verification.md
```

### Разделение ответственности

| Артефакт | Владелец | Назначение |
|---|---|---|
| `requirements.yml` | Spec Kit (L3) | Каноническая спецификация требований |
| `STATE.md` | GSD | Оперативная память сессии (блокеры, решения, позиция) |
| `SUMMARY.md` | GSD | Результат выполнения плана (что сделано, какие файлы) |
| `evidence/*.md` | Spec Kit (L5) | Верификация покрытия требований |

---

## ID-схемы

```text
Initiative:       INIT-YYYY-NNN-<slug>      # INIT-2026-003-export-data
Requirements:     REQ-<SCOPE>-NNN          # REQ-AUTH-042, REQ-PLAT-003
Service Req:      REQ-SVC-NNN             # REQ-SVC-001 (scope = код услуги)
Service code:     <PRODUCT>-<TYPE>-<ID>   # ВЦОД-VMWR-VS (по нотации владельца)
Platform ADR:     PLAT-0001-<slug>
Product ADR:      <PROD>-0001-<slug>       # ANALYTICS-0003-cache-strategy
Initiative ADR:   <INIT>-ADR-0001-<slug>   # INIT-2026-003-ADR-0002-event-schema
API version:      SemVer (major.minor.patch)
```

Все ID MUST быть короткими, стабильными, ASCII-совместимыми и сортируемыми.

---

## Языковое соглашение

| Тип контента | Язык | Пример |
|---|---|---|
| Ключи YAML-полей | **EN** (snake_case) | `system_scale`, `iso_characteristic` |
| Enum-значения стандартов | По стандарту (RU) | `С.М.М`, `ПС.Т.И`, `заполнено` |
| Текстовые поля YAML (`description`, `title`) | **EN** для contracts/ops; **RU** допустим для Enterprise IS артефактов | `activity_domain: "Управление доступом"` |
| Markdown-файлы (glossary, constitution, design.md) | **RU** | — |
| Технические файлы (openapi.yaml, slo.yaml) | **EN** | — |
| Комментарии в YAML | **RU** или **EN** — единообразно в рамках файла | — |

Соглашение ДОЛЖНО соблюдаться во всех новых артефактах. Исключения — только при явной необходимости взаимодействия с внешними системами, требующими другого языка.

---

## CI Gates — стратегия enforcement

Любой gate вводится в 2 этапа:
1. **Warning mode** на PR в течение 2 недель (с отчётами в PR/чат).
2. **Blocking mode** на merge/release для профилей Standard/Extended.

| CI-проверка | Инструменты | PR | Release | Профили |
|---|---|---|---|---|
| YAML/Markdown hygiene | yamllint, markdownlint-cli2 | warning→blocking | blocking | все |
| requirements schema | check-jsonschema | blocking | blocking | все |
| OpenAPI validate + lint | Redocly CLI / Spectral | warning (style) / blocking (errors) | blocking | Standard/Extended |
| OpenAPI breaking diff | oasdiff | blocking (без major) | blocking | Standard/Extended |
| AsyncAPI validate | AsyncAPI CLI / Spectral | warning→blocking | blocking | Standard/Extended |
| AsyncAPI breaking diff | @asyncapi/diff | warning→blocking | blocking | Standard/Extended |
| JSON Schema validate | check-jsonschema + metaschema | blocking | blocking | все |
| SLO format | local JSON Schema + check-jsonschema | warning→blocking | blocking | Standard/Extended |
| PRR gate | чек-лист + парсер | warning (PR) | blocking (release) | Standard/Extended |
| Changelog discipline | Keep a Changelog + SemVer | warning→blocking | blocking | все |
| Enterprise IS classification | check-jsonschema (subsystem-classification.schema.json) | blocking | blocking | Enterprise |

---

## Ссылки

- MADR: https://adr.github.io/madr/
- arc42: https://arc42.org/documentation/
- OpenAPI 3.1.1: https://spec.openapis.org/oas/v3.1.1
- AsyncAPI 3.0: https://www.asyncapi.com/docs/reference/specification/v3.0.0
- OpenSLO v1: https://github.com/OpenSLO/OpenSLO
- Keep a Changelog: https://keepachangelog.com/
- SemVer: https://semver.org/
- Redocly CLI: https://redocly.com/docs/cli/
- Spectral: https://stoplight.io/open-source/spectral
- oasdiff: https://github.com/oasdiff/oasdiff
- check-jsonschema: https://github.com/python-jsonschema/check-jsonschema
