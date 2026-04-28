# 09. Внедрение в команду 5-20 человек

> **Аудитория:** Tech Lead / Engineering Manager / CPTO.
> **Время:** 12 минут на чтение, 4 недели на rollout.
> **Предыдущий:** [08-when-it-breaks.md](./08-when-it-breaks.md) | **Следующий:** —

---

## TL;DR

Не пытайся раскатить SpecKit на всю команду одним флагом. **Pattern, который работает:**
1 пилотная инициатива → 2-3 ранних адоптера → шаблонизация PR-template → плановое расширение.
Срок до устойчивого adoption — 4-6 недель в команде до 20 человек.

---

## Антипаттерны, которые гарантированно провалят rollout

| Антипаттерн | Чем плох | Что делать вместо |
|---|---|---|
| «С завтрашнего дня все инициативы — в SpecKit» | Команда саботирует, потому что нет навыка | Пилот на 1 добровольной инициативе |
| Раскатить на legacy-проекты ретроактивно | Пытка, никакой ценности | Только новые инициативы |
| Ввести как KPI «каждый PR с trace.md» | Cargo-cult без понимания | Связать с реальной болью (compliance аудит, инциденты) |
| «Это для архитекторов, разработчики не трогают» | requirements.yml и trace.md меняют именно разработчики | Включить разработчиков с первого дня |
| Внедрить без AI-агента на «голых руках» | Заполнение требований без `/speckit-*` команд — пытка | Ставить Claude Code / OpenCode параллельно |

---

## 4-недельный план rollout

### Неделя 1 — Подготовка (Tech Lead solo)

**Цели:** убедиться, что инструмент работает, выбрать пилот, подготовить onboarding-материалы.

| День | Действие |
|---|---|
| Пн | Лично пройди весь туториал (00-08), создай учебную инициативу `csv-export` |
| Вт | Выбери реальную пилотную инициативу — что-то новое, средней сложности (Standard), без жёсткого дедлайна |
| Ср | Подготовь bootstrap-скрипт (см. ниже) и tests-чтобы-всё-работало |
| Чт | Проведи dry-run внедрения на пилоте — пройди 03→07 файлы туториала на реальной задаче |
| Пт | Документируй проблемы, обнови `08-when-it-breaks.md` с реальными симптомами |

**Deliverable недели:** один заполненный пилот в `initiatives/`, прошедший `make check-all`.

---

### Неделя 2 — Пилотная команда (3-5 человек)

**Цели:** двое-трое разработчиков параллельно ведут одну инициативу через SpecKit.

**Действия:**
1. Kickoff на 30 минут: показать готовый пилот (csv-export), объяснить «почему нам это надо»,
   мапнуть на конкретные боли команды (compliance, onboarding новичков, инциденты без post-mortem).
2. Распределить L4 features внутри пилота: `099-csv-export-sync` — Алиса, `100-csv-export-async` — Боб,
   `101-csv-export-events` — Кэрол.
3. Daily 15-минутный sync **только** про SpecKit-friction в первую неделю.
4. К концу недели — каждый разработчик прошёл цепочку `/speckit-specify → /speckit-plan → /speckit-tasks` хотя бы раз.

**Deliverable недели:** 2-3 mergeable PR с feature-spec'ами L4, прошедшие `make check-all`.

---

### Неделя 3 — Шаблонизация и автоматизация

**Цели:** убрать ручную рутину, чтобы инструмент перестал ощущаться как overhead.

**Действия:**

1. **Bootstrap-скрипт для нового разработчика** (см. ниже).
2. **PR-template** в `.github/pull_request_template.md`:

```markdown
## Что меняется

<краткое описание>

## SpecKit checklist

- [ ] PR ссылается на REQ-IDs: REQ-XXX-NNN
- [ ] Если изменены `contracts/` — `make lint-contracts` зелёный
- [ ] Если новые требования — `make validate` зелёный
- [ ] Если фича-уровень — `tasks.md` обновлён, `/speckit-trace` запущен
- [ ] CHANGELOG.md обновлён

## Связанные артефакты

- Initiative: INIT-YYYY-NNN-slug
- Feature spec: .specify/specs/NNN-slug/

## Test evidence

<скриншот или ссылка на CI run>
```

3. **CI gate в `.github/workflows/`** — обновить, чтобы `make check-trace` и `make check-spec-quality` блокировали merge для инициатив со статусом active.
4. **Slack/Teams канал #speckit-help** — для быстрых вопросов, чтобы не блокироваться.

**Deliverable недели:** 5+ человек могут начать новую инициативу за < 30 минут без помощи Tech Lead.

---

### Неделя 4 — Расширение и правила

**Цели:** SpecKit стал default для новых инициатив. Закреплено в team-wiki.

**Действия:**

1. **Engineering policy** (короткая, 1 страница) в Confluence/Notion:
   - «Новые инициативы Standard+ — обязательно через SpecKit».
   - «Профиль выбирается парно (PM+Tech Lead) на kickoff».
   - «PR на инициативу без зелёного `make check-all` — auto-block».
   - «Каждый разработчик прошёл туториал 00-08 в onboarding-чек-листе».

