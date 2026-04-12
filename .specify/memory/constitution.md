# Spec Constitution

> Операционная система изменений для B2B SaaS-платформы.
> Версия: 2.0.0 | Последнее обновление: 2026-04-12

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
| Service-артефакты (L2.5) | `services/<code>/` — billing, ops, responsibilities |
| Evolution proposals | `evolution-log.md` |
| Presets | `.specify/memory/presets/*.md` |

Narrative-документы (`prd.md`, `design.md`, `runbooks`) MUST ссылаться на anchors выше и НЕ дублировать их.

---

## Двухконтурный workflow (обязательная модель)

**Lifecycle-контур (L3 Initiative):** Discovery → Product → Architecture/Contracts → Ops/Readiness → Evidence

**Spec-Driven контур (L4 Feature):** spec → plan → tasks → implement

Формат L4-файлов MUST быть совместим с `.specify/specs/` и шаблонами из этого репозитория.

### Порядок навыков (Skill ordering)

**Быстрый старт:** `/speckit-quick` (auto-routing) | `/speckit-start` (guided onboarding)

**Поэтапный workflow:** profile → init → prd → requirements → contracts → specify → plan → tasks → implement → trace + rtm → consilium (Standard+) → graduate → reflect (SHOULD Standard+)

**Правило:** init создаёт структуру, последующие навыки заполняют контент.
### Управление состоянием сессии

- **Session state (MUST):** Каждый `/speckit-*` command MUST выполнять Session Update per `.specify/session/protocol.md`.
- **Ephemeral (MUST):** `.specify/session/` не коммитится. Per-initiative, max 50 строк. При resume — selective context loading.

---

## Уровни и профили обязательности

| Уровень | Профиль | Описание |
|---|---|---|
| L0 | — | Governance: эта конституция, platform templates, platform ADR |
| L1 | Domain | `domains/<domain>/` — глоссарий, canonical model, event catalog |
| L2 | Product | `products/<product>/` — архитектура, product ADR, NFR baseline |
| L2.5 | Service | `services/<service-code>/` — спека, SLO, каталоги, тарификация, РСМ |
| L3 | Initiative | prd.md, requirements.yml, contracts/, ops/, decisions/ |
| L4 | Feature | .specify/specs/{NNN}-{slug}/ spec/plan/tasks |
| L5 | Evidence | CI-генерируемые отчёты: RTM, coverage, PRR status |

**Профили** (глубина L3, выбирается по риску и масштабу):
- **Minimal** — prd.md, requirements.yml, README.md, CHANGELOG.md
- **Standard** — + design.md, ADR, contracts/*, rollout.md, slo.yaml, prr-checklist.md
- **Extended** — + threat-model.md, nfr-validation.md, migration.md, compliance/
- **Enterprise** — + трёхслойная онтология АИС, architecture-views/, subsystem-classification.yaml

---

## Принципы (MUST / SHOULD)

1. **Machine-readable first (MUST):** всё, влияющее на интеграции/совместимость/эксплуатацию, фиксируется в machine-readable anchors и валидируется CI.
2. **Single source of truth (MUST):** один объект знания — один канонический файл.
3. **Traceability by construction (MUST):** каждый `REQ-ID` имеет ссылки минимум на 1 подтверждение (тест / contract-тест / измерение SLO). `REQ-SVC-*` MUST ссылаться на `ops/slo.yaml`, `ops/incident-catalog.yml` или `ops/request-catalog.yml`.
4. **ADR-as-PR (SHOULD):** решения оформляются ADR и ревьюятся в PR.
5. **Контракты обратимо-совместимы по умолчанию (MUST):** breaking changes требуют deprecation-процесса и major-сдвига.
6. **Сервисы порождаются продуктами (MUST):** каждый `services/<code>/` MUST иметь ссылку на `products/<product>/`.
7. **Human-in-the-loop evolution (MUST):** proposals в `evolution-log.md` требуют ручного PR для применения. Автоматическое применение запрещено.

---

## Feedback Loop: Ops → Spec

| Триггер | Действие | Кто |
|---|---|---|
| SLO breach (error budget < 20%) | Создать/обновить NFR-требование + пересмотреть SLO target | On-call + Product |
| Инцидент P0/P1 | Создать ADR + обновить `threat-model.md` (Extended) | Tech Lead |
| Прод-метрика отклоняется от SLI target | Пересмотреть `ops/slo.yaml` | SRE + Product |
| Новое регуляторное требование | Обновить `compliance/regulatory-review.md` + добавить REQ | Compliance |

---

## ID-схемы

| Тип | Формат | Пример |
|---|---|---|
| Initiative | `INIT-YYYY-NNN-<slug>` | INIT-2026-003-export-data |
| Requirements | `REQ-<SCOPE>-NNN` | REQ-AUTH-042 |
| Service Req | `REQ-SVC-NNN` | REQ-SVC-001 |
| ADR (platform) | `PLAT-NNNN-<slug>` | PLAT-0001-caching |
| ADR (product) | `<PROD>-NNNN-<slug>` | ANALYTICS-0003-cache |
| ADR (initiative) | `<INIT>-ADR-NNNN-<slug>` | INIT-2026-003-ADR-0002-event |
| API version | SemVer | major.minor.patch |

ID MUST быть короткими, стабильными, ASCII-совместимыми и сортируемыми.

## Языковое соглашение

| Тип контента | Язык | Пример |
|---|---|---|
| Ключи YAML-полей | **EN** (snake_case) | `system_scale`, `iso_characteristic` |
| Enum-значения стандартов | По стандарту (RU) | `С.М.М`, `заполнено` |
| Текстовые поля YAML | **EN** (contracts/ops); **RU** (Enterprise IS) | — |
| Markdown-файлы | **RU** | — |
| Технические файлы (openapi, slo) | **EN** | — |
| Комментарии в YAML | **RU** или **EN** — единообразно в файле | — |

---

## Context Loading Rules

| Command type | Constitution | Requirements | Presets |
|---|---|---|---|
| L3 write (requirements, contracts) | lean | **full** | — |
| L4 (specify, plan, tasks, implement) | lean | index + targeted REQs | gsd (if GSD mode) |
| Evidence (trace, rtm, evidence) | lean | **full** | — |
| Governance (consilium, graduate) | lean | index | archkom |
| GSD (bridge, verify, map) | lean | index | gsd |

**Escape hatch:** `--full-context` → load all files. See `.specify/session/protocol.md` for full phase table.

---

## CI Gates

| CI-проверка | Инструменты | PR | Release | Профили |
|---|---|---|---|---|
| YAML/Markdown hygiene | yamllint, markdownlint-cli2 | warn→block | blocking | все |
| requirements schema | check-jsonschema | blocking | blocking | все |
| OpenAPI validate + lint | Redocly CLI / Spectral | warn/block | blocking | Standard+ |
| OpenAPI breaking diff | oasdiff | blocking | blocking | Standard+ |
| AsyncAPI validate | AsyncAPI CLI / Spectral | warn→block | blocking | Standard+ |
| AsyncAPI breaking diff | @asyncapi/diff | warn→block | blocking | Standard+ |
| JSON Schema validate | check-jsonschema + metaschema | blocking | blocking | все |
| SLO format | local JSON Schema | warn→block | blocking | Standard+ |
| PRR gate | чек-лист + парсер | warn (PR) | block (release) | Standard+ |
| Changelog discipline | Keep a Changelog + SemVer | warn→block | blocking | все |
| Enterprise IS classification | check-jsonschema | blocking | blocking | Enterprise |
