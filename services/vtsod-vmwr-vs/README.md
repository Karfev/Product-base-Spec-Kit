---
service_code: "ВЦОД-VMWR-VS"
service_class: "Частное облако РТК-ЦТ (ЧО РТКЦТ)"
service_name: "Предоставление облачной платформы виртуального центра обработки данных (ВЦОД)"
short_name: "Предоставление ВЦОД"
product: "private-cloud"
owner: "@cherednichenco-a-g"
criticality: "Критичная"
scope: "Бизнес-услуга"
external_spec_version: "0.6"
internal_spec_version: "0.85"
last_updated: "2026-03-02"
profile: "extended"
---

# Service: ВЦОД-VMWR-VS

**Полное наименование:** Предоставление облачной платформы виртуального центра обработки данных (ВЦОД)
**Продукт:** [`products/private-cloud/`](../../products/private-cloud/)
**Владелец:** Отдел развития услуг, Чередниченко А.Г.
**Степень критичности:** Критичная

---

## Артефакты услуги

| Файл | Профиль | Статус | Описание |
|---|---|---|---|
| `external-spec.md` | Minimal | current | Клиентская спецификация v0.6 |
| `requirements.yml` | Minimal | current | Machine-readable требования (REQ-SVC-*) |
| `internal-spec.md` | Standard+ | current | Внутренняя спецификация v0.85 |
| `rsm.md` | Standard+ | current | Ресурсно-сервисная модель (9 подсистем) |
| `responsibilities.yml` | Standard+ | current | Матрица ответственности (12 блоков) |
| `ops/slo.yaml` | Standard+ | current | SLO: доступность 99.5% |
| `ops/incident-catalog.yml` | Standard+ | current | 3 приоритета инцидентов + SLT |
| `ops/request-catalog.yml` | Standard+ | current | 9 типовых запросов + SLT |
| `billing/parameters.yml` | Extended | current | Тарифицируемые параметры (4 группы) |
| `ops/change-catalog.yml` | Extended | current | Параметры стандартных изменений (11 строк) |
| `appendices/connection-guide.md` | Extended | current | Технические условия на подключение |
| `appendices/request-forms.md` | Extended | current | Формы типовых запросов |
| `appendices/report-templates.md` | Extended | current | Формы отчётов |

## Связанный продукт

- [`products/private-cloud/`](../../products/private-cloud/) — Частное облако РТК-ЦТ (ЧО РТК-ЦТ). На базе платформы VMware предоставляются изолированные ВЦОД потребителям по модели IaaS.

## Связанные инициативы

<!-- Ссылки на инициативы, реализующие изменения в услуге ВЦОД-VMWR-VS -->
- *(нет активных инициатив)*

## Ключевые требования

| ID | Заголовок | Тип | Приоритет |
|---|---|---|---|
| `REQ-SVC-001` | Предоставление изолированной инфраструктуры ВЦОД | functional | P0 |
| `REQ-SVC-002` | Доступ к консоли управления облачным ВЦОД | functional | P0 |
| `REQ-SVC-003` | Межсетевое экранирование подсетей | functional | P1 |
| `REQ-SVC-010` | Доступность услуги 99.5% | nfr | P0 |
| `REQ-SVC-011` | SLT разрешения инцидентов | nfr | P0 |
| `REQ-SVC-012` | SLT выполнения типовых запросов | nfr | P1 |