2. **Метрики adoption** (вешаем на retro):
   - % новых инициатив через SpecKit (target: 100% к месяцу 3).
   - Time-to-first-validated-initiative для новичка (target: < 60 мин).
   - Доля PR, которые упали на `make check-all` (target: < 10%, чтобы не было friction).

3. **Retrospective через 2 недели** — что болит, что чинить.

**Deliverable недели:** policy опубликована, в onboarding-чек-листе есть пункт «прошёл tutorial 00-08».

---

## Bootstrap-скрипт

Положить в репо как `scripts/bootstrap-dev.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "==> SpecKit dev bootstrap"

# 1. Системные зависимости
echo "Checking python3 / node / make..."
command -v python3 >/dev/null || { echo "Install python3 3.10+"; exit 1; }
command -v node >/dev/null || { echo "Install node 18+"; exit 1; }
command -v make >/dev/null || { echo "Install make (use WSL on Windows)"; exit 1; }

# 2. Tooling репо
echo "Installing repo tooling..."
make install-tools

# 3. Smoke validation
echo "Running smoke validation..."
make validate || { echo "❌ make validate failed — see docs/tutorial/08-when-it-breaks.md"; exit 1; }

# 4. AI-агент — подсказка
if [ -d .claude ]; then
  echo "✅ .claude/commands/ found — slash commands available in Claude Code"
fi

echo ""
echo "==> Setup complete. Next: open docs/tutorial/03-first-initiative.md"
```

Дать каждому новичку — экономия 30+ минут.

---

## Onboarding-чек-лист для новичка

Положить в `docs/onboarding.md` или в team-wiki:

```markdown
## Day 1
- [ ] Клонировал репо, прошёл `bootstrap-dev.sh`, `make help` работает
- [ ] Прочитал `docs/tutorial/00-why-speckit.md` и `01-glossary.md`

## Day 2
- [ ] Прошёл `docs/tutorial/03-first-initiative.md` руками — создал и провалидировал учебную инициативу
- [ ] Открыл `examples/INIT-2026-099-csv-export/` — понял структуру

## Week 1
- [ ] Прочитал `docs/tutorial/04` — `08`
- [ ] Сделал первый PR с `make check-all` зелёным
- [ ] Знает, где искать при ошибке (`08-when-it-breaks.md`)
```

---

## Метрики, которые покажут, что rollout удался

| Метрика | Target к месяцу 3 |
|---|---|
| % новых инициатив через SpecKit | 100% |
| Time-to-first-validated-initiative (новичок) | < 60 минут |
| % PR с зелёным `make check-all` с первой попытки | > 80% |
| Среднее время на пре-релизный compliance аудит | < 1 рабочий день (было — недели) |
| Доля «orphan» REQ-ID без trace в evidence-report | < 5% |
| NPS «удобство SpecKit» по командному опросу | > 7/10 |

Если через 3 месяца хотя бы 4 из 6 — рollout удался.

---

## Когда стоит остановиться и пересмотреть

Если через 6 недель:
- < 50% новых инициатив через SpecKit, **И**
- разработчики жалуются, **И**
- adoption-метрики не растут

→ Это сигнал, что инструмент не подходит конкретной команде/контексту. Возможные причины:
- Команда слишком маленькая (< 5 человек) — overhead больше пользы.
- Нет реальной regulatory-боли — мотивации недостаточно.
- AI-агент не используется — ручное заполнение убивает.
- Tech Lead не lead by example.

В таких случаях разумнее откатиться к Notion + GitHub issues, чем тащить через сопротивление.

---

## Связь с другими процессами

| Процесс команды | Как мапится на SpecKit |
|---|---|
| Sprint planning | Берём L4 features из `.specify/specs/` как input |
| Sprint review | Демо `evidence/INIT-*-evidence-report.md` для DoD |
| Retro | Метрики adoption + список фрustrations |
| Code review | PR-template требует ссылок на REQ-ID |
| Architecture review | ADR через `/speckit-consilium` (если есть Архкомм) |
| Compliance audit | Один запрос: «дай evidence-report для INIT-XXX» |

---

> **💡 Для CPTO/EM.** Бюджет на onboarding — 2 рабочих дня на разработчика в первые 2 недели.
> Ниже — будет boilerplate-копирование без понимания. Эти дни окупятся через первый же
> compliance-аудит или onboarding следующего новичка.

---

## Что дальше

Если ты дочитал до сюда — поздравляю, ты обладаешь полным контекстом для самостоятельного
внедрения SpecKit в команду.

- **Источники истины:** [`README.md`](../../README.md), [`AGENTS.md`](../../AGENTS.md), [`constitution.md`](../../.specify/memory/constitution.md).
- **Шаблоны:** [`templates/`](../../templates/).
- **Эталон:** [`examples/INIT-2026-099-csv-export/`](../../examples/INIT-2026-099-csv-export/).
- **Slash-команды:** [`.claude/commands/`](../../.claude/commands/) — 32 skills, см. AGENTS.md за описаниями.

Если что-то неочевидно или туториал не покрыл твой случай — это gap, который стоит исправить.

---

**Конец туториала.** Возврат к [INDEX.md](./INDEX.md).
