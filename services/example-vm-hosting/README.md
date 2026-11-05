---
service_code: "EXAMPLE-VM-HOSTING"
service_class: "Platform IaaS (Example Virtual Data Center)"
service_name: "Example: Cloud Platform as a Virtual Data Center Service"
short_name: "Example VM Hosting"
product: "platform"
owner: "@platform-team"
criticality: "Critical"
scope: "Business Service"
external_spec_version: "0.6"
internal_spec_version: "0.85"
last_updated: "2026-03-02"
profile: "extended"
---

# Service: EXAMPLE-VM-HOSTING

**Full Name:** Example Cloud Platform as a Virtual Data Center Service
**Product:** [`products/platform/`](../../products/platform/)
**Owner:** @platform-team
**Criticality:** Critical

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

## Related Product

- [`products/platform/`](../../products/platform/) — Example platform IaaS. Virtual data center resources are provided to consumers using virtualization technology.

## Related Initiatives

<!-- Links to initiatives implementing changes to the EXAMPLE-VM-HOSTING service -->
- *(no active initiatives)*

## Ключевые требования

| ID | Заголовок | Тип | Приоритет |
|---|---|---|---|
| `REQ-SVC-001` | Предоставление изолированной инфраструктуры ВЦОД | functional | P0 |
| `REQ-SVC-002` | Доступ к консоли управления облачным ВЦОД | functional | P0 |
| `REQ-SVC-003` | Межсетевое экранирование подсетей | functional | P1 |
| `REQ-SVC-010` | Доступность услуги 99.5% | nfr | P0 |
| `REQ-SVC-011` | SLT разрешения инцидентов | nfr | P0 |
| `REQ-SVC-012` | SLT выполнения типовых запросов | nfr | P1 |
