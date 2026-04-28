# PRD: {INIT-YYYY-NNN-slug} — {short-name}

> Profile: see [`requirements.yml#metadata.profile`](./requirements.yml) (single source of truth — do not duplicate the value here).
> Source of truth по требованиям: [`requirements.yml`](./requirements.yml).
> Заполняется через `/speckit-prd <INIT-YYYY-NNN-slug>` или вручную по этому шаблону.

> **golden comment.** Удалить эту блокноут-секцию перед коммитом. Структура взята с
> учебной инициативы [`examples/INIT-2026-099-csv-export/prd.md`](../examples/INIT-2026-099-csv-export/prd.md) —
> используй её как живой пример.

---

## 1. Цель и ожидаемый эффект

> **golden comment.** Один абзац. Что болит у бизнеса/пользователя сейчас, почему
> мы это делаем именно сейчас (триггер: контракт, дедлайн, инцидент), и каким будет
> измеримый исход. SMART-метрика. НЕ описывай решение — только проблему и цель.

- **Проблема.** {…}
- **Почему сейчас.** {…}
- **Цель (Outcome).** {измеримая, в идеале одна метрика и горизонт}

---

## 2. Пользователи и сценарии (JTBD)

> **golden comment.** Personas + Jobs To Be Done. Минимум 1, максимум 4.
> Каждая JTBD-формулировка: «Хочу <action>, чтобы <outcome>». Trigger обязателен.

| Persona | Job To Be Done | Trigger |
|---|---|---|
| {…} | {…} | {…} |

---

## 3. Метрики успеха

> **golden comment.** Только то, что мы будем мерять и за что отвечаем.
> Никаких vanity-метрик. Baseline — из текущих данных или «—» если новый функционал.
> `req: REQ-XXX-NNN` ставь только для NFR, которые формализованы в requirements.yml.

| Метрика | Baseline | Target | Период | Источник |
|---|---:|---:|---|---|
| {…} | {…} | {…} | {30d / 90d post-GA} | {APM / BI / Mixpanel} |

---

## 4. Scope

> **golden comment.** Каждый in-scope item MUST маппиться на REQ-ID из requirements.yml.
> Non-goals — конкретные явно исключённые вещи, чтобы не было «а я думал…».

**In-scope:**

- {scope item 1} — `REQ-XXX-001`
- {scope item 2} — `REQ-XXX-002`

**Non-goals:**

- {что мы явно НЕ делаем в этой инициативе}
- {что отложено на Phase 2 / другую инициативу}

---

## 5. Риски и ограничения

> **golden comment.** Минимум 3, максимум 7. Митигация конкретная (не «будем мониторить»).
> Compliance/GDPR/PII — отдельная строка, обязательна для Standard+.

| Риск | Вероятность | Митигация |
|---|---|---|
| {…} | {Низкая / Средняя / Высокая} | {конкретная мера} |

**Compliance:** {Standard — N/A или ссылка на DPA; Extended — отдельный compliance/regulatory-review.md}

---

## 6. Требования

См. машинно-проверяемый реестр [`requirements.yml`](./requirements.yml).
Все REQ-ID валидируются `make validate`.

> **golden comment.** Не дублируй сюда требования из YAML — это нарушит principle
> «single source of truth» из конституции. Только ссылка.

---

## 7. Приёмка (Definition of Done)

> **golden comment.** Конкретные quality gates. Не «оттестировано», а «coverage ≥ 80%».
> Все пункты проверяемы автоматически или явным ревью.

1. `make check-all` зелёный.
2. `/speckit-evidence {INIT-YYYY-NNN-slug}` показывает: RTM coverage ≥ 80%, 0 BLOCKING items в PRR.
3. {доменный критерий — например, канареечный rollout 10% за N дней без P0/P1 инцидентов}
