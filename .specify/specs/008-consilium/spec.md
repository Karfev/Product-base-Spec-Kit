# Spec: 008-consilium

**Initiative:** INIT-2026-007-quality-augmentation
**Profile:** Minimal
**Owner:** @dmitriy
**Last updated:** 2026-04-12

## Summary

Новый command `/speckit-consilium` — structured multi-perspective review для ADR с ролями из доменной модели Архкомма. Генерирует секцию "Доменные оценки" совместимую с ADR-template-v2.

## Motivation / Problem

ADR пишется одним агентом. Нет систематического переключения между perspectives. В модели Архкомма для У1/У2 обязательны доменные оценки (ИБ, БД/нагрузки, инфраструктура, интеграции, прикладная архитектура и др.), но в SpecKit pipeline эта практика не автоматизирована. Graduated ADR PLAT-0003-async-queue принят без формальных доменных оценок.

Datarim решает аналогичную проблему через skill `consilium.md`: панель из 2-4 агентов спорят, dissent фиксируется, рекомендация консенсусная. Наша версия использует доменную модель Архкомма вместо generic ролей.

## Scope

- REQ-QUAL-001: Consilium command
- REQ-QUAL-002: Архкомм-aligned domain roles
- REQ-QUAL-003: Output в ADR "Доменные оценки"
- REQ-QUAL-006: Custom panel composition

## Non-goals

- Замена Архкомма — consilium = pre-review перед submission в комитет
- Автоматический approve ADR — только генерация review
- Real-time multi-agent orchestration — последовательная смена ролей одним агентом

## User stories

- As an architect, I want to run consilium on my ADR before submitting to Архкомм, so that I catch obvious gaps before formal review.
- As a tech lead, I want consilium roles aligned with Архкомм domains, so that the pre-review format matches what the committee expects.
- As a security engineer, I want consilium's Security role to reference my threat-model.md, so that the review is grounded in actual artifacts.

## Algorithm Design

### Consilium Pipeline

```
INPUT: ADR file path + profile (optional) + --roles (optional)

STEP 1: Determine panel composition
  if --roles provided:
    panel = parse_roles(--roles)
  elif --preset provided:
    panel = load_preset(preset)  # standard / archkom-l1 / archkom-l2
  else:
    panel = default_by_profile(initiative_profile)
    # Minimal → skip (not applicable)
    # Standard → standard preset (3 roles)
    # Extended → archkom-l1 preset (5 roles)
    # Enterprise → archkom-l2 preset (10 roles)

STEP 2: For each role in panel (sequential):
  a. Load role definition from consilium-roles.yml
  b. Load context files (L1 domain NFR, L2 NFR baseline, threat-model, SLO, etc.)
  c. Read ADR content
  d. Generate structured review:
     - Scope: what this role evaluates
     - Findings: specific observations with artifact references
     - Verdict: OK / Замечание (non-blocking) / Блокер (requires resolution)
     - Recommendations: if Замечание or Блокер

STEP 3: Aggregate results
  - Format as ADR "Доменные оценки" table
  - If any Блокер → overall status = "требует доработки"
  - If only Замечания → overall status = "одобрено с условиями"
  - If all OK → overall status = "одобрено"

STEP 4: Output
  - Append/replace "Доменные оценки" section in ADR
  - Print summary to console
```

### Role Definitions (consilium-roles.yml)

```yaml
roles:
  - name: "Прикладная архитектура"
    id: "arch"
    context_files:
      - "products/{product}/architecture/overview.md"
      - "domains/{domain}/canonical-model.md"
    checklist:
      - "Решение соответствует C4 context/containers?"
      - "Нет архитектурных anti-patterns (God service, distributed monolith)?"
      - "Backward compatibility сохранена?"
      - "Альтернативы рассмотрены с trade-offs?"

  - name: "ИБ (Information Security)"
    id: "security"
    context_files:
      - "ops/threat-model.md"
      - "domains/{domain}/nfr.md#security"
    checklist:
      - "Auth model определён и адекватен?"
      - "PII/ПДн обработка соответствует 152-ФЗ?"
      - "Input validation на всех boundaries?"
      - "Secrets management определён?"

  - name: "БД/нагрузки"
    id: "db-load"
    context_files:
      - "products/{product}/nfr-baseline/baseline.md"
      - "ops/slo.yaml"
    checklist:
      - "Схема данных нормализована / обоснована денормализация?"
      - "Миграция backward-compatible?"
      - "Индексы для hot paths определены?"
      - "Нагрузочный профиль оценён (RPS, P95 latency)?"

  - name: "Инфраструктура"
    id: "infra"
    context_files:
      - "delivery/rollout.md"
      - "ops/prr-checklist.md"
    checklist:
      - "Deployment topology определена?"
      - "Rollback strategy описана?"
      - "Горизонтальное масштабирование возможно?"
      - "Мониторинг и alerting настроены?"

  - name: "Интеграции"
    id: "integrations"
    context_files:
      - "contracts/openapi.yaml"
      - "contracts/asyncapi.yaml"
      - "domains/{domain}/event-catalog.md"
    checklist:
      - "Contract changes backward-compatible?"
      - "Breaking changes задокументированы с deprecation plan?"
      - "Event schema versioning определён?"
      - "Retry/DLQ strategy для async определена?"
```

### Presets

| Preset | Roles | Trigger |
|---|---|---|
| `standard` | arch, security, infra | Default for Standard |
| `archkom-l1` | arch, security, db-load, infra, integrations | Default for Extended, maps to ADR-template-L1 |
| `archkom-l2` | All 10 domains from ADR-template-v2 | Default for Enterprise, maps to full Архкомм |

## Requirements

- REQ-QUAL-001 (P1): Consilium command
- REQ-QUAL-002 (P1): Архкомм-aligned roles
- REQ-QUAL-003 (P1): Output format
- REQ-QUAL-006 (P2): Custom panel composition

## Acceptance criteria

- Given PLAT-0003-async-queue, when `/speckit-consilium`, then review от 3 ролей (arch, security, infra) с verdict per role
- Given Extended profile ADR, when `/speckit-consilium`, then 5 ролей (archkom-l1 preset)
- Given consilium выявил Блокер (e.g., no rollback strategy), when output записан, then ADR status = "требует доработки" с условием
- Given `--roles "ИБ,Compliance"`, when `/speckit-consilium`, then только 2 роли участвуют
- Given "Доменные оценки" section already exists in ADR, when consilium re-run, then section replaced (not duplicated)

## Open Questions

| # | Question | Owner | Deadline | Status |
|---|----------|-------|----------|--------|
| 1 | Сохранять ли историю consilium runs (v1, v2) для audit trail? | @dmitriy | 2026-04-25 | open |
| 2 | Интегрировать ли consilium в `/speckit-adr-product` как optional step? | @dmitriy | 2026-04-25 | open |
| 3 | Добавлять ли роли Стоимость (TCO), QA, CI/CD из полной модели Архкомма в v1? | @dmitriy | 2026-04-25 | open |
