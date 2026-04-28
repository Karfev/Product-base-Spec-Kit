# 07. Профили и risk-assessment

> **Аудитория:** Dev / Tech Lead.
> **Время:** 10 минут.
> **Предыдущий:** [06-traceability-and-validation.md](./06-traceability-and-validation.md) | **Следующий:** [08-when-it-breaks.md](./08-when-it-breaks.md)

---

## TL;DR

Профиль — это **уровень обязательности артефактов**. Чем выше риск изменения, тем строже профиль.
Выбираем по **риску**, а не по **размеру**: маленькая фича с PII = Extended; большой рефакторинг
без бизнес-эффекта = Minimal.

| Профиль | Когда | Дополнительные артефакты vs предыдущего |
|---|---|---|
| **Minimal** | Internal tooling, low-risk fix | PRD, requirements.yml, README, CHANGELOG |
| **Standard** | Большинство фич | + design.md, contracts/, decisions/, ops/slo.yaml, ops/prr-checklist.md, delivery/rollout.md |
| **Extended** | PII / GDPR / SOC2 / финансовые операции | + threat-model.md, nfr-validation.md, migration.md, compliance/ |
| **Enterprise** | Большие IS-class системы (АИС) | + architecture-views/, subsystem-classification.yaml, hld.md |

---

## Risk-assessment — 8 вопросов

Источник истины: [`/speckit-profile`](../../.claude/commands/speckit-profile.md) +
[`.specify/memory/risk-keywords.yml`](../../.specify/memory/risk-keywords.yml).

| # | Вопрос | YES сдвигает к |
|---|---|---|
| 1 | Handles auth / tokens / credentials? | Standard+ |
| 2 | Involves PII / GDPR / SOC2 / personal data? | **Extended (mandatory)** |
| 3 | Adds public API contracts? | Standard+ |
| 4 | Has SLO/SLA commitments to customers? | Standard+ |
| 5 | Requires DB migrations or data changes? | Standard+ |
| 6 | Revenue / data loss risk if fails? | Extended |
| 7 | IS-class system per ArchiMate (АИС)? | Enterprise |
| 8 | Affects > 1 product / team? | Standard+ |

**Decision tree (top-to-bottom, first match wins):**
1. Q7 YES → **Enterprise** (требует подтверждения архитектора).
2. Q2 YES → **Extended** (mandatory, не overrideable, regulatory).
3. 5+ YES → **Extended** (downgrade требует Tech Lead sign-off).
4. 2-4 YES → **Standard**.
5. 0-1 YES → **Minimal**.
6. **Guard:** Q1 YES → минимум **Standard** (auth — это не minimal).

---

## Auto-routing — без анкеты

```text
/speckit-quick "fix typo in README export endpoint description"
# → Minimal (нет risk-keywords, < 5 component_indicators)

/speckit-quick "add JWT auth to admin API"
# → Standard (Q1 YES + Q3 YES = guard)

/speckit-quick "GDPR data deletion endpoint with audit log"
# → Extended (Q2 YES = mandatory)

/speckit-quick "tax reporting AIS subsystem with ArchiMate ontology"
# → Enterprise (Q7 YES + множество component_indicators)
```

Под капотом: regex match по keywords из `risk-keywords.yml`. Если результат странный —
override через `/speckit-profile <INIT-ID>`.

---

## 4 учебных кейса

### Кейс 1 — Minimal: «typo in API docs»

**Описание:** правим опечатку в OpenAPI summary — `"Get user"` → `"Get user by id"`.

| Q | Ответ |
|---|---|
| Q1 auth? | NO |
| Q2 PII? | NO |
| Q3 public API? | NO (это правка описания, не контракта) |
| Q4 SLO? | NO |
| Q5 DB migration? | NO |
| Q6 revenue risk? | NO |
| Q7 IS-class? | NO |
| Q8 multi-team? | NO |

**Профиль:** **Minimal**. Артефакты: PRD (1 параграф), requirements.yml (один REQ), CHANGELOG, README.
Без design.md, без contracts/-папки, без ops/, без delivery/.

**Время на оформление:** 15-20 минут.

---

### Кейс 2 — Standard: csv-export (наш учебный пример)

**Описание:** новый эндпойнт `POST /export` для выгрузки данных клиента в CSV.

| Q | Ответ |
|---|---|
| Q1 auth? | NO (используем существующий Bearer) |
| Q2 PII? | NO (экспортируем уже существующие данные клиента) |
| Q3 public API? | YES |
| Q4 SLO? | YES (P95 < 5s) |
| Q5 DB migration? | NO (stateless) |
| Q6 revenue risk? | NO |
| Q7 IS-class? | NO |
| Q8 multi-team? | NO |

**Профиль:** **Standard** (2 YES, не triggered Q1/Q2/Q7).
Полный комплект артефактов из [04-anatomy-of-initiative.md](./04-anatomy-of-initiative.md).

**Время на оформление:** 1-2 рабочих дня (с заполнением design.md, ADR, SLO, PRR).

---

### Кейс 3 — Extended: «GDPR right to erasure»

**Описание:** эндпойнт `POST /accounts/{id}/erase` для безвозвратного удаления данных клиента
по запросу (GDPR Art. 17).

