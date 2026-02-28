# Spec Constitution

> Операционная система изменений для B2B SaaS-платформы.
> Версия: 1.0.0 | Последнее обновление: {YYYY-MM-DD}

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

Narrative-документы (`prd.md`, `design.md`, `runbooks`) MUST ссылаться на anchors выше и НЕ дублировать их.

---

## Двухконтурный workflow (обязательная модель)

### Lifecycle-контур (L3 Initiative)
```
Discovery → Product → Architecture/Contracts → Ops/Readiness → Evidence
```

### Spec-Driven контур (L4 Feature)
```
spec → plan → tasks → implement
```
Формат L4-файлов MUST быть совместим с `.specify/specs/` и шаблонами из этого репозитория.

---

## Уровни и профили обязательности

| Уровень | Профиль | Описание |
|---|---|---|
| L0 | — | Governance: эта конституция, platform templates, platform ADR |
| L1 | Domain | `domains/<domain>/` — глоссарий, canonical model, event catalog |
| L2 | Product | `products/<product>/` — архитектура, product ADR, NFR baseline |
| L3 | Initiative | Инициатива: prd.md, requirements.yml, contracts/, ops/, decisions/ |
| L4 | Feature | Фича: .specify/specs/{NNN}-{slug}/ spec/plan/tasks |
| L5 | Evidence | CI-генерируемые отчёты: RTM, coverage, PRR status |

**Профили обязательности** задают глубину L3:

- **Minimal** — prd.md, requirements.yml, README.md, CHANGELOG.md
- **Standard** — Minimal + design.md, ADR, contracts/*, rollout.md, slo.yaml, prr-checklist.md
- **Extended** — Standard + threat-model.md, nfr-validation.md, migration.md, compliance/

Профиль выбирается **по риску**, а не «по размеру фичи».

---

## Принципы (MUST / SHOULD)

1. **Machine-readable first (MUST):** всё, влияющее на интеграции/совместимость/эксплуатацию, фиксируется в machine-readable anchors и валидируется CI.
2. **Single source of truth (MUST):** один объект знания — один канонический файл.
3. **Traceability by construction (MUST):** каждый `REQ-ID` имеет ссылки минимум на 1 подтверждение (тест / contract-тест / измерение SLO).
4. **ADR-as-PR (SHOULD):** решения оформляются ADR и ревьюятся в PR.
5. **Контракты обратимо-совместимы по умолчанию (MUST):** breaking changes требуют отдельного deprecation-процесса и major-сдвига.

---

## ID-схемы

```
Initiative:    INIT-YYYY-NNN-<slug>      # INIT-2026-003-export-data
Requirements:  REQ-<SCOPE>-NNN          # REQ-AUTH-042, REQ-PLAT-003
Platform ADR:  PLAT-0001-<slug>
Product ADR:   <PROD>-0001-<slug>       # ANALYTICS-0003-cache-strategy
Initiative ADR:<INIT>-ADR-0001-<slug>   # INIT-2026-003-ADR-0002-event-schema
API version:   SemVer (major.minor.patch)
```

Все ID MUST быть короткими, стабильными, ASCII-совместимыми и сортируемыми.

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
