# SpecKit Tutorial — для Dev / Tech Lead

> Русскоязычный hands-on туториал по фреймворку SpecKit.
> Аудитория: разработчик / тимлид, впервые работающий с этим репозиторием.
> Время полного прохождения: 2-3 часа (или используй как справочник).

---

## Как читать

| Если ты… | Начинай с |
|---|---|
| **Впервые открыл репо** | [00-why-speckit.md](./00-why-speckit.md) |
| **Хочешь сразу что-то сделать** | [03-first-initiative.md](./03-first-initiative.md) (через 30 минут будет первая инициатива) |
| **CI упал / команда не работает** | [08-when-it-breaks.md](./08-when-it-breaks.md) |
| **Внедряешь SpecKit в команду** | [09-team-rollout.md](./09-team-rollout.md) |

---

## Содержание

| # | Файл | Тема | Время |
|---|---|---|---|
| 00 | [00-why-speckit.md](./00-why-speckit.md) | Зачем SpecKit, что даёт, когда не нужен | 5 мин |
| 01 | [01-glossary.md](./01-glossary.md) | 25 терминов: PRD, REQ-ID, RTM, SLO, ADR... | 7 мин (или справочник) |
| 02 | [02-install-and-tooling.md](./02-install-and-tooling.md) | Установка: Python, Node, make, AI-агент | 10-15 мин |
| 03 | [03-first-initiative.md](./03-first-initiative.md) | Worked example: csv-export от scaffold до зелёного `make validate` | 45-75 мин (первый раз) |
| 04 | [04-anatomy-of-initiative.md](./04-anatomy-of-initiative.md) | Что в каждой папке инициативы, кто-когда-зачем меняет | 15 мин |
| 05 | [05-l4-spec-cascade.md](./05-l4-spec-cascade.md) | L4: spec → plan → tasks → implement, порядок T1-T6 | 15-20 мин |
| 06 | [06-traceability-and-validation.md](./06-traceability-and-validation.md) | Что проверяет CI, как читать `trace.md`, evidence-report | 12 мин |
| 07 | [07-profiles-and-risk.md](./07-profiles-and-risk.md) | Когда Minimal/Standard/Extended/Enterprise, 4 кейса | 10 мин |
| 08 | [08-when-it-breaks.md](./08-when-it-breaks.md) | Топ-15 ошибок: симптом → причина → фикс | справочник |
| 09 | [09-team-rollout.md](./09-team-rollout.md) | Внедрение в команду 5-20 человек, 4-недельный план | 12 мин |

---

## Параллельные ресурсы

- **Эталон инициативы:** [`examples/INIT-2026-099-csv-export/`](../../examples/INIT-2026-099-csv-export/) — открой в соседней вкладке для сверки
- **Шаблоны:** [`templates/`](../../templates/) — PRD, requirements, ADR, spec
- **Все 32 slash-command:** [`AGENTS.md`](../../AGENTS.md)
- **Reference:** [`README.md`](../../README.md)
- **Governance:** [`.specify/memory/constitution.md`](../../.specify/memory/constitution.md)
- **Интерактивный гайд:** запусти `/speckit-tutorial` (если установлен Claude Code)

---

## Sidebar-конвенция «💡 Для тимлида»

В каждом файле есть блоки `> **💡 Для тимлида.** ...` — это углубление для Engineering Manager / Tech Lead.
Junior-разработчик их пропускает, lead — читает.

---

## Обратная связь

Если симптом не покрыт `08-when-it-breaks.md` — открой issue с тегом `tutorial-gap`.
Каждый такой gap — инвестиция в onboarding следующего разработчика.

---

> **Этот туториал** — часть `Product-base-Spec-Kit`, лицензия MIT.
> Last updated: 2026-04-28.
