---
service_code: "{service-code}"
service_class: "{Наименование класса услуг}"
service_name: "{Полное наименование единичной услуги}"
short_name: "{Краткое наименование}"
product: "{product}"
owner: "@{owner}"
criticality: "{Критичная|Высокая|Средняя}"
scope: "{Бизнес-услуга|Технологическая услуга}"
external_spec_version: "0.1"
internal_spec_version: "0.1"
last_updated: "{YYYY-MM-DD}"
profile: "{Minimal|Standard|Extended}"
---

# Service: {service-code}

**Полное наименование:** {Полное наименование единичной услуги}
**Продукт:** [`products/{product}/`](../../products/{product}/)
**Владелец:** @{owner}
**Степень критичности:** {Критичная|Высокая|Средняя}

---

## Артефакты услуги

| Файл | Профиль | Статус | Описание |
|---|---|---|---|
| `external-spec.md` | Minimal | {draft\|current} | Клиентская спецификация (SLA, тарификация, поддержка) |
| `requirements.yml` | Minimal | {draft\|current} | Machine-readable требования (REQ-SVC-*) |
| `internal-spec.md` | Standard+ | {draft\|current} | Внутренняя спецификация доставки |
| `rsm.md` | Standard+ | {draft\|current} | Ресурсно-сервисная модель |
| `responsibilities.yml` | Standard+ | {draft\|current} | Матрица ответственности |
| `ops/slo.yaml` | Standard+ | {draft\|current} | SLO (доступность, задержки) |
| `ops/incident-catalog.yml` | Standard+ | {draft\|current} | Каталог инцидентов и SLT |
| `ops/request-catalog.yml` | Standard+ | {draft\|current} | Каталог типовых запросов |
| `billing/parameters.yml` | Extended | {draft\|current} | Тарифицируемые параметры |
| `ops/change-catalog.yml` | Extended | {draft\|current} | Параметры изменений |
| `appendices/connection-guide.md` | Extended | {draft\|current} | Технические условия на подключение |

## Связанный продукт

- [`products/{product}/`](../../products/{product}/) — {краткое описание как продукт реализует услугу}

## Связанные инициативы

<!-- Инициативы, которые создали или изменяют эту услугу -->
- [`initiatives/{INIT-YYYY-NNN-slug}/`](../../initiatives/{INIT-YYYY-NNN-slug}/) — {краткое описание}

## Ключевые требования

| ID | Заголовок | Тип | Приоритет |
|---|---|---|---|
| `REQ-SVC-001` | {заголовок} | {functional\|nfr} | {P0\|P1\|P2} |
