# Preset: Архитектурный комитет

> Опциональный governance layer для организаций с формальным архитектурным управлением.
> Загружается: speckit-consilium, speckit-architecture, speckit-graduate (Standard+).
> Source: extracted from constitution.md v1.0.0

---

## Классификация инициатив

| Уровень Архком | Триггер | Обязательные артефакты | Маппинг на профиль |
|---|---|---|---|
| **У0** | Локальное изменение без влияния на интеграции | Командная записка | Minimal |
| **У1** | Новый API / изменение контракта / новая интеграция | HLD + АТР + 1–2 доменных оценки | Standard |
| **У2** | Сквозной процесс / высокий риск / ИБ | BRD + PRD + HLD + АТР + все доменные оценки + TCO | Extended |

## Цепочка артефактов

```text
brd.md (business why, stakeholders, budget)
  ↓ refs
prd.md (product what, scenarios, metrics → requirements.yml)
  ↓ refs
hld.md (architecture how, C4, NFR quality scenarios, deployment)
  ↓ refs
decisions/АТР (decision + domain sign-offs)
  ↓ refs
design.md (implementation: schemas, migrations, rollout)
```

**Ссылочная дисциплина (MUST):** каждый артефакт — единственный источник для своих секций. Вниз по цепочке — только ссылки, не копии.

| Информация | Single source |
|---|---|
| Бизнес-проблема, ROI, стейкхолдеры | `brd.md` |
| Сценарии, метрики, scope, acceptance criteria | `prd.md` |
| REQ-IDs (machine-readable) | `requirements.yml` |
| C4 Context, NFR scenarios, deployment topology | `hld.md` |
| Архитектурные решения, альтернативы, доменные оценки | `decisions/*.md` |
| Contracts impact, schemas, rollout steps | `design.md` |

## Доменные оценки

Опциональные секции в ADR-шаблоне (`<!-- optional: archkom -->`) активируются при `--preset archkom`. Домены: БД/нагрузки, ИБ, инфраструктура, интеграции, CI/CD, QA, модель данных, ИИ, стоимость, прикладная архитектура.

## Статусы решений

- **Одобрено** — разработка разрешена
- **Одобрено с условиями** — условия с датами закрытия фиксируются в АТР
- **Отклонено** — возврат на переработку
- **Разрешённое исключение** — временное отступление с датой закрытия