| Q | Ответ |
|---|---|
| Q1 auth? | YES (admin role + 2FA) |
| Q2 PII? | **YES — это вся суть фичи** |
| Q3 public API? | YES |
| Q4 SLO? | YES (P95 удаления < 24h) |
| Q5 DB migration? | YES (cascade delete + audit log) |
| Q6 revenue risk? | YES (если ошибётся — удалит чужой аккаунт) |
| Q7 IS-class? | NO |
| Q8 multi-team? | YES (privacy + platform + billing) |

**Профиль:** **Extended** (Q2 = mandatory).

Дополнительно к Standard:
- `compliance/regulatory-review.md` — DPIA (Data Protection Impact Assessment)
- `ops/threat-model.md` — STRIDE-анализ (особое внимание Tampering — нельзя удалить чужой аккаунт)
- `ops/nfr-validation.md` — формальная валидация NFR (24h SLO для удаления)
- `delivery/migration.md` — миграция данных (как помечаем «erased», как очищаем backup'ы)

**Время на оформление:** 1-2 недели. Privacy review — отдельный gate.

---

### Кейс 4 — Enterprise: «налоговая АИС»

**Описание:** новая подсистема в большой государственной системе (АИС «Налог-3»),
обрабатывающая декларации НДС.

| Q | Ответ |
|---|---|
| Q1-Q6 | YES |
| Q7 IS-class? | **YES — АИС с классификацией ArchiMate** |
| Q8 multi-team? | YES (5+ команд) |

**Профиль:** **Enterprise**.

Дополнительно к Extended:
- `subsystem-classification.yaml` — машинно-проверяемая классификация (`С.К.Б`, `ПС.Т.У` и т.д.)
- `architecture-views/` — 11 видов представлений (Д-1 деятельности, П-1 подсистем, Т-1 технологий и т.д.)
- 3-слойная онтология АИС в `design.md` (Activity / Application / Technology)
- `hld.md` — High-Level Design отдельно от `design.md`
- Архкомм-ревью (если выбран `--preset archkom`)

**Команда инициации:**
```bash
./tools/init.sh INIT-2026-200-vat-declarations 200-vat-declarations \
  --profile enterprise \
  --preset archkom \
  --product tax-platform \
  --owner @tax-platform-team

/speckit-architecture INIT-2026-200-vat-declarations
# → создаёт design.md с 3-слойной онтологией + architecture-views/ stubs
```

**Время на оформление:** месяц+ только на полный комплект артефактов.

---

## Антипаттерны выбора профиля

### 1. «Маленькая фича — значит Minimal»

**Нет.** Размер ≠ риск. Smal endpoint для аутентификации = Standard минимум (Q1).

### 2. «Команда жалуется на overhead → понизим до Minimal»

**Опасно.** Если по риску положен Standard — Minimal оставит дыры в SLO/PRR.
Лучше investment в onboarding/automation, чтобы Standard был дёшев.

### 3. «Сделаем Enterprise, чтобы не упустить ничего»

**Это карго-культ.** Enterprise — это для АИС-class систем.
Для обычного B2B SaaS даже Standard — большинство случаев.

### 4. «Решение по профилю принимает PM в одиночку»

**Опасно для Extended/Enterprise.** Тех. оценка risk обязательна.
Лучше парный воркшоп PM + Tech Lead с прохождением 8 вопросов.

---

## Upgrade профиля

```bash
# Upgrade на более жёсткий профиль (Standard → Extended):
./tools/upgrade.sh INIT-2026-099-csv-export --profile extended
# Создаст недостающие артефакты (threat-model, migration, compliance/) с placeholder'ами.

# С Архкомм-preset:
./tools/upgrade.sh INIT-2026-042-user-auth --profile extended --preset archkom

# Force-режим (если нужно перезаписать существующие артефакты):
./tools/upgrade.sh INIT-2026-042-user-auth --profile standard --force
```

**Downgrade** (например, Standard → Minimal) `upgrade.sh` напрямую не поддерживает — это by design, чтобы не потерять артефакты случайно. Если действительно нужен downgrade:
1. Аргументируй решение в ADR.
2. Вручную удали «лишние» артефакты из `initiatives/<INIT>/`.
3. Обнови `metadata.profile` в `requirements.yml`.
4. Закоммить с явным сообщением `[DOWNGRADE] INIT-XXX → minimal: <reason>`.

Обычно проще закрыть инициативу как `completed` и завести новую с нужным профилем.

---

## Резюме

| Если у тебя… | Профиль |
|---|---|
| Internal CLI / dev tooling без user-facing impact | Minimal |
| Новый REST endpoint с SLO для customer-facing API | Standard |
| Что угодно с PII / GDPR / SOC2 / payment | **Extended (без вариантов)** |
| Государственная информационная система с ArchiMate-классификацией | Enterprise |

**Сомневаешься между Minimal и Standard?** Бери Standard.
**Сомневаешься между Standard и Extended?** Если хоть какие-то PII — бери Extended.

---

> **💡 Для тимлида.** В первый месяц adoption поставь правило: профиль выбирается **парно**
> (PM + Tech Lead) на kickoff-е инициативы, фиксируется в `metadata.profile`. Это убирает
> 80% будущих конфликтов «а почему такой overhead» / «где у нас threat model».

---

**Дальше:** [08-when-it-breaks.md](./08-when-it-breaks.md) — топ-15 ошибок и как их чинить.
