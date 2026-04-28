# 08. Когда ломается — топ-15 ошибок

> **Аудитория:** Dev / Tech Lead.
> **Время:** справочник, читай по симптому.
> **Предыдущий:** [07-profiles-and-risk.md](./07-profiles-and-risk.md) | **Следующий:** [09-team-rollout.md](./09-team-rollout.md)

---

## TL;DR

Если CI/локальная команда упала — найди симптом ниже, скопипасти фикс. Каждый пункт:
**симптом → причина → фикс → ссылка на источник истины**.

Категории: установка, валидация requirements, contracts, trace, spec quality, release rollout, общие.

---

## Установка

### 1. `python3: command not found` или `python` указывает на 2.7

**Причина:** Windows native, или старая система без `python3`.

**Фикс:**
- Windows → переключись на WSL2 (см. [02-install-and-tooling.md](./02-install-and-tooling.md#windows-через-wsl2)).
- Старый Linux → `sudo apt-get install python3.10 python3.10-pip`.

---

### 2. `error: externally-managed-environment` при `pip install`

**Причина:** PEP 668 — pip 23+ запрещает системные установки на Ubuntu 23.04+ / macOS Brew.

**Фикс (один из):**
```bash
# Вариант 1: явно разрешить
pip install --break-system-packages -r tools/requirements.txt

# Вариант 2: virtualenv (рекомендуется)
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt

# Вариант 3: pipx
pipx install check-jsonschema
```

---

### 3. `redocly: command not found` после `make install-tools`

**Причина:** npm global bin не в `$PATH`.

**Фикс:**
```bash
export PATH="$PATH:$(npm config get prefix)/bin"
# Добавь эту строку в ~/.bashrc или ~/.zshrc
```

---

## Валидация requirements.yml

### 4. `'operational' is not one of [...]` в check-jsonschema

**Симптом:**
```
type: ['type'] failed validation. 'operational' is not one of
['functional', 'nfr', 'quality', 'constraint', 'compliance']
```

**Причина:** в YAML стоит `type: "operational"` — такого значения в схеме нет.

**Фикс:** заменить на `constraint` (для жёстких ограничений вроде «не логировать пароли»)
или `functional` с явным acceptance criteria.

**Источник истины:** [`tools/schemas/requirements.schema.json`](../../tools/schemas/requirements.schema.json), enum `requirement.type`.

---

### 5. `'acceptance_criteria' is a required property`

**Симптом:**
```
$.requirements[0]: 'acceptance_criteria' is a required property
```

**Причина:** требование `type: functional` обязано иметь `acceptance_criteria`. Это conditional schema.

**Фикс:** добавить как минимум один Given-When-Then.
```yaml
acceptance_criteria:
  - "Given <условие>, when <действие>, then <результат>"
```

**Аналогично:** `type: nfr` → требует `metrics`. `type: quality` → требует `metrics` с `iso_characteristic`.

---

### 6. `'P5' is not one of ['P0', 'P1', 'P2', 'P3']`

**Симптом:** опечатка в priority.

**Фикс:** использовать только `P0`, `P1`, `P2`, `P3`. P0 — blocking, P3 — wishlist.

---

### 7. `pattern '^REQ-[A-Z0-9]{2,16}-[0-9]{3}$' did not match`

**Симптом:** ID требования не соответствует шаблону.

**Примеры неправильных:**
- `REQ-export-001` (нижний регистр в SCOPE) → `REQ-EXPORT-001`
- `REQ-Export-1` (mixed case + non-padded number) → `REQ-EXPORT-001`
- `REQ-CSVEXPORTLONGNAME-001` (SCOPE > 16 символов) → `REQ-EXPORT-001`

**Фикс:** `REQ-<UPPERCASE 2-16 chars>-<NNN с ведущими нулями>`.

---

## Contracts (OpenAPI / AsyncAPI)

### 8. `redocly lint` падает на ошибке `no-empty-servers` или `info-license`

**Симптом:**
```
[error] no-empty-servers: Servers array is empty.
[error] info-license: Field 'license' is required in 'info'.
```

**Причина:** Redocly из коробки требовательнее, чем минимальный OpenAPI.

**Фикс:** добавить в `openapi.yaml`:
```yaml
info:
  title: ...
  version: ...
  license:
    name: Proprietary
servers:
  - url: https://api.example.local/v1
    description: Production
```

Либо настроить exceptions в `redocly.yaml` (уже есть в репо — глянь его).

---

### 9. `oasdiff` падает на «breaking change»

**Симптом:** PR-чек `contracts.yml` фейлится с `BREAKING: removed required parameter`.

**Причина:** ты убрал required-параметр или изменил response schema несовместимо.

**Фикс варианты:**

| Вариант | Когда |
|---|---|
| Откатить изменение в OpenAPI | Если правда не хотел менять контракт |
| Добавить deprecation marker | Если меняешь намеренно: пометь старое как `deprecated: true`, добавь новое поле |
| Bump major version | Если breaking change неизбежен (новый эндпойнт `/v2/...`) |

**Источник:** [oasdiff docs](https://github.com/oasdiff/oasdiff).

---

## Trace и check-trace

### 10. `make check-trace` падает с «orphan REQ-ID in trace.md»

**Симптом:**
```
trace.md line 12: REQ-EXPORT-099 not found in requirements.yml
```

**Причина:** в `trace.md` ссылка на REQ-ID, которого нет в `requirements.yml` (опечатка / удалили требование).

**Фикс:** либо вернуть требование в `requirements.yml`, либо убрать строку из `trace.md`,
либо переименовать REQ-ID в trace.md соответствующе.

---

### 11. `make check-trace` падает с «REQ has no trace evidence»

**Симптом:**
```
REQ-EXPORT-006 has no entries in trace (tests, contracts, slo, adr) — Standard profile requires >= 1.
```

**Причина:** добавил требование, но не прописал ни одной trace-ссылки.

**Фикс:** заполнить хотя бы один пункт в `trace`:
```yaml
- id: "REQ-EXPORT-006"
  ...
  trace:
    tests:
      - "tests/api/export-i18n.spec.ts::REQ-EXPORT-006"
```

Если ещё не написал тест — пометь требование `status: draft` (для draft check-trace warning, не blocking).

---

## Spec quality / structure

### 12. `make check-spec-quality` падает с «open NEEDS CLARIFICATION»

**Симптом:**
```
.specify/specs/099-csv-export/spec.md line 42: open NEEDS CLARIFICATION
```

**Причина:** в spec остались незакрытые вопросы (`- [ ] **NEEDS CLARIFICATION:** ...`).

**Фикс:** ответить на вопрос, отметить пункт как `[x]` или удалить, если стал не релевантен.
Spec не должен иметь open-questions при переходе в plan.

---

### 13. `check-spec-structure.py` падает с «missing canonical section»

**Симптом:**
```
plan.md: missing required section 'Rollout & rollback strategy'
```

**Причина:** в `plan.md` пропущена обязательная секция (canonical structure).

**Фикс:** скопировать заголовок из шаблона ([`templates/spec-template.md`](../../templates/spec-template.md))
и заполнить.

---

### 14. `tasks.md` фейлится с «T2a must come before T2b»

**Симптом:** check-spec-quality говорит, что порядок задач нарушен.

**Причина:** в `tasks.md` написал implementation (T2b) раньше тестов (T2a). Это нарушает TDD-порядок.

**Фикс:** переставь задачи так, чтобы T2a (RED) шло до T2b (GREEN).

---

## Release rollout

### 15. `make check-release-rollout` падает с «SLO not referenced in rollout.md»

**Симптом:**
```
delivery/rollout.md does not reference any SLO from ops/slo.yaml.
Standard+ profile requires SLO-based rollout criteria.
```

**Причина:** в `delivery/rollout.md` нет упоминания SLO/SLI как критериев перехода между этапами.

**Фикс:** добавить в секции «Critery перехода» строки вроде:
```markdown
| Этап Canary 10% | P95 < 5s удерживается, error rate < 0.1%, SLO budget burn < 5% | ... |
```

И ссылка на `ops/slo.yaml#csv-export-sync-latency`.

---

## Бонус-категория: общие

### Команда `make help` показывает мусор / некорректный список

**Причина:** GNU make старее 3.81 (macOS default) или используется BSD make.

**Фикс:**
```bash
# macOS — установи свежий make
brew install make
gmake help    # либо alias make=gmake
```

---

### `/speckit-xxx` команда «не найдена» в Claude Code

**Причина:** Claude Code не подхватил `.claude/commands/`. Обычно — открыли не корень репо, а подпапку.

**Фикс:** перезапусти Claude Code из корня репо. Проверь `ls .claude/commands/speckit-*.md`.

---

## Что делать, если симптома нет в списке

1. Запусти `make check-all` и прочитай **самое первое** сообщение об ошибке (не последнее).
2. Открой соответствующий валидатор в `tools/scripts/` — там часто есть пояснение.
3. Спроси `/speckit-constitution-review` — может, есть нарушение конституции, которое CI не ловит, но визуально видно.
4. Если совсем тупик — открой issue с тегом `tutorial-gap`. Симптом, не покрытый туториалом —
   это инвестиция в будущих новичков.

---

> **💡 Для тимлида.** Этот файл — кандидат на еженедельный update. Каждая вторая
> «странная» ошибка в команде должна тут оказаться с пометкой `### N. <симптом>`.
> Через 2 квартала это превратится в самый ценный документ репо для новичков.

---

**Дальше:** [09-team-rollout.md](./09-team-rollout.md) — как внедрить SpecKit в команду 5–20 человек за 4 недели.
