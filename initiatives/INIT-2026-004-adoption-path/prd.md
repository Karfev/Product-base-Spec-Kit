# PRD: SpecKit Adoption Path

**Initiative:** INIT-2026-004-adoption-path
**Owner (PM):** @karfev
**Last updated:** 2026-04-11
**Profile:** Standard

---

## Цель и ожидаемый эффект

- **Проблема:** SpecKit в текущем виде требует понимания всех 5 слоёв (L0–L5), 4 профилей и 24 команд до первого результата. Кривая входа — 2-4 недели. Команды, привыкшие к Jira + Confluence, не начинают использование, потому что не видят value в первые 30 минут. Это блокирует adoption за пределами автора фреймворка.
- **Почему сейчас:** SpecKit выходит в open-source. Без adoption path первые пользователи столкнутся с cognitive overload при scaffolding, бросят после README и не вернутся. Window of opportunity для формирования community — первые 90 дней после публикации.
- **Цель (Outcome):** Новая команда получает первый validated artifact (requirements.yml + `make validate` passing) за 30 минут без чтения полного README. Progressive adoption: Minimal → Standard → Extended без потери работы.

## Пользователи и сценарии

- **Primary personas:**
  - **New Adopter** — tech lead или PM, который увидел SpecKit на GitHub и хочет попробовать на одной фиче
  - **Growing Team** — команда, которая прошла 3+ инициатив через Minimal и готова к contracts и traceability
  - **Enterprise Architect** — нуждается в ГОСТ/ArchiMate compliance, приходит сразу за Extended/Enterprise

- **Top JTBD / сценарии:**
  1. New Adopter запускает `/speckit-start`, отвечает на 5 вопросов, получает инициативу с prd.md и validated requirements.yml — всё за одну сессию (REQ-ADOPT-001, REQ-ADOPT-002)
  2. Growing Team запускает `upgrade.sh` на existing Minimal-инициативе, получает Standard-артефакты без потери существующего контента (REQ-ADOPT-003)
  3. New Adopter читает Gate 1 Quick Start (50 строк) и понимает, что делать, без изучения 500-строчного README (REQ-ADOPT-004)

## Метрики успеха

| Метрика | Baseline | Target | Период | Источник |
|---|---:|---:|---|---|
| Time-to-first-validate | ~120 мин | < 30 мин | 30d | User testing |
| Gate 1 completion rate | 0% (нет пути) | > 70% | 60d | GitHub issues / feedback |
| Gate 1 → Gate 2 conversion | 0% | > 40% | 90d | GitHub issues / feedback |
| README bounce rate | Высокий (предположение) | Снижение 50% | 60d | GitHub analytics |

## Scope

**In-scope:**

- `/speckit-start` — unified entry command, объединяющий profile + init + prd + requirements в один guided flow (REQ-ADOPT-001)
- Clean Minimal scaffold — без пустых папок contracts/, decisions/, ops/ (REQ-ADOPT-002)
- `upgrade.sh` — миграция инициативы между профилями с сохранением контента (REQ-ADOPT-003)
- Gate 1 Quick Start — standalone документ на 50 строк (REQ-ADOPT-004)
- `/speckit-trace-viz` — Mermaid-визуализация traceability для «aha-момента» (REQ-ADOPT-005)
- Archkom как явный opt-in, отделённый от Enterprise-профиля (REQ-ADOPT-006)

**Non-goals:**

- Web UI / SaaS-версия SpecKit
- Интеграция с Jira / Confluence / Notion (Phase 2)
- Видеоуроки и интерактивные tutorials
- Автоматическая миграция из существующих PRD-форматов

## Риски и ограничения

- **Backward compatibility:** `upgrade.sh` и изменение Minimal scaffold могут сломать existing инициативы. Mitigation: upgrade.sh создаёт backup, новый scaffold не удаляет файлы — только добавляет.
- **Scope creep в /speckit-start:** Unified command рискует стать «мастером на все руки». Mitigation: строгий scope — только Minimal-профиль, 5 вопросов, 2 артефакта на выходе.
- **Quick Start устаревает:** Отдельный документ дрейфует от README. Mitigation: CI check, который валидирует, что Quick Start ссылки ведут на существующие файлы.

## Требования (ссылки на REQ)

Реестр требований — в `requirements.yml`. Здесь только ссылки:

- `REQ-ADOPT-001` (P0): Unified entry command `/speckit-start` — от вопросов до validated initiative за одну сессию
- `REQ-ADOPT-002` (P0): Clean Minimal scaffold — только prd.md, requirements.yml, CHANGELOG.md, README.md
- `REQ-ADOPT-003` (P1): Profile upgrade path — `upgrade.sh` для миграции Minimal → Standard → Extended
- `REQ-ADOPT-004` (P0): Gate 1 Quick Start — standalone документ ≤ 60 строк
- `REQ-ADOPT-005` (P1): Traceability visualization — `/speckit-trace-viz` генерирует Mermaid-граф
- `REQ-ADOPT-006` (P1): Archkom decoupling — Archkom как отдельный opt-in preset, не привязанный к Enterprise
- `REQ-ADOPT-007` (P0): Time-to-first-validate SLO — весь Gate 1 путь ≤ 30 минут для нового пользователя

## Приёмка

- User testing: новый пользователь проходит Gate 1 за < 30 минут без внешней помощи
- `make validate` проходит на артефактах, созданных через `/speckit-start`
- `upgrade.sh` корректно мигрирует demo-инициативу INIT-2026-002 из Minimal в Standard
- Definition of done по профилю: `.specify/memory/constitution.md#профили`
